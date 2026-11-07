"""
PROJECTVERSE - Production Database Migration & Demo Data Purge
1. Safely removes all 540 synthetic demo students, demo enrollments, and demo progress.
2. Creates new production tables:
   - project_enquiries
   - project_requests
   - invoices
   - contact_messages
   - email_logs
   - audit_logs
   - admins
3. Adds database indexes for production query performance.
4. Ensures primary super-admin account for aniladani843@gmail.com and admin@projectverse.com.
5. Populates technologies lookup table.
"""
import sqlite3
import hashlib
from datetime import datetime

DB_PATH = "projectverse.db"

def hash_pw(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

def migrate():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    print("Beginning Production Database Migration...")

    # 1. Purge all synthetic demo data
    print("Purging synthetic demo data...")
    cur.execute("SELECT id FROM users WHERE email LIKE '%example.test%'")
    demo_user_ids = [r[0] for r in cur.fetchall()]
    print(f"Found {len(demo_user_ids)} synthetic demo user accounts.")

    if demo_user_ids:
        placeholders = ','.join('?' * len(demo_user_ids))
        cur.execute(f"DELETE FROM project_progress WHERE enrollment_id IN (SELECT id FROM project_enrollments WHERE user_id IN ({placeholders}))", demo_user_ids)
        cur.execute(f"DELETE FROM project_assignments WHERE enrollment_id IN (SELECT id FROM project_enrollments WHERE user_id IN ({placeholders}))", demo_user_ids)
        cur.execute(f"DELETE FROM project_enrollments WHERE user_id IN ({placeholders})", demo_user_ids)
        cur.execute(f"DELETE FROM students WHERE user_id IN ({placeholders})", demo_user_ids)
        cur.execute(f"DELETE FROM notifications WHERE user_id IN ({placeholders})", demo_user_ids)
        cur.execute(f"DELETE FROM users WHERE id IN ({placeholders})", demo_user_ids)

    # Clean demo_records table if it exists
    cur.execute("DROP TABLE IF EXISTS demo_records")
    print("Demo records and synthetic users removed.")

    # 2. Add columns to users table if missing (e.g. university, failed_login_attempts, locked_until)
    cur.execute("PRAGMA table_info(users)")
    user_cols = [r[1] for r in cur.fetchall()]
    
    if "university" not in user_cols:
        cur.execute("ALTER TABLE users ADD COLUMN university TEXT")
    if "specialization" not in user_cols:
        cur.execute("ALTER TABLE users ADD COLUMN specialization TEXT")
    if "preferred_tech" not in user_cols:
        cur.execute("ALTER TABLE users ADD COLUMN preferred_tech TEXT")
    if "failed_login_attempts" not in user_cols:
        cur.execute("ALTER TABLE users ADD COLUMN failed_login_attempts INTEGER DEFAULT 0")
    if "locked_until" not in user_cols:
        cur.execute("ALTER TABLE users ADD COLUMN locked_until DATETIME")
    if "reset_token" not in user_cols:
        cur.execute("ALTER TABLE users ADD COLUMN reset_token TEXT")
    if "reset_token_expiry" not in user_cols:
        cur.execute("ALTER TABLE users ADD COLUMN reset_token_expiry DATETIME")

    # 3. Create Admins table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS admins (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER UNIQUE NOT NULL,
        department TEXT DEFAULT 'Executive Administration',
        permissions TEXT DEFAULT '["all"]',
        last_login DATETIME,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    """)

    # 4. Create Project Enquiries Table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS project_enquiries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        enquiry_number VARCHAR(64) UNIQUE NOT NULL,
        customer_name VARCHAR(255) NOT NULL,
        customer_email VARCHAR(255) NOT NULL,
        customer_phone VARCHAR(50) NOT NULL,
        college_name VARCHAR(255),
        course VARCHAR(100),
        project_id INTEGER,
        project_code VARCHAR(50),
        project_title VARCHAR(255),
        technology VARCHAR(255),
        message TEXT NOT NULL,
        status VARCHAR(50) DEFAULT 'NEW',
        admin_notes TEXT,
        assigned_to VARCHAR(255),
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(project_id) REFERENCES projects(id) ON DELETE SET NULL
    )
    """)

    # 5. Create Project Requests Table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS project_requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        request_number VARCHAR(64) UNIQUE NOT NULL,
        user_id INTEGER,
        student_name VARCHAR(255) NOT NULL,
        student_email VARCHAR(255) NOT NULL,
        student_phone VARCHAR(50) NOT NULL,
        college_name VARCHAR(255),
        course VARCHAR(100),
        project_id INTEGER NOT NULL,
        project_code VARCHAR(50) NOT NULL,
        project_title VARCHAR(255) NOT NULL,
        preferred_tech VARCHAR(255),
        deadline VARCHAR(100),
        requirements TEXT,
        team_mode VARCHAR(50) DEFAULT 'Individual',
        team_members TEXT,
        status VARCHAR(50) DEFAULT 'NEW',
        admin_notes TEXT,
        mentor_id INTEGER,
        progress_percent INTEGER DEFAULT 0,
        current_milestone VARCHAR(255) DEFAULT 'Topic Selection & Problem Statement',
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE SET NULL,
        FOREIGN KEY(project_id) REFERENCES projects(id) ON DELETE RESTRICT,
        FOREIGN KEY(mentor_id) REFERENCES mentors(id) ON DELETE SET NULL
    )
    """)

    # 6. Update Orders Table (add customer columns if missing)
    cur.execute("PRAGMA table_info(orders)")
    order_cols = [r[1] for r in cur.fetchall()]
    if "customer_name" not in order_cols:
        cur.execute("ALTER TABLE orders ADD COLUMN customer_name VARCHAR(255)")
    if "customer_email" not in order_cols:
        cur.execute("ALTER TABLE orders ADD COLUMN customer_email VARCHAR(255)")
    if "customer_phone" not in order_cols:
        cur.execute("ALTER TABLE orders ADD COLUMN customer_phone VARCHAR(50)")
    if "payment_method" not in order_cols:
        cur.execute("ALTER TABLE orders ADD COLUMN payment_method VARCHAR(50) DEFAULT 'UPI'")
    if "quotation_details" not in order_cols:
        cur.execute("ALTER TABLE orders ADD COLUMN quotation_details TEXT")
    if "admin_notes" not in order_cols:
        cur.execute("ALTER TABLE orders ADD COLUMN admin_notes TEXT")

    # 7. Create Invoices Table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS invoices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        invoice_number VARCHAR(64) UNIQUE NOT NULL,
        order_id INTEGER,
        user_id INTEGER,
        customer_name VARCHAR(255) NOT NULL,
        customer_email VARCHAR(255) NOT NULL,
        customer_phone VARCHAR(50),
        customer_college VARCHAR(255),
        project_title VARCHAR(255) NOT NULL,
        project_code VARCHAR(50) NOT NULL,
        subtotal INTEGER NOT NULL,
        tax_amount INTEGER DEFAULT 0,
        total_amount INTEGER NOT NULL,
        status VARCHAR(50) DEFAULT 'PAID',
        payment_reference VARCHAR(100),
        notes TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(order_id) REFERENCES orders(id) ON DELETE SET NULL,
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE SET NULL
    )
    """)

    # 8. Create Contact Messages Table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS contact_messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        phone VARCHAR(50),
        subject VARCHAR(255) NOT NULL,
        message TEXT NOT NULL,
        is_read INTEGER DEFAULT 0,
        status VARCHAR(50) DEFAULT 'NEW',
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # 9. Create Email Logs Table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS email_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_type VARCHAR(100) NOT NULL,
        recipient_email VARCHAR(255) NOT NULL,
        subject VARCHAR(255) NOT NULL,
        body_preview TEXT,
        status VARCHAR(50) NOT NULL,
        error_message TEXT,
        retry_count INTEGER DEFAULT 0,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        sent_at DATETIME
    )
    """)

    # 10. Create Audit Logs Table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS audit_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        user_email VARCHAR(255),
        action VARCHAR(100) NOT NULL,
        resource_type VARCHAR(100),
        resource_id VARCHAR(100),
        details TEXT,
        ip_address VARCHAR(50),
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # 11. Create Performance Indexes
    print("Creating database indexes for query acceleration...")
    indexes = [
        "CREATE INDEX IF NOT EXISTS idx_projects_code ON projects(project_code)",
        "CREATE INDEX IF NOT EXISTS idx_projects_academic ON projects(academic_level)",
        "CREATE INDEX IF NOT EXISTS idx_projects_domain ON projects(domain)",
        "CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)",
        "CREATE INDEX IF NOT EXISTS idx_users_role ON users(role)",
        "CREATE INDEX IF NOT EXISTS idx_enquiries_status ON project_enquiries(status)",
        "CREATE INDEX IF NOT EXISTS idx_enquiries_number ON project_enquiries(enquiry_number)",
        "CREATE INDEX IF NOT EXISTS idx_requests_status ON project_requests(status)",
        "CREATE INDEX IF NOT EXISTS idx_requests_number ON project_requests(request_number)",
        "CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(status)",
        "CREATE INDEX IF NOT EXISTS idx_invoices_number ON invoices(invoice_number)",
        "CREATE INDEX IF NOT EXISTS idx_notifications_user ON notifications(user_id, is_read)",
        "CREATE INDEX IF NOT EXISTS idx_email_logs_status ON email_logs(status)"
    ]
    for idx_sql in indexes:
        cur.execute(idx_sql)

    # 12. Ensure Primary Super Admin User (aniladani843@gmail.com)
    print("Configuring primary business owner and super-admin accounts...")
    admin_pw = hash_pw("Admin@12345")
    
    # Check if aniladani843@gmail.com exists
    cur.execute("SELECT id FROM users WHERE email = 'aniladani843@gmail.com'")
    owner = cur.fetchone()
    if not owner:
        cur.execute("""
        INSERT INTO users (email, password_hash, full_name, mobile, college, course, academic_year, role)
        VALUES ('aniladani843@gmail.com', ?, 'Anil (Business Owner)', '8431712924', 'PROJECTVERSE HQ', 'Executive', '2026', 'super_admin')
        """, (admin_pw,))
        owner_id = cur.lastrowid
        cur.execute("INSERT OR IGNORE INTO admins (user_id, department, permissions) VALUES (?, 'Executive Office', '[\"all\"]')", (owner_id,))
    else:
        cur.execute("UPDATE users SET role = 'super_admin' WHERE id = ?", (owner[0],))
        cur.execute("INSERT OR IGNORE INTO admins (user_id, department, permissions) VALUES (?, 'Executive Office', '[\"all\"]')", (owner[0],))

    # Also make sure admin@projectverse.com is in admins table
    cur.execute("SELECT id FROM users WHERE email = 'admin@projectverse.com'")
    adm = cur.fetchone()
    if adm:
        cur.execute("INSERT OR IGNORE INTO admins (user_id, department, permissions) VALUES (?, 'Operations', '[\"all\"]')", (adm[0],))

    # 13. Populate technologies table from existing project tech stacks
    print("Populating technologies catalog...")
    cur.execute("DELETE FROM technologies")
    tech_list = [
        ("Python", "Programming Language", "python", 98),
        ("React.js", "Frontend Framework", "code-2", 95),
        ("PyTorch", "AI / Deep Learning", "cpu", 94),
        ("FastAPI", "Backend Framework", "zap", 92),
        ("PostgreSQL", "Database", "database", 90),
        ("SQLite", "Database", "database", 85),
        ("Pandas", "Data Science", "bar-chart-2", 88),
        ("Power BI", "Business Intelligence", "pie-chart", 86),
        ("TensorFlow", "Machine Learning", "cpu", 89),
        ("Node.js", "Backend Runtime", "server", 87),
        ("Tailwind CSS", "UI Framework", "layout", 86),
        ("OpenCV", "Computer Vision", "camera", 84),
        ("Docker", "DevOps & Deployment", "box", 82),
        ("Qiskit", "Quantum Computing", "atom", 80),
        ("Neo4j", "Graph Database", "share-2", 78)
    ]
    cur.executemany("INSERT INTO technologies (name, category, icon, popularity) VALUES (?, ?, ?, ?)", tech_list)

    # 14. Update admin_settings to reflect live production
    cur.execute("INSERT OR REPLACE INTO admin_settings (setting_key, setting_value, description) VALUES ('production_mode', '1', 'Live Production Flag')")
    cur.execute("INSERT OR REPLACE INTO admin_settings (setting_key, setting_value, description) VALUES ('business_email', 'aniladani843@gmail.com', 'Primary Business Notification Email')")
    cur.execute("INSERT OR REPLACE INTO admin_settings (setting_key, setting_value, description) VALUES ('business_phone', '+91 8431712924', 'Official Business Hotline')")
    cur.execute("INSERT OR REPLACE INTO admin_settings (setting_key, setting_value, description) VALUES ('upi_id', '8431712924-3@ybl', 'Verified UPI Receiving VPA')")
    cur.execute("INSERT OR REPLACE INTO admin_settings (setting_key, setting_value, description) VALUES ('upi_name', 'ANIL', 'Official Payee Name')")
    cur.execute("DELETE FROM admin_settings WHERE setting_key = 'demo_mode'")

    conn.commit()
    conn.close()
    print("Production Database Migration Completed Successfully!")

if __name__ == "__main__":
    migrate()
