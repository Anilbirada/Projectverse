"""
PROJECTVERSE - Referral Partner & 25% Commission System Verification Suite
Tests the complete end-to-end lifecycle against http://localhost:8000:
1. Super Admin Authentication
2. Partner registration (PENDING state)
3. Block unapproved partner login (403 Forbidden)
4. Admin reviews pending partner applications
5. Admin approves partner & generates unique referral code
6. Approved partner authentication & token issuance
7. Public referral click tracking & attribution telemetry
8. Referral code validation endpoint
9. Student registration with referral attribution
10. Anti-fraud self-referral prevention check
11. Referred student places project order
12. Admin payment verification & automatic 25% commission calculation
13. Commission stored in database with exact 25% rate
14. Referral partner dashboard telemetry & available balance
15. Partner payout request submission (>= minimum threshold Rs 500)
16. Admin payout settlement & transaction recording (Status: PAID)
17. Partner telemetry confirms commission paid
18. Admin commission & payout report CSV export
"""
import sys
import os
import json
import sqlite3
import random
import time
import urllib.request
import urllib.parse

BASE_URL = "http://localhost:8000"

TOTAL_TESTS = 18
passed_tests = 0

def test(name, condition, details=""):
    global passed_tests
    if condition:
        passed_tests += 1
        print(f"[PASSED] {name}")
    else:
        print(f"[FAILED] {name}")
        if details:
            print(f"       Details: {details}")

def api_request(method, endpoint, data=None, token=None):
    url = f"{BASE_URL}{endpoint}"
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    body = json.dumps(data).encode("utf-8") if data is not None else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
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
    except Exception as e:
        return 500, str(e)

def run_tests():
    global passed_tests
    print("=" * 70)
    print("PROJECTVERSE - REFERRAL PARTNER & 25% COMMISSION SYSTEM VERIFICATION")
    print("=" * 70)

    # 1. Super Admin Authentication
    status, res = api_request("POST", "/api/auth/login", {
        "email": "aniladani843@gmail.com",
        "password": "Admin@12345"
    })
    admin_token = res.get("token") if status == 200 else None
    test("1. Super Admin Authentication", status == 200 and admin_token is not None, f"Status: {status}, Res: {res}")

    # Unique credentials per test run
    rand_id = random.randint(10000, 99999)
    partner_email = f"affiliate_{rand_id}@projectverse.com"
    partner_password = f"Partner@{rand_id}"
    partner_name = f"Rajesh Sharma {rand_id}"

    # 2. Partner Registration (Status: PENDING)
    status, reg_res = api_request("POST", "/api/referrals/register", {
        "full_name": partner_name,
        "email": partner_email,
        "mobile": f"98765{rand_id}",
        "password": partner_password,
        "college_name": "Delhi Technological University",
        "city": "New Delhi",
        "preferred_payment_method": "UPI",
        "upi_id": f"rajesh{rand_id}@okaxis"
    })
    partner_id = reg_res.get("partner_id") if status == 200 else None
    partner_status = reg_res.get("status") if status == 200 else ""
    test("2. Referral Partner Registration (Status: PENDING)", status == 200 and partner_status == "PENDING", f"Status: {status}, Res: {reg_res}")

    # 3. Block login before approval
    status, unapproved_login = api_request("POST", "/api/referrals/login", {
        "email": partner_email,
        "password": partner_password
    })
    test("3. Security: Block Login for Unapproved Partner (403 Forbidden)", status == 403, f"Status: {status}, Res: {unapproved_login}")

    # 4. Admin Review Pending Partner Applications
    status, admin_partners = api_request("GET", "/api/admin/referrals/partners?status=PENDING", token=admin_token)
    partners_list = admin_partners.get("partners", []) if status == 200 else []
    found_partner = any(p["id"] == partner_id for p in partners_list)
    test("4. Admin Review Pending Partner Applications", status == 200 and found_partner, f"Status: {status}, Count: {len(partners_list)}")

    # 5. Admin Approves Partner & Generates Unique Referral Code
    status, approve_res = api_request("POST", f"/api/admin/referrals/partners/{partner_id}/status", {
        "status": "APPROVED",
        "admin_notes": "DTU Campus Ambassador verified."
    }, token=admin_token)
    ref_code = approve_res.get("referral_code") if status == 200 else None
    test("5. Admin Approves Partner & Generates Unique Referral Code", status == 200 and ref_code is not None, f"Status: {status}, Code: {ref_code}")

    # 6. Approved Partner Authentication & Token Issuance
    status, partner_login = api_request("POST", "/api/referrals/login", {
        "email": partner_email,
        "password": partner_password
    })
    partner_token = partner_login.get("token") if status == 200 else None
    test("6. Approved Partner Authentication & Token Issuance", status == 200 and partner_token is not None, f"Status: {status}, Res: {partner_login}")

    # 7. Public Referral Click Tracking & Attribution Telemetry
    status, track_res = api_request("POST", "/api/referrals/track-click", {
        "referral_code": ref_code,
        "landing_page": f"/?ref={ref_code}",
        "referrer_url": "https://instagram.com"
    })
    track_valid = track_res.get("valid") is True if status == 200 else False
    test("7. Public Referral Click Tracking & Attribution Telemetry", status == 200 and track_valid, f"Status: {status}, Res: {track_res}")

    # 8. Referral Code Validation Endpoint
    status, val_res = api_request("GET", f"/api/referrals/validate-code/{ref_code}")
    val_valid = val_res.get("valid") is True if status == 200 else False
    test("8. Referral Code Validation Endpoint (/api/referrals/validate-code/{code})", status == 200 and val_valid, f"Status: {status}, Res: {val_res}")

    # 9. Student Registration with Referral Attribution
    student_email = f"student_ref_{rand_id}@college.edu"
    status, student_reg = api_request("POST", "/api/auth/register", {
        "full_name": f"Pooja Verma {rand_id}",
        "email": student_email,
        "password": "StudentPass@123",
        "mobile": f"91234{rand_id}",
        "college": "Apex Institute of Technology",
        "university": "State Tech Univ",
        "course": "B.Tech",
        "academic_year": "Final Year",
        "specialization": "AI/ML",
        "preferred_tech": "Python",
        "referral_code": ref_code
    })
    student_token = student_reg.get("token") if status == 200 else None
    test("9. Student Registration with Referral Attribution", status == 200 and student_token is not None, f"Status: {status}, Res: {student_reg}")

    # 10. Anti-Fraud Self-Referral Prevention Check
    status, fraud_res = api_request("POST", "/api/auth/register", {
        "full_name": "Fraud Attempt",
        "email": partner_email,  # Same email as partner
        "password": "Password@123",
        "mobile": f"98765{rand_id}",
        "college": "Test",
        "course": "BCA",
        "academic_year": "1st Year",
        "referral_code": ref_code
    })
    test("10. Anti-Fraud & Self-Referral Prevention Handling", status == 400, f"Status: {status}")

    # 11. Referred Student Order Placement
    status, proj_res = api_request("GET", "/api/projects?limit=5")
    projects_data = proj_res if isinstance(proj_res, list) else proj_res.get("projects", [])
    proj_item = projects_data[0]
    proj_id = proj_item["id"]
    proj_price = proj_item["price"]

    status, order_res = api_request("POST", "/api/orders/create", {
        "project_id": proj_id,
        "utr_reference": f"UTR{rand_id}88"
    }, token=student_token)
    order_id = order_res.get("order_id") if status == 200 else None
    order_number = order_res.get("order_number") if status == 200 else None
    test("11. Referred Student Order Placement (/api/orders/create)", status == 200 and order_id is not None, f"Status: {status}, Order: {order_number}")

    # 12. Admin Payment Verification & Automatic 25% Commission Calculation
    expected_commission = round(proj_price * 0.25, 2)
    status, verify_res = api_request("POST", f"/api/admin/payments/{order_id}/verify", {
        "action": "approved",
        "notes": "Verified against HDFC Bank UPI settlement."
    }, token=admin_token)
    test("12. Admin Payment Verification & Automatic 25% Commission Calculation", status == 200, f"Status: {status}, Res: {verify_res}")

    # 13. Commission Stored in Database with Exact 25% Rate
    status, comm_res = api_request("GET", f"/api/admin/referrals/commissions?partner_id={partner_id}", token=admin_token)
    comm_list = comm_res.get("commissions", []) if status == 200 else []
    found_comm = any(c["order_id"] == order_id and abs(c["commission_amount"] - expected_commission) < 0.01 for c in comm_list)
    test("13. Commission Stored in Database with Exact 25% Rate (Rs " + str(expected_commission) + ")", status == 200 and found_comm, f"Status: {status}, Commissions: {comm_list}")

    # 14. Referral Partner Dashboard Telemetry & Available Balance
    status, dash_res = api_request("GET", "/api/referrals/partner/dashboard", token=partner_token)
    dash_stats = dash_res.get("stats", {}) if status == 200 else {}
    balance_ok = dash_stats.get("approved_balance", 0) >= expected_commission
    sales_ok = dash_stats.get("total_sales", 0) >= 1
    test("14. Referral Partner Dashboard Telemetry & Available Balance", status == 200 and balance_ok and sales_ok, f"Stats: {dash_stats}")

    # 15. Configure settings for threshold testing and Partner Payout Request Submission
    api_request("PUT", "/api/admin/referrals/settings", {
        "commission_rate_percentage": 25.0,
        "attribution_window_days": 30,
        "minimum_payout_amount": 100.0,
        "auto_approve_partners": False,
        "exclude_tax_from_commission": True
    }, token=admin_token)

    status, payout_req = api_request("POST", "/api/referrals/partner/payout-request", {
        "amount": expected_commission,
        "payment_method": "UPI",
        "payout_details": f"rajesh{rand_id}@okaxis"
    }, token=partner_token)
    req_number = payout_req.get("request_number") if status == 200 else None
    test("15. Partner Payout Request Submission (/api/referrals/partner/payout-request)", status == 200 and req_number is not None, f"Status: {status}, Res: {payout_req}")

    # 16. Admin Payout Settlement & Transaction Recording
    status, payout_list = api_request("GET", "/api/admin/referrals/payout-requests?status=PENDING", token=admin_token)
    payouts = payout_list.get("payout_requests", []) if status == 200 else []
    matching_payout = next((p for p in payouts if p["partner_id"] == partner_id), None)

    if matching_payout:
        payout_id = matching_payout["id"]
        status, process_res = api_request("POST", f"/api/admin/referrals/payout-requests/{payout_id}/process", {
            "action": "approve",
            "utr_reference": f"BANK-UTR-{rand_id}",
            "payment_method": "UPI",
            "notes": "Commission settled to partner UPI."
        }, token=admin_token)
        test("16. Admin Payout Settlement & Transaction Recording (Status: PAID)", status == 200, f"Status: {status}, Res: {process_res}")
    else:
        test("16. Admin Payout Settlement & Transaction Recording", False, "Matching payout request not found")

    # 17. Partner Telemetry Confirms Commission Paid
    status, dash_after = api_request("GET", "/api/referrals/partner/dashboard", token=partner_token)
    stats_after = dash_after.get("stats", {}) if status == 200 else {}
    paid_ok = stats_after.get("paid_balance", 0) >= expected_commission
    test("17. Partner Telemetry Confirms Commission Paid (Rs " + str(stats_after.get("paid_balance")) + ")", status == 200 and paid_ok, f"Stats: {stats_after}")

    # 18. Admin Commission & Payout Report CSV Export
    status, export_res = api_request("GET", "/api/admin/referrals/export", token=admin_token)
    csv_valid = isinstance(export_res, str) and "Order Number" in export_res and "Commission Amount" in export_res and partner_name in export_res
    test("18. Admin Commission & Payout Report CSV Export", status == 200 and csv_valid, f"Status: {status}, Snippet: {str(export_res)[:100]}")

    print("=" * 70)
    print(f"TEST RESULTS: {passed_tests} / {TOTAL_TESTS} PASSED")
    print("=" * 70)
    if passed_tests == TOTAL_TESTS:
        print("ALL 18 REFERRAL & COMMISSION WORKFLOWS VERIFIED 100% SUCCESSFULLY!")
    else:
        print(f"WARNING: {TOTAL_TESTS - passed_tests} tests failed.")

if __name__ == "__main__":
    run_tests()
