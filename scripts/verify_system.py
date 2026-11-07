import urllib.request
import json

BASE_URL = "http://127.0.0.1:8000"

def get(url, token=None):
    req = urllib.request.Request(f"{BASE_URL}{url}")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())

def post(url, payload, token=None):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(f"{BASE_URL}{url}", data=data, method="POST")
    req.add_header("Content-Type", "application/json")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())

def run_tests():
    print("=== PROJECTVERSE SYSTEM VERIFICATION ===")

    # 1. Stats and Demo Mode
    stats = get("/api/stats")
    print(f"[OK] Total Projects: {stats.get('total_projects')}")
    print(f"[OK] Total Students (Demo ON): {stats.get('total_students')}")
    print(f"[OK] Badge Text: {stats.get('badge_text')}")
    assert stats.get('total_projects') == 90, f"Expected 90 projects, got {stats.get('total_projects')}"

    # 2. Sections
    sections = get("/api/projects/sections")
    print(f"[OK] Featured Projects: {len(sections.get('featured', []))}")
    print(f"[OK] Trending Projects: {len(sections.get('trending', []))}")
    print(f"[OK] Mentors List: {len(sections.get('mentors', []))}")
    assert len(sections.get('mentors', [])) >= 6

    # 3. All 90 Projects
    projects_data = get("/api/projects?limit=150")
    projs = projects_data.get("projects", [])
    print(f"[OK] Catalogue fetched: {len(projs)} projects")
    assert len(projs) == 90, f"Expected 90 projects, got {len(projs)}"

    # Check breakdown by category
    counts = {}
    for p in projs:
        lvl = p.get("academic_level")
        counts[lvl] = counts.get(lvl, 0) + 1
    print(f"[OK] Categories breakdown: {counts}")
    assert counts.get("BCA") == 15
    assert counts.get("B.Com") == 10
    assert counts.get("B.Tech") == 25
    assert counts.get("MCA") == 15
    assert counts.get("M.Tech") == 15
    assert counts.get("IIT-Level / Research-Grade") == 10

    # 4. Project Details for each category (testing all 9 tabs content)
    samples = ["BCA001", "BCOM001", "BTECH001", "MCA001", "MTECH001", "IIT001"]
    for code in samples:
        detail = get(f"/api/projects/{code}")
        print(f"[OK] Details for {code}: {detail.get('title')}")
        print(f"     Stream: {detail.get('academic_level')} | Price: Rs {detail.get('price')}")
        print(f"     Modules: {len(detail.get('core_modules', []))} | Resources: {len(detail.get('resources', []))}")
        assert detail.get("price") >= 799, "Price rule violated!"
        assert len(detail.get("resources", [])) == 6, "Expected 6 academic deliverables!"
        assert detail.get("dfd_description"), "Missing DFD description"
        assert detail.get("uml_description"), "Missing UML description"

    # 5. Auth: Login as Admin
    admin_login = post("/api/auth/login", {
        "email": "admin@projectverse.com",
        "password": "Admin@12345"
    })
    admin_token = admin_login.get("token")
    print(f"[OK] Admin logged in: {admin_login.get('user', {}).get('full_name')} (Role: {admin_login.get('user', {}).get('role')})")

    # 6. Admin Telemetry & Settings
    adm_stats = get("/api/admin/stats", token=admin_token)
    print(f"[OK] Admin Stats -> Projects: {adm_stats.get('total_projects')}, Demo Students: {adm_stats.get('demo_students_count')}, Genuine Students: {adm_stats.get('genuine_students_count')}")

    # 7. Test Demo Mode Toggle (OFF -> ON)
    print("\n--- Testing Demo Mode Toggle ---")
    post("/api/admin/settings", {"demo_mode": 0}, token=admin_token)
    stats_off = get("/api/stats")
    print(f"[OK] Demo OFF -> Students count: {stats_off.get('total_students')} | Badge: {stats_off.get('badge_text')}")
    assert stats_off.get('badge_text') == "Verified Platform Statistics"

    post("/api/admin/settings", {"demo_mode": 1}, token=admin_token)
    stats_on = get("/api/stats")
    print(f"[OK] Demo ON -> Students count: {stats_on.get('total_students')} | Badge: {stats_on.get('badge_text')}")
    assert stats_on.get('badge_text') == "Illustrative Demo Statistics"

    # 8. Student Registration & Capstone Enrollment Request
    print("\n--- Testing Student Registration & Capstone Enrollment ---")
    test_email = "tester_student_verification@projectverse.com"
    try:
        student_reg = post("/api/auth/register", {
            "full_name": "Test Candidate",
            "email": test_email,
            "mobile": "9876543219",
            "college": "National Institute of Engineering",
            "university": "Visvesvaraya Technological University",
            "course": "B.Tech",
            "academic_year": "Final Year",
            "specialization": "Artificial Intelligence",
            "preferred_tech": "Python, PyTorch",
            "team_mode": "Team",
            "password": "Password@123"
        })
        student_token = student_reg.get("token")
        print(f"[OK] Student registered: {student_reg.get('user', {}).get('full_name')}")
    except Exception:
        # If already registered, login
        student_login = post("/api/auth/login", {
            "email": test_email,
            "password": "Password@123"
        })
        student_token = student_login.get("token")
        print(f"[OK] Student logged in: {student_login.get('user', {}).get('full_name')}")

    # Student requests enrollment for BTECH001 dynamically
    btech_proj = get("/api/projects/BTECH001")
    enroll_req = post("/api/student/enroll-request", {
        "project_id": btech_proj["id"],
        "team_mode": "Team",
        "team_members": "Test Candidate (Leader), Rahul Nair (Member)",
        "remarks": "Major project for semester 8 AI lab evaluation."
    }, token=student_token)
    print(f"[OK] Student Enrollment Request submitted: {enroll_req.get('message')}")

    # Check Student Dashboard
    dash = get("/api/student/dashboard", token=student_token)
    print(f"[OK] Student Dashboard -> Enrolled Projects: {len(dash.get('enrolled_projects', []))}")
    assert len(dash.get('enrolled_projects', [])) >= 1

    # Student Support Ticket
    ticket_res = post("/api/support/ticket", {
        "subject": "Need CUDA environment setup details",
        "category": "Technical Code Setup",
        "message": "Does BTECH001 require CUDA 12.1 or is CPU fallback supported?"
    }, token=student_token)
    print(f"[OK] Support ticket raised: {ticket_res.get('message')}")

    print("\n=== ALL SYSTEM VERIFICATION CHECKS PASSED SUCCESSFULLY! ===")

if __name__ == "__main__":
    run_tests()
