"""
PROJECTVERSE - 90 Academic Projects Master Seeder
Seeds exactly 90 unique, high-quality academic projects across 6 categories:
1. BCA (15 projects)
2. B.Com (10 projects)
3. B.Tech (25 projects)
4. MCA (15 projects)
5. M.Tech (15 projects)
6. IIT-Level / Research-Grade (10 projects)

Total: 90 Projects
Includes comprehensive technical architecture, DFD descriptions, UML descriptions,
ER schemas, real-world applications, testing suites, and deployment guidelines.
"""
import os
import json
import sqlite3

def generate_catalogue():
    conn = sqlite3.connect("projectverse.db")
    cur = conn.cursor()

    # Clear previous project records and replace with exactly 90 projects
    cur.execute("DELETE FROM projects")
    cur.execute("DELETE FROM project_resources")

    # Master list of exactly 90 projects
    bca_titles = [
        "Student Management System",
        "College Attendance Management System",
        "Online Examination Portal",
        "Library Management System",
        "Hostel Management System",
        "Online Shopping Platform",
        "Hospital Management System",
        "Employee Management System",
        "Online Food Ordering System",
        "Expense Tracker",
        "Inventory Management System",
        "Job Portal Application",
        "Event Management System",
        "College Placement Management System",
        "Online Learning Management System"
    ]

    bcom_titles = [
        "Business Sales Analytics Dashboard",
        "Financial Performance Analysis",
        "GST Billing and Invoice Management",
        "Inventory and Stock Analysis",
        "Banking Customer Analysis",
        "Retail Business Analytics",
        "Employee Payroll Management",
        "Market Research Dashboard",
        "E-Commerce Sales Analysis",
        "Financial Risk Analysis Dashboard"
    ]

    btech_titles = [
        "AI-Powered Resume Analyzer",
        "Smart Traffic Management System",
        "Fake News Detection Using Machine Learning",
        "AI-Based Disease Prediction System",
        "Face Recognition Attendance System",
        "Smart Agriculture Monitoring System",
        "College Placement Prediction System",
        "Blockchain-Based Voting System",
        "IoT-Based Smart Home Automation",
        "Real-Time Object Detection System",
        "Network Intrusion Detection System",
        "AI-Powered Chatbot",
        "Cloud-Based File Management System",
        "Smart Parking Management System",
        "Online Fraud Detection System",
        "Voice-Based Virtual Assistant",
        "Water Quality Monitoring System",
        "Accident Detection and Alert System",
        "Sign Language Recognition System",
        "Student Performance Prediction",
        "AI-Based Code Error Detector",
        "Smart Energy Management System",
        "Cybersecurity Threat Detection Platform",
        "Recommendation System Using Machine Learning",
        "Multi-College Management Platform"
    ]

    mca_titles = [
        "AI-Powered College ERP System",
        "Multi-Agent AI Automation Platform",
        "Retrieval-Augmented Generation Knowledge Assistant",
        "Intelligent Document Processing System",
        "AI-Based Customer Support Platform",
        "Enterprise Resource Planning System",
        "Advanced Learning Management System",
        "AI-Based Interview Preparation Platform",
        "Real-Time Collaborative Project Management System",
        "Automated Software Testing Platform",
        "Cloud-Based Hospital Management System",
        "Intelligent Recruitment Management System",
        "AI-Based Financial Advisory Platform",
        "Multi-Tenant SaaS Management Platform",
        "Smart Business Workflow Automation System"
    ]

    mtech_titles = [
        "Deep Learning-Based Medical Image Analysis",
        "Explainable Artificial Intelligence Framework",
        "Federated Learning for Privacy-Preserving AI",
        "Advanced Network Intrusion Detection Using Deep Learning",
        "Autonomous Vehicle Decision Support System",
        "Edge AI-Based Real-Time Monitoring",
        "Blockchain-Based Secure Data Management",
        "Large Language Model Optimization",
        "Advanced Cyber Threat Intelligence Platform",
        "AI-Based Predictive Maintenance",
        "Multimodal Emotion Recognition",
        "Distributed Machine Learning Framework",
        "Computer Vision-Based Industrial Defect Detection",
        "AI-Based Smart Grid Optimization",
        "Privacy-Preserving Healthcare Analytics"
    ]

    iit_titles = [
        "Autonomous AI Research Agent with Multi-Agent Collaboration",
        "Advanced RAG System with Graph-Based Knowledge Retrieval",
        "AI-Based Protein Structure Analysis Platform",
        "Reinforcement Learning-Based Autonomous Traffic Optimization",
        "Privacy-Preserving Federated AI Learning Framework",
        "Real-Time Satellite Image Analysis Using Deep Learning",
        "Large-Scale Graph Neural Network Platform",
        "Explainable Medical AI Decision Support System",
        "Quantum-Inspired Optimization Framework",
        "AI-Powered Cybersecurity Threat Intelligence System"
    ]

    print(f"Counts: BCA={len(bca_titles)}, BCOM={len(bcom_titles)}, BTECH={len(btech_titles)}, MCA={len(mca_titles)}, MTECH={len(mtech_titles)}, IIT={len(iit_titles)}")
    total_projects = len(bca_titles) + len(bcom_titles) + len(btech_titles) + len(mca_titles) + len(mtech_titles) + len(iit_titles)
    print(f"Total projects to generate: {total_projects}")

    # Build detailed project data
    projects_data = []

    # 1. BCA Projects (15)
    bca_domains = ["Full Stack Web", "Database Systems", "Management Software", "E-Commerce", "Enterprise Portal"]
    bca_tech_options = [
        {"frontend": "React.js & Tailwind CSS", "backend": "Node.js & Express.js", "database": "MongoDB / SQLite", "apis": "RESTful API, JWT Auth", "ai": "None (Pure Application Engineering)"},
        {"frontend": "HTML5, Bootstrap 5 & JavaScript", "backend": "Python & Flask", "database": "SQLite / MySQL", "apis": "REST Endpoints, JSON Export", "ai": "None (Standard Database Architecture)"},
        {"frontend": "Vue.js & Tailwind CSS", "backend": "Python & Django", "database": "PostgreSQL", "apis": "Django REST Framework, Session Auth", "ai": "None (Robust Enterprise Logic)"},
        {"frontend": "Angular & Bootstrap", "backend": "Node.js & Express", "database": "MySQL 8.0", "apis": "REST API, PDFKit for Invoicing", "ai": "None (Production CRUD Architecture)"}
    ]

    for i, title in enumerate(bca_titles, 1):
        code = f"BCA{i:03d}"
        tech = bca_tech_options[(i - 1) % len(bca_tech_options)]
        domain = bca_domains[(i - 1) % len(bca_domains)]
        price = 799 + ((i * 70) % 700)
        disc_price = price + 500

        modules = [
            {"module_name": "Authentication & RBAC", "description": "Secure password hashing, token sessions, and role separation (Admin, Staff, Student)."},
            {"module_name": f"Core {title.split()[0]} Processing", "description": f"Workflow pipeline managing all transaction entities, state machine transitions, and data integrity."},
            {"module_name": "Reporting & Analytics", "description": "Automated PDF and Excel generation with dynamic charting for semester audits."},
            {"module_name": "Audit Logging & Security", "description": "Tamper-evident activity logs recording timestamps, user IDs, and modified fields."}
        ]

        features = {
            "Core Administrative": [f"Full lifecycle management for {title}", "Role-based authorization and granular permissions", "Automated input validation and duplicate prevention"],
            "Operational & Workflow": ["Real-time status updates and multi-step approval pipelines", "Search, pagination, and multi-field filtering", "Automated notifications on critical state transitions"],
            "Reports & Deliverables": ["One-click PDF statement and summary generation", "CSV / Excel data import and export", "Visual dashboard with KPI counters"]
        }

        dfd = f"DFD Level 0: External entities (Student/Admin/Staff) send requests -> System validates credentials -> Database updates -> Acknowledgement dispatched.\nDFD Level 1: Auth Module validates token -> Business Logic Process executes transactional updates on {title} store -> Reporting Process compiles audit log."
        uml = f"Class Diagram: User (id, email, role) 1--* {title.replace(' ', '')}Record (id, status, created_at, updated_at). Sequence Diagram: Client initiates HTTP POST -> Controller validates schema -> Repository commits SQL transaction -> View renders confirmation."

        projects_data.append({
            "project_code": code,
            "title": title,
            "academic_level": "BCA",
            "category": "BCA Projects",
            "subcategory": domain,
            "domain": domain,
            "difficulty": "Beginner" if i <= 5 else "Intermediate",
            "timeline": "4-6 Weeks",
            "duration": "4-6 Weeks",
            "price": price,
            "discount_price": disc_price,
            "tech_summary": f"{tech['frontend']}, {tech['backend']}, {tech['database']}",
            "image_url": f"/static/projects/bca/{code}.webp",
            "description": f"A comprehensive {title} designed specifically for BCA curriculum requirements. Implements reliable three-tier architecture, normalized relational schemas, and responsive user interfaces.",
            "problem_statement": f"Academic institutions and commercial departments frequently face administrative bottlenecks, human errors, and record redundancy due to fragmented or manual workflows in {title.lower()} management.",
            "proposed_solution": f"PROJECTVERSE {code} provides an automated, centralized web platform engineered with structured database normalization, role-based controls, and instant report generation.",
            "objectives": f"1. Automate end-to-end data processing for {title.lower()}.\n2. Enforce strict referential integrity across relational tables.\n3. Deliver intuitive desktop and mobile-responsive dashboards for faculty and students.\n4. Ensure compliance with University BCA practical guidelines and viva defense expectations.",
            "scope": f"Full source code, normalized SQL schema, responsive front-end dashboard, REST backend controllers, and complete academic submission documentation.",
            "real_world_apps": f"College departments, educational trusts, small-to-medium enterprises, and administrative offices needing reliable, low-latency management systems.",
            "target_users": "College Administrators, Department Heads, Students, Faculty Mentors, and Non-Teaching Staff.",
            "expected_outcomes": f"A fully operational {title} application with zero runtime dependency errors, comprehensive viva defense documentation, and instant export capabilities.",
            "tech_stack_json": json.dumps(tech),
            "features_json": json.dumps(features),
            "core_modules_json": json.dumps(modules),
            "user_roles": "Administrator (Full System Configuration), Staff / Faculty (Data Entry & Verification), Student / End-User (Self-Service Dashboard).",
            "architecture": f"Three-Tier MVC Architecture: Presentation Layer ({tech['frontend']}) decoupled from Business Logic Layer ({tech['backend']}) and Data Persistence Layer ({tech['database']}).",
            "database_design": f"Normalized 3NF relational database schema with indexed primary keys, foreign key constraints, cascade rules, and audit logging tables.",
            "dfd_description": dfd,
            "uml_description": uml,
            "api_docs": f"GET /api/{code.lower()}/records - List records with pagination\nPOST /api/{code.lower()}/create - Submit verified record\nPUT /api/{code.lower()}/:id - Update record with RBAC verification\nDELETE /api/{code.lower()}/:id - Soft-delete with audit trail.",
            "development_roadmap": "Week 1: Requirement Gathering & SRS. Week 2: Database Schema & Wireframes. Week 3: Backend API & Auth. Week 4: Frontend Integration & Testing. Week 5: Report Compilation & Viva Prep.",
            "prerequisites": "Basic understanding of HTML/CSS, JavaScript, relational databases (SQL), and web server fundamentals.",
            "learning_outcomes": "Mastery of CRUD architectures, authentication patterns, database normalization, and full-stack deployment.",
            "testing_requirements": "Unit testing of backend controllers, schema validation tests, cross-browser compatibility tests, and role permission audits.",
            "expected_output": "Complete deployable source code repository, working demo instance, IEEE project report (50+ pages), SRS document, and viva presentation slides.",
            "deployment_instructions": "Clone repository, run package manager install, configure environment variables in .env, execute migration script, and run local development server.",
            "documentation_requirements": "IEEE format project report, Software Requirement Specification (SRS), ER diagram, DFD Level 0/1/2, Gantt chart, and Viva Voce question bank.",
            "academic_deliverables": "Full Source Code ZIP, IEEE Format Final Report (.docx/.pdf), SRS Documentation, Architecture & ER Diagrams, PowerPoint Presentation (.pptx), Viva Voce Q&A Bank.",
            "is_published": 1,
            "is_featured": 1 if i in [1, 3, 6, 12] else 0,
            "popularity_score": 90 + (i % 8),
            "is_trending": 1 if i in [1, 6, 14] else 0,
            "is_research": 0
        })

    # 2. B.Com Projects (10)
    bcom_domains = ["Financial Analytics", "Taxation & GST", "Retail & Commerce", "Banking Operations", "Risk Management"]
    bcom_tech_options = [
        {"frontend": "Streamlit & Plotly Interactive Dashboards", "backend": "Python Data Engine (Pandas, NumPy)", "database": "PostgreSQL & SQLite", "apis": "FastAPI REST, Excel/CSV Exporters", "ai": "Statistical & Econometric Time-Series Analysis"},
        {"frontend": "React.js with Chart.js & ApexCharts", "backend": "Python Flask / Django", "database": "MySQL & Redis Cache", "apis": "Financial Modeling REST API", "ai": "Predictive Regression & Moving Average Models"},
        {"frontend": "Modern HTML5, Tailwind & Power BI Embedded", "backend": "Python (Pandas, OpenPyXL)", "database": "Relational SQL Data Warehouse", "apis": "Accounting Standard API, GST Ledger API", "ai": "Financial Ratio Analysis & Trend Forecasting"}
    ]

    for i, title in enumerate(bcom_titles, 1):
        code = f"BCOM{i:03d}"
        tech = bcom_tech_options[(i - 1) % len(bcom_tech_options)]
        domain = bcom_domains[(i - 1) % len(bcom_domains)]
        price = 849 + ((i * 50) % 500)
        disc_price = price + 450

        modules = [
            {"module_name": "Data Ingestion & Cleaning", "description": "Automated ingestion of raw transaction ledgers, CSV balance sheets, and bank transaction files."},
            {"module_name": "Financial Metric Calculator", "description": "Formulas computing EBITDA, liquidity ratios, working capital cycles, and tax compliances."},
            {"module_name": "Interactive KPI Dashboard", "description": "Visual multi-chart reporting with drill-down filters by fiscal year, quarter, and product line."},
            {"module_name": "Audit & Compliance Reporting", "description": "Complies with statutory reporting guidelines, variance checks, and audit trails."}
        ]

        features = {
            "Financial Analytics": [f"Automated computation for {title}", "Comprehensive variance analysis against budget benchmarks", "Dynamic cash flow and liquidity forecasting"],
            "Business Intelligence": ["Multi-dimensional interactive drill-downs and heatmaps", "Executive summary KPI scorecards", "Automated anomaly detection in ledger transactions"],
            "Statutory Compliance": ["GST, TDS, and corporate tax calculation worksheets", "Standardized balance sheet and P&L export to Excel/PDF", "Complete audit trail for accounting reconciliation"]
        }

        dfd = f"DFD Level 0: Accounting Data Sources -> Ingestion Engine -> Analytical Computation Engine -> Financial Dashboard & Audit Reports.\nDFD Level 1: Ledger Ingestion -> Normalization & Validation -> Financial Ratio Calculations -> Visualization Cache -> Presentation Layer."
        uml = f"Class Diagram: Transaction (tx_id, date, amount, debit_ac, credit_ac) 1--* LedgerEntry 1--1 FinancialReport (ebitda, margin, tax_liability)."

        projects_data.append({
            "project_code": code,
            "title": title,
            "academic_level": "B.Com",
            "category": "B.Com Projects",
            "subcategory": domain,
            "domain": domain,
            "difficulty": "Intermediate",
            "timeline": "4-6 Weeks",
            "duration": "4-6 Weeks",
            "price": price,
            "discount_price": disc_price,
            "tech_summary": f"{tech['frontend']}, {tech['backend']}, {tech['database']}",
            "image_url": f"/static/projects/bcom/{code}.webp",
            "description": f"A specialized commerce and business analytics project focusing on {title.lower()}. Features quantitative business intelligence, statutory calculation models, and executive visual dashboards.",
            "problem_statement": f"Corporate managers and commerce analysts struggle with disparate spreadsheets, manual reconciliation errors, and delayed insights in {title.lower()}.",
            "proposed_solution": f"PROJECTVERSE {code} automates business computations, ledger reconciliations, and financial visualizations into a streamlined analytics dashboard.",
            "objectives": f"1. Streamline business performance metrics for {title.lower()}.\n2. Enable real-time variance and ratio analysis for financial decision making.\n3. Implement statutory compliance validations (GST, accounting standards).\n4. Provide an intuitive analytics interface tailored for commerce and management students.",
            "scope": f"Complete Python/Web analytical codebase, sample financial datasets, dynamic dashboard visualizers, calculation notebooks, and university-aligned academic report.",
            "real_world_apps": "Retail chains, commercial banks, financial advisory firms, audit consultancies, and corporate finance departments.",
            "target_users": "Financial Controllers, Accounts Managers, Business Analysts, Commerce Evaluators, and Auditors.",
            "expected_outcomes": f"An end-to-end analytical platform that processes complex business datasets and outputs boardroom-ready visual reports and compliant balance summaries.",
            "tech_stack_json": json.dumps(tech),
            "features_json": json.dumps(features),
            "core_modules_json": json.dumps(modules),
            "user_roles": "Chief Financial Officer (Executive Summary), Financial Analyst (Data Modeling & Scenarios), Auditor (Ledger Verification).",
            "architecture": "Modern Analytics Architecture: Data Pipeline -> Processing Engine (Pandas/SQL) -> Metric Computation Layer -> Reactive Dashboard Interface.",
            "database_design": "Star schema / snowflake design optimized for analytical queries with Fact_Transactions and Dimension tables (Dim_Date, Dim_Account, Dim_Product).",
            "dfd_description": dfd,
            "uml_description": uml,
            "api_docs": f"GET /api/{code.lower()}/kpis - Retrieve executive financial metrics\nPOST /api/{code.lower()}/upload-ledger - Ingest transaction CSV\nGET /api/{code.lower()}/variance-analysis - Compute budget variance ratios.",
            "development_roadmap": "Week 1: Financial Modeling & Formula Definitions. Week 2: Dataset Preparation & Ingestion Pipeline. Week 3: Dashboard & KPI Visuals. Week 4: Sensitivity Testing & Documentation.",
            "prerequisites": "Foundational knowledge of corporate accounting, financial ratios, Excel fundamentals, and basic Python data processing.",
            "learning_outcomes": "Practical mastery of business analytics, financial ratio computation, interactive dashboard engineering, and statutory reporting.",
            "testing_requirements": "Mathematical verification against standard accounting ledgers, boundary value analysis on taxation tiers, and visual performance checks.",
            "expected_output": "Working analytical dashboard, sample corporate datasets, 45+ page formal project report, viva guide, and business interpretation slides.",
            "deployment_instructions": "Install Python dependencies via requirements.txt, launch dashboard engine, and navigate to local dashboard URL in any modern browser.",
            "documentation_requirements": "Comprehensive B.Com project report, ratio analysis methodology, dataset dictionary, test reconciliation certificates, and viva defense notes.",
            "academic_deliverables": "Source Code & Jupyter Notebooks, Financial Analytics Report, Dataset Sheets, PPT Presentation, Viva Voce Q&A.",
            "is_published": 1,
            "is_featured": 1 if i in [1, 3, 5] else 0,
            "popularity_score": 88 + (i % 10),
            "is_trending": 1 if i in [1, 3] else 0,
            "is_research": 0
        })

    # 3. B.Tech Projects (25)
    btech_domains = ["Artificial Intelligence & ML", "IoT & Embedded Systems", "Cybersecurity & Blockchain", "Cloud & Distributed Systems", "Computer Vision & Deep Learning"]
    btech_tech_options = [
        {"frontend": "React.js / Next.js & Tailwind", "backend": "Python FastAPI & PyTorch / Scikit-Learn", "database": "PostgreSQL & Vector DB (Chroma/FAISS)", "apis": "FastAPI REST, WebSocket Real-Time", "ai": "Transformer Models, Random Forests & Ensemble Classifiers"},
        {"frontend": "React Native / React.js Web", "backend": "Node.js & Python Microservices", "database": "MongoDB & Redis", "apis": "MQTT Broker, WebSockets, REST", "ai": "Computer Vision (YOLOv8, OpenCV) & Edge Inference"},
        {"frontend": "Next.js 14 & Shadcn UI", "backend": "Python FastAPI & Solidity / Web3.js", "database": "PostgreSQL & IPFS Decentralized Storage", "apis": "Ethers.js, MetaMask Web3 RPC, REST", "ai": "Cryptographic Zero-Knowledge Logic & Machine Learning Anomaly Detection"},
        {"frontend": "Vue 3 & Vite", "backend": "Python Flask & TensorFlow / Keras", "database": "MySQL & Redis Cache", "apis": "RESTful API, Celery Async Worker Queue", "ai": "Deep Neural Networks, CNNs & Bi-LSTM NLP Models"}
    ]

    for i, title in enumerate(btech_titles, 1):
        code = f"BTECH{i:03d}"
        tech = btech_tech_options[(i - 1) % len(btech_tech_options)]
        domain = btech_domains[(i - 1) % len(btech_domains)]
        price = 999 + ((i * 80) % 800)
        disc_price = price + 600

        modules = [
            {"module_name": "Data Acquisition & Preprocessing", "description": "Real-time stream processing, feature engineering, and automated dataset normalization."},
            {"module_name": "Core Intelligence / Algorithm Engine", "description": f"Custom pipeline implementing state-of-the-art algorithms tailored for {title.lower()}."},
            {"module_name": "Interactive Engineering Dashboard", "description": "High-throughput UI with low-latency telemetry, real-time charts, and alert triggers."},
            {"module_name": "Security & Verification Layer", "description": "End-to-end token validation, tamper checks, and comprehensive error resilience."}
        ]

        features = {
            "Engineering Pipeline": [f"High-performance architecture for {title}", "Sub-second inference and real-time event processing", "Scalable asynchronous task queues (Celery/Redis)"],
            "Machine Learning / Core Logic": ["Pre-trained and fine-tuned predictive models with high accuracy", "Confusion matrix, ROC-AUC, and precision/recall evaluation metrics", "Automated feature scaling and cross-validation"],
            "Production Features": ["Interactive web dashboard with dark-mode engineering theme", "Docker containerization support", "RESTful API with OpenAPI / Swagger documentation"]
        }

        dfd = f"DFD Level 0: User/Sensor Input -> Ingestion Gateway -> Core Processing/Inference Engine -> Relational/Vector Storage -> Real-time UI.\nDFD Level 1: Authentication -> Pipeline Preprocessing -> Model Inference Execution -> Alert & Visualization Dispatch."
        uml = f"Class Diagram: Sensor/UserInput 1--* ProcessingPipeline 1--1 ModelClassifier (predict(), evaluate()). Sequence Diagram: Client event -> API Gateway -> Model worker -> DB record -> Push Notification."

        projects_data.append({
            "project_code": code,
            "title": title,
            "academic_level": "B.Tech",
            "category": "B.Tech Projects",
            "subcategory": domain,
            "domain": domain,
            "difficulty": "Intermediate" if i <= 10 else "Advanced",
            "timeline": "6-8 Weeks",
            "duration": "6-8 Weeks",
            "price": price,
            "discount_price": disc_price,
            "tech_summary": f"{tech['frontend']}, {tech['backend']}, {tech['database']}, {tech['ai']}",
            "image_url": f"/static/projects/btech/{code}.webp",
            "description": f"An industry-standard B.Tech capstone project implementing {title}. Combines modern full-stack development, algorithmic rigor, and realistic hardware/cloud simulated workflows.",
            "problem_statement": f"Existing real-world implementations of {title.lower()} suffer from scalability bottlenecks, high latency, inaccurate baseline models, and lack of verified production interfaces.",
            "proposed_solution": f"PROJECTVERSE {code} delivers a modular engineering solution featuring trained neural/algorithmic models, sub-second latency, and intuitive real-time dashboards.",
            "objectives": f"1. Engineer a production-grade prototype for {title.lower()}.\n2. Validate algorithmic accuracy with empirical benchmark datasets.\n3. Implement secure, decoupled client-server microservices.\n4. Complete IEEE conference-style thesis and patent/copyright submission artifacts.",
            "scope": f"Full source code repository, trained model weights (.pt/.pkl/.h5), interactive front-end, REST API backend, Docker configuration, and comprehensive IEEE research report.",
            "real_world_apps": "Smart cities, healthcare diagnostics, enterprise cybersecurity, automated logistics, intelligent surveillance, and smart campus deployments.",
            "target_users": "System Engineers, Operations Analysts, Academic Defense Panels, and End-Users.",
            "expected_outcomes": f"A thoroughly verified system demonstrating >90% empirical performance on test benchmarks, zero critical runtime flaws, and seamless containerized execution.",
            "tech_stack_json": json.dumps(tech),
            "features_json": json.dumps(features),
            "core_modules_json": json.dumps(modules),
            "user_roles": "Administrator (System Governance), Engineer / Analyst (Telemetry & Pipeline Control), Evaluator (Audit & Metrics).",
            "architecture": "Event-Driven Microservices Architecture: Decoupled API Gateway, Asynchronous Worker Queue, Model Inference Engine, and Reactive Client.",
            "database_design": "Hybrid Storage Model: PostgreSQL for relational entities, Redis for caching/pub-sub, and Chroma/FAISS for vector embeddings.",
            "dfd_description": dfd,
            "uml_description": uml,
            "api_docs": f"POST /api/{code.lower()}/predict - Real-time inference\nGET /api/{code.lower()}/telemetry - Live metrics stream\nGET /api/{code.lower()}/metrics - Model accuracy benchmarks.",
            "development_roadmap": "Week 1: Problem Definition & Literature Survey. Week 2-3: Dataset Engineering & Model Training. Week 4-5: Backend API & Microservices. Week 6: UI & Hardware Integration. Week 7: Testing. Week 8: Final Thesis & Presentation.",
            "prerequisites": "Proficiency in Python or JavaScript, understanding of data structures, algorithms, foundational machine learning or network concepts.",
            "learning_outcomes": "Deep understanding of end-to-end ML/Engineering pipelines, REST API design, asynchronous processing, and engineering research documentation.",
            "testing_requirements": "PyTest unit test suite, Locust load testing, confusion matrix evaluation, and 100% API endpoint health verification.",
            "expected_output": "Complete GitHub-ready source code repository, pre-trained model weights, IEEE format documentation (60+ pages), and viva presentation deck.",
            "deployment_instructions": "Docker Compose one-click launch: 'docker-compose up --build' or run virtual environment with pip install -r requirements.txt.",
            "documentation_requirements": "IEEE formatted thesis report, system design diagrams, circuit schematics where applicable, test result logs, and viva defense flashcards.",
            "academic_deliverables": "Full Source Code ZIP, Trained Model Artifacts, IEEE Report (.docx/.pdf), SRS & Design Diagrams, Presentation Deck (.pptx), Viva Guide.",
            "is_published": 1,
            "is_featured": 1 if i in [1, 3, 5, 8, 10, 15, 23] else 0,
            "popularity_score": 92 + (i % 8),
            "is_trending": 1 if i in [1, 5, 8, 10, 15] else 0,
            "is_research": 0
        })

    # 4. MCA Projects (15)
    mca_domains = ["Enterprise SaaS & Cloud", "Multi-Agent Systems", "Applied Generative AI", "Distributed Architecture", "Autonomous Workflows"]
    mca_tech_options = [
        {"frontend": "Next.js 14 (App Router) & Tailwind CSS", "backend": "Python FastAPI & LangChain / LangGraph", "database": "PostgreSQL (pgvector) & Redis", "apis": "OpenAI / Claude / HuggingFace API, GraphQL, REST", "ai": "Retrieval-Augmented Generation (RAG) & Autonomous Multi-Agent Workflows"},
        {"frontend": "React 18 with TanStack Query & TypeScript", "backend": "Node.js (NestJS) & Python AI Microservices", "database": "PostgreSQL & MongoDB Dual-Engine", "apis": "gRPC Microservices, WebSockets, Kafka", "ai": "Document OCR (Tesseract/LayoutLM) & Semantic Embedding Vectors"},
        {"frontend": "Next.js with Radix UI & Tailwind", "backend": "Python FastAPI & Dockerized Workers", "database": "PostgreSQL & MinIO S3 Object Store", "apis": "REST, WebSockets, OAuth2 / OIDC Single Sign-On", "ai": "Sentence Transformers, Cross-Encoders & Re-Ranking Pipelines"}
    ]

    for i, title in enumerate(mca_titles, 1):
        code = f"MCA{i:03d}"
        tech = mca_tech_options[(i - 1) % len(mca_tech_options)]
        domain = mca_domains[(i - 1) % len(mca_domains)]
        price = 1199 + ((i * 70) % 700)
        disc_price = price + 700

        modules = [
            {"module_name": "Multi-Tenant Cloud Core", "description": "Schema isolation, tenant configuration, and granular enterprise permission policies."},
            {"module_name": f"Autonomous {title.split()[0]} Engine", "description": f"AI and agentic workflow orchestration engine automating core operations for {title.lower()}."},
            {"module_name": "Knowledge Retrieval & Vector Search", "description": "Hybrid search (BM25 + Dense Vectors) with contextual re-ranking and citation traceability."},
            {"module_name": "Enterprise Telemetry & Analytics", "description": "Live request tracking, latency monitoring, error auditing, and usage billing."}
        ]

        features = {
            "Enterprise Architecture": [f"Production-ready design for {title}", "Multi-tenant isolation and cloud scalability", "Comprehensive OAuth2 and JWT role-based access control"],
            "AI & Autonomous Intelligence": ["Agentic decision making with self-correction and memory loops", "Vector semantic search with pgvector and dense embeddings", "Automated document indexing and summarization"],
            "Operational Tooling": ["Real-time collaborative editing and WebSockets sync", "Automated CI/CD pipeline configuration", "Complete administrative dashboard with usage metrics"]
        }

        dfd = f"DFD Level 0: Enterprise Client -> API Gateway -> Orchestration Layer -> Vector/Relational Stores -> AI Engine -> Client.\nDFD Level 1: Tenant Validation -> Agent Dispatcher -> Context Retrieval -> LLM / Processing Node -> Response Formatter."
        uml = f"Class Diagram: Tenant 1--* User 1--* AgentTask 1--* VectorEmbedding. Sequence: User queries -> Orchestrator retrieves vector context -> Generates response -> Commits audit log."

        projects_data.append({
            "project_code": code,
            "title": title,
            "academic_level": "MCA",
            "category": "MCA Projects",
            "subcategory": domain,
            "domain": domain,
            "difficulty": "Advanced",
            "timeline": "6-8 Weeks",
            "duration": "6-8 Weeks",
            "price": price,
            "discount_price": disc_price,
            "tech_summary": f"{tech['frontend']}, {tech['backend']}, {tech['database']}, {tech['ai']}",
            "image_url": f"/static/projects/mca/{code}.webp",
            "description": f"An advanced Master of Computer Applications (MCA) enterprise project implementing {title}. Focuses on enterprise software patterns, distributed microservices, multi-agent AI, and cloud scalability.",
            "problem_statement": f"Legacy academic and business systems lack intelligent automation, scalable multi-tenancy, and modern AI integration, resulting in high operational overhead in {title.lower()}.",
            "proposed_solution": f"PROJECTVERSE {code} provides an enterprise multi-tenant software platform combining agentic AI, robust data pipelines, and responsive next-generation interfaces.",
            "objectives": f"1. Architect an enterprise-ready system for {title.lower()}.\n2. Integrate autonomous AI and vector retrieval workflows seamlessly.\n3. Ensure high availability, data consistency, and tenant isolation.\n4. Satisfy top-tier University MCA project guidelines and defense requirements.",
            "scope": f"Full source code with modular architecture, container definitions, migration scripts, vector database seeders, and IEEE-format academic thesis.",
            "real_world_apps": "University ERP systems, enterprise SaaS providers, healthcare networks, corporate HR platforms, and autonomous customer experience suites.",
            "target_users": "Enterprise System Administrators, Department Leads, End-Users, and Academic Evaluators.",
            "expected_outcomes": f"A scalable, enterprise-grade software system with high automated test coverage, robust multi-agent reliability, and comprehensive documentation.",
            "tech_stack_json": json.dumps(tech),
            "features_json": json.dumps(features),
            "core_modules_json": json.dumps(modules),
            "user_roles": "Tenant Admin (Workspace Configuration), Staff / Member (Day-to-day Operations), System Auditor (Security & Log Audit).",
            "architecture": "Modern Clean Architecture / Domain-Driven Design: Decoupled Domain, Use Cases, Repositories, and Presentation Layer.",
            "database_design": "PostgreSQL with pgvector extension for hybrid relational-vector storage, optimized with compound B-Tree and HNSW indexes.",
            "dfd_description": dfd,
            "uml_description": uml,
            "api_docs": f"POST /api/{code.lower()}/agent/execute - Trigger autonomous task\nGET /api/{code.lower()}/knowledge - Semantic search\nGET /api/{code.lower()}/telemetry - System audit logs.",
            "development_roadmap": "Week 1: Domain-Driven Modeling & Architecture. Week 2: Database & Multi-Tenant Setup. Week 3: Agentic Logic & Vector Search. Week 4: API & Frontend Integration. Week 5: Performance Tuning. Week 6: Comprehensive Thesis.",
            "prerequisites": "Strong understanding of object-oriented design, relational databases, REST APIs, and basic familiarity with modern JavaScript/TypeScript or Python.",
            "learning_outcomes": "Mastery of enterprise cloud architectures, multi-tenant patterns, agentic AI workflows, and professional software engineering methodologies.",
            "testing_requirements": "End-to-end testing with Playwright / Cypress, API contract testing, stress testing for concurrent tenant requests, and vector similarity benchmarks.",
            "expected_output": "Production-ready codebase, complete Dockerized environment, 65+ page IEEE thesis document, SRS, architecture blueprints, and viva deck.",
            "deployment_instructions": "Docker Compose deployment with automated seeders: 'docker-compose up -d' followed by database migration and initialization.",
            "documentation_requirements": "MCA University format project thesis, System Architecture Document (SAD), Class & Sequence diagrams, Test Matrices, and Viva Voce preparation compendium.",
            "academic_deliverables": "Enterprise Source Code Repository, Full IEEE Thesis (.docx/.pdf), Database Migration Scripts, Postman API Collection, Presentation (.pptx), Viva Voce Q&A.",
            "is_published": 1,
            "is_featured": 1 if i in [1, 2, 3, 6, 9] else 0,
            "popularity_score": 94 + (i % 6),
            "is_trending": 1 if i in [1, 2, 3, 8] else 0,
            "is_research": 0
        })

    # 5. M.Tech Projects (15)
    mtech_domains = ["Deep Learning & Medical Imaging", "Explainable & Trustworthy AI", "Privacy-Preserving Computing", "Edge AI & IoT Systems", "Distributed ML & Optimization"]
    mtech_tech_options = [
        {"frontend": "React.js / Next.js with Medical DICOM Viewer", "backend": "Python FastAPI & PyTorch / TorchVision", "database": "PostgreSQL & S3 / MinIO Object Storage", "apis": "DICOMweb, REST API, TensorRT", "ai": "Convolutional Neural Networks (ResNet, DenseNet, EfficientNet) & U-Net Segmentation"},
        {"frontend": "Streamlit / React Interactive Research Dashboard", "backend": "Python PyTorch & Flower (FL) Framework", "database": "PostgreSQL & SQLite", "apis": "Federated gRPC Protocol, REST", "ai": "Federated Averaging (FedAvg), Differential Privacy (DP-SGD) & Secure Aggregation"},
        {"frontend": "Next.js & Plotly Scientific Visualizers", "backend": "Python FastAPI & PyTorch / HuggingFace Transformers", "database": "PostgreSQL & Redis Cache", "apis": "vLLM High-Throughput Inference Engine, REST", "ai": "Quantization (INT8/INT4), Low-Rank Adaptation (LoRA), and FlashAttention-2 Optimization"}
    ]

    for i, title in enumerate(mtech_titles, 1):
        code = f"MTECH{i:03d}"
        tech = mtech_tech_options[(i - 1) % len(mtech_tech_options)]
        domain = mtech_domains[(i - 1) % len(mtech_domains)]
        price = 1499 + ((i * 80) % 900)
        disc_price = price + 800

        modules = [
            {"module_name": "Scientific Data Pipeline", "description": "High-throughput data loader with augmentations, cross-validation splits, and tensor caching."},
            {"module_name": "Advanced Neural Architecture", "description": f"Custom mathematical formulation and loss function implementation for {title.lower()}."},
            {"module_name": "Explainability & Interpretability", "description": "Grad-CAM heatmaps, SHAP/LIME attribution scores, and attention map visualizers."},
            {"module_name": "Empirical Benchmark Evaluator", "description": "Computes statistical metrics (F1, AUC-ROC, BLEU, Perplexity, Dice score) with confidence intervals."}
        ]

        features = {
            "Research Methodology": [f"Rigorous experimental methodology for {title}", "Custom loss functions and mathematical objective formulation", "Extensive ablation studies comparing baseline vs proposed model"],
            "Model Architecture & Optimization": ["State-of-the-art deep learning architectures (Transformers, CNNs, GNNs)", "Hardware acceleration with TensorRT and mixed-precision (FP16/BF16)", "Differential privacy and model robustness verification"],
            "Empirical Results & Visualization": ["Interactive confusion matrices, ROC-PR curves, and loss landscapes", "Explainable AI visualizers (Grad-CAM, SHAP, feature attributions)", "Reproducible Jupyter research notebooks and training scripts"]
        }

        dfd = f"DFD Level 0: Raw Scientific Input -> Preprocessing & Augmentation Pipeline -> Deep Neural Network -> Loss & Metric Evaluation -> Visual Research Interface.\nDFD Level 1: Input Tensor -> Feature Extraction Backbone -> Decision / Generation Head -> Explainability Engine -> Report Generator."
        uml = f"Class Diagram: DatasetLoader 1--* ModelArchitecture (forward(), compute_loss()) 1--1 EvaluationMetrics (dice_score, roc_auc, shap_values)."

        projects_data.append({
            "project_code": code,
            "title": title,
            "academic_level": "M.Tech",
            "category": "M.Tech Projects",
            "subcategory": domain,
            "domain": domain,
            "difficulty": "Research",
            "timeline": "8-12 Weeks",
            "duration": "8-12 Weeks",
            "price": price,
            "discount_price": disc_price,
            "tech_summary": f"{tech['frontend']}, {tech['backend']}, {tech['database']}, {tech['ai']}",
            "image_url": f"/static/projects/mtech/{code}.webp",
            "description": f"A postgraduate research-oriented M.Tech project in {title}. Focuses on theoretical formulation, novel architectural variants, empirical ablation benchmarks, and IEEE conference publication standards.",
            "problem_statement": f"Current research baselines for {title.lower()} suffer from computational inefficiencies, vulnerability to distribution shifts, lack of interpretability, and poor generalization on real-world datasets.",
            "proposed_solution": f"PROJECTVERSE {code} introduces an advanced mathematical model and optimized deep learning pipeline that surpasses conventional baseline metrics while preserving computational efficiency.",
            "objectives": f"1. Formulate a novel mathematical and architectural framework for {title.lower()}.\n2. Conduct extensive comparative ablation experiments on standard benchmark datasets.\n3. Incorporate explainable AI (XAI) and robustness guarantees.\n4. Produce publication-ready IEEE conference research manuscripts and thesis defense materials.",
            "scope": f"Complete experimental code, training and evaluation scripts, pre-trained checkpoint weights, ablation notebooks, and 75+ page M.Tech master's thesis.",
            "real_world_apps": "Clinical radiology, autonomous robotics, privacy-critical financial networks, smart manufacturing, and critical infrastructure defense.",
            "target_users": "Research Scholars, Machine Learning Scientists, University Defense Committees, and Industrial R&D Labs.",
            "expected_outcomes": f"Empirical validation proving statistically significant improvements over published baselines, complete ablation graphs, and a defense-ready M.Tech thesis.",
            "tech_stack_json": json.dumps(tech),
            "features_json": json.dumps(features),
            "core_modules_json": json.dumps(modules),
            "user_roles": "Lead Researcher (Experimentation & Hyperparameter Tuning), Faculty Advisor (Ablation Audit & Thesis Review), Defense Examiner (Peer Review).",
            "architecture": "Research Pipeline Architecture: Data Ingestion -> Normalized Tensor Processing -> PyTorch Deep Architecture -> Metric Computation & Explainability Visualization.",
            "database_design": "Research Artifact Database: Experiment runs, hyperparameter logs, checkpoint metadata, and evaluation metrics stored with reproducible seeds.",
            "dfd_description": dfd,
            "uml_description": uml,
            "api_docs": f"POST /api/{code.lower()}/infer - High-precision model inference\nPOST /api/{code.lower()}/explain - Generate Grad-CAM / SHAP attribution\nGET /api/{code.lower()}/ablation - Retrieve comparative benchmark metrics.",
            "development_roadmap": "Weeks 1-2: Literature Review & Mathematical Formulation. Weeks 3-4: Baseline Implementation. Weeks 5-6: Proposed Model & Loss Function. Weeks 7-8: Ablation Studies & Tuning. Weeks 9-10: Explainability & Benchmarks. Weeks 11-12: Master's Thesis Drafting.",
            "prerequisites": "Advanced knowledge of linear algebra, calculus, probability, Python, PyTorch / TensorFlow, and deep learning architectures.",
            "learning_outcomes": "Expertise in research paper reproduction, custom neural architecture design, ablation experimentation, and scholarly scientific writing.",
            "testing_requirements": "Statistical significance testing (p-values, Wilcoxon signed-rank), k-fold cross validation, inference latency benchmarks on GPU, and adversarial robustness testing.",
            "expected_output": "Complete PyTorch research codebase, trained model checkpoints (.pt), comprehensive 75+ page M.Tech thesis, IEEE format camera-ready paper draft, and defense presentation.",
            "deployment_instructions": "Create Python 3.10 virtual environment, install CUDA-enabled PyTorch, download benchmark dataset, and execute evaluate.py or train.py.",
            "documentation_requirements": "Complete M.Tech University thesis, IEEE conference manuscript draft, mathematical derivation appendix, ablation table charts, and viva presentation deck.",
            "academic_deliverables": "Full Research Source Code, Pre-trained Model Checkpoints, Master's Thesis (.docx/.pdf), IEEE Paper Draft, Slide Deck (.pptx), Comprehensive Viva Guide.",
            "is_published": 1,
            "is_featured": 1 if i in [1, 2, 3, 6, 8, 12] else 0,
            "popularity_score": 95 + (i % 5),
            "is_trending": 1 if i in [1, 3, 8] else 0,
            "is_research": 1
        })

    # 6. IIT-Level / Research-Grade Projects (10)
    iit_domains = ["Autonomous Multi-Agent AI", "Graph Neural Networks & RAG", "Computational Biology & AI", "Reinforcement Learning", "Quantum-Inspired Optimization"]
    iit_tech_options = [
        {"frontend": "React 18 / Next.js with WebGL & 3D Cytoscape Graph Visualization", "backend": "Python FastAPI, PyTorch Geometric & Ray Distributed", "database": "Neo4j Graph Database & pgvector", "apis": "GraphRAG API, Distributed Ray RPC, REST", "ai": "Graph Neural Networks (GCN, GAT), Knowledge Graph Embedding & Multi-Hop Reasoning"},
        {"frontend": "Next.js & Three.js 3D Molecular / Spatial Viewer", "backend": "Python FastAPI & PyTorch / DeepSpeed", "database": "PostgreSQL & Vector DB", "apis": "Biopython, PDB API, Distributed RPC", "ai": "Equivariant Graph Neural Networks, Transformer Structural Attention & Energy Minimization"},
        {"frontend": "React & Plotly Real-Time Simulation Canvas", "backend": "Python & Ray RLlib / Stable-Baselines3", "database": "TimescaleDB & Redis", "apis": "OpenAI Gym / Gymnasium Environment, WebSockets", "ai": "Deep Q-Learning, PPO, Multi-Agent Reinforcement Learning (MAPPO)"},
        {"frontend": "Next.js & Quantum Circuit Visualizer", "backend": "Python & Qiskit / PennyLane / Cirq Simulator", "database": "PostgreSQL & Redis", "apis": "Quantum Engine RPC, REST", "ai": "Quantum Approximate Optimization Algorithm (QAOA) & Variational Quantum Eigensolver (VQE)"}
    ]

    for i, title in enumerate(iit_titles, 1):
        code = f"IIT{i:03d}"
        tech = iit_tech_options[(i - 1) % len(iit_tech_options)]
        domain = iit_domains[(i - 1) % len(iit_domains)]
        price = 1999 + ((i * 100) % 1000)
        disc_price = price + 1000

        modules = [
            {"module_name": "Theoretical Formulation Core", "description": "Implements mathematically rigorous algorithms inspired by premier research publications."},
            {"module_name": "Distributed Computation Engine", "description": "Ray/Dask cluster coordination for parallel graph processing, simulation, or tensor computations."},
            {"module_name": "Interactive Scientific Visualizer", "description": "High-fidelity interactive 3D, graph, or real-time simulation canvas built with WebGL/Three.js."},
            {"module_name": "Peer-Review Benchmark Suite", "description": "Exhaustive comparison against international state-of-the-art standards with convergence proofs."}
        ]

        features = {
            "Research-Grade Innovations": [f"Frontier engineering methodology for {title}", "Graph-based or distributed multi-agent autonomous coordination", "Convergence proofs, theoretical bound analysis, and state space modeling"],
            "State-of-the-Art Architecture": ["Hybrid Knowledge Graphs + Dense Embedding Vector retrieval", "Scalable distributed computation with Ray or PyTorch Distributed", "Zero-compromise reproducibility with fixed seeds and deterministic kernels"],
            "Scholarly Artifacts": ["Interactive 3D visualization and knowledge exploration canvas", "Publication-ready LaTeX research manuscript", "Comprehensive mathematical derivations and proofs appendix"]
        }

        dfd = f"DFD Level 0: High-Dimensional Input -> Distributed Preprocessing -> Complex Graph/Agent/Quantum Engine -> Empirical Validation -> Interactive Visualizer.\nDFD Level 1: Input Tensor/Graph -> Knowledge Graph Indexer -> Autonomous Agent Dispatch -> Consensus / Optimization Head -> Visualization Stream."
        uml = f"Class Diagram: GraphNode 1--* GraphEdge 1--* AgentState (act(), observe(), update_policy()). Sequence: Simulation step -> Distributed Worker -> Consensus -> Realtime WebGL Render."

        projects_data.append({
            "project_code": code,
            "title": title,
            "academic_level": "IIT-Level / Research-Grade",
            "category": "IIT-Level / Research-Grade Projects",
            "subcategory": domain,
            "domain": domain,
            "difficulty": "Research",
            "timeline": "10-16 Weeks",
            "duration": "10-16 Weeks",
            "price": price,
            "discount_price": disc_price,
            "tech_summary": f"{tech['frontend']}, {tech['backend']}, {tech['database']}, {tech['ai']}",
            "image_url": f"/static/projects/iit/{code}.webp",
            "description": f"An IIT-inspired, research-grade capstone project exploring {title}. Designed for students pursuing publication in prestigious IEEE/ACM conferences and top-tier postgraduate admissions.",
            "problem_statement": f"Frontier problems in {title.lower()} remain unresolved by conventional heuristics, requiring cross-disciplinary synthesis of graph representation, autonomous agents, and distributed optimization.",
            "proposed_solution": f"PROJECTVERSE {code} presents a research-grade framework combining theoretical mathematical formulations, distributed computation, and empirical validation against international benchmarks.",
            "objectives": f"1. Formulate and solve complex research objectives in {title.lower()}.\n2. Deliver scalable implementations utilizing graph neural networks, multi-agent systems, or quantum-inspired heuristics.\n3. Validate performance on competitive international benchmark datasets.\n4. Complete a research manuscript suitable for submission to premier academic conferences.",
            "scope": f"Complete research implementation code, dataset scripts, trained model checkpoints, interactive WebGL visualizer, LaTeX manuscript, and 80+ page master's thesis.",
            "real_world_apps": "Next-generation search engines, pharmaceutical drug discovery, autonomous metropolitan transport, national cyber defense, and quantum computing simulations.",
            "target_users": "Premier Institute Research Scholars, AI Scientists, PhD Candidates, and Industrial Research Labs.",
            "expected_outcomes": f"A pioneering research artifact demonstrating theoretical novelty, empirical superiority over baselines, and peer-review ready scientific documentation.",
            "tech_stack_json": json.dumps(tech),
            "features_json": json.dumps(features),
            "core_modules_json": json.dumps(modules),
            "user_roles": "Principal Investigator (Research Governance), Research Engineer (Experiment Execution), External Reviewer (Peer Validation).",
            "architecture": "Distributed Research Architecture: Knowledge Graph Engine (Neo4j) -> Distributed Compute Cluster (Ray) -> PyTorch Geometric / Qiskit Core -> Reactive WebGL Presentation.",
            "database_design": "Hybrid Neo4j Property Graph Database for multi-hop semantic topologies and PostgreSQL for relational experiment telemetry.",
            "dfd_description": dfd,
            "uml_description": uml,
            "api_docs": f"POST /api/{code.lower()}/simulate - Execute distributed research simulation\nPOST /api/{code.lower()}/graph/query - Multi-hop semantic traversal\nGET /api/{code.lower()}/convergence - Retrieve empirical convergence curves.",
            "development_roadmap": "Weeks 1-3: Theoretical Foundations & Literature Survey. Weeks 4-6: Graph & Agent Modeling. Weeks 7-9: Distributed Implementation. Weeks 10-12: Benchmark Evaluation. Weeks 13-14: Ablation Studies. Weeks 15-16: LaTeX Paper & Thesis.",
            "prerequisites": "Advanced algorithms, discrete mathematics, linear algebra, graph theory, Python, and modern deep learning or quantum computing frameworks.",
            "learning_outcomes": "World-class competency in frontier AI/CS research, mathematical modeling, distributed scientific programming, and peer-reviewed scholarly dissemination.",
            "testing_requirements": "Theoretical convergence verification, statistical significance testing (p < 0.01), distributed node fault-tolerance tests, and benchmark comparison against published literature.",
            "expected_output": "Frontier research repository, Dockerized distributed setup, 80+ page research thesis, camera-ready LaTeX conference paper, and scholarly defense slides.",
            "deployment_instructions": "Setup distributed cluster with Docker or Conda, launch Neo4j / Redis backing services, initialize graph seeder, and run benchmark pipeline.",
            "documentation_requirements": "Complete IIT-grade Research Thesis, LaTeX Conference Manuscript, Mathematical Proof Appendix, Benchmark Reproducibility Guide, and Defense Deck.",
            "academic_deliverables": "Frontier Source Code, Pre-trained Checkpoints, Full Thesis (.docx/.pdf), LaTeX Research Manuscript, High-Res Architecture Schematics, Defense Presentation.",
            "is_published": 1,
            "is_featured": 1 if i in [1, 2, 3, 5, 7, 9] else 0,
            "popularity_score": 98 + (i % 3),
            "is_trending": 1 if i in [1, 2, 7] else 0,
            "is_research": 1
        })

    print(f"Prepared {len(projects_data)} detailed project specifications.")
    assert len(projects_data) == 90, f"Error: Expected 90 projects, got {len(projects_data)}"

    # Insert into projects table
    for p in projects_data:
        cur.execute("""
        INSERT INTO projects (
            project_code, title, slug, academic_level, category, subcategory, difficulty,
            duration, price, discount_price, tech_summary, image_url, description,
            problem_statement, proposed_solution, objectives, scope, real_world_apps,
            expected_outcomes, tech_stack_json, features_json, user_roles, architecture,
            database_design, api_docs, development_roadmap, academic_deliverables,
            is_published, is_featured, domain, timeline, prerequisites, learning_outcomes,
            testing_requirements, expected_output, deployment_instructions,
            documentation_requirements, target_users, core_modules_json,
            dfd_description, uml_description, popularity_score, is_trending, is_research
        ) VALUES (
            :project_code, :title, :project_code, :academic_level, :category, :subcategory, :difficulty,
            :duration, :price, :discount_price, :tech_summary, :image_url, :description,
            :problem_statement, :proposed_solution, :objectives, :scope, :real_world_apps,
            :expected_outcomes, :tech_stack_json, :features_json, :user_roles, :architecture,
            :database_design, :api_docs, :development_roadmap, :academic_deliverables,
            :is_published, :is_featured, :domain, :timeline, :prerequisites, :learning_outcomes,
            :testing_requirements, :expected_output, :deployment_instructions,
            :documentation_requirements, :target_users, :core_modules_json,
            :dfd_description, :uml_description, :popularity_score, :is_trending, :is_research
        )
        """, p)

        proj_id = cur.lastrowid

        # Insert 6 standard academic deliverables in project_resources
        deliverables = [
            ("Complete Source Code ZIP", "source_code", f"/static/uploads/resources/{p['project_code']}_source_code.zip", "14.2 MB", "Fully commented source code, dependencies, and environment files."),
            ("IEEE Format Final Report", "report", f"/static/uploads/resources/{p['project_code']}_final_report.pdf", "4.8 MB", "Complete 50-80 page report formatted per university guidelines."),
            ("Software Requirement Specification (SRS)", "srs", f"/static/uploads/resources/{p['project_code']}_srs.pdf", "2.1 MB", "Formal requirements document with functional & non-functional specs."),
            ("System Architecture & ER Diagrams", "diagrams", f"/static/uploads/resources/{p['project_code']}_diagrams.zip", "3.4 MB", "High-res ER diagrams, DFD Level 0/1/2, Class, and Sequence diagrams."),
            ("Presentation Slides (PPT)", "ppt", f"/static/uploads/resources/{p['project_code']}_presentation.pptx", "8.6 MB", "Professional 25-slide defense presentation with speaker notes."),
            ("Viva Voce Question & Answer Bank", "viva", f"/static/uploads/resources/{p['project_code']}_viva_qa.pdf", "1.5 MB", "50+ curated defense questions and model technical answers.")
        ]
        for name, rtype, fpath, fsize, desc in deliverables:
            cur.execute("""
            INSERT INTO project_resources (project_id, resource_name, resource_type, file_path, file_size, description)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (proj_id, name, rtype, fpath, fsize, desc))

    # Update categories table with real counts
    cur.execute("SELECT academic_level, COUNT(*) FROM projects GROUP BY academic_level")
    counts = cur.fetchall()
    print("Project counts in DB by level:", counts)

    for level, count in counts:
        cur.execute("UPDATE categories SET project_count = ? WHERE name = ? OR display_name LIKE ?", (count, level, f"%{level}%"))

    conn.commit()
    conn.close()
    print("Successfully seeded all 90 projects with complete technical specifications and deliverables!")

if __name__ == "__main__":
    generate_catalogue()
