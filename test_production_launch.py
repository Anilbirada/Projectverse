"""
PROJECTVERSE - Production Launch End-to-End Verification Test Suite
Tests every critical production workflow against http://localhost:8000
"""

import urllib.request
import urllib.parse
import json
import sqlite3
import time

BASE_URL = "http://localhost:8000"

def query_db(query, params=()):
    conn = sqlite3.connect("projectverse.db", timeout=30.0)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(query, params)
    rows = cur.fetchall()
    conn.close()
    return rows

def query_one(query, params=()):
    rows = query_db(query, params)
    return rows[0] if rows else None

def request(method, endpoint, data=None, token=None):
    url = f"{BASE_URL}{endpoint}"
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    body = json.dumps(data).encode("utf-8") if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            content = resp.read().decode("utf-8")
            try:
                return resp.status, json.loads(content)
            except Exception:
                return resp.status, content
    except urllib.error.HTTPError as e:
        content = e.read().decode("utf-8")
        try:
            return e.code, json.loads(content)
        except Exception:
            return e.code, content

def run_tests():
    print("=" * 70)
    print("PROJECTVERSE - PRODUCTION LAUNCH VERIFICATION")
    print("=" * 70)
    passed = 0
    total = 0

    def test(name, condition, detail=""):
        nonlocal passed, total
        total += 1
        status = "PASSED" if condition else "FAILED"
        print(f"[{status}] {name}")
        if not condition and detail:
            print(f"       Details: {detail}")
        if condition:
            passed += 1

    # 1. Health Endpoint
    code, res = request("GET", "/api/health")
    test("1. Health Endpoint (/api/health)", code == 200 and res.get("status") == "healthy" and res.get("projects_count") == 90, f"Got: {res}")

    # 2. Database Integrity Check
    p_count = query_one("SELECT COUNT(*) as count FROM projects")["count"]
    test("2. Exact 90 Catalogue Projects in DB", p_count == 90, f"Count: {p_count}")

    min_price = query_one("SELECT MIN(price) as min_p FROM projects")["min_p"]
    test("3. Minimum Price Rule Enforced (>= 799)", min_price >= 799, f"Min price: {min_price}")

    demo_count = query_one("SELECT COUNT(*) as count FROM users WHERE email LIKE '%example.test%'")["count"]
    test("4. Zero Demo Records in Users Table", demo_count == 0, f"Demo users count: {demo_count}")

    # 3. Super Admin Authentication
    code, res = request("POST", "/api/auth/login", {
        "email": "aniladani843@gmail.com",
        "password": "Admin@12345"
    })
    admin_token = res.get("token") if code == 200 else None
    test("5. Super Admin Login (aniladani843@gmail.com)", code == 200 and admin_token is not None, f"Code: {code}, Res: {res}")

    # 4. Student Registration
    test_email = f"kavya.sharma_{int(time.time())}@gmail.com"
    code, res = request("POST", "/api/auth/register", {
        "full_name": "Kavya Sharma",
        "email": test_email,
        "password": "Password@123",
        "mobile": "9845123456",
        "college": "RV College of Engineering",
        "university": "Visvesvaraya Technological University",
        "course": "B.Tech",
        "academic_year": "Final Year",
        "specialization": "Artificial Intelligence",
        "preferred_tech": "Python / React",
        "team_mode": "Individual"
    })
    test("6. Customer Registration (/api/auth/register)", code in [200, 201] or "already exists" in str(res), f"Res: {res}")

    # 5. Customer Login
    code, res = request("POST", "/api/auth/login", {
        "email": test_email,
        "password": "Password@123"
    })
    student_token = res.get("token") if code == 200 else None
    test("7. Customer Login with JWT Token", code == 200 and student_token is not None, f"Res: {res}")

    # Fetch a valid project ID from the database (IDs are 121..210)
    valid_proj = query_one("SELECT id, project_code, title FROM projects LIMIT 1")
    valid_proj_id = valid_proj["id"]

    # 6. Customer Submits Project Enquiry
    code, res = request("POST", "/api/enquiries/create", {
        "customer_name": "Kavya Sharma",
        "customer_email": test_email,
        "customer_phone": "9845123456",
        "college_name": "RV College of Engineering",
        "course": "B.Tech CSE",
        "project_id": valid_proj_id,
        "technology": "Python / React",
        "message": "Need synopsis approval and full IEEE code deliverables for upcoming semester 8 review."
    })
    enquiry_number = res.get("enquiry_number") if code == 200 else None
    enquiry_id = res.get("enquiry_id") if code == 200 else None
    test("8. Project Enquiry Submission (/api/enquiries/create)", code == 200 and enquiry_number and enquiry_number.startswith("ENQ-"), f"Res: {res}")

    # 7. Check Email Logs Table for Automated Dispatch to aniladani843@gmail.com
    email_row = query_one("SELECT id, event_type, recipient_email, status, subject FROM email_logs WHERE recipient_email = 'aniladani843@gmail.com' ORDER BY id DESC LIMIT 1")
    test("9. Email Logged for Dispatch to Owner (aniladani843@gmail.com)", email_row is not None and email_row["recipient_email"] == "aniladani843@gmail.com", f"Row: {dict(email_row) if email_row else None}")

    # 8. Check Admin Notification Created
    notif_row = query_one("SELECT id, title, message FROM notifications WHERE type = 'enquiry' ORDER BY id DESC LIMIT 1")
    test("10. Admin Notification Centre Record Created", notif_row is not None and "ENQ-" in notif_row["title"], f"Row: {dict(notif_row) if notif_row else None}")

    # 9. Customer Submits Capstone Project Request
    code, res = request("POST", "/api/requests/create", {
        "student_name": "Kavya Sharma",
        "student_email": test_email,
        "student_phone": "9845123456",
        "college_name": "RV College of Engineering",
        "course": "B.Tech CSE",
        "project_id": valid_proj_id,
        "preferred_tech": "Python / PyTorch",
        "deadline": "6 Weeks",
        "requirements": "Complete source code, PPT, and report formatted in IEEE standards.",
        "team_mode": "Individual"
    }, token=student_token)
    req_number = res.get("request_number") if code == 200 else None
    req_id = res.get("request_id") if code == 200 else None
    test("11. Capstone Project Request Submission (/api/requests/create)", code == 200 and req_number and req_number.startswith("REQ-"), f"Res: {res}")

    # 10. Student Dashboard Fetch
    code, res = request("GET", "/api/student/dashboard", token=student_token)
    test("12. Customer Dashboard (/api/student/dashboard)", code == 200 and "enquiries" in res and "requests" in res, f"Keys: {list(res.keys()) if isinstance(res, dict) else res}")

    # 11. Admin Enquiry Management
    if admin_token and enquiry_id:
        code, res = request("PUT", f"/api/admin/enquiries/{enquiry_id}/status", {
            "status": "CONTACTED",
            "admin_notes": "Called student on WhatsApp +919845123456; shared project synopsis."
        }, token=admin_token)
        test("13. Admin Enquiry Status Update & Notes", code == 200, f"Res: {res}")

    # 12. Admin Request Approval & Mentor Assignment
    if admin_token and req_id:
        code, res = request("POST", f"/api/admin/requests/{req_id}/action", {
            "action": "approve"
        }, token=admin_token)
        test("14. Admin Capstone Request Approval", code == 200, f"Res: {res}")

        code, res = request("POST", f"/api/admin/requests/{req_id}/assign-mentor", {
            "mentor_id": 1
        }, token=admin_token)
        test("15. Admin Mentor Assignment", code == 200, f"Res: {res}")

        code, res = request("POST", f"/api/admin/requests/{req_id}/progress", {
            "progress_percentage": 50,
            "milestone_notes": "Backend API and database architecture completed."
        }, token=admin_token)
        test("16. Admin Progress Milestone Update", code == 200, f"Res: {res}")

    # 13. Customer Submits UPI Order
    code, res = request("POST", "/api/orders/create", {
        "project_id": valid_proj_id,
        "utr_reference": "492817293810"
    }, token=student_token)
    order_id = res.get("order_id") if code == 200 else None
    test("17. Customer UPI Order Submission (/api/orders/create)", code == 200 and order_id is not None, f"Res: {res}")

    # 14. Admin Verifies Payment and Generates Official GST Invoice
    if admin_token and order_id:
        code, res = request("POST", f"/api/admin/payments/{order_id}/verify", {
            "status": "approved",
            "notes": "Verified against bank settlement to ANIL."
        }, token=admin_token)
        test("18. Admin Payment Verification (/api/admin/payments/{id}/verify)", code == 200, f"Res: {res}")

        code, res = request("POST", f"/api/admin/orders/{order_id}/generate-invoice", token=admin_token)
        inv_number = res.get("invoice_number") if code == 200 else None
        test("19. Admin GST Invoice Generation (/api/admin/orders/{id}/generate-invoice)", code == 200 and inv_number and inv_number.startswith("INV-"), f"Res: {res}")

        # 15. Printable HTML Invoice Endpoint
        if inv_number:
            code, html = request("GET", f"/api/invoices/{inv_number}")
            test("20. Printable HTML Invoice Display (/api/invoices/{inv})", code == 200 and "TAX INVOICE" in str(html) and "18% GST" in str(html), f"HTML snippet: {str(html)[:150]}")

    # 16. Admin Email Logs Review and Retry
    if admin_token:
        code, res = request("GET", "/api/admin/email-logs", token=admin_token)
        logs = res.get("logs", []) if isinstance(res, dict) else (res if isinstance(res, list) else [])
        test("21. Admin Email Notification Logs (/api/admin/email-logs)", code == 200 and len(logs) > 0, f"Logs count: {len(logs)}")

        if logs:
            first_log_id = logs[0]["id"]
            code, res = request("POST", f"/api/admin/email-logs/{first_log_id}/retry", token=admin_token)
            test("22. Admin 1-Click Email Retry (/api/admin/email-logs/{id}/retry)", code == 200, f"Res: {res}")

    # 17. Public Marketplace Stats
    code, res = request("GET", "/api/stats")
    test("23. Public Marketplace Stats (100% Genuine Data)", code == 200 and "total_projects" in res and res.get("total_projects") == 90, f"Stats: {res}")

    print("=" * 70)
    print(f"TEST RESULTS: {passed} / {total} PASSED")
    print("=" * 70)
    if passed == total:
        print("ALL 23 CRITICAL PRODUCTION WORKFLOWS VERIFIED SUCCESSFULLY!")
    else:
        print(f"WARNING: {total - passed} tests failed.")

if __name__ == "__main__":
    run_tests()
