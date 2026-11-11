"""
PROJECTVERSE - Referral & 25% Commission Management Database Migration
Creates tables for:
- referral_partners
- referral_codes
- referral_clicks
- referral_attributions
- referral_conversions
- referral_commissions
- referral_payout_requests
- referral_payout_transactions
- referral_settings
"""
import sqlite3
import os

DB_PATH = os.getenv("PROJECTVERSE_DB", "projectverse.db")

def migrate():
    conn = sqlite3.connect(DB_PATH, timeout=30.0)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA busy_timeout=30000")
    cur = conn.cursor()

    # 1. Referral Partners
    cur.execute("""
    CREATE TABLE IF NOT EXISTS referral_partners (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        full_name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        mobile TEXT NOT NULL,
        password_hash TEXT NOT NULL,
        college_name TEXT,
        city TEXT,
        preferred_payment_method TEXT DEFAULT 'UPI',
        upi_id TEXT,
        bank_account_name TEXT,
        bank_account_number TEXT,
        bank_ifsc TEXT,
        bank_name TEXT,
        status TEXT DEFAULT 'PENDING',  -- PENDING, APPROVED, REJECTED, SUSPENDED
        admin_notes TEXT DEFAULT '',
        total_clicks INTEGER DEFAULT 0,
        total_registrations INTEGER DEFAULT 0,
        total_sales INTEGER DEFAULT 0,
        total_commission_earned REAL DEFAULT 0.0,
        total_commission_paid REAL DEFAULT 0.0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
    )
    """)

    # 2. Referral Codes
    cur.execute("""
    CREATE TABLE IF NOT EXISTS referral_codes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        partner_id INTEGER NOT NULL,
        code TEXT UNIQUE NOT NULL,
        url_slug TEXT,
        is_active INTEGER DEFAULT 1,
        clicks_count INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (partner_id) REFERENCES referral_partners(id) ON DELETE CASCADE
    )
    """)

    # 3. Referral Clicks
    cur.execute("""
    CREATE TABLE IF NOT EXISTS referral_clicks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        referral_code TEXT NOT NULL,
        partner_id INTEGER,
        ip_address TEXT,
        user_agent TEXT,
        referrer_url TEXT,
        landing_page TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (partner_id) REFERENCES referral_partners(id) ON DELETE SET NULL
    )
    """)

    # 4. Referral Attributions (Student registered via referral link)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS referral_attributions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        partner_id INTEGER NOT NULL,
        referral_code TEXT NOT NULL,
        student_user_id INTEGER NOT NULL,
        student_email TEXT,
        student_mobile TEXT,
        ip_address TEXT,
        attribution_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        expires_at TIMESTAMP,
        is_active INTEGER DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (partner_id) REFERENCES referral_partners(id) ON DELETE CASCADE,
        FOREIGN KEY (student_user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    """)

    # 5. Referral Conversions (Order placed by referred student)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS referral_conversions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        partner_id INTEGER NOT NULL,
        referral_code TEXT NOT NULL,
        attribution_id INTEGER,
        order_id INTEGER UNIQUE NOT NULL,
        order_number TEXT NOT NULL,
        user_id INTEGER NOT NULL,
        project_id INTEGER NOT NULL,
        order_amount REAL NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (partner_id) REFERENCES referral_partners(id) ON DELETE CASCADE,
        FOREIGN KEY (attribution_id) REFERENCES referral_attributions(id) ON DELETE SET NULL,
        FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
    )
    """)

    # 6. Referral Commissions (25% calculated on verified orders)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS referral_commissions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        partner_id INTEGER NOT NULL,
        conversion_id INTEGER,
        order_id INTEGER UNIQUE NOT NULL,
        order_number TEXT NOT NULL,
        order_amount REAL NOT NULL,
        commission_rate REAL DEFAULT 0.25,
        commission_amount REAL NOT NULL,
        status TEXT DEFAULT 'PENDING',  -- PENDING, APPROVED, PAYOUT_REQUESTED, PROCESSING, PAID, REVERSED
        notes TEXT DEFAULT '',
        payout_request_id INTEGER,
        approved_by TEXT,
        approved_at TIMESTAMP,
        paid_at TIMESTAMP,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (partner_id) REFERENCES referral_partners(id) ON DELETE CASCADE,
        FOREIGN KEY (conversion_id) REFERENCES referral_conversions(id) ON DELETE SET NULL,
        FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE
    )
    """)

    # 7. Referral Payout Requests
    cur.execute("""
    CREATE TABLE IF NOT EXISTS referral_payout_requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        request_number TEXT UNIQUE NOT NULL,
        partner_id INTEGER NOT NULL,
        amount REAL NOT NULL,
        payment_method TEXT DEFAULT 'UPI',
        payout_details TEXT,  -- UPI ID or Bank account info
        status TEXT DEFAULT 'PENDING',  -- PENDING, PROCESSING, PAID, REJECTED
        admin_notes TEXT DEFAULT '',
        requested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        processed_at TIMESTAMP,
        FOREIGN KEY (partner_id) REFERENCES referral_partners(id) ON DELETE CASCADE
    )
    """)

    # 8. Referral Payout Transactions (Proof of bank/UPI settlement)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS referral_payout_transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        payout_request_id INTEGER NOT NULL,
        partner_id INTEGER NOT NULL,
        amount REAL NOT NULL,
        payment_method TEXT DEFAULT 'UPI',
        utr_reference TEXT NOT NULL,
        receipt_path TEXT,
        status TEXT DEFAULT 'PAID',
        processed_by TEXT,
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (payout_request_id) REFERENCES referral_payout_requests(id) ON DELETE CASCADE,
        FOREIGN KEY (partner_id) REFERENCES referral_partners(id) ON DELETE CASCADE
    )
    """)

    # 9. Referral Settings
    cur.execute("""
    CREATE TABLE IF NOT EXISTS referral_settings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        setting_key TEXT UNIQUE NOT NULL,
        setting_value TEXT NOT NULL,
        description TEXT,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Insert default settings if not exists
    default_settings = [
        ("commission_rate_percentage", "25", "Standard referral commission percentage (e.g. 25%)"),
        ("attribution_window_days", "30", "Attribution window in days (cookie / localStorage duration)"),
        ("minimum_payout_amount", "500", "Minimum balance in INR required to request a payout"),
        ("auto_approve_partners", "0", "Require admin approval for new partners (1 = auto, 0 = manual)"),
        ("exclude_tax_from_commission", "1", "Exclude 18% GST tax from commission calculation base")
    ]
    for key, val, desc in default_settings:
        cur.execute("""
        INSERT OR IGNORE INTO referral_settings (setting_key, setting_value, description)
        VALUES (?, ?, ?)
        """, (key, val, desc))

    # Add indexes for high performance
    cur.execute("CREATE INDEX IF NOT EXISTS idx_ref_codes_code ON referral_codes(code)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_ref_clicks_code ON referral_clicks(referral_code)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_ref_attr_user ON referral_attributions(student_user_id)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_ref_attr_code ON referral_attributions(referral_code)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_ref_comm_partner ON referral_commissions(partner_id)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_ref_comm_status ON referral_commissions(status)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_ref_conv_order ON referral_conversions(order_id)")

    conn.commit()
    conn.close()
    print("Referral & 25% Commission system tables created successfully!")

if __name__ == "__main__":
    migrate()
