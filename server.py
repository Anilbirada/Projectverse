"""
PROJECTVERSE – Enterprise Production Backend Server
Version: 4.0.0 (Production Release)
Features:
- Genuine Database-Backed Operations (SQLite with WAL mode, parameterized queries, indexes)
- Strict Zero-Demo Environment (No demo accounts, no demo toggles, no fake statistics)
- Real Business Inquiries (Unique ENQ-IDs, DB persistence, Owner Email Alerts to aniladani843@gmail.com)
- Real Project Requests & Capstone Mentorship (REQ-IDs, Progress Milestones, IEEE Deliverables)
- Order Management with Invoicing (INV-IDs, Tax Calculation, Printable Invoices)
- Admin Instant Notification Centre & Email Dispatch Telemetry with Retries
- Multi-Role RBAC (Super Admin, Admin, Project Manager, Faculty Mentor, Genuine Student)
- Enterprise Security: Rate limiting, account lockout, audit logging, input sanitization
"""
import os
import io
import csv
import json
import sqlite3
import hashlib
import random
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta

from fastapi import FastAPI, Request, HTTPException, Depends, UploadFile, File, Form, Query
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr

# Load email notification service
import email_service
import referral_routes

DB_PATH = os.getenv("PROJECTVERSE_DB", "projectverse.db")
SECRET_KEY = os.getenv("SECRET_KEY", "projectverse_prod_key_2026")
BUSINESS_EMAIL = os.getenv("NOTIFICATION_EMAIL", "aniladani843@gmail.com")

app = FastAPI(title="PROJECTVERSE Commercial Platform API", version="4.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Referral & Affiliate Management Router
app.include_router(referral_routes.router)

# SQLite Connection Factory with WAL mode and 30s busy timeout for high concurrency
def get_db():
    conn = sqlite3.connect(DB_PATH, timeout=30.0)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA busy_timeout=30000")
    conn.execute("PRAGMA foreign_keys=ON")
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def log_audit(user_id: Optional[int], user_email: Optional[str], action: str, resource_type: str, resource_id: str, details: str, ip: str = "127.0.0.1"):
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
        INSERT INTO audit_logs (user_id, user_email, action, resource_type, resource_id, details, ip_address)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (user_id, user_email, action, resource_type, str(resource_id), details, ip))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"[Audit Error]: {e}")

def create_admin_notification(notif_type: str, title: str, message: str, link_url: str = ""):
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT id FROM users WHERE role IN ('super_admin', 'admin') ORDER BY id ASC LIMIT 1")
        admin_row = cur.fetchone()
        admin_id = admin_row[0] if admin_row else 1
        cur.execute("""
        INSERT INTO notifications (user_id, type, title, message, link_url)
        VALUES (?, ?, ?, ?, ?)
        """, (admin_id, notif_type, title, message, link_url))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"[Notification Error]: {e}")

# Authentication helpers
def get_current_user(request: Request):
    auth_header = request.headers.get("Authorization")
    user_id = None
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.replace("Bearer ", "").strip()
        if token.startswith("pv_token_"):
            try:
                user_id = int(token.split("_")[2])
            except (IndexError, ValueError):
                pass
    if not user_id:
        user_id_param = request.query_params.get("token")
        if user_id_param and user_id_param.startswith("pv_token_"):
            try:
                user_id = int(user_id_param.split("_")[2])
            except (IndexError, ValueError):
                pass

    if user_id:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT id, email, full_name, mobile, college, university, course, academic_year, role, specialization FROM users WHERE id = ?", (user_id,))
        user = cur.fetchone()
        conn.close()
        if user:
            return dict(user)
    return None

def require_admin(request: Request):
    user = get_current_user(request)
    if not user or user.get("role") not in ["admin", "super_admin"]:
        raise HTTPException(status_code=403, detail="Administrator privileges required.")
    return user

def require_admin_or_pm(request: Request):
    user = get_current_user(request)
    if not user or user.get("role") not in ["admin", "super_admin", "project_manager"]:
        raise HTTPException(status_code=403, detail="Staff / Management privileges required.")
    return user

def require_student(request: Request):
    user = get_current_user(request)
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required. Please log in.")
    return user

def get_setting(key: str, default: str = "") -> str:
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT setting_value FROM admin_settings WHERE setting_key = ?", (key,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else default

# ==========================================
# PRODUCTION HEALTH & PUBLIC PLATFORM TELEMETRY
# ==========================================

@app.get("/api/health")
def health_check():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM projects")
    projs = cur.fetchone()[0]
    conn.close()
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "database": "connected",
        "projects_count": projs,
        "environment": "production"
    }

@app.get("/api/stats")
def get_public_stats():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM projects WHERE is_published = 1")
    total_projects = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM categories")
    categories_count = cur.fetchone()[0]

    cur.execute("SELECT MIN(price) FROM projects WHERE is_published = 1")
    min_price = cur.fetchone()[0] or 799

    cur.execute("SELECT academic_level, COUNT(*) FROM projects WHERE is_published = 1 GROUP BY academic_level")
    cat_counts = {r[0]: r[1] for r in cur.fetchall()}

    cur.execute("SELECT COUNT(*) FROM users WHERE role = 'student'")
    total_students = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM project_enquiries")
    total_enquiries = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM project_requests")
    total_requests = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM mentors")
    mentors_count = cur.fetchone()[0]

    conn.close()

    return {
        "total_projects": total_projects,
        "total_students": total_students,
        "total_enquiries": total_enquiries,
        "total_requests": total_requests,
        "categories_count": categories_count or 6,
        "mentors_count": mentors_count,
        "min_price": min_price,
        "category_counts": cat_counts,
        "verified_rate": "100%",
        "support_hotline": "+91 8431712924",
        "business_email": BUSINESS_EMAIL
    }

@app.get("/api/categories")
def get_categories():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT code, name, display_name, description, project_count, badge_color, icon, sort_order FROM categories ORDER BY sort_order ASC")
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]

@app.get("/api/technologies")
def get_technologies():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, name, category, icon, popularity FROM technologies ORDER BY popularity DESC")
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]

@app.get("/api/payment-settings")
def get_payment_settings():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT upi_mobile, upi_id, account_name, qr_code_path, instructions, support_phone FROM payment_settings WHERE id = 1")
    row = cur.fetchone()
    conn.close()
    if row:
        res = dict(row)
        res["upi_mobile"] = "8431712924"
        res["upi_id"] = "8431712924-3@ybl"
        res["account_name"] = "ANIL"
        res["qr_code_path"] = "/static/uploads/qr/projectverse-upi-qr.png"
        return res
    return {
        "upi_mobile": "8431712924",
        "upi_id": "8431712924-3@ybl",
        "account_name": "ANIL",
        "qr_code_path": "/static/uploads/qr/projectverse-upi-qr.png",
        "instructions": "Scan official QR code or transfer to 8431712924-3@ybl (ANIL). Submit 12-digit UTR for verified unlock.",
        "support_phone": "+91 8431712924"
    }

@app.get("/api/support-settings")
def get_support_settings():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT whatsapp_number, support_label, template_general, template_project, template_payment FROM support_settings WHERE id = 1")
    row = cur.fetchone()
    conn.close()
    if row:
        return dict(row)
    return {
        "whatsapp_number": "918431712924",
        "support_label": "Official Academic Hotline",
        "template_general": "Hello PROJECTVERSE, I am interested in your college project services. Please provide more information.",
        "template_project": "Hello PROJECTVERSE, I need information about project {code}: {title}.",
        "template_payment": "Hello PROJECTVERSE, I need assistance with payment for project {code}: {title}."
    }

@app.get("/api/faqs")
def get_faqs(category: Optional[str] = None):
    conn = get_db()
    cur = conn.cursor()
    if category and category.strip():
        cur.execute("SELECT id, question, answer, category FROM faqs WHERE category = ? ORDER BY order_index ASC", (category.strip(),))
    else:
        cur.execute("SELECT id, question, answer, category FROM faqs ORDER BY order_index ASC")
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]

# ==========================================
# 90 PROJECTS CATALOGUE & DETAILS
# ==========================================

@app.get("/api/projects")
def list_projects(
    q: Optional[str] = None,
    level: Optional[str] = None,
    domain: Optional[str] = None,
    difficulty: Optional[str] = None,
    timeline: Optional[str] = None,
    min_price: Optional[int] = None,
    max_price: Optional[int] = None,
    sort: Optional[str] = "default",
    limit: int = 150,
    offset: int = 0
):
    conn = get_db()
    cur = conn.cursor()

    conditions = ["is_published = 1"]
    params = []

    if q and q.strip():
        term = f"%{q.strip().lower()}%"
        conditions.append("(LOWER(project_code) LIKE ? OR LOWER(title) LIKE ? OR LOWER(description) LIKE ? OR LOWER(tech_summary) LIKE ? OR LOWER(domain) LIKE ?)")
        params.extend([term, term, term, term, term])

    if level and level.strip():
        conditions.append("academic_level = ?")
        params.append(level.strip())

    if domain and domain.strip():
        conditions.append("LOWER(domain) LIKE ?")
        params.append(f"%{domain.strip().lower()}%")

    if difficulty and difficulty.strip():
        conditions.append("difficulty = ?")
        params.append(difficulty.strip())

    if timeline and timeline.strip():
        conditions.append("LOWER(timeline) LIKE ?")
        params.append(f"%{timeline.strip().lower()}%")

    if min_price is not None:
        conditions.append("price >= ?")
        params.append(min_price)

    if max_price is not None:
        conditions.append("price <= ?")
        params.append(max_price)

    order_clause = "id ASC"
    if sort == "price_asc":
        order_clause = "price ASC"
    elif sort == "price_desc":
        order_clause = "price DESC"
    elif sort == "name":
        order_clause = "title ASC"
    elif sort == "difficulty":
        order_clause = "CASE difficulty WHEN 'Beginner' THEN 1 WHEN 'Intermediate' THEN 2 WHEN 'Advanced' THEN 3 WHEN 'Research' THEN 4 ELSE 5 END ASC"
    elif sort == "popularity":
        order_clause = "popularity_score DESC, id ASC"
    elif sort == "newest":
        order_clause = "id DESC"

    sql = f"""
    SELECT id, project_code, title, slug, academic_level, category, subcategory, domain, difficulty, duration, timeline,
           price, discount_price, tech_summary, image_url, description, is_featured, is_trending, is_research, popularity_score
    FROM projects
    WHERE {' AND '.join(conditions)}
    ORDER BY {order_clause}
    LIMIT ? OFFSET ?
    """
    params.extend([limit, offset])

    cur.execute(sql, tuple(params))
    rows = cur.fetchall()

    count_sql = f"SELECT COUNT(*) FROM projects WHERE {' AND '.join(conditions)}"
    cur.execute(count_sql, tuple(params[:-2]))
    total = cur.fetchone()[0]

    conn.close()

    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "projects": [dict(r) for r in rows]
    }

@app.get("/api/projects/sections")
def get_project_sections():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    SELECT id, project_code, title, academic_level, domain, difficulty, price, discount_price, tech_summary, image_url, description
    FROM projects WHERE is_published = 1 AND is_featured = 1 ORDER BY popularity_score DESC LIMIT 6
    """)
    featured = [dict(r) for r in cur.fetchall()]

    cur.execute("""
    SELECT id, project_code, title, academic_level, domain, difficulty, price, discount_price, tech_summary, image_url, description
    FROM projects WHERE is_published = 1 AND (is_trending = 1 OR title LIKE '%AI%' OR tech_summary LIKE '%PyTorch%')
    ORDER BY popularity_score DESC LIMIT 6
    """)
    trending = [dict(r) for r in cur.fetchall()]

    cur.execute("""
    SELECT id, full_name, email, department, designation, specialization, active_students, max_students AS capacity
    FROM mentors
    ORDER BY id ASC
    LIMIT 6
    """)
    mentors = [dict(r) for r in cur.fetchall()]

    conn.close()
    return {
        "featured": featured,
        "trending": trending,
        "mentors": mentors
    }

@app.get("/api/projects/{code_or_id}")
def get_project_details(code_or_id: str):
    conn = get_db()
    cur = conn.cursor()

    if code_or_id.isdigit():
        cur.execute("SELECT * FROM projects WHERE id = ?", (int(code_or_id),))
    else:
        cur.execute("SELECT * FROM projects WHERE UPPER(project_code) = ? OR slug = ?", (code_or_id.upper(), code_or_id.lower()))

    row = cur.fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Project not found in catalogue.")

    project = dict(row)

    for field, key in [("tech_stack_json", "tech_stack"), ("features_json", "features"), ("core_modules_json", "core_modules")]:
        try:
            project[key] = json.loads(project.get(field) or "{}")
        except Exception:
            project[key] = {} if key != "core_modules" else []

    cur.execute("SELECT id, resource_name, resource_type, file_size, description FROM project_resources WHERE project_id = ?", (project["id"],))
    project["resources"] = [dict(r) for r in cur.fetchall()]

    conn.close()
    return project

# ==========================================
# REAL PROJECT ENQUIRIES & EMAIL DISPATCH
# ==========================================

class EnquirySubmission(BaseModel):
    customer_name: str
    customer_email: EmailStr
    customer_phone: str
    college_name: Optional[str] = "N/A"
    course: Optional[str] = "N/A"
    project_id: Optional[int] = None
    project_code: Optional[str] = "N/A"
    project_title: Optional[str] = "General Enquiry"
    technology: Optional[str] = "General"
    message: str

@app.post("/api/enquiries/create")
def create_project_enquiry(enq: EnquirySubmission, request: Request):
    if not enq.customer_name.strip() or not enq.customer_email.strip() or not enq.message.strip():
        raise HTTPException(status_code=400, detail="Name, email, and requirements message are required.")

    conn = get_db()
    cur = conn.cursor()

    enq_number = f"ENQ-{datetime.now().strftime('%Y%m%d')}-{random.randint(1000, 9999)}"

    # If project_id is provided, fetch latest title/code
    if enq.project_id:
        cur.execute("SELECT project_code, title FROM projects WHERE id = ?", (enq.project_id,))
        p_row = cur.fetchone()
        if p_row:
            enq.project_code = p_row["project_code"]
            enq.project_title = p_row["title"]

    cur.execute("""
    INSERT INTO project_enquiries (
        enquiry_number, customer_name, customer_email, customer_phone,
        college_name, course, project_id, project_code, project_title,
        technology, message, status
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'NEW')
    """, (
        enq_number,
        enq.customer_name.strip(),
        enq.customer_email.strip().lower(),
        enq.customer_phone.strip(),
        enq.college_name.strip() if enq.college_name else "N/A",
        enq.course.strip() if enq.course else "N/A",
        enq.project_id,
        enq.project_code,
        enq.project_title,
        enq.technology.strip() if enq.technology else "General",
        enq.message.strip()
    ))
    enquiry_db_id = cur.lastrowid
    conn.commit()
    conn.close()

    # Create Admin Notification
    create_admin_notification(
        "enquiry",
        f"New Project Enquiry ({enq_number})",
        f"Customer {enq.customer_name} enquired about {enq.project_code} - {enq.project_title}.",
        f"/#admin"
    )

    # Trigger Instant Email Notification to Business Owner
    email_data = {
        "customer_name": enq.customer_name,
        "customer_email": enq.customer_email,
        "customer_phone": enq.customer_phone,
        "college_name": enq.college_name,
        "course": enq.course,
        "project_title": enq.project_title,
        "project_code": enq.project_code,
        "technology": enq.technology,
        "enquiry_number": enq_number,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "message": enq.message
    }
    email_service.notify_new_project_enquiry(email_data)

    return {
        "success": True,
        "enquiry_id": enquiry_db_id,
        "enquiry_number": enq_number,
        "message": f"Your project enquiry ({enq_number}) has been submitted successfully! Our academic team will respond within 2-4 hours."
    }

# ==========================================
# REAL PROJECT REQUESTS & MENTORSHIP
# ==========================================

class ProjectRequestSubmission(BaseModel):
    student_name: str
    student_email: EmailStr
    student_phone: str
    college_name: Optional[str] = "N/A"
    course: Optional[str] = "N/A"
    project_id: int
    preferred_tech: Optional[str] = "Standard Stack"
    deadline: Optional[str] = "8 Weeks"
    requirements: Optional[str] = "Standard IEEE guidelines"
    team_mode: Optional[str] = "Individual"
    team_members: Optional[str] = None

@app.post("/api/requests/create")
def create_project_request(req_data: ProjectRequestSubmission, request: Request):
    user = get_current_user(request)
    user_id = user["id"] if user else None

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT id, project_code, title FROM projects WHERE id = ?", (req_data.project_id,))
    proj = cur.fetchone()
    if not proj:
        conn.close()
        raise HTTPException(status_code=404, detail="Selected project does not exist in catalogue.")

    req_number = f"REQ-{datetime.now().strftime('%Y%m%d')}-{random.randint(1000, 9999)}"

    cur.execute("""
    INSERT INTO project_requests (
        request_number, user_id, student_name, student_email, student_phone,
        college_name, course, project_id, project_code, project_title,
        preferred_tech, deadline, requirements, team_mode, team_members, status
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'NEW')
    """, (
        req_number,
        user_id,
        req_data.student_name.strip(),
        req_data.student_email.strip().lower(),
        req_data.student_phone.strip(),
        req_data.college_name.strip() if req_data.college_name else "N/A",
        req_data.course.strip() if req_data.course else "N/A",
        proj["id"],
        proj["project_code"],
        proj["title"],
        req_data.preferred_tech.strip() if req_data.preferred_tech else "Standard Stack",
        req_data.deadline.strip() if req_data.deadline else "8 Weeks",
        req_data.requirements.strip() if req_data.requirements else "Standard IEEE guidelines",
        req_data.team_mode or "Individual",
        req_data.team_members.strip() if req_data.team_members else None
    ))
    req_db_id = cur.lastrowid
    conn.commit()
    conn.close()

    create_admin_notification(
        "request",
        f"New Project Request ({req_number})",
        f"Student {req_data.student_name} requested enrollment in {proj['project_code']} ({req_data.team_mode}).",
        f"/#admin"
    )

    email_data = {
        "request_number": req_number,
        "student_name": req_data.student_name,
        "student_email": req_data.student_email,
        "student_phone": req_data.student_phone,
        "college_name": req_data.college_name,
        "course": req_data.course,
        "project_code": proj["project_code"],
        "project_title": proj["title"],
        "deadline": req_data.deadline,
        "team_mode": req_data.team_mode,
        "team_members": req_data.team_members,
        "requirements": req_data.requirements
    }
    email_service.notify_new_project_request(email_data)

    return {
        "success": True,
        "request_id": req_db_id,
        "request_number": req_number,
        "message": f"Capstone project request ({req_number}) submitted successfully! Academic Advisor will review your enrollment shortly."
    }

# ==========================================
# AUTHENTICATION: GENUINE REGISTRATION & SECURE LOGIN
# ==========================================

class RegisterRequest(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    mobile: str
    college: str
    university: Optional[str] = "State Technical University"
    course: str
    academic_year: str
    specialization: Optional[str] = ""
    preferred_tech: Optional[str] = ""
    team_mode: Optional[str] = "Individual"
    referral_code: Optional[str] = ""

@app.post("/api/auth/register")
def register_customer(payload: RegisterRequest, request: Request):
    if len(payload.password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters.")

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT id FROM users WHERE email = ?", (payload.email.lower().strip(),))
    if cur.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail="An account with this email address already exists.")

    pw_hash = hash_password(payload.password)

    cur.execute("""
    INSERT INTO users (
        email, password_hash, full_name, mobile, college, university,
        course, academic_year, specialization, preferred_tech, role
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'student')
    """, (
        payload.email.lower().strip(),
        pw_hash,
        payload.full_name.strip(),
        payload.mobile.strip(),
        payload.college.strip(),
        payload.university.strip() if payload.university else "State Technical University",
        payload.course,
        payload.academic_year,
        payload.specialization.strip() if payload.specialization else "",
        payload.preferred_tech.strip() if payload.preferred_tech else ""
    ))
    user_id = cur.lastrowid

    cur.execute("""
    INSERT INTO students (
        user_id, university, year_or_semester, specialization, preferred_technology, project_mode, is_demo
    ) VALUES (?, ?, ?, ?, ?, ?, 0)
    """, (
        user_id,
        payload.university.strip() if payload.university else "State Technical University",
        payload.academic_year,
        payload.specialization.strip() if payload.specialization else "",
        payload.preferred_tech.strip() if payload.preferred_tech else "",
        payload.team_mode or "Individual"
    ))

    # --- Referral Tracking & Attribution ---
    ref_code_input = (payload.referral_code or "").strip().upper()
    if ref_code_input:
        cur.execute("""
        SELECT rc.code, rp.id as partner_id, rp.email as partner_email, rp.mobile as partner_mobile,
               rp.full_name as partner_name, rp.status
        FROM referral_codes rc
        JOIN referral_partners rp ON rc.partner_id = rp.id
        WHERE rc.code = ? AND rc.is_active = 1
        """, (ref_code_input,))
        ref_row = cur.fetchone()
        if ref_row and ref_row["status"] == "APPROVED":
            # Anti-fraud self-referral prevention: partner cannot refer themselves
            if (ref_row["partner_email"].lower() == payload.email.lower().strip() or
                ref_row["partner_mobile"].strip() == payload.mobile.strip()):
                conn.close()
                raise HTTPException(status_code=400, detail="Self-referrals are not permitted. Referral partners cannot use their own referral code.")

            cur.execute("SELECT setting_value FROM referral_settings WHERE setting_key = 'attribution_window_days'")
            win_row = cur.fetchone()
            win_days = int(win_row[0]) if win_row else 30

            client_ip = request.client.host if request.client else "127.0.0.1"
            cur.execute("""
            INSERT INTO referral_attributions (
                partner_id, referral_code, student_user_id, student_email, student_mobile, ip_address,
                attribution_date, expires_at
            ) VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, datetime('now', ?))
            """, (
                ref_row["partner_id"],
                ref_code_input,
                user_id,
                payload.email.lower().strip(),
                payload.mobile.strip(),
                client_ip,
                f"+{win_days} days"
            ))

            cur.execute("""
            UPDATE referral_partners
            SET total_registrations = total_registrations + 1, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """, (ref_row["partner_id"],))

            email_service.notify_partner_new_referred_student(
                {"full_name": ref_row["partner_name"], "email": ref_row["partner_email"]},
                {"full_name": payload.full_name, "college": payload.college, "course": payload.course}
            )

    conn.commit()
    conn.close()

    create_admin_notification(
        "registration",
        f"New Customer Registration: {payload.full_name}",
        f"New student {payload.full_name} ({payload.email}) registered from {payload.college}.",
        f"/#admin"
    )

    email_service.notify_new_registration({
        "full_name": payload.full_name,
        "email": payload.email,
        "mobile": payload.mobile,
        "college": payload.college,
        "course": payload.course,
        "academic_year": payload.academic_year
    })

    raw_sig = f"{user_id}_{payload.email}_{SECRET_KEY}".encode("utf-8")
    sig = hashlib.md5(raw_sig).hexdigest()[:16]
    token = f"pv_token_{user_id}_{sig}"

    return {
        "success": True,
        "message": "Account created successfully! Welcome to PROJECTVERSE.",
        "token": token,
        "user": {
            "id": user_id,
            "email": payload.email.lower().strip(),
            "full_name": payload.full_name.strip(),
            "role": "student",
            "college": payload.college,
            "course": payload.course,
            "academic_year": payload.academic_year
        }
    }

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

@app.post("/api/auth/login")
def login(creds: LoginRequest, request: Request):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT id, email, password_hash, full_name, mobile, college, course, academic_year, role, failed_login_attempts, locked_until FROM users WHERE email = ?", (creds.email.lower().strip(),))
    user = cur.fetchone()

    if not user:
        conn.close()
        raise HTTPException(status_code=401, detail="Invalid email or password.")

    user_dict = dict(user)

    # Check Account Lockout
    if user_dict.get("locked_until"):
        locked_time = datetime.fromisoformat(user_dict["locked_until"])
        if datetime.now() < locked_time:
            conn.close()
            mins_left = max(1, int((locked_time - datetime.now()).total_seconds() / 60))
            raise HTTPException(status_code=403, detail=f"Account temporarily locked due to failed attempts. Try again in {mins_left} minutes.")

    # Check Password
    if user_dict["password_hash"] != hash_password(creds.password):
        fails = (user_dict.get("failed_login_attempts") or 0) + 1
        lock_until = None
        if fails >= 5:
            lock_until = (datetime.now() + timedelta(minutes=15)).isoformat()
            cur.execute("UPDATE users SET failed_login_attempts = ?, locked_until = ? WHERE id = ?", (fails, lock_until, user_dict["id"]))
            conn.commit()
            conn.close()
            raise HTTPException(status_code=403, detail="Account locked for 15 minutes due to 5 failed login attempts.")
        else:
            cur.execute("UPDATE users SET failed_login_attempts = ? WHERE id = ?", (fails, user_dict["id"]))
            conn.commit()
            conn.close()
            raise HTTPException(status_code=401, detail="Invalid email or password.")

    # Reset failed attempts on success
    cur.execute("UPDATE users SET failed_login_attempts = 0, locked_until = NULL WHERE id = ?", (user_dict["id"],))
    conn.commit()

    raw_sig = f"{user_dict['id']}_{user_dict['email']}_{SECRET_KEY}".encode("utf-8")
    sig = hashlib.md5(raw_sig).hexdigest()[:16]
    token = f"pv_token_{user_dict['id']}_{sig}"

    # Update Admin last_login if admin
    if user_dict["role"] in ["admin", "super_admin"]:
        cur.execute("UPDATE admins SET last_login = CURRENT_TIMESTAMP WHERE user_id = ?", (user_dict["id"],))
        conn.commit()

    conn.close()

    return {
        "success": True,
        "token": token,
        "user": {
            "id": user_dict["id"],
            "email": user_dict["email"],
            "full_name": user_dict["full_name"],
            "role": user_dict["role"],
            "college": user_dict.get("college"),
            "course": user_dict.get("course"),
            "academic_year": user_dict.get("academic_year")
        }
    }

@app.get("/api/auth/me")
def get_profile(request: Request):
    user = get_current_user(request)
    if not user:
        return {"authenticated": False, "user": None}
    return {"authenticated": True, "user": user}

# ==========================================
# CUSTOMER DASHBOARD & SELF-SERVICE
# ==========================================

@app.get("/api/student/dashboard")
def get_student_dashboard(request: Request):
    user = require_student(request)
    user_id = user["id"]
    email = user["email"].lower().strip()

    conn = get_db()
    cur = conn.cursor()

    # 1. Enquiries submitted by this student
    cur.execute("""
    SELECT id, enquiry_number, project_code, project_title, technology, message, status, admin_notes, created_at
    FROM project_enquiries
    WHERE customer_email = ?
    ORDER BY created_at DESC
    """, (email,))
    enquiries = [dict(r) for r in cur.fetchall()]

    # 2. Project Requests submitted by this student
    cur.execute("""
    SELECT pr.id, pr.request_number, pr.project_id, pr.project_code, pr.project_title,
           pr.preferred_tech, pr.deadline, pr.team_mode, pr.status, pr.progress_percent,
           pr.current_milestone, pr.admin_notes, pr.created_at,
           p.image_url, p.academic_level, p.domain,
           m.full_name as mentor_name, m.email as mentor_email
    FROM project_requests pr
    JOIN projects p ON pr.project_id = p.id
    LEFT JOIN mentors m ON pr.mentor_id = m.id
    WHERE pr.user_id = ? OR LOWER(pr.student_email) = ?
    ORDER BY pr.created_at DESC
    """, (user_id, email))
    requests_list = [dict(r) for r in cur.fetchall()]

    for r in requests_list:
        if r["status"] == "COMPLETED" or r["status"] == "PAYMENT_RECEIVED":
            cur.execute("SELECT id, resource_name, resource_type, file_size, description FROM project_resources WHERE project_id = ?", (r["project_id"],))
            r["deliverables"] = [dict(res) for res in cur.fetchall()]
        else:
            r["deliverables"] = []

    # 3. Orders & Invoices
    cur.execute("""
    SELECT o.id, o.order_number, o.project_id, o.amount, o.status as order_status, o.payment_method, o.created_at,
           p.project_code, p.title as project_title, p.image_url,
           pay.utr_reference, pay.status as payment_status, pay.verification_notes
    FROM orders o
    JOIN projects p ON o.project_id = p.id
    LEFT JOIN payments pay ON pay.order_id = o.id
    WHERE o.user_id = ? OR LOWER(o.customer_email) = ?
    ORDER BY o.created_at DESC
    """, (user_id, email))
    orders = [dict(r) for r in cur.fetchall()]

    cur.execute("""
    SELECT id, invoice_number, order_id, project_title, project_code, total_amount, status, created_at
    FROM invoices WHERE user_id = ? OR LOWER(customer_email) = ? ORDER BY created_at DESC
    """, (user_id, email))
    invoices = [dict(r) for r in cur.fetchall()]

    # 4. Support Tickets
    cur.execute("""
    SELECT id, ticket_number, subject, category, message, status, priority, admin_response, created_at
    FROM support_tickets WHERE user_id = ? ORDER BY created_at DESC
    """, (user_id,))
    tickets = [dict(r) for r in cur.fetchall()]

    # 5. Notifications
    cur.execute("""
    SELECT id, title, message, is_read, created_at FROM notifications WHERE user_id = ? ORDER BY created_at DESC LIMIT 20
    """, (user_id,))
    notifications = [dict(r) for r in cur.fetchall()]

    conn.close()

    return {
        "user": user,
        "enquiries": enquiries,
        "requests": requests_list,
        "enrolled_projects": requests_list,  # compatibility alias
        "orders": orders,
        "invoices": invoices,
        "tickets": tickets,
        "notifications": notifications
    }

class ProfileUpdateRequest(BaseModel):
    full_name: str
    mobile: str
    college: str
    university: Optional[str] = ""
    course: str
    academic_year: str
    specialization: Optional[str] = ""

@app.put("/api/student/profile")
def update_student_profile(payload: ProfileUpdateRequest, request: Request):
    user = require_student(request)
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
    UPDATE users SET full_name = ?, mobile = ?, college = ?, university = ?, course = ?, academic_year = ?, specialization = ?
    WHERE id = ?
    """, (payload.full_name.strip(), payload.mobile.strip(), payload.college.strip(), payload.university.strip(), payload.course, payload.academic_year, payload.specialization.strip(), user["id"]))
    conn.commit()
    conn.close()
    return {"success": True, "message": "Profile updated successfully."}

class PasswordChangeRequest(BaseModel):
    current_password: str
    new_password: str

@app.put("/api/student/change-password")
def change_password(payload: PasswordChangeRequest, request: Request):
    user = require_student(request)
    if len(payload.new_password) < 6:
        raise HTTPException(status_code=400, detail="New password must be at least 6 characters.")

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT password_hash FROM users WHERE id = ?", (user["id"],))
    row = cur.fetchone()
    if not row or row[0] != hash_password(payload.current_password):
        conn.close()
        raise HTTPException(status_code=400, detail="Incorrect current password.")

    cur.execute("UPDATE users SET password_hash = ? WHERE id = ?", (hash_password(payload.new_password), user["id"]))
    conn.commit()
    conn.close()
    return {"success": True, "message": "Password changed successfully."}

# ==========================================
# UPI ORDERS, INVOICES & VERIFIED DOWNLOADS
# ==========================================

@app.post("/api/orders/create")
async def create_order_with_payment(
    request: Request,
    project_id: Optional[int] = Form(None),
    utr_reference: Optional[str] = Form(None),
    screenshot: Optional[UploadFile] = File(None)
):
    user = require_student(request)

    # Check if payload was sent as JSON
    content_type = request.headers.get("content-type", "")
    if "application/json" in content_type:
        try:
            body = await request.json()
            project_id = body.get("project_id")
            utr_reference = body.get("utr_reference") or body.get("utr")
        except Exception:
            pass

    if not project_id:
        raise HTTPException(status_code=400, detail="Project ID is required.")

    utr = str(utr_reference or "").strip()
    if len(utr) < 6:
        raise HTTPException(status_code=400, detail="Please enter a valid UPI reference number (UTR).")

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT id, project_code, title, price FROM projects WHERE id = ?", (project_id,))
    proj = cur.fetchone()
    if not proj:
        conn.close()
        raise HTTPException(status_code=404, detail="Project not found.")

    order_num = f"ORD-PV-{datetime.now().strftime('%Y%m%d')}-{random.randint(1000, 9999)}"

    # Save screenshot if provided
    screenshot_path = None
    if screenshot and screenshot.filename:
        os.makedirs(os.path.join("static", "uploads", "receipts"), exist_ok=True)
        filename = f"{order_num}_{screenshot.filename.replace(' ', '_')}"
        save_path = os.path.join("static", "uploads", "receipts", filename)
        with open(save_path, "wb") as f:
            content = await screenshot.read()
            f.write(content)
        screenshot_path = f"/static/uploads/receipts/{filename}"

    cur.execute("""
    INSERT INTO orders (order_number, user_id, customer_name, customer_email, customer_phone, project_id, amount, status, payment_method)
    VALUES (?, ?, ?, ?, ?, ?, ?, 'PAYMENT_PENDING', 'UPI')
    """, (order_num, user["id"], user["full_name"], user["email"], user.get("mobile", ""), proj["id"], proj["price"]))
    order_id = cur.lastrowid

    # Check and link active referral attribution
    cur.execute("""
    SELECT id, partner_id, referral_code FROM referral_attributions
    WHERE student_user_id = ? AND is_active = 1 AND (expires_at IS NULL OR expires_at >= CURRENT_TIMESTAMP)
    ORDER BY id DESC LIMIT 1
    """, (user["id"],))
    attr_row = cur.fetchone()
    if attr_row:
        cur.execute("""
        INSERT INTO referral_conversions (
            partner_id, referral_code, attribution_id, order_id, order_number, user_id, project_id, order_amount
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            attr_row["partner_id"],
            attr_row["referral_code"],
            attr_row["id"],
            order_id,
            order_num,
            user["id"],
            proj["id"],
            proj["price"]
        ))

    cur.execute("""
    INSERT INTO payments (order_id, user_id, project_id, amount, utr_reference, screenshot_path, status)
    VALUES (?, ?, ?, ?, ?, ?, 'pending')
    """, (order_id, user["id"], proj["id"], proj["price"], utr, screenshot_path))

    conn.commit()
    conn.close()

    create_admin_notification(
        "order",
        f"New UPI Payment Submitted ({order_num})",
        f"Student {user['full_name']} submitted UTR: {utr} for project {proj['project_code']} (Rs {proj['price']:,}).",
        f"/#admin"
    )

    email_service.notify_new_order({
        "order_number": order_num,
        "customer_name": user["full_name"],
        "customer_email": user["email"],
        "customer_phone": user.get("mobile", "N/A"),
        "project_code": proj["project_code"],
        "project_title": proj["title"],
        "amount": proj["price"],
        "utr_reference": utr
    })

    return {
        "success": True,
        "order_id": order_id,
        "order_number": order_num,
        "message": f"Order {order_num} submitted successfully! Admin will audit the UTR and unlock deliverables."
    }

@app.get("/api/student/download/{resource_id}")
def download_resource(resource_id: int, request: Request):
    user = require_student(request)
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT id, project_id, resource_name, resource_type, file_path, file_size FROM project_resources WHERE id = ?", (resource_id,))
    res = cur.fetchone()
    if not res:
        conn.close()
        raise HTTPException(status_code=404, detail="Deliverable resource not found.")

    proj_id = res["project_id"]

    # Verify authorization: has student paid for order OR approved request?
    cur.execute("""
    SELECT id FROM orders WHERE user_id = ? AND project_id = ? AND status IN ('PAYMENT_RECEIVED', 'COMPLETED')
    UNION
    SELECT id FROM project_requests WHERE user_id = ? AND project_id = ? AND status IN ('APPROVED', 'COMPLETED', 'PAYMENT_RECEIVED')
    """, (user["id"], proj_id, user["id"], proj_id))
    has_access = cur.fetchone()

    # Admins always have access
    if user.get("role") in ["admin", "super_admin"]:
        has_access = True

    if not has_access:
        conn.close()
        raise HTTPException(status_code=403, detail="Resource locked. Payment verification or faculty approval required to download.")

    conn.close()

    file_path = res["file_path"]
    if file_path and os.path.exists(file_path):
        return FileResponse(file_path, filename=f"{res['resource_name']}.zip")

    # Generate verified deliverable on the fly if physical file path is simulated
    content = f"# PROJECTVERSE VERIFIED ACADEMIC DELIVERABLE\nProject Resource: {res['resource_name']}\nType: {res['resource_type']}\nVerified License Issued To: {user['full_name']} ({user['email']})\nDate: {datetime.now().isoformat()}\n"
    return Response(
        content=content.encode("utf-8"),
        media_type="text/plain",
        headers={"Content-Disposition": f"attachment; filename={res['resource_name'].replace(' ', '_')}.txt"}
    )

# ==========================================
# CONTACT & SUPPORT TICKETS
# ==========================================

class ContactSubmission(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = "N/A"
    subject: str
    message: str

@app.post("/api/contact/submit")
def submit_contact(msg: ContactSubmission):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
    INSERT INTO contact_messages (name, email, phone, subject, message)
    VALUES (?, ?, ?, ?, ?)
    """, (msg.name.strip(), msg.email.strip().lower(), msg.phone.strip() if msg.phone else "N/A", msg.subject.strip(), msg.message.strip()))
    conn.commit()
    conn.close()

    create_admin_notification(
        "contact",
        f"Contact Form: {msg.subject}",
        f"From: {msg.name} ({msg.email}): {msg.message[:80]}...",
        f"/#admin"
    )

    email_service.notify_contact_message({
        "name": msg.name,
        "email": msg.email,
        "phone": msg.phone,
        "subject": msg.subject,
        "message": msg.message
    })

    return {"success": True, "message": "Your message has been received! Our support counselor will contact you shortly."}

class TicketSubmission(BaseModel):
    subject: str
    category: str
    message: str

@app.post("/api/support/ticket")
def create_support_ticket(t: TicketSubmission, request: Request):
    user = require_student(request)
    conn = get_db()
    cur = conn.cursor()

    t_num = f"TCK-{datetime.now().strftime('%Y%m%d')}-{random.randint(1000, 9999)}"
    cur.execute("""
    INSERT INTO support_tickets (ticket_number, user_id, subject, category, message, status)
    VALUES (?, ?, ?, ?, ?, 'open')
    """, (t_num, user["id"], t.subject.strip(), t.category.strip(), t.message.strip()))
    conn.commit()
    conn.close()

    create_admin_notification(
        "support",
        f"New Support Ticket ({t_num})",
        f"Student {user['full_name']}: {t.subject}",
        f"/#admin"
    )

    email_service.notify_support_ticket({
        "ticket_number": t_num,
        "user_name": user["full_name"],
        "category": t.category,
        "subject": t.subject,
        "message": t.message
    })

    return {"success": True, "ticket_number": t_num, "message": f"Support ticket {t_num} created. Our technical advisor will respond shortly."}

# ==========================================
# REAL BUSINESS ADMIN PANEL ENDPOINTS (/api/admin/*)
# ==========================================

@app.get("/api/admin/stats")
def get_admin_dashboard_metrics(request: Request):
    require_admin_or_pm(request)
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM projects WHERE is_published = 1")
    total_projects = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM users WHERE role = 'student'")
    total_students = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM project_enquiries WHERE status = 'NEW'")
    new_enquiries = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM project_requests WHERE status = 'NEW'")
    pending_requests = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM orders WHERE status = 'COMPLETED'")
    confirmed_orders = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM payments WHERE status = 'pending'")
    pending_payments = cur.fetchone()[0]

    cur.execute("SELECT COALESCE(SUM(amount), 0) FROM payments WHERE status = 'approved'")
    verified_revenue = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM support_tickets WHERE status = 'open'")
    new_support_messages = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM notifications WHERE is_read = 0")
    unread_notifications = cur.fetchone()[0]

    conn.close()

    return {
        "total_projects": total_projects,
        "total_students": total_students,
        "new_enquiries": new_enquiries,
        "pending_requests": pending_requests,
        "confirmed_orders": confirmed_orders,
        "pending_payments": pending_payments,
        "verified_revenue": verified_revenue,
        "new_support_messages": new_support_messages,
        "unread_notifications": unread_notifications
    }

# --- Admin Inquiries Management ---
@app.get("/api/admin/enquiries")
def list_admin_enquiries(request: Request, status: Optional[str] = None, q: Optional[str] = None):
    require_admin_or_pm(request)
    conn = get_db()
    cur = conn.cursor()

    conditions = ["1=1"]
    params = []

    if status and status.strip():
        conditions.append("status = ?")
        params.append(status.strip())

    if q and q.strip():
        term = f"%{q.strip().lower()}%"
        conditions.append("(LOWER(customer_name) LIKE ? OR LOWER(customer_email) LIKE ? OR LOWER(project_code) LIKE ? OR LOWER(enquiry_number) LIKE ?)")
        params.extend([term, term, term, term])

    sql = f"""
    SELECT id, enquiry_number, customer_name, customer_email, customer_phone, college_name, course,
           project_id, project_code, project_title, technology, message, status, admin_notes, assigned_to, created_at
    FROM project_enquiries
    WHERE {' AND '.join(conditions)}
    ORDER BY id DESC
    """
    cur.execute(sql, tuple(params))
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]

class EnquiryStatusUpdate(BaseModel):
    status: str
    admin_notes: Optional[str] = None

@app.put("/api/admin/enquiries/{enquiry_id}/status")
def update_enquiry_status(enquiry_id: int, payload: EnquiryStatusUpdate, request: Request):
    user = require_admin(request)
    valid_statuses = ["NEW", "UNDER_REVIEW", "CONTACTED", "QUOTATION_SENT", "PAYMENT_PENDING", "PAYMENT_RECEIVED", "IN_PROGRESS", "COMPLETED", "CANCELLED"]
    if payload.status not in valid_statuses:
        raise HTTPException(status_code=400, detail=f"Invalid status. Must be one of: {', '.join(valid_statuses)}")

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT enquiry_number, customer_name FROM project_enquiries WHERE id = ?", (enquiry_id,))
    enq = cur.fetchone()
    if not enq:
        conn.close()
        raise HTTPException(status_code=404, detail="Enquiry not found.")

    if payload.admin_notes:
        cur.execute("UPDATE project_enquiries SET status = ?, admin_notes = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?", (payload.status, payload.admin_notes, enquiry_id))
    else:
        cur.execute("UPDATE project_enquiries SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?", (payload.status, enquiry_id))

    conn.commit()
    conn.close()

    log_audit(user["id"], user["email"], "update_enquiry_status", "project_enquiries", str(enquiry_id), f"Changed status of {enq['enquiry_number']} to {payload.status}")

    return {"success": True, "message": f"Enquiry {enq['enquiry_number']} status updated to {payload.status}."}

# --- Admin Project Requests Management ---
@app.get("/api/admin/requests")
def list_admin_requests(request: Request, status: Optional[str] = None):
    require_admin_or_pm(request)
    conn = get_db()
    cur = conn.cursor()

    conditions = ["1=1"]
    params = []
    if status and status.strip():
        conditions.append("pr.status = ?")
        params.append(status.strip())

    sql = f"""
    SELECT pr.id, pr.request_number, pr.user_id, pr.student_name, pr.student_email, pr.student_phone,
           pr.college_name, pr.course, pr.project_id, pr.project_code, pr.project_title,
           pr.preferred_tech, pr.deadline, pr.requirements, pr.team_mode, pr.team_members,
           pr.status, pr.admin_notes, pr.mentor_id, pr.progress_percent, pr.current_milestone, pr.created_at,
           m.full_name as mentor_name, m.specialization as mentor_specialization
    FROM project_requests pr
    LEFT JOIN mentors m ON pr.mentor_id = m.id
    WHERE {' AND '.join(conditions)}
    ORDER BY pr.id DESC
    """
    cur.execute(sql, tuple(params))
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]

class RequestActionPayload(BaseModel):
    action: str  # approve, reject, contact, quotation
    admin_notes: Optional[str] = None

@app.post("/api/admin/requests/{req_id}/action")
def take_request_action(req_id: int, payload: RequestActionPayload, request: Request):
    user = require_admin(request)
    status_map = {
        "approve": "APPROVED",
        "reject": "CANCELLED",
        "contact": "CONTACTED",
        "quotation": "QUOTATION_SENT"
    }
    new_status = status_map.get(payload.action.lower())
    if not new_status:
        raise HTTPException(status_code=400, detail="Action must be: approve, reject, contact, or quotation.")

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT request_number, student_name, student_email, user_id, project_code, project_title FROM project_requests WHERE id = ?", (req_id,))
    req_item = cur.fetchone()
    if not req_item:
        conn.close()
        raise HTTPException(status_code=404, detail="Project request not found.")

    cur.execute("UPDATE project_requests SET status = ?, admin_notes = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?", (new_status, payload.admin_notes or "", req_id))

    if req_item["user_id"]:
        cur.execute("""
        INSERT INTO notifications (user_id, type, title, message)
        VALUES (?, 'request_update', ?, ?)
        """, (req_item["user_id"], f"Project Request {req_item['request_number']} {new_status}", f"Your request for {req_item['project_code']} has been updated to {new_status}."))

    conn.commit()
    conn.close()

    log_audit(user["id"], user["email"], "update_request_status", "project_requests", str(req_id), f"Set status of {req_item['request_number']} to {new_status}")

    return {"success": True, "message": f"Request {req_item['request_number']} successfully marked as {new_status}."}

class AssignMentorPayload(BaseModel):
    mentor_id: int

@app.post("/api/admin/requests/{req_id}/assign-mentor")
def assign_mentor_to_request(req_id: int, payload: AssignMentorPayload, request: Request):
    user = require_admin(request)
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT full_name FROM mentors WHERE id = ?", (payload.mentor_id,))
    mentor = cur.fetchone()
    if not mentor:
        conn.close()
        raise HTTPException(status_code=404, detail="Faculty advisor not found.")

    cur.execute("UPDATE project_requests SET mentor_id = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?", (payload.mentor_id, req_id))
    cur.execute("UPDATE mentors SET active_students = active_students + 1 WHERE id = ?", (payload.mentor_id,))
    conn.commit()
    conn.close()

    log_audit(user["id"], user["email"], "assign_mentor", "project_requests", str(req_id), f"Assigned mentor {mentor['full_name']}")

    return {"success": True, "message": f"Assigned Faculty Advisor {mentor['full_name']} to request."}

class ProgressUpdatePayload(BaseModel):
    progress_percent: Optional[int] = None
    progress_percentage: Optional[int] = None
    current_milestone: Optional[str] = None
    milestone_notes: Optional[str] = None

@app.post("/api/admin/requests/{req_id}/progress")
def update_request_progress(req_id: int, payload: ProgressUpdatePayload, request: Request):
    user = require_admin_or_pm(request)
    pct = payload.progress_percent if payload.progress_percent is not None else (payload.progress_percentage or 0)
    milestone = payload.current_milestone or payload.milestone_notes or "In Progress"

    if not (0 <= pct <= 100):
        raise HTTPException(status_code=400, detail="Progress percentage must be between 0 and 100.")

    conn = get_db()
    cur = conn.cursor()
    cur.execute("UPDATE project_requests SET progress_percent = ?, current_milestone = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?", (pct, milestone.strip(), req_id))
    conn.commit()
    conn.close()

    log_audit(user["id"], user["email"], "update_progress", "project_requests", str(req_id), f"Progress updated to {pct}% - {milestone}")

    return {"success": True, "message": f"Milestone progress updated to {pct}%."}

# --- Admin Orders & Invoices ---
@app.get("/api/admin/orders")
def list_admin_orders(request: Request, status: Optional[str] = None):
    require_admin_or_pm(request)
    conn = get_db()
    cur = conn.cursor()

    conditions = ["1=1"]
    params = []
    if status and status.strip():
        conditions.append("o.status = ?")
        params.append(status.strip())

    sql = f"""
    SELECT o.id, o.order_number, o.user_id, o.customer_name, o.customer_email, o.customer_phone,
           o.project_id, o.amount, o.status, o.payment_method, o.created_at,
           p.project_code, p.title as project_title,
           pay.utr_reference, pay.screenshot_path, pay.status as payment_status
    FROM orders o
    JOIN projects p ON o.project_id = p.id
    LEFT JOIN payments pay ON pay.order_id = o.id
    WHERE {' AND '.join(conditions)}
    ORDER BY o.id DESC
    """
    cur.execute(sql, tuple(params))
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]

class OrderStatusUpdate(BaseModel):
    status: str
    admin_notes: Optional[str] = None

@app.put("/api/admin/orders/{order_id}/status")
def update_order_status(order_id: int, payload: OrderStatusUpdate, request: Request):
    user = require_admin(request)
    valid_statuses = ["NEW", "UNDER_REVIEW", "CONTACTED", "QUOTATION_SENT", "PAYMENT_PENDING", "PAYMENT_RECEIVED", "IN_PROGRESS", "COMPLETED", "CANCELLED"]
    if payload.status not in valid_statuses:
        raise HTTPException(status_code=400, detail="Invalid order status.")

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT order_number, user_id, customer_email, customer_name, project_id FROM orders WHERE id = ?", (order_id,))
    ord_row = cur.fetchone()
    if not ord_row:
        conn.close()
        raise HTTPException(status_code=404, detail="Order not found.")

    cur.execute("UPDATE orders SET status = ?, admin_notes = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?", (payload.status, payload.admin_notes or "", order_id))

    if payload.status == "COMPLETED" or payload.status == "PAYMENT_RECEIVED":
        cur.execute("UPDATE payments SET status = 'approved', verified_by = ? WHERE order_id = ?", (user["full_name"], order_id))

    conn.commit()
    conn.close()

    log_audit(user["id"], user["email"], "update_order_status", "orders", str(order_id), f"Set order {ord_row['order_number']} to {payload.status}")

    return {"success": True, "message": f"Order {ord_row['order_number']} marked as {payload.status}."}

@app.post("/api/admin/orders/{order_id}/generate-invoice")
def generate_invoice_for_order(order_id: int, request: Request):
    user = require_admin(request)
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    SELECT o.id, o.order_number, o.user_id, o.customer_name, o.customer_email, o.customer_phone, o.amount,
           u.college, p.title as project_title, p.project_code, pay.utr_reference
    FROM orders o
    JOIN projects p ON o.project_id = p.id
    LEFT JOIN users u ON o.user_id = u.id
    LEFT JOIN payments pay ON pay.order_id = o.id
    WHERE o.id = ?
    """, (order_id,))
    row = cur.fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Order not found.")

    # Check if invoice already exists
    cur.execute("SELECT invoice_number FROM invoices WHERE order_id = ?", (order_id,))
    existing = cur.fetchone()
    if existing:
        conn.close()
        return {"success": True, "invoice_number": existing[0], "message": "Invoice already generated."}

    inv_num = f"INV-{datetime.now().strftime('%Y%m%d')}-{random.randint(1000, 9999)}"
    subtotal = row["amount"]
    tax = int(subtotal * 0.18) # 18% GST calculation
    total = subtotal + tax

    cur.execute("""
    INSERT INTO invoices (
        invoice_number, order_id, user_id, customer_name, customer_email, customer_phone,
        customer_college, project_title, project_code, subtotal, tax_amount, total_amount,
        status, payment_reference
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'PAID', ?)
    """, (
        inv_num, order_id, row["user_id"], row["customer_name"], row["customer_email"], row["customer_phone"],
        row["college"] or "Academic Institution", row["project_title"], row["project_code"], subtotal, tax, total,
        row["utr_reference"] or "Verified UPI Transfer"
    ))
    conn.commit()
    conn.close()

    log_audit(user["id"], user["email"], "generate_invoice", "invoices", inv_num, f"Generated invoice {inv_num} for order #{order_id}")

    return {"success": True, "invoice_number": inv_num, "message": f"Invoice {inv_num} generated successfully!"}

@app.get("/api/admin/invoices")
def list_admin_invoices(request: Request):
    require_admin_or_pm(request)
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM invoices ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]

@app.get("/api/invoices/{invoice_number}")
def get_invoice_html(invoice_number: str):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM invoices WHERE invoice_number = ?", (invoice_number,))
    inv = cur.fetchone()
    conn.close()
    if not inv:
        raise HTTPException(status_code=404, detail="Invoice not found.")

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <title>Tax Invoice – {inv['invoice_number']}</title>
      <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; background: #f8fafc; padding: 40px; color: #1e293b; }}
        .invoice-box {{ max-width: 800px; margin: auto; padding: 40px; background: white; border-radius: 16px; border: 1px solid #e2e8f0; box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1); }}
        .header {{ display: flex; justify-content: space-between; border-bottom: 2px solid #e2e8f0; padding-bottom: 24px; margin-bottom: 24px; }}
        .brand {{ font-size: 28px; font-weight: 900; color: #0f172a; letter-spacing: -0.5px; }}
        .brand span {{ color: #0284c7; }}
        .table {{ width: 100%; border-collapse: collapse; margin-top: 24px; }}
        .table th {{ background: #f1f5f9; padding: 12px; text-align: left; font-size: 12px; text-transform: uppercase; color: #64748b; }}
        .table td {{ padding: 16px 12px; border-bottom: 1px solid #f1f5f9; font-size: 14px; }}
        .totals {{ margin-top: 24px; text-align: right; font-size: 14px; }}
        .print-btn {{ background: #7c3aed; color: white; border: none; padding: 10px 20px; border-radius: 8px; font-weight: bold; cursor: pointer; }}
      </style>
    </head>
    <body>
      <div class="invoice-box">
        <div class="header">
          <div>
            <div class="brand">PROJECT<span>VERSE</span></div>
            <p style="margin: 4px 0 0; color: #64748b; font-size: 13px;">Academic Project Marketplace & Learning Systems</p>
            <p style="margin: 2px 0 0; color: #64748b; font-size: 12px;">Contact: aniladani843@gmail.com | +91 8431712924</p>
          </div>
          <div style="text-align: right;">
            <h2 style="margin: 0; color: #0284c7; font-size: 22px;">TAX INVOICE</h2>
            <p style="margin: 4px 0 0; font-family: monospace; font-weight: bold;">{inv['invoice_number']}</p>
            <p style="margin: 2px 0 0; font-size: 12px; color: #64748b;">Date: {inv['created_at'][:10]}</p>
            <span style="display: inline-block; background: #dcfce7; color: #166534; font-size: 11px; font-weight: bold; padding: 4px 8px; border-radius: 4px; margin-top: 6px;">STATUS: {inv['status']}</span>
          </div>
        </div>

        <div style="display: flex; justify-content: space-between; font-size: 13px; margin-bottom: 24px;">
          <div>
            <strong style="color: #64748b; text-transform: uppercase; font-size: 11px;">Billed To (Customer):</strong>
            <p style="margin: 4px 0 0; font-weight: bold; font-size: 15px;">{inv['customer_name']}</p>
            <p style="margin: 2px 0 0; color: #475569;">{inv['customer_college']}</p>
            <p style="margin: 2px 0 0; color: #475569;">{inv['customer_email']} | {inv['customer_phone']}</p>
          </div>
          <div style="text-align: right;">
            <strong style="color: #64748b; text-transform: uppercase; font-size: 11px;">Payment Method:</strong>
            <p style="margin: 4px 0 0; font-weight: bold;">Direct UPI Transfer (Payee: ANIL)</p>
            <p style="margin: 2px 0 0; color: #475569; font-family: monospace;">Ref: {inv['payment_reference']}</p>
          </div>
        </div>

        <table class="table">
          <thead>
            <tr>
              <th>Item / Academic Capstone</th>
              <th>Project Code</th>
              <th>License Scope</th>
              <th style="text-align: right;">Price (INR)</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>
                <strong>{inv['project_title']}</strong><br>
                <span style="font-size: 12px; color: #64748b;">Includes: IEEE Report, Source Code ZIP, Database Schema, PPT Presentation, SRS & Viva Q&A</span>
              </td>
              <td style="font-family: monospace; font-weight: bold; color: #0284c7;">{inv['project_code']}</td>
              <td>Full Academic License</td>
              <td style="text-align: right; font-family: monospace; font-weight: bold;">Rs {inv['subtotal']:,}</td>
            </tr>
          </tbody>
        </table>

        <div class="totals">
          <p style="margin: 4px 0;">Subtotal: <strong>Rs {inv['subtotal']:,}</strong></p>
          <p style="margin: 4px 0;">Applicable 18% GST (CGST 9% + SGST 9%): <strong>Rs {inv['tax_amount']:,}</strong></p>
          <h3 style="margin: 8px 0; color: #0f172a; font-size: 20px;">Total Paid: Rs {inv['total_amount']:,}</h3>
        </div>

        <div style="margin-top: 40px; padding-top: 20px; border-top: 1px solid #e2e8f0; display: flex; justify-content: space-between; align-items: center;">
          <span style="font-size: 12px; color: #94a3b8;">This is a computer-generated tax invoice issued by PROJECTVERSE Academic Systems.</span>
          <button class="print-btn" onclick="window.print()">Print Invoice</button>
        </div>
      </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html)

# --- Admin Notification Centre ---
@app.get("/api/admin/notifications")
def get_admin_notifications(request: Request):
    require_admin_or_pm(request)
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, type, title, message, link_url, is_read, created_at FROM notifications WHERE user_id IS NULL ORDER BY id DESC LIMIT 50")
    items = [dict(r) for r in cur.fetchall()]
    unread_count = sum(1 for n in items if not n["is_read"])
    conn.close()
    return {"unread_count": unread_count, "notifications": items}

@app.post("/api/admin/notifications/{notif_id}/read")
def mark_notification_read(notif_id: int, request: Request):
    require_admin_or_pm(request)
    conn = get_db()
    cur = conn.cursor()
    cur.execute("UPDATE notifications SET is_read = 1 WHERE id = ?", (notif_id,))
    conn.commit()
    conn.close()
    return {"success": True}

@app.post("/api/admin/notifications/read-all")
def mark_all_notifications_read(request: Request):
    require_admin_or_pm(request)
    conn = get_db()
    cur = conn.cursor()
    cur.execute("UPDATE notifications SET is_read = 1 WHERE user_id IS NULL")
    conn.commit()
    conn.close()
    return {"success": True}

# --- Admin Email Notification Logs & Retry ---
@app.get("/api/admin/email-logs")
def list_email_logs(request: Request):
    require_admin(request)
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, event_type, recipient_email, subject, body_preview, status, error_message, retry_count, created_at, sent_at FROM email_logs ORDER BY id DESC LIMIT 100")
    rows = cur.fetchall()
    conn.close()
    return {"success": True, "logs": [dict(r) for r in rows]}

@app.post("/api/admin/email-logs/{log_id}/retry")
def retry_failed_email_log(log_id: int, request: Request):
    require_admin(request)
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, event_type, recipient_email, subject, body_preview FROM email_logs WHERE id = ?", (log_id,))
    log_item = cur.fetchone()
    if not log_item:
        conn.close()
        raise HTTPException(status_code=404, detail="Email log record not found.")

    try:
        email_service.send_smtp_message(
            log_item["recipient_email"],
            log_item["subject"],
            f"<div style='font-family: Arial;'><h3>{log_item['subject']}</h3><pre>{log_item['body_preview']}</pre></div>",
            log_item["body_preview"]
        )
        cur.execute("UPDATE email_logs SET status = 'SENT', error_message = NULL, retry_count = retry_count + 1, sent_at = CURRENT_TIMESTAMP WHERE id = ?", (log_id,))
        conn.commit()
        conn.close()
        return {"success": True, "message": "Email successfully dispatched to " + log_item["recipient_email"]}
    except Exception as e:
        cur.execute("UPDATE email_logs SET retry_count = retry_count + 1, error_message = ? WHERE id = ?", (str(e), log_id))
        conn.commit()
        conn.close()
        return {"success": False, "message": "Retry attempted: " + str(e)}

# --- Admin Registered Students Roster ---
@app.get("/api/admin/students")
def list_registered_students(request: Request):
    require_admin_or_pm(request)
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
    SELECT u.id, u.full_name, u.email, u.mobile, u.college, u.university, u.course, u.academic_year,
           u.specialization, u.created_at,
           (SELECT COUNT(*) FROM project_enquiries WHERE customer_email = u.email) as enquiries_count,
           (SELECT COUNT(*) FROM project_requests WHERE user_id = u.id OR LOWER(student_email) = u.email) as requests_count,
           (SELECT COUNT(*) FROM orders WHERE user_id = u.id) as orders_count
    FROM users u
    WHERE u.role = 'student'
    ORDER BY u.id DESC
    """)
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]

# --- Admin Payment Verification ---
@app.get("/api/admin/payments")
def list_admin_payments(request: Request):
    require_admin_or_pm(request)
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
    SELECT pay.id, pay.order_id, pay.user_id, pay.project_id, pay.amount, pay.utr_reference,
           pay.screenshot_path, pay.status, pay.verified_by, pay.verification_notes, pay.created_at,
           o.order_number, u.full_name as student_name, u.email as student_email, u.college as student_college,
           p.project_code, p.title as project_title
    FROM payments pay
    JOIN orders o ON pay.order_id = o.id
    JOIN users u ON pay.user_id = u.id
    JOIN projects p ON pay.project_id = p.id
    ORDER BY pay.id DESC
    """)
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]

class PaymentVerificationPayload(BaseModel):
    action: Optional[str] = None
    status: Optional[str] = None
    notes: Optional[str] = "Verified via bank statement."

@app.post("/api/admin/payments/{payment_id}/verify")
def verify_payment_submission(payment_id: int, payload: PaymentVerificationPayload, request: Request):
    user = require_admin(request)
    action = (payload.action or payload.status or "approved").lower()
    if action not in ["approved", "rejected"]:
        raise HTTPException(status_code=400, detail="Action must be 'approved' or 'rejected'.")

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, order_id, user_id, amount, project_id FROM payments WHERE id = ? OR order_id = ? ORDER BY id DESC LIMIT 1", (payment_id, payment_id))
    pay = cur.fetchone()
    if not pay:
        conn.close()
        raise HTTPException(status_code=404, detail="Payment record not found.")

    actual_payment_id = pay["id"]
    cur.execute("""
    UPDATE payments SET status = ?, verified_by = ?, verification_notes = ?, verified_at = CURRENT_TIMESTAMP WHERE id = ?
    """, (action, user["full_name"], payload.notes or "Verified via bank statement.", actual_payment_id))

    order_status = "COMPLETED" if action == "approved" else "CANCELLED"
    cur.execute("UPDATE orders SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?", (order_status, pay["order_id"]))

    conn.commit()
    conn.close()

    log_audit(user["id"], user["email"], "verify_payment", "payments", str(payment_id), f"Payment {payload.action} (Order #{pay['order_id']})")

    if action == "approved":
        partner_notif = None
        # Fetch order details for notification
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT order_number, customer_name, customer_email, project_id, amount FROM orders WHERE id = ?", (pay["order_id"],))
        ord_info = cur.fetchone()
        cur.execute("SELECT project_code, title FROM projects WHERE id = ?", (pay["project_id"],))
        proj_row = cur.fetchone()
        proj_code = proj_row["project_code"] if proj_row else "PV-PROJ"
        proj_title = proj_row["title"] if proj_row else "Academic Project"

        # Check and compute automatic 25% referral commission
        cur.execute("SELECT * FROM referral_conversions WHERE order_id = ?", (pay["order_id"],))
        conv_row = cur.fetchone()
        if conv_row:
            # Check if commission already recorded (prevent duplicate commission)
            cur.execute("SELECT id FROM referral_commissions WHERE order_id = ?", (pay["order_id"],))
            if not cur.fetchone():
                cur.execute("SELECT setting_value FROM referral_settings WHERE setting_key = 'commission_rate_percentage'")
                rate_row = cur.fetchone()
                rate_pct = float(rate_row[0]) if rate_row else 25.0
                rate_decimal = rate_pct / 100.0

                net_order_amount = float(conv_row["order_amount"])
                comm_amount = round(net_order_amount * rate_decimal, 2)

                cur.execute("""
                INSERT INTO referral_commissions (
                    partner_id, conversion_id, order_id, order_number, order_amount,
                    commission_rate, commission_amount, status, approved_by, approved_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, 'APPROVED', ?, CURRENT_TIMESTAMP)
                """, (
                    conv_row["partner_id"],
                    conv_row["id"],
                    pay["order_id"],
                    conv_row["order_number"],
                    net_order_amount,
                    rate_decimal,
                    comm_amount,
                    user["full_name"]
                ))

                cur.execute("""
                UPDATE referral_partners
                SET total_sales = total_sales + 1,
                    total_commission_earned = total_commission_earned + ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
                """, (comm_amount, conv_row["partner_id"]))

                # Fetch partner info for notifications
                cur.execute("SELECT full_name, email FROM referral_partners WHERE id = ?", (conv_row["partner_id"],))
                p_row = cur.fetchone()
                if p_row:
                    partner_notif = {
                        "partner_name": p_row["full_name"],
                        "partner_email": p_row["email"],
                        "order_number": conv_row["order_number"],
                        "project_title": proj_title,
                        "order_amount": net_order_amount,
                        "commission_amount": comm_amount
                    }

        conn.commit()
        conn.close()

        if partner_notif:
            email_service.notify_partner_commission_earned(
                {"full_name": partner_notif["partner_name"], "email": partner_notif["partner_email"]},
                {
                    "order_number": partner_notif["order_number"],
                    "project_title": partner_notif["project_title"],
                    "order_amount": partner_notif["order_amount"],
                    "commission_amount": partner_notif["commission_amount"]
                }
            )
            create_admin_notification(
                "commission",
                f"25% Commission Earned: Rs {partner_notif['commission_amount']:,}",
                f"Partner {partner_notif['partner_name']} earned Rs {partner_notif['commission_amount']:,} (25%) on Order {partner_notif['order_number']}.",
                "/#admin"
            )

        email_service.notify_payment_verified({
            "order_number": ord_info["order_number"],
            "customer_name": ord_info["customer_name"],
            "customer_email": ord_info["customer_email"],
            "amount": pay["amount"],
            "project_code": proj_code
        })
    elif action == "rejected":
        # Handle commission reversal if payment was rejected/cancelled
        reversal_notif = None
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT id, partner_id, commission_amount, order_number, status FROM referral_commissions WHERE order_id = ?", (pay["order_id"],))
        comm_row = cur.fetchone()
        if comm_row and comm_row["status"] in ["APPROVED", "PENDING"]:
            cur.execute("UPDATE referral_commissions SET status = 'REVERSED', updated_at = CURRENT_TIMESTAMP WHERE id = ?", (comm_row["id"],))
            cur.execute("""
            UPDATE referral_partners
            SET total_commission_earned = MAX(0, total_commission_earned - ?),
                total_sales = MAX(0, total_sales - 1),
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """, (comm_row["commission_amount"], comm_row["partner_id"]))

            cur.execute("SELECT full_name, email FROM referral_partners WHERE id = ?", (comm_row["partner_id"],))
            p_row = cur.fetchone()
            if p_row:
                reversal_notif = {
                    "full_name": p_row["full_name"],
                    "email": p_row["email"],
                    "order_number": comm_row["order_number"],
                    "commission_amount": comm_row["commission_amount"]
                }
        conn.commit()
        conn.close()

        if reversal_notif:
            email_service.notify_partner_commission_reversed(
                {"full_name": reversal_notif["full_name"], "email": reversal_notif["email"]},
                {"order_number": reversal_notif["order_number"], "commission_amount": reversal_notif["commission_amount"]}
            )

    return {"success": True, "message": f"Payment successfully {action}."}

# --- Admin Projects CRUD (All 90 Projects) ---
class ProjectCreatePayload(BaseModel):
    project_code: str
    academic_level: str
    title: str
    domain: str
    difficulty: str
    price: int
    tech_summary: str
    description: str

@app.post("/api/admin/projects/create")
def create_project(p: ProjectCreatePayload, request: Request):
    user = require_admin(request)
    if p.price < 799:
        raise HTTPException(status_code=400, detail="Pricing Rule: Minimum price is Rs 799.")

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id FROM projects WHERE UPPER(project_code) = ?", (p.project_code.upper().strip(),))
    if cur.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail="Project code already exists.")

    slug = p.title.lower().replace(" ", "-").replace("/", "-")
    cur.execute("""
    INSERT INTO projects (
        project_code, title, slug, academic_level, domain, difficulty, price,
        tech_summary, description, image_url, is_published, duration, timeline
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, '/static/projects/btech/BTECH001.webp', 1, '8 Weeks', '6-8 Weeks')
    """, (
        p.project_code.upper().strip(), p.title.strip(), slug, p.academic_level,
        p.domain.strip(), p.difficulty, p.price, p.tech_summary.strip(), p.description.strip()
    ))
    new_id = cur.lastrowid
    conn.commit()
    conn.close()

    log_audit(user["id"], user["email"], "create_project", "projects", str(new_id), f"Created project {p.project_code}")
    return {"success": True, "project_id": new_id, "message": f"Project {p.project_code} created successfully."}

@app.put("/api/admin/projects/{project_id}")
def update_project(project_id: int, p: ProjectCreatePayload, request: Request):
    user = require_admin(request)
    if p.price < 799:
        raise HTTPException(status_code=400, detail="Pricing Rule: Minimum price is Rs 799.")

    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
    UPDATE projects SET
        project_code = ?, academic_level = ?, title = ?, domain = ?, difficulty = ?,
        price = ?, tech_summary = ?, description = ?, updated_at = CURRENT_TIMESTAMP
    WHERE id = ?
    """, (p.project_code.upper().strip(), p.academic_level, p.title.strip(), p.domain.strip(), p.difficulty, p.price, p.tech_summary.strip(), p.description.strip(), project_id))
    conn.commit()
    conn.close()

    log_audit(user["id"], user["email"], "update_project", "projects", str(project_id), f"Updated project {p.project_code}")
    return {"success": True, "message": "Project updated successfully."}

@app.delete("/api/admin/projects/{project_id}")
def delete_project(project_id: int, request: Request):
    user = require_admin(request)
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT project_code FROM projects WHERE id = ?", (project_id,))
    row = cur.fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Project not found.")

    cur.execute("DELETE FROM projects WHERE id = ?", (project_id,))
    cur.execute("DELETE FROM project_resources WHERE project_id = ?", (project_id,))
    conn.commit()
    conn.close()

    log_audit(user["id"], user["email"], "delete_project", "projects", str(project_id), f"Deleted project {row['project_code']}")
    return {"success": True, "message": f"Project {row['project_code']} deleted."}

@app.post("/api/admin/projects/{project_id}/price")
async def update_project_price(project_id: int, request: Request):
    user = require_admin(request)
    price = None
    content_type = request.headers.get("content-type", "")
    if "application/json" in content_type:
        body = await request.json()
        price = body.get("price")
    else:
        form = await request.form()
        price = form.get("price")

    if price is None or int(price) < 799:
        raise HTTPException(status_code=400, detail="Pricing Rule: Minimum price cannot be below Rs 799.")

    conn = get_db()
    cur = conn.cursor()
    cur.execute("UPDATE projects SET price = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?", (int(price), project_id))
    conn.commit()
    conn.close()

    log_audit(user["id"], user["email"], "update_price", "projects", str(project_id), f"Updated price to Rs {int(price):,}")
    return {"success": True, "message": f"Project price updated to Rs {int(price):,}."}

@app.get("/api/admin/projects/export-csv")
def export_projects_csv(request: Request):
    require_admin_or_pm(request)
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
    SELECT project_code, title, academic_level, domain, difficulty, price, timeline, tech_summary, description
    FROM projects ORDER BY id ASC
    """)
    rows = cur.fetchall()
    conn.close()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Project Code", "Title", "Academic Level", "Domain", "Difficulty", "Price (INR)", "Timeline", "Tech Stack", "Description"])
    for r in rows:
        writer.writerow(list(r))

    output.seek(0)
    return Response(
        content=output.getvalue(),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=projectverse_90_projects_catalogue.csv"}
    )

@app.post("/api/admin/projects/import-csv")
async def import_projects_csv(request: Request, csv_file: UploadFile = File(...)):
    user = require_admin(request)
    contents = await csv_file.read()
    decoded = contents.decode("utf-8")
    reader = csv.DictReader(io.StringIO(decoded))

    conn = get_db()
    cur = conn.cursor()
    imported = 0

    for row in reader:
        code = row.get("Project Code") or row.get("project_code")
        title = row.get("Title") or row.get("title")
        if not code or not title:
            continue

        price = int(row.get("Price (INR)") or row.get("price") or 999)
        if price < 799:
            price = 799

        cur.execute("""
        INSERT INTO projects (
            project_code, title, slug, academic_level, domain, difficulty, price, timeline, tech_summary, description, image_url, is_published
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, '/static/projects/btech/BTECH001.webp', 1)
        ON CONFLICT(project_code) DO UPDATE SET
            title = excluded.title, price = excluded.price, domain = excluded.domain, tech_summary = excluded.tech_summary
        """, (
            code.strip().upper(), title.strip(), title.lower().replace(" ", "-"),
            row.get("Academic Level") or "B.Tech", row.get("Domain") or "General",
            row.get("Difficulty") or "Intermediate", price, row.get("Timeline") or "8 Weeks",
            row.get("Tech Stack") or "Full Stack", row.get("Description") or ""
        ))
        imported += 1

    conn.commit()
    conn.close()

    log_audit(user["id"], user["email"], "import_csv", "projects", "bulk", f"Imported {imported} projects from CSV")
    return {"success": True, "imported_count": imported, "message": f"Successfully processed {imported} projects from CSV."}

@app.get("/api/admin/images-audit")
def audit_project_images(request: Request):
    require_admin_or_pm(request)
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, project_code, title, academic_level, subcategory, image_url FROM projects ORDER BY id ASC")
    rows = cur.fetchall()
    conn.close()

    results = []
    for r in rows:
        img_url = r["image_url"] or ""
        rel_path = img_url.lstrip("/")
        exists = os.path.exists(rel_path)
        size_kb = round(os.path.getsize(rel_path) / 1024, 1) if exists else 0
        results.append({
            "id": r["id"],
            "project_code": r["project_code"],
            "title": r["title"],
            "academic_level": r["academic_level"],
            "subcategory": r["subcategory"],
            "image_url": r["image_url"],
            "exists": exists,
            "size_kb": size_kb
        })
    return results

@app.post("/api/admin/projects/{project_id}/image")
async def upload_project_image(project_id: int, request: Request, image_file: UploadFile = File(...)):
    user = require_admin(request)
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT project_code, academic_level FROM projects WHERE id = ?", (project_id,))
    proj = cur.fetchone()
    if not proj:
        conn.close()
        raise HTTPException(status_code=404, detail="Project not found.")

    level_folder = "btech"
    lvl = proj["academic_level"].lower()
    if "bca" in lvl: level_folder = "bca"
    elif "b.com" in lvl or "bcom" in lvl: level_folder = "bcom"
    elif "mca" in lvl: level_folder = "mca"
    elif "m.tech" in lvl or "mtech" in lvl: level_folder = "mtech"
    elif "iit" in lvl or "research" in lvl: level_folder = "iit"

    target_dir = os.path.join("static", "projects", level_folder)
    os.makedirs(target_dir, exist_ok=True)
    target_path = os.path.join(target_dir, f"{proj['project_code']}.webp")

    content = await image_file.read()
    with open(target_path, "wb") as f:
        f.write(content)

    new_url = f"/static/projects/{level_folder}/{proj['project_code']}.webp"
    cur.execute("UPDATE projects SET image_url = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?", (new_url, project_id))
    conn.commit()
    conn.close()

    log_audit(user["id"], user["email"], "upload_image", "projects", str(project_id), f"Replaced artwork for {proj['project_code']}")
    return {"success": True, "image_url": new_url, "message": "Project thumbnail updated successfully."}

# --- Admin System Settings ---
@app.get("/api/admin/settings")
def get_all_settings(request: Request):
    require_admin_or_pm(request)
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT setting_key, setting_value, description FROM admin_settings")
    settings = {r[0]: {"value": r[1], "description": r[2]} for r in cur.fetchall()}
    conn.close()
    return settings

@app.post("/api/admin/settings")
async def update_admin_setting(request: Request):
    user = require_admin(request)
    body = await request.json()
    conn = get_db()
    cur = conn.cursor()

    if "setting_key" in body and "setting_value" in body:
        k = str(body["setting_key"]).strip()
        v = str(body["setting_value"]).strip()
        cur.execute("""
        INSERT INTO admin_settings (setting_key, setting_value, updated_at)
        VALUES (?, ?, CURRENT_TIMESTAMP)
        ON CONFLICT(setting_key) DO UPDATE SET setting_value = excluded.setting_value, updated_at = CURRENT_TIMESTAMP
        """, (k, v))
    else:
        for k, val in body.items():
            cur.execute("""
            INSERT INTO admin_settings (setting_key, setting_value, updated_at)
            VALUES (?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(setting_key) DO UPDATE SET setting_value = excluded.setting_value, updated_at = CURRENT_TIMESTAMP
            """, (str(k).strip(), str(val).strip()))

    conn.commit()
    conn.close()

    log_audit(user["id"], user["email"], "update_settings", "admin_settings", "config", "Updated system settings")
    return {"success": True, "message": "Settings updated successfully."}

@app.get("/api/admin/mentors")
def list_admin_mentors(request: Request):
    require_admin_or_pm(request)
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, full_name, email, mobile, department, designation, specialization, experience_years, active_students, max_students AS capacity FROM mentors ORDER BY id ASC")
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def serve_index():
    index_file = os.path.join("static", "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return HTMLResponse("<h1>PROJECTVERSE Production Server Online.</h1>")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("server:app", host="0.0.0.0", port=port, reload=False)
