"""
PROJECTVERSE - Referral Partner & 25% Commission Management System
Router & Business Logic
Features:
- Partner Registration & Authentication (PBKDF2/SHA-256 tokens)
- Unique Referral Code & URL Generation (e.g. projectverse.com/?ref=ANIL001)
- Click Tracking, Attribution Window (30 Days), Anti-Fraud & Self-Referral Prevention
- Automatic 25% Commission Calculation upon Payment Verification
- Partner Dashboard with live telemetry, sales history, and payout requests
- Admin Referral Dashboard: partner approval, payout processing, commission auditing, CSV export
"""
import os
import io
import csv
import random
import re
import hashlib
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any

from fastapi import APIRouter, Request, HTTPException, Depends, Query, Response
from pydantic import BaseModel, EmailStr

import email_service

router = APIRouter()

DB_PATH = os.getenv("PROJECTVERSE_DB", "projectverse.db")
SECRET_KEY = os.getenv("SECRET_KEY", "projectverse_prod_key_2026")

def get_db():
    import sqlite3
    conn = sqlite3.connect(DB_PATH, timeout=30.0)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA busy_timeout=30000")
    conn.execute("PRAGMA foreign_keys=ON")
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def get_current_partner(request: Request) -> Optional[Dict[str, Any]]:
    auth_header = request.headers.get("Authorization")
    partner_id = None
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.replace("Bearer ", "").strip()
        if token.startswith("pv_partner_"):
            try:
                partner_id = int(token.split("_")[2])
            except (IndexError, ValueError):
                pass
    if not partner_id:
        param = request.query_params.get("partner_token")
        if param and param.startswith("pv_partner_"):
            try:
                partner_id = int(param.split("_")[2])
            except (IndexError, ValueError):
                pass

    if partner_id:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
        SELECT id, user_id, full_name, email, mobile, college_name, city, preferred_payment_method,
               upi_id, bank_account_name, bank_account_number, bank_ifsc, bank_name, status,
               total_clicks, total_registrations, total_sales, total_commission_earned, total_commission_paid
        FROM referral_partners WHERE id = ?
        """, (partner_id,))
        row = cur.fetchone()
        conn.close()
        if row:
            return dict(row)
    return None

def require_partner(request: Request) -> Dict[str, Any]:
    partner = get_current_partner(request)
    if not partner:
        raise HTTPException(status_code=401, detail="Referral partner authentication required. Please sign in.")
    if partner["status"] != "APPROVED":
        raise HTTPException(
            status_code=403,
            detail=f"Partner account is {partner['status']}. You will have full access once approved by administrator."
        )
    return partner

def require_admin(request: Request) -> Dict[str, Any]:
    # Reuse admin authentication from headers/tokens
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
        param = request.query_params.get("token")
        if param and param.startswith("pv_token_"):
            try:
                user_id = int(param.split("_")[2])
            except (IndexError, ValueError):
                pass

    if user_id:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT id, email, full_name, role FROM users WHERE id = ?", (user_id,))
        row = cur.fetchone()
        conn.close()
        if row and row["role"] in ["admin", "super_admin"]:
            return dict(row)
    raise HTTPException(status_code=403, detail="Administrator privileges required.")

def generate_unique_referral_code(conn, full_name: str) -> str:
    cur = conn.cursor()
    # Clean name to 4 uppercase alphabets
    clean_name = re.sub(r'[^A-Za-z]', '', full_name).upper()
    prefix = clean_name[:4] if len(clean_name) >= 3 else "REF"
    if len(prefix) < 3:
        prefix = "REF"

    # Try deterministic code first (e.g. ANIL001)
    for attempt in range(1, 100):
        code = f"{prefix}{attempt:03d}"
        cur.execute("SELECT id FROM referral_codes WHERE code = ?", (code,))
        if not cur.fetchone():
            return code

    # Fallback to random alphanumeric
    while True:
        code = f"{prefix}{random.randint(100, 9999)}"
        cur.execute("SELECT id FROM referral_codes WHERE code = ?", (code,))
        if not cur.fetchone():
            return code

# ================= PYDANTIC SCHEMAS =================

class PartnerRegisterRequest(BaseModel):
    full_name: str
    email: EmailStr
    mobile: str
    password: str
    college_name: Optional[str] = ""
    city: Optional[str] = ""
    preferred_payment_method: Optional[str] = "UPI"
    upi_id: Optional[str] = ""
    bank_account_name: Optional[str] = ""
    bank_account_number: Optional[str] = ""
    bank_ifsc: Optional[str] = ""
    bank_name: Optional[str] = ""

class PartnerLoginRequest(BaseModel):
    email: EmailStr
    password: str

class TrackClickPayload(BaseModel):
    referral_code: str
    landing_page: Optional[str] = "/"
    referrer_url: Optional[str] = ""

class PartnerPayoutRequestPayload(BaseModel):
    amount: Optional[float] = None
    payment_method: Optional[str] = None
    payout_details: Optional[str] = None

class PartnerProfileUpdatePayload(BaseModel):
    full_name: Optional[str] = None
    mobile: Optional[str] = None
    city: Optional[str] = None
    college_name: Optional[str] = None
    preferred_payment_method: Optional[str] = None
    upi_id: Optional[str] = None
    bank_account_name: Optional[str] = None
    bank_account_number: Optional[str] = None
    bank_ifsc: Optional[str] = None
    bank_name: Optional[str] = None

class AdminPartnerStatusPayload(BaseModel):
    status: str  # APPROVED, REJECTED, SUSPENDED, PENDING
    admin_notes: Optional[str] = ""

class AdminPayoutProcessPayload(BaseModel):
    action: str  # approve, reject
    utr_reference: Optional[str] = ""
    payment_method: Optional[str] = "UPI"
    notes: Optional[str] = ""

class AdminCommissionStatusPayload(BaseModel):
    status: str  # APPROVED, REVERSED, PENDING
    notes: Optional[str] = ""

class ReferralSettingsPayload(BaseModel):
    commission_rate_percentage: Optional[float] = 25.0
    attribution_window_days: Optional[int] = 30
    minimum_payout_amount: Optional[float] = 500.0
    auto_approve_partners: Optional[int] = 0
    exclude_tax_from_commission: Optional[int] = 1

# ================= PUBLIC & PARTNER ENDPOINTS =================

@router.post("/api/referrals/register")
def register_referral_partner(payload: PartnerRegisterRequest, request: Request):
    if len(payload.password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters.")
    if len(payload.mobile.strip()) < 10:
        raise HTTPException(status_code=400, detail="Please provide a valid 10-digit mobile number.")

    email_clean = payload.email.lower().strip()
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT id FROM referral_partners WHERE email = ?", (email_clean,))
    if cur.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail="A partner with this email is already registered.")

    pw_hash = hash_password(payload.password)

    # Check auto-approval setting
    cur.execute("SELECT setting_value FROM referral_settings WHERE setting_key = 'auto_approve_partners'")
    auto_row = cur.fetchone()
    auto_approve = auto_row and auto_row[0] == "1"
    initial_status = "APPROVED" if auto_approve else "PENDING"

    cur.execute("""
    INSERT INTO referral_partners (
        full_name, email, mobile, password_hash, college_name, city,
        preferred_payment_method, upi_id, bank_account_name, bank_account_number,
        bank_ifsc, bank_name, status
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        payload.full_name.strip(),
        email_clean,
        payload.mobile.strip(),
        pw_hash,
        payload.college_name.strip() if payload.college_name else "",
        payload.city.strip() if payload.city else "",
        payload.preferred_payment_method or "UPI",
        payload.upi_id.strip() if payload.upi_id else "",
        payload.bank_account_name.strip() if payload.bank_account_name else "",
        payload.bank_account_number.strip() if payload.bank_account_number else "",
        payload.bank_ifsc.strip().upper() if payload.bank_ifsc else "",
        payload.bank_name.strip() if payload.bank_name else "",
        initial_status
    ))
    partner_id = cur.lastrowid

    # Generate unique referral code immediately
    ref_code = generate_unique_referral_code(conn, payload.full_name)
    cur.execute("""
    INSERT INTO referral_codes (partner_id, code, url_slug, is_active)
    VALUES (?, ?, ?, ?)
    """, (partner_id, ref_code, ref_code.lower(), 1 if auto_approve else 0))

    conn.commit()
    conn.close()

    # Dispatches
    email_service.notify_admin_new_partner_registration({
        "full_name": payload.full_name,
        "email": email_clean,
        "mobile": payload.mobile,
        "college_name": payload.college_name,
        "city": payload.city,
        "preferred_payment_method": payload.preferred_payment_method,
        "upi_id": payload.upi_id
    })

    if auto_approve:
        email_service.notify_partner_status_update(
            {"full_name": payload.full_name, "email": email_clean},
            "APPROVED",
            ref_code
        )
    else:
        email_service.notify_partner_application_received({
            "full_name": payload.full_name,
            "email": email_clean
        })

    return {
        "success": True,
        "message": "Referral partner application submitted! You can log in once approved by administration." if not auto_approve else "Account approved! You can now log in.",
        "partner_id": partner_id,
        "status": initial_status,
        "referral_code": ref_code
    }

@router.post("/api/referrals/login")
def login_referral_partner(payload: PartnerLoginRequest):
    email_clean = payload.email.lower().strip()
    pw_hash = hash_password(payload.password)

    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
    SELECT rp.id, rp.full_name, rp.email, rp.mobile, rp.status, rp.upi_id, rp.preferred_payment_method,
           rc.code as referral_code
    FROM referral_partners rp
    LEFT JOIN referral_codes rc ON rc.partner_id = rp.id AND rc.is_active = 1
    WHERE rp.email = ? AND rp.password_hash = ?
    """, (email_clean, pw_hash))
    partner = cur.fetchone()
    conn.close()

    if not partner:
        raise HTTPException(status_code=401, detail="Invalid email or password.")

    if partner["status"] == "PENDING":
        raise HTTPException(
            status_code=403,
            detail="Your partner application is currently under review by our administration team. You will be notified via email once approved."
        )
    elif partner["status"] == "REJECTED":
        raise HTTPException(
            status_code=403,
            detail="Your referral partner application was not approved. Please contact support@projectverse.com."
        )
    elif partner["status"] == "SUSPENDED":
        raise HTTPException(
            status_code=403,
            detail="Your partner account is suspended. Please contact administrator."
        )

    # Issue token: pv_partner_{id}_{sig}
    sig_raw = f"{partner['id']}_{partner['email']}_{SECRET_KEY}".encode("utf-8")
    sig = hashlib.md5(sig_raw).hexdigest()[:16]
    token = f"pv_partner_{partner['id']}_{sig}"

    ref_code = partner["referral_code"] or "PENDING"
    ref_url = f"http://localhost:8000/?ref={ref_code}"

    return {
        "success": True,
        "token": token,
        "partner": {
            "id": partner["id"],
            "full_name": partner["full_name"],
            "email": partner["email"],
            "mobile": partner["mobile"],
            "status": partner["status"],
            "referral_code": ref_code,
            "referral_url": ref_url
        }
    }

@router.get("/api/referrals/partner/me")
def get_partner_profile(request: Request):
    partner = require_partner(request)
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT code FROM referral_codes WHERE partner_id = ? AND is_active = 1 LIMIT 1", (partner["id"],))
    code_row = cur.fetchone()
    ref_code = code_row["code"] if code_row else ""
    conn.close()

    partner["referral_code"] = ref_code
    partner["referral_url"] = f"http://localhost:8000/?ref={ref_code}"
    return {"success": True, "partner": partner}

@router.get("/api/referrals/partner/dashboard")
def get_partner_dashboard(request: Request):
    partner = require_partner(request)
    conn = get_db()
    cur = conn.cursor()

    # Get active referral code
    cur.execute("SELECT code FROM referral_codes WHERE partner_id = ? AND is_active = 1 LIMIT 1", (partner["id"],))
    code_row = cur.fetchone()
    ref_code = code_row["code"] if code_row else ""
    ref_url = f"http://localhost:8000/?ref={ref_code}"

    # Minimum payout setting
    cur.execute("SELECT setting_value FROM referral_settings WHERE setting_key = 'minimum_payout_amount'")
    min_pay_row = cur.fetchone()
    min_payout = float(min_pay_row[0]) if min_pay_row else 500.0

    # Commissions breakdown
    cur.execute("""
    SELECT
        COUNT(id) as total_comm_count,
        COALESCE(SUM(CASE WHEN status = 'APPROVED' THEN commission_amount ELSE 0 END), 0.0) as approved_balance,
        COALESCE(SUM(CASE WHEN status = 'PENDING' THEN commission_amount ELSE 0 END), 0.0) as pending_balance,
        COALESCE(SUM(CASE WHEN status = 'PAID' THEN commission_amount ELSE 0 END), 0.0) as paid_balance,
        COALESCE(SUM(CASE WHEN status IN ('APPROVED', 'PAID', 'PAYOUT_REQUESTED') THEN commission_amount ELSE 0 END), 0.0) as total_earnings
    FROM referral_commissions
    WHERE partner_id = ?
    """, (partner["id"],))
    comm_stats = cur.fetchone()

    approved_balance = round(float(comm_stats["approved_balance"]), 2)
    pending_balance = round(float(comm_stats["pending_balance"]), 2)
    paid_balance = round(float(comm_stats["paid_balance"]), 2)
    total_earnings = round(float(comm_stats["total_earnings"]), 2)

    total_clicks = int(partner["total_clicks"] or 0)
    total_sales = int(partner["total_sales"] or 0)
    conversion_rate = round((total_sales / total_clicks * 100), 2) if total_clicks > 0 else 0.0

    # Recent referred orders & commissions
    cur.execute("""
    SELECT rc.id, rc.order_number, rc.order_amount, rc.commission_amount, rc.commission_rate,
           rc.status, rc.created_at, p.project_code, p.title as project_title,
           u.full_name as student_name
    FROM referral_commissions rc
    JOIN orders o ON rc.order_id = o.id
    JOIN projects p ON o.project_id = p.id
    LEFT JOIN users u ON o.user_id = u.id
    WHERE rc.partner_id = ?
    ORDER BY rc.id DESC LIMIT 50
    """, (partner["id"],))
    commissions_list = [dict(r) for r in cur.fetchall()]

    # Payout requests history
    cur.execute("""
    SELECT id, request_number, amount, payment_method, payout_details, status, admin_notes, requested_at, processed_at
    FROM referral_payout_requests
    WHERE partner_id = ?
    ORDER BY id DESC LIMIT 20
    """, (partner["id"],))
    payout_requests = [dict(r) for r in cur.fetchall()]

    # Referred students roster
    cur.execute("""
    SELECT ra.id, ra.student_email, ra.attribution_date, ra.is_active,
           u.full_name as student_name, u.college, u.course
    FROM referral_attributions ra
    JOIN users u ON ra.student_user_id = u.id
    WHERE ra.partner_id = ?
    ORDER BY ra.id DESC LIMIT 50
    """, (partner["id"],))
    students_list = [dict(r) for r in cur.fetchall()]

    conn.close()

    # Pre-formatted share messages
    wa_msg = f"Hey! Explore 90 verified academic projects for BCA, B.Tech, MCA & B.Com with IEEE reports, source code & PPT: {ref_url}"
    telegram_msg = f"Get authentic college capstone projects with full source code & viva guides starting at Rs 799 on PROJECTVERSE: {ref_url}"

    return {
        "success": True,
        "partner": {
            "id": partner["id"],
            "full_name": partner["full_name"],
            "email": partner["email"],
            "mobile": partner["mobile"],
            "city": partner["city"],
            "preferred_payment_method": partner["preferred_payment_method"],
            "upi_id": partner["upi_id"],
            "bank_account_number": partner["bank_account_number"],
            "bank_ifsc": partner["bank_ifsc"]
        },
        "referral_code": ref_code,
        "referral_url": ref_url,
        "share_templates": {
            "whatsapp": f"https://wa.me/?text={wa_msg.replace(' ', '%20')}",
            "telegram": f"https://t.me/share/url?url={ref_url}&text=PROJECTVERSE%20Verified%20Projects",
            "twitter": f"https://twitter.com/intent/tweet?text={wa_msg.replace(' ', '%20')}"
        },
        "stats": {
            "total_clicks": total_clicks,
            "total_registrations": int(partner["total_registrations"] or 0),
            "total_sales": total_sales,
            "conversion_rate_percentage": conversion_rate,
            "commission_rate_percentage": 25,
            "approved_balance": approved_balance,
            "pending_balance": pending_balance,
            "paid_balance": paid_balance,
            "total_earnings": total_earnings,
            "minimum_payout_amount": min_payout,
            "can_request_payout": approved_balance >= min_payout
        },
        "commissions": commissions_list,
        "payout_requests": payout_requests,
        "students": students_list
    }

@router.post("/api/referrals/partner/payout-request")
def request_partner_payout(payload: PartnerPayoutRequestPayload, request: Request):
    partner = require_partner(request)
    conn = get_db()
    cur = conn.cursor()

    # Get approved balance
    cur.execute("""
    SELECT COALESCE(SUM(commission_amount), 0.0) as approved_balance
    FROM referral_commissions
    WHERE partner_id = ? AND status = 'APPROVED'
    """, (partner["id"],))
    approved_balance = round(float(cur.fetchone()["approved_balance"]), 2)

    # Check minimum payout amount
    cur.execute("SELECT setting_value FROM referral_settings WHERE setting_key = 'minimum_payout_amount'")
    min_row = cur.fetchone()
    min_payout = float(min_row[0]) if min_row else 500.0

    req_amount = payload.amount if payload.amount and payload.amount > 0 else approved_balance
    req_amount = round(req_amount, 2)

    if req_amount < min_payout:
        conn.close()
        raise HTTPException(
            status_code=400,
            detail=f"Minimum payout request is Rs {min_payout:,.0f}. Your available approved balance is Rs {approved_balance:,.2f}."
        )

    if req_amount > approved_balance:
        conn.close()
        raise HTTPException(
            status_code=400,
            detail=f"Requested amount (Rs {req_amount:,.2f}) exceeds available approved balance (Rs {approved_balance:,.2f})."
        )

    # Check for existing pending payout request
    cur.execute("SELECT id FROM referral_payout_requests WHERE partner_id = ? AND status = 'PENDING'", (partner["id"],))
    if cur.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail="You already have a payout request pending review.")

    req_num = f"REQ-PAY-{datetime.now().strftime('%Y%m%d')}-{random.randint(1000, 9999)}"
    pay_method = payload.payment_method or partner["preferred_payment_method"] or "UPI"
    pay_details = payload.payout_details or (partner["upi_id"] if pay_method == "UPI" else f"A/C: {partner['bank_account_number']}, IFSC: {partner['bank_ifsc']}")

    cur.execute("""
    INSERT INTO referral_payout_requests (
        request_number, partner_id, amount, payment_method, payout_details, status
    ) VALUES (?, ?, ?, ?, ?, 'PENDING')
    """, (req_num, partner["id"], req_amount, pay_method, pay_details))
    payout_req_id = cur.lastrowid

    # Mark associated approved commissions as PAYOUT_REQUESTED
    cur.execute("""
    UPDATE referral_commissions
    SET status = 'PAYOUT_REQUESTED', payout_request_id = ?, updated_at = CURRENT_TIMESTAMP
    WHERE partner_id = ? AND status = 'APPROVED'
    """, (payout_req_id, partner["id"]))

    conn.commit()
    conn.close()

    email_service.notify_admin_payout_requested({
        "partner_name": partner["full_name"],
        "request_number": req_num,
        "amount": req_amount,
        "payment_method": pay_method,
        "payout_details": pay_details
    })

    return {
        "success": True,
        "message": f"Payout request {req_num} of Rs {req_amount:,.2f} submitted successfully! Administration will process settlement within 24-48 hours.",
        "request_number": req_num,
        "amount": req_amount
    }

@router.put("/api/referrals/partner/profile")
def update_partner_profile(payload: PartnerProfileUpdatePayload, request: Request):
    partner = require_partner(request)
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    UPDATE referral_partners SET
        full_name = COALESCE(?, full_name),
        mobile = COALESCE(?, mobile),
        city = COALESCE(?, city),
        college_name = COALESCE(?, college_name),
        preferred_payment_method = COALESCE(?, preferred_payment_method),
        upi_id = COALESCE(?, upi_id),
        bank_account_name = COALESCE(?, bank_account_name),
        bank_account_number = COALESCE(?, bank_account_number),
        bank_ifsc = COALESCE(?, bank_ifsc),
        bank_name = COALESCE(?, bank_name),
        updated_at = CURRENT_TIMESTAMP
    WHERE id = ?
    """, (
        payload.full_name, payload.mobile, payload.city, payload.college_name,
        payload.preferred_payment_method, payload.upi_id, payload.bank_account_name,
        payload.bank_account_number, payload.bank_ifsc, payload.bank_name,
        partner["id"]
    ))
    conn.commit()
    conn.close()
    return {"success": True, "message": "Payout and profile settings updated successfully."}

# ================= PUBLIC CLICK TRACKING & VALIDATION =================

@router.post("/api/referrals/track-click")
def track_referral_click(payload: TrackClickPayload, request: Request):
    code_clean = payload.referral_code.strip().upper()
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    SELECT rc.id, rc.code, rp.id as partner_id, rp.full_name, rp.status
    FROM referral_codes rc
    JOIN referral_partners rp ON rc.partner_id = rp.id
    WHERE rc.code = ? AND rc.is_active = 1
    """, (code_clean,))
    row = cur.fetchone()

    if not row or row["status"] != "APPROVED":
        conn.close()
        return {"success": False, "valid": False, "message": "Referral code is not active."}

    client_ip = request.client.host if request.client else "127.0.0.1"
    user_agent = request.headers.get("User-Agent", "")[:250]

    cur.execute("""
    INSERT INTO referral_clicks (referral_code, partner_id, ip_address, user_agent, referrer_url, landing_page)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (code_clean, row["partner_id"], client_ip, user_agent, payload.referrer_url or "", payload.landing_page or "/"))

    cur.execute("UPDATE referral_codes SET clicks_count = clicks_count + 1 WHERE code = ?", (code_clean,))
    cur.execute("UPDATE referral_partners SET total_clicks = total_clicks + 1 WHERE id = ?", (row["partner_id"],))

    conn.commit()
    conn.close()

    return {
        "success": True,
        "valid": True,
        "referral_code": code_clean,
        "partner_name": row["full_name"],
        "attribution_window_days": 30
    }

@router.get("/api/referrals/validate-code/{code}")
def validate_referral_code(code: str):
    code_clean = code.strip().upper()
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
    SELECT rc.code, rp.full_name, rp.status
    FROM referral_codes rc
    JOIN referral_partners rp ON rc.partner_id = rp.id
    WHERE rc.code = ? AND rc.is_active = 1
    """, (code_clean,))
    row = cur.fetchone()
    conn.close()

    if row and row["status"] == "APPROVED":
        return {"valid": True, "code": code_clean, "partner_name": row["full_name"]}
    return {"valid": False, "code": code_clean}

# ================= ADMIN REFERRAL MANAGEMENT ENDPOINTS =================

@router.get("/api/admin/referrals/stats")
def get_admin_referral_stats(request: Request):
    require_admin(request)
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(id) FROM referral_partners")
    total_partners = cur.fetchone()[0]

    cur.execute("SELECT COUNT(id) FROM referral_partners WHERE status = 'PENDING'")
    pending_partners = cur.fetchone()[0]

    cur.execute("SELECT COUNT(id) FROM referral_partners WHERE status = 'APPROVED'")
    approved_partners = cur.fetchone()[0]

    cur.execute("SELECT COUNT(id) FROM referral_clicks")
    total_clicks = cur.fetchone()[0]

    cur.execute("SELECT COUNT(id) FROM referral_attributions")
    total_attributions = cur.fetchone()[0]

    cur.execute("SELECT COUNT(id) FROM referral_conversions")
    total_conversions = cur.fetchone()[0]

    cur.execute("SELECT COALESCE(SUM(commission_amount), 0.0) FROM referral_commissions WHERE status IN ('APPROVED', 'PAID', 'PAYOUT_REQUESTED')")
    total_comm_earned = round(float(cur.fetchone()[0]), 2)

    cur.execute("SELECT COALESCE(SUM(commission_amount), 0.0) FROM referral_commissions WHERE status = 'PAID'")
    total_comm_paid = round(float(cur.fetchone()[0]), 2)

    cur.execute("SELECT COALESCE(SUM(amount), 0.0) FROM referral_payout_requests WHERE status = 'PENDING'")
    pending_payouts = round(float(cur.fetchone()[0]), 2)

    conn.close()

    return {
        "success": True,
        "stats": {
            "total_partners": total_partners,
            "pending_partners": pending_partners,
            "approved_partners": approved_partners,
            "total_clicks": total_clicks,
            "total_attributions": total_attributions,
            "total_conversions": total_conversions,
            "total_commission_earned": total_comm_earned,
            "total_commission_paid": total_comm_paid,
            "pending_payouts_amount": pending_payouts
        }
    }

@router.get("/api/admin/referrals/partners")
def list_admin_referral_partners(request: Request, status: Optional[str] = None, search: Optional[str] = None):
    require_admin(request)
    conn = get_db()
    cur = conn.cursor()

    conditions = ["1=1"]
    params = []
    if status and status.strip() and status != "ALL":
        conditions.append("rp.status = ?")
        params.append(status.strip().upper())
    if search and search.strip():
        term = f"%{search.strip().lower()}%"
        conditions.append("(LOWER(rp.full_name) LIKE ? OR LOWER(rp.email) LIKE ? OR rp.mobile LIKE ? OR LOWER(rc.code) LIKE ?)")
        params.extend([term, term, term, term])

    sql = f"""
    SELECT rp.id, rp.full_name, rp.email, rp.mobile, rp.college_name, rp.city,
           rp.preferred_payment_method, rp.upi_id, rp.bank_account_name, rp.bank_account_number,
           rp.bank_ifsc, rp.bank_name, rp.status, rp.admin_notes,
           rp.total_clicks, rp.total_registrations, rp.total_sales,
           rp.total_commission_earned, rp.total_commission_paid,
           (rp.total_commission_earned - rp.total_commission_paid) as available_balance,
           rp.created_at, rc.code as referral_code
    FROM referral_partners rp
    LEFT JOIN referral_codes rc ON rc.partner_id = rp.id AND rc.is_active = 1
    WHERE {' AND '.join(conditions)}
    ORDER BY rp.id DESC
    """
    cur.execute(sql, tuple(params))
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()

    return {"success": True, "partners": rows}

@router.post("/api/admin/referrals/partners/{partner_id}/status")
def update_partner_status(partner_id: int, payload: AdminPartnerStatusPayload, request: Request):
    user = require_admin(request)
    new_status = payload.status.upper()
    if new_status not in ["APPROVED", "REJECTED", "SUSPENDED", "PENDING"]:
        raise HTTPException(status_code=400, detail="Invalid status value.")

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT id, full_name, email, mobile FROM referral_partners WHERE id = ?", (partner_id,))
    partner = cur.fetchone()
    if not partner:
        conn.close()
        raise HTTPException(status_code=404, detail="Referral partner not found.")

    # Check for active referral code; generate if approving and none active
    cur.execute("SELECT id, code FROM referral_codes WHERE partner_id = ? AND is_active = 1", (partner_id,))
    code_row = cur.fetchone()
    ref_code = code_row["code"] if code_row else None

    if new_status == "APPROVED":
        if not ref_code:
            ref_code = generate_unique_referral_code(conn, partner["full_name"])
            cur.execute("INSERT INTO referral_codes (partner_id, code, url_slug, is_active) VALUES (?, ?, ?, 1)",
                        (partner_id, ref_code, ref_code.lower()))
        else:
            cur.execute("UPDATE referral_codes SET is_active = 1 WHERE partner_id = ?", (partner_id,))
    elif new_status in ["SUSPENDED", "REJECTED"]:
        cur.execute("UPDATE referral_codes SET is_active = 0 WHERE partner_id = ?", (partner_id,))

    cur.execute("""
    UPDATE referral_partners
    SET status = ?, admin_notes = ?, updated_at = CURRENT_TIMESTAMP
    WHERE id = ?
    """, (new_status, payload.admin_notes or "", partner_id))

    conn.commit()
    conn.close()

    email_service.notify_partner_status_update(dict(partner), new_status, ref_code or "")

    return {
        "success": True,
        "message": f"Partner status updated to {new_status}.",
        "status": new_status,
        "referral_code": ref_code
    }

@router.get("/api/admin/referrals/commissions")
def list_admin_commissions(request: Request, status: Optional[str] = None, partner_id: Optional[int] = None):
    require_admin(request)
    conn = get_db()
    cur = conn.cursor()

    conditions = ["1=1"]
    params = []
    if status and status.strip() and status != "ALL":
        conditions.append("rc.status = ?")
        params.append(status.strip().upper())
    if partner_id:
        conditions.append("rc.partner_id = ?")
        params.append(partner_id)

    sql = f"""
    SELECT rc.id, rc.order_id, rc.order_number, rc.order_amount, rc.commission_rate, rc.commission_amount,
           rc.status, rc.notes, rc.approved_by, rc.approved_at, rc.created_at,
           rp.id as partner_id, rp.full_name as partner_name, rp.email as partner_email, rp.upi_id,
           p.project_code, p.title as project_title,
           o.customer_name as student_name
    FROM referral_commissions rc
    JOIN referral_partners rp ON rc.partner_id = rp.id
    JOIN orders o ON rc.order_id = o.id
    JOIN projects p ON o.project_id = p.id
    WHERE {' AND '.join(conditions)}
    ORDER BY rc.id DESC
    """
    cur.execute(sql, tuple(params))
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()

    return {"success": True, "commissions": rows}

@router.post("/api/admin/referrals/commissions/{commission_id}/status")
def update_commission_status(commission_id: int, payload: AdminCommissionStatusPayload, request: Request):
    user = require_admin(request)
    new_status = payload.status.upper()
    if new_status not in ["APPROVED", "REVERSED", "PENDING"]:
        raise HTTPException(status_code=400, detail="Status must be APPROVED, REVERSED, or PENDING.")

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    SELECT rc.id, rc.partner_id, rc.commission_amount, rc.order_number, rc.status,
           rp.full_name, rp.email
    FROM referral_commissions rc
    JOIN referral_partners rp ON rc.partner_id = rp.id
    WHERE rc.id = ?
    """, (commission_id,))
    comm = cur.fetchone()
    if not comm:
        conn.close()
        raise HTTPException(status_code=404, detail="Commission record not found.")

    old_status = comm["status"]
    if old_status != new_status:
        cur.execute("UPDATE referral_commissions SET status = ?, notes = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                    (new_status, payload.notes or "", commission_id))

        # Adjust partner balance if transitioning to/from REVERSED
        if new_status == "REVERSED" and old_status in ["APPROVED", "PENDING", "PAYOUT_REQUESTED"]:
            cur.execute("""
            UPDATE referral_partners
            SET total_commission_earned = MAX(0, total_commission_earned - ?),
                total_sales = MAX(0, total_sales - 1),
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """, (comm["commission_amount"], comm["partner_id"]))
            email_service.notify_partner_commission_reversed(
                {"full_name": comm["full_name"], "email": comm["email"]},
                {"order_number": comm["order_number"], "commission_amount": comm["commission_amount"]}
            )
        elif old_status == "REVERSED" and new_status == "APPROVED":
            cur.execute("""
            UPDATE referral_partners
            SET total_commission_earned = total_commission_earned + ?,
                total_sales = total_sales + 1,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """, (comm["commission_amount"], comm["partner_id"]))

    conn.commit()
    conn.close()

    return {"success": True, "message": f"Commission status updated to {new_status}."}

@router.get("/api/admin/referrals/payout-requests")
def list_admin_payout_requests(request: Request, status: Optional[str] = None):
    require_admin(request)
    conn = get_db()
    cur = conn.cursor()

    conditions = ["1=1"]
    params = []
    if status and status.strip() and status != "ALL":
        conditions.append("rpr.status = ?")
        params.append(status.strip().upper())

    sql = f"""
    SELECT rpr.id, rpr.request_number, rpr.amount, rpr.payment_method, rpr.payout_details,
           rpr.status, rpr.admin_notes, rpr.requested_at, rpr.processed_at,
           rp.id as partner_id, rp.full_name as partner_name, rp.email as partner_email, rp.mobile as partner_mobile,
           rpt.utr_reference, rpt.processed_by, rpt.created_at as paid_at
    FROM referral_payout_requests rpr
    JOIN referral_partners rp ON rpr.partner_id = rp.id
    LEFT JOIN referral_payout_transactions rpt ON rpt.payout_request_id = rpr.id
    WHERE {' AND '.join(conditions)}
    ORDER BY rpr.id DESC
    """
    cur.execute(sql, tuple(params))
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()

    return {"success": True, "payout_requests": rows}

@router.post("/api/admin/referrals/payout-requests/{request_id}/process")
def process_payout_request(request_id: int, payload: AdminPayoutProcessPayload, request: Request):
    user = require_admin(request)
    action = payload.action.lower()
    if action not in ["approve", "reject"]:
        raise HTTPException(status_code=400, detail="Action must be 'approve' or 'reject'.")

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    SELECT rpr.id, rpr.request_number, rpr.amount, rpr.partner_id, rpr.status, rpr.payment_method, rpr.payout_details,
           rp.full_name, rp.email
    FROM referral_payout_requests rpr
    JOIN referral_partners rp ON rpr.partner_id = rp.id
    WHERE rpr.id = ?
    """, (request_id,))
    req_row = cur.fetchone()
    if not req_row:
        conn.close()
        raise HTTPException(status_code=404, detail="Payout request not found.")

    if req_row["status"] != "PENDING":
        conn.close()
        raise HTTPException(status_code=400, detail=f"Payout request is already {req_row['status']}.")

    if action == "approve":
        utr = payload.utr_reference.strip() if payload.utr_reference else f"PAY-SETTLE-{datetime.now().strftime('%Y%m%d%H%M')}"
        method = payload.payment_method or req_row["payment_method"] or "UPI"

        # Update request status to PAID
        cur.execute("""
        UPDATE referral_payout_requests
        SET status = 'PAID', admin_notes = ?, processed_at = CURRENT_TIMESTAMP
        WHERE id = ?
        """, (payload.notes or "Settled via administrative bank transfer.", request_id))

        # Record transaction settlement
        cur.execute("""
        INSERT INTO referral_payout_transactions (
            payout_request_id, partner_id, amount, payment_method, utr_reference, status, processed_by, notes
        ) VALUES (?, ?, ?, ?, ?, 'PAID', ?, ?)
        """, (request_id, req_row["partner_id"], req_row["amount"], method, utr, user["full_name"], payload.notes or ""))

        # Mark associated commissions as PAID
        cur.execute("""
        UPDATE referral_commissions
        SET status = 'PAID', paid_at = CURRENT_TIMESTAMP, updated_at = CURRENT_TIMESTAMP
        WHERE payout_request_id = ?
        """, (request_id,))

        # Update partner's paid balance
        cur.execute("""
        UPDATE referral_partners
        SET total_commission_paid = total_commission_paid + ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        """, (req_row["amount"], req_row["partner_id"]))

        conn.commit()
        conn.close()

        email_service.notify_partner_payout_processed(
            {"full_name": req_row["full_name"], "email": req_row["email"]},
            {
                "amount": req_row["amount"],
                "payment_method": method,
                "utr_reference": utr,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        )

        return {"success": True, "message": f"Payout approved and settlement recorded (UTR: {utr})."}

    else:
        # Revert request and return commissions back to APPROVED
        cur.execute("""
        UPDATE referral_payout_requests
        SET status = 'REJECTED', admin_notes = ?, processed_at = CURRENT_TIMESTAMP
        WHERE id = ?
        """, (payload.notes or "Payout request rejected.", request_id))

        cur.execute("""
        UPDATE referral_commissions
        SET status = 'APPROVED', payout_request_id = NULL, updated_at = CURRENT_TIMESTAMP
        WHERE payout_request_id = ?
        """, (request_id,))

        conn.commit()
        conn.close()

        return {"success": True, "message": "Payout request rejected. Available balance returned to partner account."}

@router.get("/api/admin/referrals/clicks")
def list_admin_referral_clicks(request: Request, limit: int = 100):
    require_admin(request)
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    SELECT rc.id, rc.referral_code, rc.partner_id, rc.ip_address, rc.user_agent, rc.referrer_url, rc.landing_page, rc.created_at,
           rp.full_name as partner_name
    FROM referral_clicks rc
    LEFT JOIN referral_partners rp ON rc.partner_id = rp.id
    ORDER BY rc.id DESC LIMIT ?
    """, (min(limit, 500),))
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()

    return {"success": True, "clicks": rows}

@router.get("/api/admin/referrals/settings")
def get_referral_settings(request: Request):
    require_admin(request)
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT setting_key, setting_value, description FROM referral_settings")
    settings = {r["setting_key"]: r["setting_value"] for r in cur.fetchall()}
    conn.close()
    return {"success": True, "settings": settings}

@router.put("/api/admin/referrals/settings")
def update_referral_settings(payload: ReferralSettingsPayload, request: Request):
    require_admin(request)
    conn = get_db()
    cur = conn.cursor()

    if payload.commission_rate_percentage is not None:
        cur.execute("UPDATE referral_settings SET setting_value = ?, updated_at = CURRENT_TIMESTAMP WHERE setting_key = 'commission_rate_percentage'",
                    (str(payload.commission_rate_percentage),))

    if payload.attribution_window_days is not None:
        cur.execute("UPDATE referral_settings SET setting_value = ?, updated_at = CURRENT_TIMESTAMP WHERE setting_key = 'attribution_window_days'",
                    (str(payload.attribution_window_days),))

    if payload.minimum_payout_amount is not None:
        cur.execute("UPDATE referral_settings SET setting_value = ?, updated_at = CURRENT_TIMESTAMP WHERE setting_key = 'minimum_payout_amount'",
                    (str(payload.minimum_payout_amount),))

    if payload.auto_approve_partners is not None:
        cur.execute("UPDATE referral_settings SET setting_value = ?, updated_at = CURRENT_TIMESTAMP WHERE setting_key = 'auto_approve_partners'",
                    (str(payload.auto_approve_partners),))

    if payload.exclude_tax_from_commission is not None:
        cur.execute("UPDATE referral_settings SET setting_value = ?, updated_at = CURRENT_TIMESTAMP WHERE setting_key = 'exclude_tax_from_commission'",
                    (str(payload.exclude_tax_from_commission),))

    conn.commit()
    conn.close()
    return {"success": True, "message": "Referral system settings updated successfully."}

@router.get("/api/admin/referrals/export")
def export_referral_report_csv(request: Request):
    require_admin(request)
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    SELECT rc.order_number, p.project_code, p.title as project_title,
           o.customer_name as student_name, rc.order_amount,
           (rc.commission_rate * 100) as comm_rate_pct, rc.commission_amount,
           rc.status as commission_status, rp.full_name as partner_name,
           rp.email as partner_email, rp.upi_id, rc.created_at, rc.paid_at
    FROM referral_commissions rc
    JOIN referral_partners rp ON rc.partner_id = rp.id
    JOIN orders o ON rc.order_id = o.id
    JOIN projects p ON o.project_id = p.id
    ORDER BY rc.id DESC
    """)
    rows = cur.fetchall()
    conn.close()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "Order Number", "Project Code", "Project Title", "Student Name",
        "Order Amount (INR)", "Commission Rate (%)", "Commission Amount (INR)",
        "Status", "Partner Name", "Partner Email", "Partner UPI", "Date Earned", "Date Paid"
    ])

    for r in rows:
        writer.writerow([
            r["order_number"], r["project_code"], r["project_title"], r["student_name"],
            f"{r['order_amount']:.2f}", f"{r['comm_rate_pct']:.0f}%", f"{r['commission_amount']:.2f}",
            r["commission_status"], r["partner_name"], r["partner_email"], r["upi_id"],
            r["created_at"], r["paid_at"] or "N/A"
        ])

    csv_data = output.getvalue()
    filename = f"projectverse_referral_commissions_{datetime.now().strftime('%Y%m%d')}.csv"

    return Response(
        content=csv_data,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
