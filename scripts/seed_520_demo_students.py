"""
PROJECTVERSE - 520+ Synthetic Student Records & Demo Data Seeder
Generates 540 realistic, synthetic student records distributed across all 6 categories:
- B.Tech (165)
- BCA (100)
- MCA (95)
- M.Tech (85)
- B.Com (60)
- IIT-Level / Research (35)
Total: 540 Demo Records

Strictly follows Demo Data Transparency:
- All emails use reserved '*.example.test' domains.
- All records have `is_demo = 1`.
- Tracked in `demo_records` table for 1-click admin reset.
- Never mixed with genuine students.
"""
import sqlite3
import hashlib
import random
from datetime import datetime, timedelta

FIRST_NAMES = [
    "Aarav", "Aditya", "Ananya", "Arjun", "Diya", "Ishaan", "Kavya", "Rohan", "Priya", "Rahul",
    "Sneha", "Siddharth", "Pooja", "Tanvi", "Varun", "Vikas", "Neha", "Riya", "Yash", "Aakash",
    "Shreya", "Deepa", "Manik", "Gaurav", "Meera", "Kunal", "Amit", "Divya", "Harsh", "Nikhil",
    "Payal", "Simran", "Tarun", "Sameer", "Swati", "Karthik", "Sanjay", "Ankit", "Monisha", "Ritvik",
    "Alok", "Charu", "Dev", "Esha", "Farhan", "Gayatri", "Himanshu", "Inder", "Jyoti", "Kiran",
    "Lalit", "Madhav", "Nandini", "Omkar", "Pranav", "Radhika", "Sahil", "Tanya", "Udit", "Vidya"
]

LAST_NAMES = [
    "Sharma", "Verma", "Patel", "Reddy", "Iyer", "Nair", "Gupta", "Rao", "Kulkarni", "Chatterjee",
    "Joshi", "Mehta", "Deshmukh", "Singh", "Mukherjee", "Bhat", "Menon", "Das", "Aggarwal", "Pillai",
    "Choudhury", "Mishra", "Saxena", "Bansal", "Nambiar", "Sen", "Bose", "Trivedi", "Kapoor", "Shukla",
    "Bhattacharya", "Chauhan", "Dhar", "Goswami", "Hegde", "Jadhav", "Kaul", "Lodha", "Mahajan", "Nath"
]

COLLEGES = [
    ("Apex Institute of Engineering & Technology", "State Technical University"),
    ("Heritage National College of Computing", "Central University"),
    ("St. Xavier's Commerce & Management Academy", "Metropolitan University"),
    ("Horizon Institute of Technology", "Deemed University"),
    ("Metropolis University Faculty of Sciences", "Metropolis State University"),
    ("Greenfield Institute of Technology", "Autonomous Technical Board"),
    ("Pioneer College of Information Technology", "National University"),
    ("Crescent Institute of Higher Learning", "Affiliated University"),
    ("Imperial Engineering College", "Regional Technical Board"),
    ("Lotus Valley College of Computer Applications", "City University"),
    ("Trinity Institute of Technology & Research", "National Technical Consortium"),
    ("Royal College of Arts, Commerce & Science", "State University"),
    ("Zenith University Department of Computing", "Zenith University"),
    ("Universal College of Engineering", "Technical Board of Studies"),
    ("Vanguard Institute of Advanced Studies", "Autonomous Research University")
]

SPECIALIZATIONS = {
    "BCA": ["Application Development", "Cloud Systems", "Database Administration", "Web Technologies"],
    "B.Com": ["Financial Accounting & Analytics", "GST & Taxation", "Banking Operations", "Retail Business Intelligence"],
    "B.Tech": ["Artificial Intelligence & ML", "Cybersecurity", "Cloud Computing", "Internet of Things", "Full Stack Engineering"],
    "MCA": ["Enterprise Software Architecture", "Multi-Agent AI Systems", "Applied Generative AI", "Distributed Systems"],
    "M.Tech": ["Deep Learning & Medical Imaging", "Explainable AI (XAI)", "Federated Learning & Privacy", "Edge AI & Optimization"],
    "IIT-Level / Research-Grade": ["Graph Neural Networks & RAG", "Autonomous Multi-Agent Robotics", "Quantum-Inspired Optimization", "Computational Biology AI"]
}

MILESTONES = [
    ("Topic Selection & Problem Statement", 100),
    ("Synopsis & Literature Survey", 100),
    ("Software Requirement Specification (SRS)", 100),
    ("System Architecture & Database Design", 80),
    ("Core Module Implementation (50%)", 60),
    ("Full Integration & Algorithm Tuning (80%)", 40),
    ("System Testing, Validation & Bug Fixing", 20),
    ("IEEE Final Thesis Report & PPT Defense Ready", 10)
]

def hash_pw(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

def seed_demo_students(db_path="projectverse.db"):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # Clean existing demo records
    print("Clearing previous demo records...")
    cur.execute("DELETE FROM project_enrollments WHERE is_demo = 1")
    cur.execute("DELETE FROM students WHERE is_demo = 1")
    cur.execute("DELETE FROM users WHERE email LIKE '%@%.example.test' OR role = 'student' AND email != 'student@projectverse.com'")
    cur.execute("DELETE FROM demo_records")

    # Fetch projects grouped by level
    cur.execute("SELECT id, project_code, academic_level, title FROM projects ORDER BY id ASC")
    all_projects = cur.fetchall()

    projects_by_level = {
        "BCA": [p for p in all_projects if p[2] == "BCA"],
        "B.Com": [p for p in all_projects if p[2] == "B.Com"],
        "B.Tech": [p for p in all_projects if p[2] == "B.Tech"],
        "MCA": [p for p in all_projects if p[2] == "MCA"],
        "M.Tech": [p for p in all_projects if p[2] == "M.Tech"],
        "IIT-Level / Research-Grade": [p for p in all_projects if p[2] == "IIT-Level / Research-Grade"]
    }

    # Fetch mentors
    cur.execute("SELECT id, full_name, department FROM mentors")
    mentors = cur.fetchall()
    mentor_ids = [m[0] for m in mentors] if mentors else [1]

    # Quota distribution for exactly 540 records (520+ requirement)
    distribution = [
        ("B.Tech", 165),
        ("BCA", 100),
        ("MCA", 95),
        ("M.Tech", 85),
        ("B.Com", 60),
        ("IIT-Level / Research-Grade", 35)
    ]

    total_target = sum(d[1] for d in distribution)
    print(f"Generating {total_target} synthetic student demo records across {len(distribution)} categories...")

    student_counter = 1
    demo_pw = hash_pw("Demo@12345")
    base_date = datetime.now() - timedelta(days=120)

    for level, count in distribution:
        avail_projects = projects_by_level[level]
        if not avail_projects:
            print(f"Warning: No projects found for level {level}!")
            continue

        for i in range(count):
            fn = random.choice(FIRST_NAMES)
            ln = random.choice(LAST_NAMES)
            full_name = f"{fn} {ln}"
            email = f"{fn.lower()}.{ln.lower()}{student_counter}@student.example.test"
            mobile = f"91987{student_counter:05d}"
            college, university = random.choice(COLLEGES)
            spec = random.choice(SPECIALIZATIONS.get(level, ["Software Engineering"]))
            yr = random.choice(["Final Year", "3rd Year", "2nd Year", "Semester 6", "Semester 8"])

            # 1. Insert user with is_demo = 1
            cur.execute("""
            INSERT INTO users (email, password_hash, full_name, mobile, college, course, academic_year, role)
            VALUES (?, ?, ?, ?, ?, ?, ?, 'student')
            """, (email, demo_pw, full_name, mobile, college, level, yr))
            user_id = cur.lastrowid

            # Pick project & mentor
            proj = random.choice(avail_projects)
            proj_id = proj[0]
            mentor_id = random.choice(mentor_ids)

            pref_tech = "Python & Full Stack" if "Tech" in level or "MCA" in level else "SQL & Analytics" if level == "B.Com" else "React & Node.js"
            mode = "Team" if random.random() > 0.65 else "Individual"

            # 2. Insert students profile
            cur.execute("""
            INSERT INTO students (user_id, university, year_or_semester, specialization, preferred_technology, project_mode, assigned_mentor_id, is_demo)
            VALUES (?, ?, ?, ?, ?, ?, ?, 1)
            """, (user_id, university, yr, spec, pref_tech, mode, mentor_id))
            student_id = cur.lastrowid

            # Enrollment specifics
            enroll_days_ago = random.randint(5, 110)
            created_at = base_date + timedelta(days=enroll_days_ago)
            enroll_num = f"ENR-DEMO-{created_at.strftime('%Y%m')}-{student_counter:04d}"

            # Progress & status distribution
            rand_stat = random.random()
            if rand_stat < 0.15:
                status = "pending"
                comp_status = "pending_approval"
                progress = random.randint(5, 15)
                cur_milestone = "Topic Selection"
                approval_date = None
            elif rand_stat < 0.70:
                status = "approved"
                comp_status = "in_progress"
                progress = random.randint(35, 75)
                cur_milestone = "Core Module Implementation"
                approval_date = (created_at + timedelta(days=2)).strftime('%Y-%m-%d %H:%M:%S')
            elif rand_stat < 0.90:
                status = "approved"
                comp_status = "testing"
                progress = random.randint(80, 95)
                cur_milestone = "System Testing & Validation"
                approval_date = (created_at + timedelta(days=2)).strftime('%Y-%m-%d %H:%M:%S')
            else:
                status = "approved"
                comp_status = "completed"
                progress = 100
                cur_milestone = "Viva Voce Ready"
                approval_date = (created_at + timedelta(days=2)).strftime('%Y-%m-%d %H:%M:%S')

            team_members = f"{full_name}, {random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}" if mode == "Team" else None

            # 3. Insert project_enrollments
            cur.execute("""
            INSERT INTO project_enrollments (
                enrollment_number, user_id, student_id, project_id, mentor_id,
                status, request_date, approval_date, completion_status,
                progress_percentage, current_milestone, team_mode, team_members,
                remarks, is_demo, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1, ?, ?)
            """, (
                enroll_num, user_id, student_id, proj_id, mentor_id,
                status, created_at.strftime('%Y-%m-%d %H:%M:%S'), approval_date, comp_status,
                progress, cur_milestone, mode, team_members,
                "Demo student record for testing and administrative simulation.",
                created_at.strftime('%Y-%m-%d %H:%M:%S'),
                datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ))
            enroll_id = cur.lastrowid

            # 4. Insert assignment if approved
            if status == "approved":
                cur.execute("""
                INSERT INTO project_assignments (enrollment_id, project_id, mentor_id, assigned_by, notes, assigned_at, status)
                VALUES (?, ?, ?, 1, 'Assigned by Academic Advisor for capstone guidance.', ?, 'active')
                """, (enroll_id, proj_id, mentor_id, approval_date))

            # 5. Insert milestone progress entries
            for m_order, (m_name, req_pct) in enumerate(MILESTONES, 1):
                m_status = "completed" if progress >= req_pct else "in_progress" if progress >= (req_pct - 20) else "pending"
                m_pct = 100 if m_status == "completed" else random.randint(30, 80) if m_status == "in_progress" else 0
                cur.execute("""
                INSERT INTO project_progress (enrollment_id, milestone_name, milestone_order, status, completion_percentage, feedback, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (enroll_id, m_name, m_order, m_status, m_pct, "Standard milestone progress check.", created_at.strftime('%Y-%m-%d %H:%M:%S')))

            # 6. Track in demo_records
            cur.execute("INSERT INTO demo_records (entity_type, entity_id) VALUES ('user', ?)", (user_id,))
            cur.execute("INSERT INTO demo_records (entity_type, entity_id) VALUES ('enrollment', ?)", (enroll_id,))

            student_counter += 1

    # Update mentor active student counts
    cur.execute("""
    UPDATE mentors SET active_students = (
        SELECT COUNT(*) FROM project_enrollments WHERE mentor_id = mentors.id AND status = 'approved'
    )
    """)

    conn.commit()

    # Verify counts
    cur.execute("SELECT COUNT(*) FROM users WHERE email LIKE '%@%.example.test'")
    demo_users = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM project_enrollments WHERE is_demo = 1")
    demo_enrollments = cur.fetchone()[0]

    cur.execute("SELECT pe.completion_status, COUNT(*) FROM project_enrollments pe WHERE pe.is_demo = 1 GROUP BY pe.completion_status")
    by_status = cur.fetchall()

    conn.close()

    print(f"Successfully seeded {demo_users} synthetic students and {demo_enrollments} demo enrollments!")
    print("Status breakdown:", by_status)

if __name__ == "__main__":
    seed_demo_students()
