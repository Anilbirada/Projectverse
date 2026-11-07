"""
PROJECTVERSE - Database Schema Upgrade Script
Extends projectverse.db with enterprise student management, mentors,
project requests, milestones, demo mode settings, and enhanced project schema.
"""
import sqlite3

def upgrade_schema(db_path="projectverse.db"):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # 1. Ensure projects table has all required technical documentation columns
    cur.execute("PRAGMA table_info(projects)")
    existing_cols = [r[1] for r in cur.fetchall()]

    new_project_cols = [
        ("domain", "TEXT DEFAULT 'Software Engineering'"),
        ("timeline", "TEXT DEFAULT '6-8 Weeks'"),
        ("prerequisites", "TEXT DEFAULT 'Basic Programming'"),
        ("learning_outcomes", "TEXT DEFAULT 'Practical Industry Skills'"),
        ("testing_requirements", "TEXT DEFAULT 'Unit, Integration and Functional Testing'"),
        ("expected_output", "TEXT DEFAULT 'Fully Working Deployed System and Documentation'"),
        ("deployment_instructions", "TEXT DEFAULT 'Docker and Cloud Deployment Guide'"),
        ("documentation_requirements", "TEXT DEFAULT 'IEEE Format Project Report, SRS, PPT, Architecture Diagrams'"),
        ("target_users", "TEXT DEFAULT 'Students, Academicians, Industry Evaluators'"),
        ("core_modules_json", "TEXT DEFAULT '[]'"),
        ("dfd_description", "TEXT DEFAULT ''"),
        ("uml_description", "TEXT DEFAULT ''"),
        ("popularity_score", "INTEGER DEFAULT 90"),
        ("is_trending", "INTEGER DEFAULT 0"),
        ("is_research", "INTEGER DEFAULT 0")
    ]

    for col_name, col_type in new_project_cols:
        if col_name not in existing_cols:
            print(f"Adding column '{col_name}' to projects table...")
            cur.execute(f"ALTER TABLE projects ADD COLUMN {col_name} {col_type}")

    # 2. Categories table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        code TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        display_name TEXT NOT NULL,
        description TEXT,
        project_count INTEGER DEFAULT 0,
        badge_color TEXT DEFAULT 'purple',
        icon TEXT DEFAULT 'folder',
        sort_order INTEGER DEFAULT 0,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # 3. Technologies table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS technologies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        category TEXT NOT NULL,
        icon TEXT DEFAULT 'code',
        popularity INTEGER DEFAULT 80
    )
    """)

    # 4. Mentors table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS mentors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        full_name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        mobile TEXT,
        department TEXT NOT NULL,
        designation TEXT DEFAULT 'Senior Academic Mentor',
        specialization TEXT NOT NULL,
        experience_years INTEGER DEFAULT 5,
        max_students INTEGER DEFAULT 25,
        active_students INTEGER DEFAULT 0,
        is_available INTEGER DEFAULT 1,
        bio TEXT,
        avatar_url TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # 5. Students table (extended profile)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER UNIQUE,
        university TEXT,
        year_or_semester TEXT,
        specialization TEXT,
        preferred_technology TEXT,
        project_mode TEXT DEFAULT 'Individual',
        assigned_mentor_id INTEGER,
        enrollment_status TEXT DEFAULT 'active',
        is_demo INTEGER DEFAULT 0,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY(assigned_mentor_id) REFERENCES mentors(id) ON DELETE SET NULL
    )
    """)

    # 6. Project Enrollments / Requests table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS project_enrollments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        enrollment_number TEXT UNIQUE NOT NULL,
        user_id INTEGER NOT NULL,
        student_id INTEGER,
        project_id INTEGER NOT NULL,
        mentor_id INTEGER,
        status TEXT DEFAULT 'pending',
        request_date DATETIME DEFAULT CURRENT_TIMESTAMP,
        approval_date DATETIME,
        completion_status TEXT DEFAULT 'in_progress',
        progress_percentage INTEGER DEFAULT 10,
        current_milestone TEXT DEFAULT 'Topic Approved',
        team_mode TEXT DEFAULT 'Individual',
        team_members TEXT,
        remarks TEXT,
        is_demo INTEGER DEFAULT 0,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY(project_id) REFERENCES projects(id) ON DELETE CASCADE,
        FOREIGN KEY(mentor_id) REFERENCES mentors(id) ON DELETE SET NULL
    )
    """)

    # 7. Project Assignments table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS project_assignments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        enrollment_id INTEGER NOT NULL,
        project_id INTEGER NOT NULL,
        mentor_id INTEGER NOT NULL,
        assigned_by INTEGER,
        notes TEXT,
        assigned_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        status TEXT DEFAULT 'active',
        FOREIGN KEY(enrollment_id) REFERENCES project_enrollments(id) ON DELETE CASCADE,
        FOREIGN KEY(project_id) REFERENCES projects(id) ON DELETE CASCADE,
        FOREIGN KEY(mentor_id) REFERENCES mentors(id) ON DELETE CASCADE
    )
    """)

    # 8. Project Progress Milestones table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS project_progress (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        enrollment_id INTEGER NOT NULL,
        milestone_name TEXT NOT NULL,
        milestone_order INTEGER NOT NULL,
        status TEXT DEFAULT 'pending',
        completion_percentage INTEGER DEFAULT 0,
        feedback TEXT,
        submission_url TEXT,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(enrollment_id) REFERENCES project_enrollments(id) ON DELETE CASCADE
    )
    """)

    # 9. Support Tickets table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS support_tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticket_number TEXT UNIQUE NOT NULL,
        user_id INTEGER NOT NULL,
        subject TEXT NOT NULL,
        category TEXT DEFAULT 'General',
        message TEXT NOT NULL,
        status TEXT DEFAULT 'open',
        priority TEXT DEFAULT 'normal',
        admin_response TEXT,
        is_demo INTEGER DEFAULT 0,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    """)

    # 10. Admin Settings table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS admin_settings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        setting_key TEXT UNIQUE NOT NULL,
        setting_value TEXT NOT NULL,
        description TEXT,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # 11. Demo Records Tracker table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS demo_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        entity_type TEXT NOT NULL,
        entity_id INTEGER NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # 12. Seed default admin_settings
    default_settings = [
        ("demo_mode", "1", "Toggle Illustrative Demo Mode (1=ON, 0=OFF)"),
        ("site_name", "PROJECTVERSE", "Official Marketplace Name"),
        ("site_tagline", "Ideas Into Innovation.", "Marketplace Tagline"),
        ("whatsapp_number", "918431712924", "Official Support WhatsApp Hotline"),
        ("upi_id", "8431712924-3@ybl", "Official Receiving UPI ID"),
        ("upi_name", "ANIL", "Official Receiving Payee Name"),
        ("min_price", "799", "Enforced Minimum Price for Projects"),
        ("enable_mentor_assignment", "1", "Allow automatic or manual mentor assignment"),
        ("enable_team_projects", "1", "Allow students to enroll in team project mode")
    ]
    for key, val, desc in default_settings:
        cur.execute("""
        INSERT OR IGNORE INTO admin_settings (setting_key, setting_value, description)
        VALUES (?, ?, ?)
        """, (key, val, desc))

    # 13. Seed default 6 Categories
    categories = [
        ("BCA", "BCA", "BCA Projects", "Foundation in application development, databases, and web systems.", 15, "purple", "monitor", 1),
        ("BCOM", "B.Com", "B.Com Projects", "Financial analytics, retail metrics, GST billing, and business intelligence.", 10, "emerald", "bar-chart-2", 2),
        ("BTECH", "B.Tech", "B.Tech Projects", "Core engineering, AI, ML, IoT, cloud, blockchain, and cybersecurity systems.", 25, "cyan", "cpu", 3),
        ("MCA", "MCA", "MCA Projects", "Advanced enterprise architectures, distributed platforms, RAG, and multi-agent AI.", 15, "indigo", "layers", 4),
        ("MTECH", "M.Tech", "M.Tech Projects", "Research-oriented engineering, federated learning, LLM optimization, and edge AI.", 15, "amber", "zap", 5),
        ("IIT", "IIT-Level / Research-Grade", "IIT-Level / Research-Grade Projects", "Challenging research themes inspired by premier engineering research institutes.", 10, "rose", "award", 6)
    ]
    for code, name, disp, desc, count, color, icon, order in categories:
        cur.execute("""
        INSERT OR REPLACE INTO categories (code, name, display_name, description, project_count, badge_color, icon, sort_order)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (code, name, disp, desc, count, color, icon, order))

    # 14. Seed Users with RBAC roles
    # Roles: super_admin, admin, project_manager, mentor, student
    # Password for all demo staff: Staff@12345
    import hashlib
    def hash_pw(pw):
        return hashlib.sha256(pw.encode()).hexdigest()

    staff_users = [
        ("superadmin@projectverse.com", hash_pw("Admin@12345"), "Super Administrator", "9876540001", "PROJECTVERSE HQ", "HQ", "Executive", "super_admin"),
        ("admin@projectverse.com", hash_pw("Admin@12345"), "PROJECTVERSE Administrator", "8431712924", "PROJECTVERSE HQ", "HQ", "Admin", "admin"),
        ("pm@projectverse.com", hash_pw("Staff@12345"), "Rajesh Verma (Project Manager)", "9876540002", "PROJECTVERSE Operations", "Operations", "PM", "project_manager"),
        ("mentor@projectverse.com", hash_pw("Staff@12345"), "Dr. Kavita Narang (Lead Academic Mentor)", "9876540003", "Faculty of Computer Science", "CSE", "Faculty", "mentor")
    ]
    for email, pw, name, mob, coll, crs, yr, role in staff_users:
        cur.execute("""
        INSERT OR REPLACE INTO users (email, password_hash, full_name, mobile, college, course, academic_year, role)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (email, pw, name, mob, coll, crs, yr, role))

    # 15. Seed Initial Mentors
    mentors_data = [
        ("Dr. Kavita Narang", "kavita.narang@projectverse.com", "9876540003", "Computer Science & Engineering", "Chief Academic Mentor", "Artificial Intelligence & Distributed Systems", 14, 25, 6, "Ph.D. in Computer Science with 14 years mentoring final-year engineering projects."),
        ("Prof. Arvind Swaminathan", "arvind.s@projectverse.com", "9876540004", "Data Science & Mathematics", "Senior Faculty Advisor", "Machine Learning, Deep Learning & Predictive Analytics", 11, 25, 5, "Specializes in PyTorch, statistical modeling, and data science capstone defenses."),
        ("Er. Priya Chandran", "priya.c@projectverse.com", "9876540005", "Information Technology", "Enterprise Architect Mentor", "Full Stack Development, Microservices & Cloud", 9, 25, 7, "Ex-SaaS Lead Engineer guiding students on React, Next.js, and cloud deployments."),
        ("Dr. Sandeep Kulkarni", "sandeep.k@projectverse.com", "9876540006", "Commerce & Financial Analytics", "Business Intelligence Mentor", "GST, Financial Modeling, Power BI & Business Analytics", 12, 25, 4, "Commerce advisor guiding B.Com and MBA analytics projects with real-world case studies."),
        ("Dr. Vikramaditya Roy", "vikram.roy@projectverse.com", "9876540007", "Cybersecurity & Cryptography", "Research Fellow Mentor", "Blockchain, Zero Trust, Network Security & Ethical Hacking", 10, 25, 4, "Security researcher advising B.Tech and M.Tech thesis defenses on intrusion detection."),
        ("Er. Meera Nambiar", "meera.n@projectverse.com", "9876540008", "Advanced AI & NLP", "Research Mentor", "Generative AI, LLM Optimization, Graph Neural Networks", 8, 20, 5, "Published author in IEEE conferences; guides IIT-grade advanced RAG and multi-agent platforms.")
    ]
    for name, email, mob, dept, desig, spec, exp, max_s, act_s, bio in mentors_data:
        cur.execute("""
        INSERT OR REPLACE INTO mentors (full_name, email, mobile, department, designation, specialization, experience_years, max_students, active_students, is_available, bio)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 1, ?)
        """, (name, email, mob, dept, desig, spec, exp, max_s, act_s, bio))

    conn.commit()
    conn.close()
    print("Database schema successfully upgraded with enterprise tables, settings, categories, and staff!")

if __name__ == "__main__":
    upgrade_schema()
