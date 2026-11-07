# PROJECTVERSE
### Enterprise Academic Project Marketplace & Learning Platform
**Tagline:** *Ideas Into Innovation — Explore. Learn. Build. Deploy.*  
**Production Version:** `4.0.0 (Production Release)`  
**Repository:** [https://github.com/Anilbirada/Projectverse](https://github.com/Anilbirada/Projectverse)

---

## 1. Problem Statement: The Academic Project Crisis

Every academic year, over **1.5 million engineering, computer applications, and commerce students** across BCA, B.Com, B.Tech, MCA, and M.Tech programs face significant obstacles when submitting capstone projects:

1. **Non-Functional & Outdated Code:** Most projects sourced from online repositories or local vendors contain deprecated dependencies, unhandled runtime exceptions, and lack database schemas.
2. **Missing Academic Deliverables:** Colleges and universities require strictly formatted deliverables—including IEEE format project reports, System Requirement Specifications (SRS), database entity diagrams, viva-voce questionnaires, and PowerPoint presentations. Standard code repositories provide none of these.
3. **Predatory Middlemen & Zero Transparency:** Traditional project brokers charge students inflated fees without providing verifiable source code, technical guidance, or payment receipts.
4. **Lack of Mentorship & Progress Visibility:** Students working on team or individual capstone projects have no structured way to track milestones (e.g. 25% architecture, 50% backend, 75% testing, 100% viva defense) or receive technical guidance from verified mentors.

---

## 2. The Enterprise Solution: PROJECTVERSE

**PROJECTVERSE** is a commercial academic project marketplace and development platform designed to bridge the gap between academic requirements and enterprise software development.

### Business & Commercial Model
- **90 Production-Ready Academic Projects:** Fully implemented across 6 distinct academic streams with a minimum price rule starting at **₹799**.
- **Complete Project Kits:** Every project includes full source code, IEEE-compliant documentation, SQL schemas, PPT slides, SRS, and viva questions.
- **Instant Project Enquiry System:** Direct customer lead generation capturing student academic details, university, course, and technical requirements.
- **Direct WhatsApp Hotline Integration:** Real-time pre-filled WhatsApp consultation linked to the official support hotline (`+91 8431712924`).
- **Verified Direct UPI Payment Workflow:** Direct bank payments to the official UPI VPA (`8431712924-3@ybl`, Payee: `ANIL`) with 12-digit UTR tracking and manual/automated bank settlement verification.
- **Automated 18% GST Tax Invoices:** Generates verifiable, computer-generated Tax Invoices (`INV-YYYYMMDD-XXXX`) calculating CGST (9%) and SGST (9%) with a printable layout.
- **Automated Business Alerts:** Immediate notification dispatch and database auditing for every enquiry, request, registration, and order sent directly to the business owner (`aniladani843@gmail.com`).
- **Capstone Mentorship Management:** Custom project request portal where students submit custom problem statements, receive official quotations, get paired with mentors, and track progress milestones in real time.

---

## 3. Catalogue Architecture: Exactly 90 Projects

The marketplace catalogue provides exactly 90 academic projects distributed across 6 categories:

| Category | Stream / Discipline | Project Count | Scope & Focus |
|:---|:---|:---:|:---|
| **BCA** | Bachelor of Computer Applications | **15** | Full-stack web portals, attendance, hospital, library, inventory & student systems |
| **B.Com** | Commerce, Finance & Analytics | **10** | Business sales analytics, GST billing, financial risk, retail dashboards, banking metrics |
| **B.Tech** | Computer Science & Engineering | **25** | AI/ML, computer vision, IoT smart agriculture, blockchain voting, network security |
| **MCA** | Master of Computer Applications | **15** | Cloud microservices, distributed workflows, AI healthcare, automated HR portals |
| **M.Tech** | Postgraduate Engineering Research | **15** | Deep learning, federated learning, NLP Transformers, autonomous drones, smart grid IoT |
| **IIT-Grade** | Research & Publication Grade | **10** | Quantum cryptography, real-time edge AI, biomedical signal processing, zero-knowledge proofs |
| **TOTAL** | **Enterprise Academic Portfolio** | **90** | **100% Database-Backed & Verified** |

### Standard Deliverables with Every Project
Each purchased project includes:
1. **Source Code Package (ZIP):** Clean, modular, fully commented source code adhering to PEP 8 / Clean Code standards.
2. **IEEE Formatted Project Report (.docx / .pdf):** 60–120 page comprehensive documentation with Literature Survey, System Architecture, UML Diagrams, Test Cases, and Results.
3. **Database Schema (.sql / .db):** Normalized relational tables, foreign key constraints, indexes, and sample seed records.
4. **Presentation Slides (.pptx):** 20–30 slide deck prepared for project defense before university evaluation committees.
5. **System Requirement Specification (SRS):** IEEE 830 compliant software requirements document.
6. **Viva-Voce Q&A Guide:** Top 50 most frequently asked faculty questions with model answers.

---

## 4. Technical Architecture & Tech Stack

```
   ┌──────────────────────────────────────────────────────────────┐
   │                    BROWSER CLIENT (SPA)                      │
   │  HTML5 + Tailwind CSS + Vanilla ES6+ + Lucide Icons (Glass) │
   └──────────────────────────────┬───────────────────────────────┘
                                  │ JSON / REST / Multipart Form Data
                                  ▼
   ┌──────────────────────────────────────────────────────────────┐
   │                FASTAPI BACKEND SERVER (Python 3.12)          │
   │  • Rate Limiter & Security Headers                           │
   │  • Multi-Role RBAC (Super Admin, Mentor, Student)            │
   │  • Business Alerting Engine (email_service.py)               │
   │  • GST Invoice Generation Engine                             │
   └──────────────────────────────┬───────────────────────────────┘
                                  │ Parameterized Queries (WAL Concurrency)
                                  ▼
   ┌──────────────────────────────────────────────────────────────┐
   │             SQLITE 3 ENTERPRISE DATABASE (projectverse.db)   │
   │  • 18 Relational Tables with Foreign Keys & Indexes          │
   │  • PRAGMA journal_mode = WAL; PRAGMA busy_timeout = 30000;  │
   └──────────────────────────────────────────────────────────────┘
```

- **Frontend:** Pure Vanilla JavaScript (ES6+), Tailwind CSS, Lucide Icons. Zero heavyweight external JS framework dependencies for fast loading speeds.
- **Backend:** Python 3.12, FastAPI, ASGI Uvicorn server, Pydantic v2 data validation.
- **Database:** SQLite 3 in **Write-Ahead Logging (WAL)** mode with 30-second busy timeout locks to handle high concurrent read/write throughput without table locks.
- **Authentication & Security:** PBKDF2-SHA256 password hashing with salt, JWT token-based authentication, Role-Based Access Control (RBAC), and security audit logging.

---

## 5. Database Architecture & Credentials

The application uses an SQLite 3 relational database (`projectverse.db`).

### Master Tables
- `users`: Authentication records, email, password hash, role (`super_admin`, `admin`, `mentor`, `student`), mobile, college.
- `students`: Academic profiles (university, course, semester, specialization, preferred stack).
- `projects`: Catalogue master (project code, title, category, description, price, tags, deliverables).
- `project_enquiries`: Genuine customer enquiries (`ENQ-YYYYMMDD-XXXX`) with college, stack, requirements.
- `project_requests`: Custom capstone requests (`REQ-YYYYMMDD-XXXX`), status, quotation, assigned mentor, milestone progress.
- `orders`: Purchase orders (`ORD-YYYYMMDD-XXXX`), pricing, payment status.
- `payments`: UPI transaction settlements, 12-digit UTR numbers, screenshot proofs, admin verification notes.
- `invoices`: 18% GST computer-generated tax invoices (`INV-YYYYMMDD-XXXX`).
- `notifications`: Admin notification centre records with read/unread tracking.
- `email_logs`: Transactional email dispatch telemetry with retry counters.
- `audit_logs`: Administrative operation security logs.

### Administrator & Business Credentials
- **Admin Panel URL:** `http://localhost:8000/#admin`
- **Super-Admin Email:** `aniladani843@gmail.com`
- **Super-Admin Password:** `Admin@12345`
- **Owner Notification Destination:** `aniladani843@gmail.com`
- **Official WhatsApp Hotline:** `+91 8431712924`
- **Official UPI VPA:** `8431712924-3@ybl` (Payee Name: `ANIL`)

---

## 6. Step-by-Step Installation & Run Guide

Follow these steps to set up and run PROJECTVERSE on your local machine or server.

### Prerequisites
- **Python 3.10, 3.11, or 3.12** installed on your system.
- **Git** installed on your system.

---

### Step 1: Clone the Repository
Open your terminal or command prompt and clone the repository:
```bash
git clone https://github.com/Anilbirada/Projectverse.git
cd Projectverse
```

---

### Step 2: Create and Activate a Virtual Environment

**On Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**On Windows (Command Prompt):**
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

**On Linux / macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

---

### Step 3: Install Required Dependencies
Install the required packages using `requirements.txt`:
```bash
pip install -r requirements.txt
```

---

### Step 4: Configure Environment Variables
Copy the example environment configuration to create your `.env` file:

**On Windows (PowerShell):**
```powershell
Copy-Item .env.example .env
```

**On Linux / macOS:**
```bash
cp .env.example .env
```

*(Optional: To enable live outgoing Gmail SMTP delivery, open `.env` and set your 16-character Google App Password under `SMTP_PASSWORD`.)*

---

### Step 5: Verify the Production Suite (23 / 23 Tests)
Run the automated end-to-end verification suite to ensure database connectivity, catalogue integrity, and business workflows:
```bash
python test_production_launch.py
```
*Expected Output: `ALL 23 CRITICAL PRODUCTION WORKFLOWS VERIFIED SUCCESSFULLY!`*

---

### Step 6: Start the Server

**Option A: Using Python directly**
```bash
python server.py
```

**Option B: Using Uvicorn directly (with auto-reload for development)**
```bash
uvicorn server:app --host 0.0.0.0 --port 8000 --reload
```

**Option C: On Windows using the batch launcher**
Double-click `start.bat` or run:
```cmd
start.bat
```

---

### Step 7: Open the Application in Your Browser
- **Public Marketplace Homepage:** [http://localhost:8000](http://localhost:8000)
- **Catalogue View (All 90 Projects):** [http://localhost:8000/#catalogue](http://localhost:8000/#catalogue)
- **Super-Admin Control Panel:** [http://localhost:8000/#admin](http://localhost:8000/#admin)  
  *(Log in with `aniladani843@gmail.com` / `Admin@12345`)*
- **Interactive REST API Documentation (Swagger UI):** [http://localhost:8000/docs](http://localhost:8000/docs)
- **Alternative API Documentation (Redoc):** [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 7. Production Deployment (Docker & Cloud)

### Option 1: Docker & Docker Compose (Recommended for Cloud Servers)
Run PROJECTVERSE inside isolated containers with persistent database storage:
```bash
# Build and start in detached mode
docker-compose up -d --build

# Inspect running container logs
docker-compose logs -f

# Stop container
docker-compose down
```

### Option 2: Linux Systemd Service (Ubuntu / Debian / RHEL)
Install the included systemd service unit file for 24/7 background operation:
```bash
sudo cp projectverse.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable projectverse
sudo systemctl start projectverse
sudo systemctl status projectverse
```

### Option 3: Automated Database Backup
Create point-in-time database snapshots with automated WAL checkpointing:
```bash
python backup_db.py
```
*Snapshots are saved to the `backups/` directory with UTC timestamps.*

---

## 8. REST API Endpoints Overview

| Method | Endpoint | Description | Access Level |
|:---|:---|:---|:---|
| `GET` | `/api/health` | System health check & project count | Public |
| `GET` | `/api/projects` | Fetch catalogue with search, stream, and price filters | Public |
| `GET` | `/api/projects/{id}` | Detailed project view with syllabus & deliverables | Public |
| `POST` | `/api/auth/register` | Register student account with academic profile | Public |
| `POST` | `/api/auth/login` | JWT authentication for students and administrators | Public |
| `POST` | `/api/enquiries/create` | Submit project enquiry with owner email dispatch | Public |
| `POST` | `/api/requests/create` | Submit custom capstone request | Authenticated Student |
| `POST` | `/api/orders/create` | Submit order with UPI payment reference (UTR) | Authenticated Student |
| `GET` | `/api/student/dashboard` | Student dashboard (enquiries, requests, orders, profile) | Authenticated Student |
| `GET` | `/api/invoices/{inv_number}` | View & print computer-generated 18% GST tax invoice | Authenticated Student / Admin |
| `GET` | `/api/admin/stats` | Telemetry metrics (revenue, enquiries, orders, students) | Super Admin |
| `POST` | `/api/admin/payments/{id}/verify` | Approve or reject UPI transaction settlements | Super Admin |
| `POST` | `/api/admin/orders/{id}/generate-invoice` | Generate official GST Tax Invoice | Super Admin |
| `POST` | `/api/admin/requests/{id}/progress` | Update capstone milestone progress (25%, 50%, 100%) | Super Admin / Mentor |
| `GET` | `/api/admin/email-logs` | Review email dispatch logs and error telemetry | Super Admin |
| `POST` | `/api/admin/email-logs/{id}/retry` | 1-click retry failed email transmissions | Super Admin |

---

## 9. Contact & Business Support

- **Platform Architect & Business Owner:** Anil Biradar
- **Official Email:** [aniladani843@gmail.com](mailto:aniladani843@gmail.com)
- **WhatsApp Support Hotline:** [+91 8431712924](https://wa.me/918431712924)
- **Official UPI VPA:** `8431712924-3@ybl` (Payee Name: `ANIL`)
- **Website:** [http://localhost:8000](http://localhost:8000)
- **GitHub Repository:** [https://github.com/Anilbirada/Projectverse](https://github.com/Anilbirada/Projectverse)

---
*© 2026 PROJECTVERSE. All Rights Reserved. Engineered for BCA, B.Com, B.Tech, MCA & M.Tech Academic Excellence.*
