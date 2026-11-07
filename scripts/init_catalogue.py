"""
PROJECTVERSE - Comprehensive Database & Catalogue Builder
Generates all 120 Academic Projects with full technical specifications,
database schema, seed admin & student accounts, and starter deliverables.
"""
import sqlite3
import json
import hashlib
import os

DB_PATH = "projectverse.db"

RAW_CATALOGUE = [
    # BCA Projects (60)
    # Cat 1: AI & ML (BCA001 - BCA010)
    ("BCA001", "AI-Powered Resume Analyzer and Job Recommendation System", "BCA", "Artificial Intelligence & Machine Learning", "Intermediate", "6-8 Weeks", 1899, 2499,
     "Python, FastAPI, React, spaCy, Scikit-learn, SQLite",
     "An intelligent web application that scans resumes using Natural Language Processing (NLP), extracts candidate skills, evaluates ATS compatibility, and recommends matching job openings.",
     "Manual resume screening is slow, inconsistent, and often rejects qualified candidates due to arbitrary ATS filters. Students and job seekers lack clear feedback on why their resumes fail automated screenings.",
     "Deploy an NLP-driven resume parsing engine that extracts skills and experience, computes an ATS match percentage, highlights skill gaps, and recommends matching job openings via cosine similarity.",
     ["Parse PDF/DOCX resumes automatically", "Extract entities: contact, skills, education, experience", "Compute ATS match score against job descriptions", "Recommend relevant job roles based on parsed skills"],
     "Placement cells, job portals, student career services, and HR tech platforms.",
     "Corporate HR departments, university placement cells, and individual job aspirants.",
     "Over 88% skill extraction accuracy, sub-3-second parsing time, and actionable resume optimization reports."),

    ("BCA002", "Intelligent Student Performance Prediction System", "BCA", "Artificial Intelligence & Machine Learning", "Intermediate", "5-7 Weeks", 1499, 1999,
     "Python, FastAPI, Scikit-learn, Chart.js, SQLite",
     "A predictive analytics system that analyzes historical academic data, attendance records, and internal marks to forecast semester exam performance and identify at-risk students.",
     "Educational institutions struggle to identify struggling students early in the semester, leading to higher failure rates and dropout risks without timely academic intervention.",
     "Implement machine learning classification algorithms (Random Forest and Logistic Regression) that evaluate student metrics to predict performance tiers and alert academic mentors.",
     ["Track student attendance and continuous evaluation scores", "Predict final exam performance categories", "Generate early alerts for students at academic risk", "Provide faculty dashboards with remedial action recommendations"],
     "Higher education institutions, colleges, and academic counseling cells.",
     "College academic dean offices, department heads, and faculty mentors.",
     "Early risk detection 4 weeks prior to exams with >90% prediction accuracy."),

    ("BCA003", "AI-Based Career Guidance and Recommendation Platform", "BCA", "Artificial Intelligence & Machine Learning", "Intermediate", "5-6 Weeks", 1499, 1899,
     "Python, FastAPI, Scikit-learn, HTML5, Tailwind CSS",
     "An interactive career assessment platform that evaluates student aptitudes, interests, and academic skills to recommend optimal career pathways and personalized learning roadmaps.",
     "Students often face uncertainty and peer pressure when choosing career specializations, resulting in mismatched skills and career dissatisfaction.",
     "Provide a psychometric and technical assessment engine coupled with K-Nearest Neighbors matching to align candidate profiles with current industry roles and structured roadmaps.",
     ["Interactive multi-domain assessment questionnaire", "Skill-vector computation across technical and analytical domains", "Automated career matching with market demand insights", "Step-by-step milestone learning roadmap generation"],
     "Undergraduate students, career counseling centers, and edtech platforms.",
     "Student career advisory centers, coaching academies, and self-guided learners.",
     "Personalized career match reports with clear 6-month skill development roadmaps."),

    ("BCA004", "Face Recognition-Based Attendance Management System", "BCA", "Artificial Intelligence & Machine Learning", "Intermediate", "6-8 Weeks", 1899, 2499,
     "Python, OpenCV, face_recognition, FastAPI, SQLite",
     "A contactless biometric attendance system using computer vision to detect student faces in real-time camera streams, match against registered profiles, and log attendance logs.",
     "Traditional attendance registers and manual roll calls waste valuable lecture time and are vulnerable to proxy marking.",
     "Utilize deep metric face encodings (128-dimensional vectors) and OpenCV to recognize enrolled student faces in real time and automatically log timestamps in the database.",
     ["Fast student facial enrollment with webcam capture", "Real-time multi-face detection in video stream", "Automatic attendance timestamping with proxy prevention", "Exportable daily and monthly attendance reports in Excel/CSV"],
     "College classrooms, university laboratories, and examination halls.",
     "Academic institutions, corporate training centers, and secure facility check-ins.",
     "Over 95% recognition accuracy under standard indoor lighting with instant record logging."),

    ("BCA005", "AI-Powered College Enquiry Chatbot", "BCA", "Artificial Intelligence & Machine Learning", "Beginner", "4-5 Weeks", 999, 1499,
     "Python, FastAPI, NLTK, HTML5, JavaScript",
     "A 24/7 intelligent conversational bot designed to answer student queries regarding college admissions, fee structures, courses, examination schedules, and campus facilities.",
     "College admission desks and administrative offices receive overwhelming repetitive phone calls and emails during admission seasons.",
     "Deploy an NLP intent-classification chatbot with customizable intent files and fallback assistance to deliver instant, accurate answers around the clock.",
     ["Natural language query understanding and intent recognition", "Pre-trained knowledge base for admissions, courses, and fees", "Interactive quick-reply buttons and brochure download links", "Admin portal to update intents and review unresolved queries"],
     "College websites, admission landing pages, and student portal widgets.",
     "Prospective applicants, enrolled students, and college administrative staff.",
     "Instant query resolution with over 90% accuracy for common institutional queries."),

    ("BCA006", "Fake News Detection Using Machine Learning", "BCA", "Artificial Intelligence & Machine Learning", "Intermediate", "5-6 Weeks", 1299, 1799,
     "Python, Scikit-learn, PassiveAggressiveClassifier, FastAPI, Chart.js",
     "A machine learning text verification portal that evaluates news articles, headlines, and web snippets to predict whether content is authentic or fabricated.",
     "The unchecked dissemination of misinformation and sensationalist fake news creates public confusion and erodes trust in verified information.",
     "Build an NLP classification pipeline using TF-IDF vectorization and a Passive Aggressive Classifier to identify deceptive linguistic patterns in news text.",
     ["Text and URL input for real-time news credibility verification", "TF-IDF n-gram feature extraction and probability scoring", "Highlighting of suspicious phrases and sensationalist keywords", "Verification history log and fact-checking resource links"],
     "Social media monitoring, digital journalism, and media literacy platforms.",
     "Fact-checking organizations, digital readers, and research scholars.",
     "Over 92% classification accuracy on benchmark fake news datasets with instant verdicts."),

    ("BCA007", "AI-Based Disease Prediction System", "BCA", "Artificial Intelligence & Machine Learning", "Intermediate", "6-7 Weeks", 1699, 2199,
     "Python, FastAPI, DecisionTreeClassifier, Tailwind CSS, SQLite",
     "A diagnostic decision-support web application that analyzes user-selected symptoms to predict probable health conditions, severity levels, and relevant specialist recommendations.",
     "Patients often delay seeking timely medical advice or consult the wrong specialists due to lack of accessible preliminary health guidance.",
     "Utilize a trained multi-class Decision Tree model on clinical symptom-disease mapping datasets to provide immediate preliminary evaluations with medical precautions.",
     ["Multi-symptom interactive search and tag selection", "Probable disease identification with confidence percentage", "Recommended medical specialist and precautionary health tips", "Downloadable preliminary assessment report in PDF format"],
     "Telemedicine portals, community health kiosks, and medical advisory apps.",
     "Healthcare clinics, wellness platforms, and patient triage centers.",
     "Instant preliminary health guidance across 42 common diseases with 90%+ diagnostic match."),

    ("BCA008", "Smart Interview Preparation and Evaluation System", "BCA", "Artificial Intelligence & Machine Learning", "Intermediate", "6-8 Weeks", 1899, 2499,
     "Python, FastAPI, Sentence-Transformers, SpeechRecognition, Chart.js",
     "An automated mock interview platform that poses technical and behavioral questions, evaluates spoken or typed responses using semantic NLP, and provides detailed performance feedback.",
     "Students struggle in campus placements due to lack of realistic interview practice, poor articulation, and absence of structured feedback.",
     "Build a virtual interviewer that poses role-specific questions, transcribes speech, evaluates answer completeness via semantic similarity, and scores responses across key competencies.",
     ["Role-based interview simulation (Full Stack, Python, HR, Management)", "Speech-to-text response capture with typing alternative", "Semantic scoring against benchmark answers and keyword coverage", "Comprehensive performance report with radar charts and tips"],
     "College training and placement cells, coding bootcamps, and career mentoring.",
     "Graduating students, placement officers, and job recruitment trainers.",
     "Actionable scoring across technical accuracy, clarity, and keyword coverage in under 5 seconds."),

    ("BCA009", "AI-Powered Personal Finance Assistant", "BCA", "Artificial Intelligence & Machine Learning", "Intermediate", "5-6 Weeks", 1399, 1899,
     "Python, FastAPI, Scikit-learn, Chart.js, SQLite",
     "A smart personal budgeting and expense tracking application that automatically categorizes transactions, forecasts future expenditure trends, and alerts users to overspending risks.",
     "Individuals frequently struggle to maintain budgeting discipline and lack visibility into recurring expense patterns across multiple payment channels.",
     "Use machine learning text classification to automatically categorize expenses from descriptions and apply linear regression to forecast end-of-month financial trajectories.",
     ["Natural language expense logging with automated category tagging", "Monthly budget tracking against user-defined spending limits", "Spending forecasting and predictive budget overrun warnings", "Interactive cashflow diagrams and category distribution charts"],
     "Personal finance, student money management, and small business expense logging.",
     "Students, freelancers, young professionals, and household budget managers.",
     "Automated categorization with >94% accuracy and proactive budget alerts."),

    ("BCA010", "Intelligent Document Classification System", "BCA", "Artificial Intelligence & Machine Learning", "Intermediate", "5-7 Weeks", 1599, 2099,
     "Python, FastAPI, Scikit-learn, PyPDF2, SQLite",
     "An automated document organization portal that ingests PDF and text files, classifies them into legal, financial, academic, or HR domains, and extracts critical metadata.",
     "Organizations face productivity bottlenecks from manually sorting, indexing, and filing thousands of incoming digital documents.",
     "Construct a machine learning document classifier using TF-IDF feature extraction and Support Vector Machines (SVM) to index and organize files automatically.",
     ["Multi-format file upload (PDF, DOCX, TXT) with drag-and-drop", "Automated domain categorization with confidence score", "Key phrase extraction and metadata indexing (dates, entities)", "Full-text search and organized archive explorer"],
     "Enterprise document management, college administrative archives, and legal offices.",
     "Administrative staff, office managers, and compliance auditors.",
     "Over 93% classification accuracy with automated folder routing and search indexing."),

    # Cat 2: Full Stack Web Development (BCA011 - BCA020)
    ("BCA011", "Advanced Student Management System", "BCA", "Full Stack Web Development", "Intermediate", "5-6 Weeks", 1299, 1799,
     "React / HTML5, FastAPI, SQLite / PostgreSQL, Bootstrap",
     "A comprehensive institutional portal for managing student academic records, course enrollments, attendance tracking, fee receipts, and performance grade sheets.",
     "Colleges maintaining disparate paper records or disconnected spreadsheets suffer from data discrepancies, delayed reporting, and administrative overhead.",
     "Deliver a unified role-based web application with secure authentication for administrators, faculty, and students to streamline institutional recordkeeping.",
     ["Student admission and profile record management", "Course enrollment and semester subject allocation", "Continuous assessment marks entry and grade calculation", "Fee payment tracking with receipt generation"],
     "Degree colleges, polytechnic institutions, and vocational training schools.",
     "College registrars, department heads, faculty members, and students.",
     "Centralized digital records with zero paperwork and automated GPA computation."),

    ("BCA012", "College Placement Management Portal", "BCA", "Full Stack Web Development", "Intermediate", "6-7 Weeks", 1699, 2199,
     "React / Tailwind CSS, Python, FastAPI, SQLite",
     "A centralized recruitment coordination platform connecting students, college placement officers, and corporate recruiters for job drives, applications, and shortlisting.",
     "Placement drives involve cumbersome coordination across hundreds of eligible students, scattered resumes, and slow interview scheduling.",
     "Provide a streamlined portal where recruiters post job eligibility criteria, students apply with verified academic profiles, and placement officers monitor hiring statistics.",
     ["Company registration and campus drive posting", "Automated student eligibility screening based on CGPA and backlogs", "One-click application submission with resume attachment", "Placement drive rounds scheduling and offer letter tracking"],
     "University placement directorates, training departments, and recruiting firms.",
     "Training & placement officers (TPO), student applicants, and HR recruiters.",
     "Automated eligibility filtering saving 80% administrative effort during campus drives."),

    ("BCA013", "Online Examination and Assessment Platform", "BCA", "Full Stack Web Development", "Intermediate", "6-8 Weeks", 1899, 2499,
     "FastAPI, JavaScript, HTML5, SQLite, Tailwind CSS",
     "A secure web-based testing platform featuring timed multiple-choice assessments, randomized question banks, automated evaluation, and instant performance scorecards.",
     "Conducting pen-and-paper assessments is resource-intensive, slow to evaluate, and susceptible to manual grading errors.",
     "Develop a responsive online examination engine with countdown timers, question randomization, auto-save capabilities, and instant result analytics.",
     ["Teacher question bank creation with categorization and difficulty levels", "Timed online exams with auto-submission on expiration", "Randomized question sequences to deter cheating", "Instant automatic score calculation with detailed answer reviews"],
     "Educational institutions, entrance exam centers, and recruitment screening tests.",
     "Examiners, school/college teachers, and examination candidates.",
     "Zero-latency automated grading with anti-cheating browser blur tracking."),

    ("BCA014", "Hospital Management System", "BCA", "Full Stack Web Development", "Intermediate", "6-8 Weeks", 1799, 2399,
     "Python, FastAPI, SQLite, Tailwind CSS, Lucide Icons",
     "An integrated healthcare facility management portal managing outpatient appointments, doctor schedules, patient medical histories, and digital billing.",
     "Small and medium hospitals struggle with unorganized patient queues, lost paper prescription records, and disconnected billing counters.",
     "Implement a multi-tier clinical administration system linking front-desk appointments, doctor consultation desks, and pharmacy billing into one database.",
     ["Patient registration and OPD appointment booking", "Doctor daily roster and consultation queue management", "Digital prescription writing and diagnosis record storage", "OPD billing and receipt generation with payment tracking"],
     "Clinics, nursing homes, polyclinics, and diagnostic centers.",
     "Receptionists, consulting doctors, hospital administrators, and patients.",
     "Reduced patient wait times and instant access to longitudinal medical records."),

    ("BCA015", "Apartment Management and Maintenance System", "BCA", "Full Stack Web Development", "Intermediate", "5-6 Weeks", 1399, 1899,
     "HTML5, Tailwind CSS, Python, FastAPI, SQLite",
     "A residential society portal for managing flat owner records, monthly maintenance fee invoicing, facility bookings, and resident complaint resolution.",
     "Gated communities and apartment associations struggle with uncoordinated maintenance fee collection, transparency issues, and delayed complaint handling.",
     "Provide a transparent community platform where residents pay dues, book amenities (clubhouse, gym), and track maintenance tickets in real time.",
     ["Resident directory and flat ownership ledger", "Automated monthly maintenance bill generation", "Facility and clubhouse reservation calendar", "Helpdesk ticket logging with status tracking (Open, In-Progress, Resolved)"],
     "Residential housing societies, gated communities, and real estate associations.",
     "Society management committee, flat owners, tenants, and security staff.",
     "100% transparent society accounting and faster resolution of resident grievances."),

    ("BCA016", "Online Learning Management System", "BCA", "Full Stack Web Development", "Intermediate", "6-7 Weeks", 1699, 2199,
     "FastAPI, JavaScript, Tailwind CSS, SQLite, Video Embeds",
     "A dynamic e-learning portal enabling instructors to publish modular video courses, upload study notes, organize module quizzes, and track learner progress.",
     "Distance education and remote training programs need structured content delivery platforms with integrated assessments and progress analytics.",
     "Build a responsive LMS where educators structure lessons into sequential modules and students view lectures, download materials, and earn completion badges.",
     ["Instructor course creation with video embeds and PDF resources", "Student enrollment and curriculum progress percentage tracking", "End-of-module assessment quizzes with minimum passing thresholds", "Discussion forum per lesson for peer and tutor Q&A"],
     "Corporate training teams, coaching centers, and private online educators.",
     "Course instructors, enrolled students, and platform administrators.",
     "Structured self-paced learning with real-time course completion telemetry."),

    ("BCA017", "E-Commerce Shopping Platform", "BCA", "Full Stack Web Development", "Intermediate", "6-7 Weeks", 1599, 2099,
     "Python, FastAPI, SQLite, Tailwind CSS, JavaScript",
     "A full-featured digital retail storefront with product catalog browsing, faceted filtering, dynamic shopping cart, address management, and order checkout.",
     "Retail businesses transitioning online require dependable, responsive e-commerce web applications without heavy licensing costs.",
     "Create a complete e-commerce application featuring catalog search, category navigation, shopping cart sessions, mock payment processing, and order status updates.",
     ["Product catalog with multiple images, specifications, and inventory counts", "Live search, price range filtering, and category sorting", "Shopping cart with quantity updates and order summary calculations", "Customer checkout flow with order history and tracking"],
     "Small businesses, retail shops, and niche merchandise sellers.",
     "Store customers, inventory managers, and store administrators.",
     "Smooth shopping experience with persistent cart and order fulfillment workflows."),

    ("BCA018", "Library Management and Book Recommendation System", "BCA", "Full Stack Web Development", "Intermediate", "5-6 Weeks", 1399, 1899,
     "FastAPI, SQLite, Tailwind CSS, JavaScript",
     "A modern digital library administration platform featuring automated book issue/return tracking, fine calculation for overdue items, and genre-based recommendations.",
     "College libraries face cataloging bottlenecks, unreturned books, and manual fine calculation errors when using outdated register systems.",
     "Deploy an automated library catalog with ISBN tracking, student borrowing limits, overdue fine calculations, and collaborative book suggestions.",
     ["Comprehensive book catalog with ISBN, author, and shelf location", "Student issue and return workflow with barcode/ID support", "Automated overdue fine computation based on return due dates", "Genre and author-based reading recommendation engine"],
     "School and college libraries, departmental book banks, and reading clubs.",
     "Librarians, assistant staff, students, and faculty borrowers.",
     "Zero book loss, automated overdue calculations, and improved book circulation."),

    ("BCA019", "Smart Inventory and Billing Management System", "BCA", "Full Stack Web Development", "Intermediate", "5-6 Weeks", 1499, 1999,
     "Python, FastAPI, SQLite, Tailwind CSS, Printable Invoices",
     "A point-of-sale inventory and billing web application for retail and wholesale merchants featuring stock alerts, GST calculation, and printable thermal invoices.",
     "Small retailers suffer financial leakage from untracked inventory shrinkage, stock-outs of high-demand items, and slow manual billing.",
     "Implement an inventory ledger that automatically deducts stock upon billing, calculates tax rates, issues formatted invoices, and flags low-stock items.",
     ["Product SKU management with purchase and selling price records", "Fast barcode/code search for rapid point-of-sale item addition", "Automated GST/tax computation and discount deduction", "Low-stock automated warning thresholds and supplier purchase orders"],
     "Retail outlets, hardware stores, grocery marts, and electronics shops.",
     "Cashiers, warehouse storekeepers, and business owners.",
     "Rapid checkout under 30 seconds per invoice and real-time inventory visibility."),

    ("BCA020", "College Event Management Platform", "BCA", "Full Stack Web Development", "Beginner", "4-5 Weeks", 999, 1499,
     "HTML5, Tailwind CSS, FastAPI, SQLite, QR Tickets",
     "A centralized campus events portal for announcing college festivals, technical symposiums, and cultural competitions with online registrations and digital passes.",
     "Campus event coordination via paper forms and WhatsApp leads to chaotic registrations, double bookings, and gate management headaches.",
     "Create a centralized campus event hub where student clubs publish event schedules, manage team registrations, and verify attendee entry using QR tickets.",
     ["Event catalog categorized by Technical, Cultural, Sports, and Workshops", "Single and team registration workflows with participant verification", "Digital e-ticket generation with unique QR verification codes", "Club coordinator dashboard for attendee check-in and attendance logs"],
     "University student councils, campus clubs, and academic departments.",
     "Club presidents, faculty coordinators, and student participants.",
     "Effortless campus-wide event coordination with digital paperless ticketing."),

    # Cat 3: Python & Automation (BCA021 - BCA030)
    ("BCA021", "AI-Powered Email Classification and Automation", "BCA", "Python & Automation", "Intermediate", "5-6 Weeks", 1399, 1899,
     "Python, IMAP/SMTP, Scikit-learn, FastAPI, SQLite",
     "An intelligent inbox automation utility that connects to email accounts, categorizes messages into Priority, Newsletter, Support, or Spam, and triggers automated replies.",
     "Support teams and professionals spend hours daily sorting emails, resulting in slow turnaround times for urgent inquiries.",
     "Build a Python automation script that reads incoming emails via IMAP, applies an NLP Naive Bayes classifier, tags messages, and sends automated template replies.",
     ["Secure IMAP/SMTP connection with OAuth / App Passwords", "NLP text categorization into predefined business buckets", "Automated rule-based autoreplies for common queries", "Dashboard showing email distribution analytics and response times"],
     "Customer support inboxes, freelance professionals, and executive mail sorting.",
     "Support agents, inbox administrators, and business professionals.",
     "Over 90% inbox triage accuracy, saving 2+ hours of manual sorting daily."),

    ("BCA022", "Automated Invoice Generation System", "BCA", "Python & Automation", "Beginner", "4-5 Weeks", 899, 1399,
     "Python, ReportLab, Pandas, FastAPI, SQLite",
     "A Python-driven batch billing automation tool that ingests client service spreadsheets, computes taxes, and compiles professional branded PDF invoices automatically.",
     "Generating dozens or hundreds of recurring invoices manually each month is tedious, prone to calculation errors, and delays client payment cycles.",
     "Develop an automated Python invoice pipeline using ReportLab that reads billing data from Excel/CSV and outputs standardized, audit-ready PDF invoices.",
     ["Batch Excel/CSV file upload with client billing items", "Automated tax calculation, discounts, and currency formatting", "High-resolution branded PDF invoice generation with tables", "Automated email dispatch with attached PDF invoices"],
     "Freelancers, IT service agencies, consultancy firms, and subscription services.",
     "Accountants, billing managers, and business owners.",
     "Instant generation of 500+ formatted invoices in under 30 seconds."),

    ("BCA023", "Smart Expense Tracker with Analytics", "BCA", "Python & Automation", "Beginner", "4-5 Weeks", 799, 1299,
     "Python, SQLite, Matplotlib, Tailwind CSS, FastAPI",
     "A practical daily expense management application with automated receipt summary generation, budget threshold alerts, and monthly visual financial analytics.",
     "Students and young earners struggle to maintain financial discipline without simple, automated tools that visualize where their money goes.",
     "Create a lightweight, accessible tracker with category-based expense logging, daily balance recalculations, and automated monthly spending summaries.",
     ["Fast expense and income entry with customizable category tags", "Automated calculation of savings rate and daily spending average", "Monthly spending trends and category breakdown pie charts", "Exportable monthly financial summary reports"],
     "Students, individuals, and small household budgeting.",
     "Individual users and family budget trackers.",
     "Clear financial visibility with automated monthly expense audits."),

    ("BCA024", "Python-Based Desktop Management Application", "BCA", "Python & Automation", "Beginner", "4-5 Weeks", 899, 1399,
     "Python, Tkinter / CustomTkinter, Psutil, OS Libraries",
     "A native desktop utility that monitors system resources (CPU, RAM, Disk), cleans temporary clutter files, manages startup items, and provides batch file renaming.",
     "Everyday computer users suffer from sluggish PC performance due to accumulated cache junk, unorganized files, and rogue background processes.",
     "Develop a desktop system suite using Python and psutil that cleans cache, visualizes hardware telemetry, and provides batch file management tools.",
     ["Real-time CPU, RAM, and Disk utilization telemetry graphs", "One-click junk and temporary file scanner and safe cleaner", "Batch file renamer with regex and sequential numbering", "Process manager to identify and safely terminate heavy processes"],
     "Personal computers, computer labs, and office workstations.",
     "Lab assistants, IT support technicians, and everyday PC users.",
     "Reclaims gigabytes of disk space and provides instant system diagnostics."),

    ("BCA025", "Automated Web Scraping and Price Monitoring System", "BCA", "Python & Automation", "Intermediate", "5-6 Weeks", 1399, 1899,
     "Python, BeautifulSoup4, Requests, APScheduler, FastAPI",
     "An automated price intelligence tool that scrapes e-commerce product pages at scheduled intervals, tracks price drops, and alerts users via email or web notifications.",
     "Shoppers and procurement agents miss optimal purchase windows because manually checking fluctuating e-commerce prices is tedious.",
     "Build an automated scraper with scheduler background tasks that monitors product URLs, records price history in SQLite, and fires alerts on price cuts.",
     ["Product URL addition with selector extraction engine", "Automated background cron scraping every hour or day", "Interactive historical price fluctuation charts", "Instant email/web alert triggered when price drops below target"],
     "Online bargain hunting, e-commerce market intelligence, and procurement.",
     "Online shoppers, retail analysts, and procurement officers.",
     "Reliable automated price tracking with zero manual intervention."),

    ("BCA026", "Intelligent File Management and Organizer", "BCA", "Python & Automation", "Beginner", "4-5 Weeks", 899, 1399,
     "Python, Watchdog, Shutil, OS, Tkinter / Web UI",
     "An automated directory monitoring tool that watches the Downloads and Desktop folders, automatically sorting files into organized subfolders by type and date.",
     "User storage folders quickly become cluttered dumping grounds, making file retrieval tedious and wasting valuable local storage.",
     "Implement a background daemon using Python's Watchdog library that detects new files and automatically routes them to Documents, Images, Code, or Archives.",
     ["Real-time directory monitoring of target folders (Downloads, Desktop)", "Rule-based routing based on file extension, size, and creation date", "Duplicate file finder using MD5 checksum hashing", "Detailed organization audit log with one-click undo functionality"],
     "Personal workstations, office desktops, and institutional lab computers.",
     "Students, office workers, and laboratory administrators.",
     "Maintains clean, organized directories automatically without manual effort."),

    ("BCA027", "Automated Report Generation System", "BCA", "Python & Automation", "Intermediate", "5-6 Weeks", 1299, 1799,
     "Python, Pandas, Jinja2, WeasyPrint / ReportLab, FastAPI",
     "An automated business reporting engine that connects to raw operational databases, performs statistical aggregations, and compiles polished executive PDF reports.",
     "Operational teams spend days every month manually compiling spreadsheets, building charts, and formatting PowerPoint or PDF executive summaries.",
     "Develop a data-to-document pipeline in Python that queries database metrics, calculates KPIs, embeds charts, and generates executive-ready PDF reports on schedule.",
     ["Database query connectors for sales, attendance, and inventory data", "Automated KPI calculation (growth rate, totals, averages, outliers)", "Dynamic chart generation using Matplotlib and embedding into PDF", "Scheduled report dispatch to stakeholder email distribution lists"],
     "Corporate operations, college academic audits, and sales organizations.",
     "Department managers, academic coordinators, and data analysts.",
     "Automates hours of monthly reporting work into a single automated trigger."),

    ("BCA028", "AI-Powered Customer Support System", "BCA", "Python & Automation", "Intermediate", "5-6 Weeks", 1499, 1999,
     "Python, FastAPI, Scikit-learn, SQLite, Tailwind CSS",
     "A smart helpdesk ticketing platform that analyzes customer problem descriptions, predicts ticket priority, routes issues to relevant departments, and drafts replies.",
     "Customer service desks face high backlogs and delayed response times because support tickets must be manually read, categorized, and assigned.",
     "Deploy an NLP classification pipeline that tags incoming customer tickets, predicts urgency (Urgent, High, Normal), and suggests standard troubleshooting steps.",
     ["Customer ticket submission portal with issue description and attachments", "Automated issue category tagging (Billing, Technical, Account, Hardware)", "Urgency detection and automated routing to specialist agents", "Agent workspace with AI-suggested response templates"],
     "E-commerce customer service, SaaS software helpdesks, and IT service teams.",
     "Customer support agents, team leads, and end consumers.",
     "60% reduction in first-response time with automated triage."),

    ("BCA029", "Personal Productivity and Task Automation Assistant", "BCA", "Python & Automation", "Beginner", "4-5 Weeks", 899, 1399,
     "Python, SQLite, APScheduler, Tailwind CSS, FastAPI",
     "A personal productivity suite combining a Pomodoro timer, prioritized task Kanban boards, recurring habit streaks, and automated desktop reminders.",
     "Students and remote workers struggle with digital distractions, missed task deadlines, and disorganized daily routines.",
     "Create a lightweight, distraction-free productivity dashboard that synchronizes daily tasks, schedules focus blocks, and tracks habit consistency over time.",
     ["Kanban task board with To-Do, In-Progress, and Completed columns", "Integrated Pomodoro focus timer with audible notifications", "Daily habit tracker with streak counters and completion logs", "Daily morning agenda summary and end-of-day accomplishment logs"],
     "Student study routines, freelance project tracking, and remote work discipline.",
     "Students, developers, and knowledge workers.",
     "Improved daily focus and measurable completion rates across academic tasks."),

    ("BCA030", "Smart Data Cleaning and Analysis Platform", "BCA", "Python & Automation", "Intermediate", "5-6 Weeks", 1399, 1899,
     "Python, Pandas, NumPy, FastAPI, Tailwind CSS",
     "An automated web-based data wrangling tool that ingests messy CSV/Excel datasets, detects missing values and anomalies, executes cleaning recipes, and exports clean data.",
     "Data analysts spend over 70% of their project time doing repetitive, tedious data cleaning and formatting tasks before any analysis can begin.",
     "Build an intuitive web interface backed by Pandas that automatically identifies data type mismatches, missing values, duplicates, and outliers with one-click cleanup options.",
     ["CSV and Excel dataset upload with instant structural summary", "Automated detection of nulls, duplicates, and format inconsistencies", "One-click cleaning recipes (imputation, deduplication, normalization)", "Descriptive statistical summary and clean dataset export"],
     "Data analytics training, research projects, and small business data audits.",
     "Student researchers, data science beginners, and business analysts.",
     "Reduces raw data preparation time from hours to minutes."),

    # Cat 4: Data Science & Business Intelligence (BCA031 - BCA040)
    ("BCA031", "Student Admission Data Analytics Dashboard", "BCA", "Data Science & Business Intelligence", "Intermediate", "5-6 Weeks", 1399, 1899,
     "Python, Pandas, Plotly / Chart.js, FastAPI, SQLite",
     "An institutional business intelligence dashboard visualizing multi-year student admission trends, demographic distributions, cut-off percentages, and course popularity.",
     "College admission directorates lack interactive visual tools to understand shifting applicant demographics, geographic catchment areas, and course demand.",
     "Implement an interactive data analytics dashboard that aggregates historical admission figures and presents key institutional KPIs via interactive charts.",
     ["Multi-year admission intake comparison by course and department", "Geographical heatmaps of incoming student hometowns and schools", "Cut-off marks trend lines and gender diversity ratios", "Predictive seat occupancy estimation for upcoming academic terms"],
     "College management boards, university admissions teams, and accreditation reviews.",
     "Admission deans, college trustees, and institutional researchers.",
     "Data-backed insights for academic course planning and marketing allocations."),

    ("BCA032", "Sales Forecasting and Business Intelligence System", "BCA", "Data Science & Business Intelligence", "Intermediate", "6-7 Weeks", 1699, 2199,
     "Python, Statsmodels / Scikit-learn, Pandas, Chart.js, FastAPI",
     "A time-series forecasting web application that analyzes historical retail sales figures to project future revenue, identify seasonality, and optimize inventory purchasing.",
     "Retailers face cash flow challenges and stock-outs because they rely on gut feeling rather than scientific time-series forecasting for ordering inventory.",
     "Deploy time-series modeling (ARIMA and Linear Trend Analysis) on historical sales data to forecast weekly and monthly demand curves with confidence intervals.",
     ["Historical sales dataset upload and automated cleaning", "Time-series decomposition into trend, seasonality, and residual noise", "30-day and 90-day future sales projections with confidence bounds", "Product-level revenue contribution Pareto analysis (80/20 rule)"],
     "Retail stores, wholesale distributors, and e-commerce merchants.",
     "Inventory planners, sales directors, and business executives.",
     "Over 88% forecast accuracy, reducing surplus inventory holding costs."),

    ("BCA033", "Customer Segmentation Using Machine Learning", "BCA", "Data Science & Business Intelligence", "Intermediate", "5-6 Weeks", 1499, 1999,
     "Python, Scikit-learn (K-Means), Pandas, Plotly, FastAPI",
     "An unsupervised machine learning portal that clusters retail customer bases into distinct behavioral personas using RFM (Recency, Frequency, Monetary) metrics.",
     "Marketing campaigns suffer from low conversion rates when businesses treat all customers uniformly instead of tailoring offers to distinct customer segments.",
     "Apply K-Means clustering to customer transaction data to categorize buyers into VIPs, Loyalists, Occasional Buyers, and At-Risk segments with targeted marketing advice.",
     ["Customer transaction data ingestion and RFM score calculation", "Optimal cluster detection using the Elbow Method and Silhouette Analysis", "Interactive 2D and 3D customer cluster visualization plots", "Actionable marketing recommendations tailored to each customer segment"],
     "Retail chains, e-commerce stores, and loyalty program management.",
     "Marketing managers, CRM leads, and business analysts.",
     "Clear behavioral segmentation enabling targeted promotions and higher retention."),

    ("BCA034", "Employee Attrition Prediction System", "BCA", "Data Science & Business Intelligence", "Intermediate", "6-7 Weeks", 1599, 2099,
     "Python, Scikit-learn (RandomForest), FastAPI, Chart.js, SQLite",
     "A predictive HR analytics platform that analyzes workplace satisfaction, overtime hours, salary bands, and tenure to identify employees at high risk of resigning.",
     "Employee turnover is costly and disruptive, yet HR teams rarely have early warning signs before a valuable team member hands in their resignation.",
     "Train a Random Forest classifier on organizational HR data to compute flight-risk probabilities and highlight primary drivers of employee dissatisfaction.",
     ["Employee profile ingestion and historical tenure metrics", "Individual and department-level attrition risk probability scores", "Feature importance charts highlighting top turnover drivers (pay, hours, role)", "Retention strategy recommendations for HR business partners"],
     "Corporate HR departments, IT consultancy firms, and talent management agencies.",
     "HR directors, team managers, and talent retention officers.",
     "Identifies flight-risk talent with >89% accuracy months before resignation."),

    ("BCA035", "Retail Store Performance Analytics", "BCA", "Data Science & Business Intelligence", "Intermediate", "5-6 Weeks", 1399, 1899,
     "Python, Pandas, FastAPI, Chart.js, SQLite",
     "A multi-outlet retail business intelligence portal tracking key store performance metrics including footfall, average basket size, category margins, and cashier efficiency.",
     "Retail chain managers struggle to compare performance across multiple store branches when data remains trapped in isolated branch POS databases.",
     "Build an aggregated analytics dashboard that consolidates multi-store transaction streams into executive scorecards with benchmark rankings.",
     ["Multi-branch revenue, footfall, and gross margin comparison", "Top-selling SKUs and dead-stock identification across outlets", "Peak shopping hours heatmap for optimal staff scheduling", "Employee sales performance and billing speed leaderboards"],
     "Supermarket chains, retail apparel franchises, and multi-location businesses.",
     "Retail operations heads, store managers, and regional directors.",
     "Actionable insights driving 15% improvement in multi-outlet inventory turn."),

    ("BCA036", "Stock Market Data Analysis Dashboard", "BCA", "Data Science & Business Intelligence", "Intermediate", "5-6 Weeks", 1499, 1999,
     "Python, yfinance / Pandas, Plotly / Lightweight Charts, FastAPI",
     "An interactive equity research dashboard providing historical stock price visualizations, technical indicators (SMA, EMA, RSI, MACD), and volatility metrics.",
     "Retail investors lack affordable, intuitive tools to analyze stock price movements, technical momentum signals, and historical risk indicators.",
     "Create a financial charting web application that fetches live and historical ticker data, computes technical indicators, and visualizes candlestick charts.",
     ["Ticker search with real-time and historical candlestick chart feeds", "Technical indicator overlays: 50/200 SMA, Exponential MA, RSI, MACD", "Historical volatility and drawdown risk calculations", "Volume distribution profiles and price alert trigger settings"],
     "Retail stock trading education, finance student projects, and investment clubs.",
     "Finance students, amateur stock traders, and equity analysts.",
     "Clear technical visualization empowering disciplined, data-driven investing."),

    ("BCA037", "E-Commerce Customer Behaviour Analysis", "BCA", "Data Science & Business Intelligence", "Intermediate", "5-6 Weeks", 1499, 1999,
     "Python, Pandas, Scikit-learn, Chart.js, FastAPI",
     "A clickstream and purchase funnel analytics dashboard that tracks user drop-off stages, shopping cart abandonment rates, and product view-to-purchase conversion.",
     "E-commerce websites lose significant revenue at intermediate checkout stages without knowing which page or UX friction point is causing the abandonment.",
     "Build a conversion funnel visualization system that maps customer journeys from product view to payment confirmation and identifies leakage points.",
     ["Multi-stage conversion funnel: View -> Cart -> Checkout -> Purchase", "Cart abandonment rate tracking and abandoned revenue calculation", "Product pairing affinity analysis (frequently bought together)", "User device and referral source conversion breakdown"],
     "E-commerce storefronts, digital marketing agencies, and UX design audits.",
     "E-commerce store owners, digital marketers, and growth engineers.",
     "Pinpoints checkout drop-off bottlenecks, enabling targeted CRO improvements."),

    ("BCA038", "Student Placement Analytics Dashboard", "BCA", "Data Science & Business Intelligence", "Intermediate", "5-6 Weeks", 1399, 1899,
     "Python, Pandas, FastAPI, Chart.js, SQLite",
     "A dedicated institutional analytics portal tracking campus placement statistics, average salary packages, recruiter hiring patterns, and department-wise placement rates.",
     "Universities need accurate, audit-compliant placement analytics for regulatory bodies (NAAC/NIRF) and prospective student prospectuses.",
     "Develop a comprehensive placement intelligence portal with interactive drill-down charts showing placement percentages, CTC ranges, and recruiter loyalty.",
     ["Department-wise placed student percentages and backlog correlations", "Salary package distribution graphs (Highest, Average, Median CTC)", "Recruiting company hiring history and industry sector breakdown", "Automated NIRF / NAAC placement data summary report generation"],
     "College placement directorates, accreditation committees, and college leadership.",
     "Placement officers, department heads, and accreditation coordinators.",
     "Instant generation of verified placement reports for NIRF and NAAC accreditation."),

    ("BCA039", "Crime Data Analysis and Visualization System", "BCA", "Data Science & Business Intelligence", "Intermediate", "5-6 Weeks", 1499, 1999,
     "Python, Pandas, Folium / Leaflet, FastAPI, SQLite",
     "A spatial-temporal public safety analytics portal mapping crime incident reports, identifying high-risk geographic hotspots, and analyzing seasonal crime patterns.",
     "Law enforcement agencies and urban researchers require visual, map-based analytical tools to deploy police patrols effectively based on empirical crime trends.",
     "Build a geospatial analytics web dashboard utilizing Leaflet and Pandas to visualize crime density heatmaps, filter by crime category, and inspect temporal spikes.",
     ["Incident reporting and categorizing (Theft, Burglary, Cyber, Assault)", "Interactive geographic crime density heatmap and cluster markers", "Time-of-day and day-of-week incident frequency bar charts", "Patrol route optimization suggestions based on historical hotspots"],
     "Municipal police departments, urban safety research, and neighborhood watch groups.",
     "Law enforcement planners, city administrators, and public safety researchers.",
     "Empirical hotspot visualization assisting proactive police resource deployment."),

    ("BCA040", "Financial Performance Analysis Dashboard", "BCA", "Data Science & Business Intelligence", "Intermediate", "5-6 Weeks", 1499, 1999,
     "Python, Pandas, FastAPI, Chart.js, SQLite",
     "A corporate financial health dashboard calculating key accounting ratios (Liquidity, Solvency, Profitability) and visualizing quarterly income statements and balance sheets.",
     "Business owners and finance students struggle to interpret dense accounting ledgers without interactive ratio analysis and visual trend benchmarks.",
     "Create a financial intelligence dashboard that computes Dupont analysis, Quick Ratio, Debt-to-Equity, and Operating Margins from standard financial statements.",
     ["Balance sheet and Profit & Loss statement data ingestion", "Automated computation of 15+ financial ratios across 4 categories", "Interactive year-over-year revenue and expense trend analysis", "Financial health score and bankruptcy risk indicators (Altman Z-Score)"],
     "SME financial auditing, business incubators, and corporate finance classrooms.",
     "Chief financial officers, business owners, and accounting students.",
     "Instant financial diagnostic health check with clear comparative ratio charts."),

    # Cat 5: Mobile & Modern Applications (BCA041 - BCA050)
    ("BCA041", "Smart Grocery Shopping Mobile Application", "BCA", "Mobile & Modern Applications", "Intermediate", "6-7 Weeks", 1699, 2199,
     "React Native / PWA, FastAPI, SQLite, Tailwind CSS",
     "A responsive mobile-first shopping app for local grocery orders featuring digital aisle navigation, recurring shopping lists, and scheduled doorstep delivery.",
     "Neighborhood grocery stores lose customers to major delivery apps because they lack accessible digital ordering systems tailored for regular customers.",
     "Build a lightweight, mobile-responsive PWA enabling neighborhood customers to browse fresh produce, maintain weekly recurring lists, and schedule delivery slots.",
     ["Category-wise grocery catalog with weight and price variants", "Smart recurring grocery list generator with one-tap reordering", "Delivery time slot selection and cash/UPI payment options", "Order status tracking from packing to out-for-delivery"],
     "Local supermarkets, neighborhood grocery stores, and residential societies.",
     "Shoppers, store cashiers, and local delivery runners.",
     "Frictionless grocery ordering experience on any smartphone browser."),

    ("BCA042", "Online Food Ordering and Delivery Application", "BCA", "Mobile & Modern Applications", "Intermediate", "6-7 Weeks", 1799, 2399,
     "React / Mobile Web, FastAPI, SQLite, Leaflet Maps",
     "A complete food delivery ordering portal featuring restaurant digital menus, item customization (toppings, spice level), live order tracking, and cart management.",
     "Independent restaurants lose heavy commissions to third-party delivery aggregators and need direct customer ordering portals.",
     "Develop a full-stack food ordering platform with category browsing, special dietary filters, add-ons management, and simulated rider tracking on a map.",
     ["Restaurant digital menu with photo gallery and item customizations", "Live cart with tax, delivery charge, and discount coupon engine", "Simulated real-time delivery tracking with interactive map updates", "Customer order history and instant receipt reordering"],
     "Independent restaurants, cloud kitchens, and campus food courts.",
     "Hungry customers, kitchen chefs, and restaurant managers.",
     "Direct restaurant ordering saving 25%+ aggregator commission charges."),

    ("BCA043", "Personal Fitness Tracking Application", "BCA", "Mobile & Modern Applications", "Beginner", "4-5 Weeks", 899, 1399,
     "HTML5 / PWA, Tailwind CSS, JavaScript, SQLite, Chart.js",
     "A mobile-responsive fitness companion tracking daily calorie intake, workout routines, water hydration milestones, and body weight progression charts.",
     "Fitness beginners struggle to maintain workout consistency and balance calorie intake without complicated, subscription-heavy fitness apps.",
     "Build an accessible fitness logging app that calculates BMI, estimates daily caloric burn, and visualizes weekly workout consistency.",
     ["Workout routine logger with exercise library (sets, reps, weights)", "Daily calorie and macro-nutrient tracker with food database", "Water intake tracker with milestone progress bar", "Body weight progression trend line and BMI indicator"],
     "Personal health, student fitness tracking, and fitness coaching clients.",
     "Gym enthusiasts, fitness beginners, and personal fitness trainers.",
     "Clean, distraction-free health habit tracking without subscription barriers."),

    ("BCA044", "Blood Donor and Emergency Management Application", "BCA", "Mobile & Modern Applications", "Intermediate", "5-6 Weeks", 1499, 1999,
     "HTML5 / Mobile Web, FastAPI, SQLite, Geolocation, SMS Alerts",
     "A life-saving community healthcare portal connecting voluntary blood donors with hospitals and emergency patients based on blood group and geographic proximity.",
     "Finding rare blood groups during hospital emergencies is agonizingly slow when families rely on unstructured social media broadcast messages.",
     "Develop a location-aware donor registry that matches emergency blood requests with verified nearby donors and sends instant notifications.",
     ["Voluntary donor registration with blood group, city, and last donation date", "Emergency blood request broadcast with hospital location and units needed", "Proximity and blood compatibility matching algorithm (O-, AB+, etc.)", "Donor privacy protection with masked communication links"],
     "Hospital blood banks, Red Cross chapters, and student voluntary organizations.",
     "Emergency patient relatives, voluntary donors, and blood bank coordinators.",
     "Cuts emergency blood sourcing time from hours to under 20 minutes."),

    ("BCA045", "Smart Travel Planning Application", "BCA", "Mobile & Modern Applications", "Intermediate", "5-6 Weeks", 1499, 1999,
     "Tailwind CSS, JavaScript, FastAPI, SQLite, Leaflet Maps",
     "A collaborative trip itinerary planner that organizes day-by-day travel schedules, destination attraction maps, budget splitting, and packing checklists.",
     "Planning group trips is messy, resulting in scattered flight tickets, conflicting itineraries, and awkward expense splitting among friends.",
     "Create a mobile-friendly travel planner where users curate daily schedules, visualize stops on a map, and track shared travel expenses automatically.",
     ["Day-by-day itinerary builder with time slots and attraction notes", "Interactive destination map with pinned places of interest", "Shared trip expense tracker with split-bill calculations", "Collaborative packing checklist with item assignment to travelers"],
     "Leisure travel, student backpacker trips, and family vacation planning.",
     "Solo travelers, trip organizers, and group vacationers.",
     "Streamlined vacation planning with day-by-day itineraries and fair cost sharing."),

    ("BCA046", "Local Service Provider Booking Application", "BCA", "Mobile & Modern Applications", "Intermediate", "6-7 Weeks", 1699, 2199,
     "Mobile Web / React, FastAPI, SQLite, Tailwind CSS",
     "An on-demand local home services marketplace connecting homeowners with electricians, plumbers, appliance technicians, and carpenters.",
     "Homeowners struggle to find reliable local service technicians with transparent pricing, while skilled workers lack consistent customer leads.",
     "Build a two-sided marketplace where customers book verified service slots, review upfront rate cards, and track service status to completion.",
     ["Service catalog (Plumbing, Electrical, Carpentry, AC Repair)", "Verified professional profiles with hourly rates and ratings", "Appointment booking calendar with address selection", "Customer rating and review system upon job completion"],
     "Urban home services, residential communities, and technician cooperatives.",
     "Homeowners, self-employed tradespeople, and platform coordinators.",
     "Transparent pricing and hassle-free domestic service appointment booking."),

    ("BCA047", "Digital Complaint Management Application", "BCA", "Mobile & Modern Applications", "Beginner", "4-5 Weeks", 999, 1499,
     "Tailwind CSS, HTML5, FastAPI, SQLite, File Uploads",
     "A civic and institutional grievance redressal portal allowing students or citizens to submit geo-tagged complaints with photo proof and track resolution stages.",
     "Civic and campus grievances get lost in bureaucratic black holes due to lack of transparent public ticketing and accountability mechanisms.",
     "Implement a transparent complaint management system with photo attachments, category routing, time-bound SLA tracking, and status updates.",
     ["Complaint submission with photo proof upload and category selection", "Unique tracking ID with real-time status tracker (Logged, In Progress, Resolved)", "Department assignment and SLA escalation timer for overdue tickets", "Citizen feedback rating after grievance is closed"],
     "Municipal corporations, college campus administration, and public utilities.",
     "Citizens/students, grievance redressal officers, and department heads.",
     "Transparent public accountability with time-stamped complaint resolution."),

    ("BCA048", "Smart Parking Management Application", "BCA", "Mobile & Modern Applications", "Intermediate", "5-6 Weeks", 1399, 1899,
     "HTML5 / Mobile Web, FastAPI, SQLite, Tailwind CSS",
     "An intelligent vehicle parking reservation portal that displays real-time slot availability, calculates hourly tariffs, and generates digital parking passes.",
     "Drivers waste fuel and cause urban traffic congestion circling crowded shopping malls and commercial districts searching for parking spots.",
     "Provide a real-time parking slot visualizer where drivers check open spots before arrival, reserve space, and receive a digital QR exit token.",
     ["Interactive floor-wise parking slot grid with live vacant/occupied colors", "Vehicle entry check-in and automated hourly parking tariff calculation", "Digital parking ticket with barcode/QR verification for gate checkout", "Daily revenue, vehicle turnover, and peak occupancy analytics"],
     "Shopping malls, commercial complexes, airports, and college campus parking.",
     "Motorists, parking lot attendants, and facility administrators.",
     "Eliminates parking search time and prevents revenue leakage at parking gates."),

    ("BCA049", "Campus Connect Student Mobile Application", "BCA", "Mobile & Modern Applications", "Intermediate", "5-6 Weeks", 1399, 1899,
     "Mobile PWA, FastAPI, SQLite, Tailwind CSS, Lucide Icons",
     "A dedicated campus social and academic portal featuring club announcements, peer textbook exchange, lost-and-found board, and timetable widgets.",
     "Campus communication is fragmented across noisy messaging groups, causing students to miss important academic notices and club events.",
     "Create an all-in-one student campus app combining verified institutional circulars, peer-to-peer used book exchange, and digital notice boards.",
     ["Digital notice board with department and club announcement feeds", "Peer-to-peer book and study material exchange marketplace", "Lost and Found bulletin board with photo upload and claim feature", "Daily personalized lecture timetable and exam date countdown"],
     "Colleges, universities, and polytechnic student communities.",
     "Students, faculty club coordinators, and student council officers.",
     "Unified campus engagement in one reliable, privacy-focused mobile portal."),

    ("BCA050", "Online Appointment Booking Application", "BCA", "Mobile & Modern Applications", "Beginner", "4-5 Weeks", 899, 1399,
     "HTML5, Tailwind CSS, FastAPI, SQLite, Calendar Engine",
     "A universal appointment scheduling platform for doctors, salons, and consultants with automated time-slot allocation and calendar reminders.",
     "Service professionals waste hours managing appointment books manually via phone calls, leading to double-bookings and no-shows.",
     "Build an automated booking application where clients select available 30-minute calendar slots, receive instant confirmations, and manage cancellations.",
     ["Professional service menu with duration and consultation fees", "Interactive calendar with automatic masking of already-booked slots", "Instant booking confirmation with cancellation and reschedule options", "Admin calendar agenda view with daily and weekly client schedules"],
     "Doctor clinics, beauty salons, legal consultants, and academic advisors.",
     "Clients, service practitioners, and clinic receptionists.",
     "Eliminates double bookings and reduces client no-shows by 40%."),

    # Cat 6: Cybersecurity, Cloud & Advanced Systems (BCA051 - BCA060)
    ("BCA051", "Malicious URL Detection System", "BCA", "Cybersecurity, Cloud & Advanced Systems", "Intermediate", "5-6 Weeks", 1499, 1999,
     "Python, Scikit-learn, FastAPI, URL Lexical Parser, SQLite",
     "A cybersecurity web scanner that analyzes website URLs using lexical feature extraction and machine learning to detect phishing and malware links.",
     "Users inadvertently click deceptive phishing and malicious links hidden behind URL shorteners, leading to credential theft and malware infections.",
     "Extract lexical properties from submitted URLs (length, special characters, entropy, IP presence) and classify safety status using a Random Forest model.",
     ["Live URL inspection with instant Safe vs Malicious verdict", "Lexical security breakdown (domain age, subdomains, suspicious tokens)", "Batch URL scanner for auditing marketing or email link lists", "Blacklist and whitelist management portal with audit logs"],
     "Corporate email security, web browser extensions, and security awareness labs.",
     "Security analysts, enterprise employees, and internet users.",
     "Over 93% detection accuracy for phishing and zero-day malicious URLs."),

    ("BCA052", "Password Strength Analysis and Security Application", "BCA", "Cybersecurity, Cloud & Advanced Systems", "Beginner", "4-5 Weeks", 799, 1299,
     "JavaScript, Python, FastAPI, zxcvbn Entropy Engine, Tailwind",
     "An interactive security assessment tool that calculates password entropy, estimates brute-force cracking time, and checks credentials against breached databases.",
     "Users consistently choose weak, predictable passwords or reuse credentials across multiple critical services, making them vulnerable to credential stuffing.",
     "Provide real-time entropy calculation, dictionary pattern matching, and simulated GPU crack-time estimates alongside a secure random password generator.",
     ["Real-time password entropy calculation and visual strength meter", "Detection of dictionary words, keyboard sequences, and personal patterns", "Realistic brute-force crack-time estimates across CPU/GPU clusters", "Cryptographically secure multi-format password generator"],
     "Cybersecurity training workshops, student orientation, and enterprise login portals.",
     "General web users, IT security trainers, and system administrators.",
     "Drives adoption of secure, high-entropy passwords across user populations."),

    ("BCA053", "Secure File Sharing Application", "BCA", "Cybersecurity, Cloud & Advanced Systems", "Intermediate", "5-6 Weeks", 1499, 1999,
     "Python, Cryptography (AES-256), FastAPI, SQLite, Tailwind",
     "An end-to-end encrypted file sharing platform featuring AES-256 client-side encryption, time-limited self-destructing download links, and password protection.",
     "Sharing sensitive documents over ordinary email or public cloud drives exposes confidential files to data leaks and unauthorized access.",
     "Implement AES-256 encryption where files are encrypted before upload, protected with one-time passcodes, and permanently purged after expiry or first download.",
     ["Drag-and-drop secure file upload with client/server AES-256 encryption", "Time-based link expiration (1 hour, 24 hours, 7 days)", "Optional download password protection and download count limits", "Automated background cron task for permanent file shredding after expiry"],
     "Confidential corporate communications, legal document dispatch, and privacy labs.",
     "Privacy-conscious users, legal clerks, and security professionals.",
     "Guaranteed cryptographic privacy with zero permanent footprint after expiry."),

    ("BCA054", "Cloud-Based Document Management System", "BCA", "Cybersecurity, Cloud & Advanced Systems", "Intermediate", "6-7 Weeks", 1699, 2199,
     "Python, FastAPI, SQLite / S3 Compatible, Tailwind CSS",
     "A secure collaborative cloud storage system featuring hierarchical folder structures, role-based sharing permissions, document versioning, and activity audit trails.",
     "Teams using unstructured shared drives experience file overwrites, unauthorized access, and lack of accountability for modified documents.",
     "Deliver an enterprise document portal with granular access control (View, Edit, Admin), file version control, and tamper-evident audit logs.",
     ["Hierarchical folder navigation with search and tagging", "Granular sharing permissions (Public, Restricted, Specific Users)", "Document version history with rollback to previous revisions", "Comprehensive user activity audit trail (View, Download, Modify, Delete)"],
     "SME office collaboration, legal archives, and college departmental document vaults.",
     "Office administrators, department managers, and staff members.",
     "Organized cloud document governance with complete revision history."),

    ("BCA055", "Phishing Website Detection System", "BCA", "Cybersecurity, Cloud & Advanced Systems", "Intermediate", "5-6 Weeks", 1499, 1999,
     "Python, Beautiful Soup, Scikit-learn, FastAPI, Tailwind CSS",
     "An automated web security auditing tool that inspects HTML source code, SSL certificate validity, and URL structures to flag counterfeit phishing websites.",
     "Cybercriminals rapidly spin up clone websites mimicking popular banks and portals to harvest user credentials and payment card numbers.",
     "Build an automated HTML and DOM inspector that checks for suspicious external form action targets, missing HTTPS, and domain homoglyph attacks.",
     ["Webpage HTML scraper extracting form action attributes and scripts", "Heuristic security evaluation (domain mismatch, hidden iframes, no HTTPS)", "Machine learning classification score indicating phishing likelihood", "Visual security report with breakdown of discovered red flags"],
     "Fintech security portals, web security education, and consumer browser extensions.",
     "Security researchers, bank fraud prevention teams, and online shoppers.",
     "Rapid detection of counterfeit phishing landing pages in <2 seconds."),

    ("BCA056", "Role-Based Access Control Management System", "BCA", "Cybersecurity, Cloud & Advanced Systems", "Intermediate", "5-6 Weeks", 1399, 1899,
     "Python, FastAPI, JWT Auth, SQLite, Tailwind CSS",
     "A robust identity and access management (IAM) demonstration framework implementing role-based access control (RBAC), JWT authentication, and permission matrices.",
     "Software developers frequently implement naive authorization checks, leading to severe privilege escalation vulnerabilities and unauthorized data exposure.",
     "Create a reference RBAC management platform where administrators define custom roles, map granular permissions, and enforce secure JWT token claims.",
     ["User registration and authentication with bcrypt password hashing", "Role creation (Admin, Manager, Editor, Viewer) with permission checkboxes", "Protected route demonstration verifying claims and access restrictions", "Security audit logs recording privilege grant and denial events"],
     "Enterprise software development, computer science security labs, and SaaS backends.",
     "Security engineers, software architects, and backend developers.",
     "Battle-tested, standards-compliant RBAC implementation protecting API resources."),

    ("BCA057", "Cybersecurity Awareness and Training Platform", "BCA", "Cybersecurity, Cloud & Advanced Systems", "Beginner", "4-5 Weeks", 899, 1399,
     "HTML5, Tailwind CSS, FastAPI, SQLite, Interactive Modules",
     "An interactive employee security training platform featuring simulated phishing emails, password safety modules, interactive quizzes, and certification badges.",
     "Over 85% of corporate cyber breaches stem from human error and social engineering rather than technical software vulnerabilities.",
     "Provide an engaging learning portal with realistic phishing email scenarios, safe browsing modules, and automated employee awareness scoring.",
     ["Interactive micro-learning modules (Phishing, Ransomware, Social Engineering)", "Simulated phishing email identifier test with instant explanations", "End-of-module assessment quizzes with passing score criteria", "Automated employee cybersecurity readiness certificate generation"],
     "Corporate onboarding, college campus cyber awareness, and IT security workshops.",
     "Corporate employees, college students, and corporate security officers.",
     "Measurable reduction in employee susceptibility to social engineering attacks."),

    ("BCA058", "Secure Online Voting Management System", "BCA", "Cybersecurity, Cloud & Advanced Systems", "Intermediate", "6-7 Weeks", 1699, 2199,
     "Python, FastAPI, Cryptographic Hashes (SHA-256), SQLite, Tailwind",
     "A tamper-evident digital voting platform for campus and organizational elections featuring voter token verification, encrypted ballots, and verifiable tallies.",
     "Traditional campus elections conducted with paper ballots or basic online polls are vulnerable to duplicate voting and accusations of vote tampering.",
     "Build a verifiable electronic voting system where voter identity is verified via unique OTP/token, votes are cryptographically anonymized, and tally is verifiable.",
     ["Voter roll registration with student ID and one-time voting token generation", "Secret ballot voting interface with real-time confirmation receipt", "Cryptographic ballot hashing (SHA-256) preventing vote alteration", "Automated transparent tallying and candidate winner declaration"],
     "College student council elections, club leadership polls, and society ballots.",
     "Election commissioners, student voters, and candidate nominees.",
     "100% duplicate-proof, audit-verifiable election tallying with secret ballots."),

    ("BCA059", "Cloud-Based Backup and Recovery System", "BCA", "Cybersecurity, Cloud & Advanced Systems", "Intermediate", "5-6 Weeks", 1499, 1999,
     "Python, SQLite, FastAPI, Cron Scheduler, Gzip/Zip",
     "An automated database and file backup management system that schedules periodic snapshots, compresses archives, and provides one-click disaster recovery restoration.",
     "Small organizations suffer catastrophic data loss from ransomware or hardware failure because they lack automated, reliable backup procedures.",
     "Develop a scheduled backup utility that takes automated database dumps, compresses directories with timestamped versions, and provides restore validation.",
     ["Automated cron scheduling for hourly, daily, or weekly backup jobs", "ZIP and Gzip compression with timestamped version naming", "Storage usage telemetry and automated cleanup of obsolete archives", "One-click point-in-time disaster recovery restore workflow"],
     "Web hosting management, SME file servers, and departmental database backups.",
     "System administrators, database managers, and DevOps engineers.",
     "Guaranteed data recoverability with automated zero-touch backup cycles."),

    ("BCA060", "Blockchain-Based Certificate Verification System", "BCA", "Cybersecurity, Cloud & Advanced Systems", "Intermediate", "6-8 Weeks", 1899, 2499,
     "Python, Web3 / Cryptographic Ledger, FastAPI, SQLite, QR Code",
     "A decentralized academic credential verification portal that stores certificate cryptographic hashes on a tamper-proof ledger, enabling instant employer QR verification.",
     "Forged educational degrees and counterfeit certificates deceive employers and dilute the credibility of legitimate academic institutions.",
     "Implement a blockchain-inspired verifiable ledger where universities issue certificates with cryptographic hashes and QR codes that anyone can verify instantly.",
     ["Institutional portal for issuing digital degrees and student transcripts", "Cryptographic hashing (SHA-256) and tamper-proof ledger logging", "Public verification portal: upload certificate PDF or scan QR code", "Instant authentic/counterfeit verification verdict with issuing metadata"],
     "Universities, professional certification boards, and employer HR background checks.",
     "University registrars, corporate HR recruiters, and graduating students.",
     "Zero-counterfeit credential verification in under 3 seconds without paperwork.")
]

# Section B: BE Computer Science Engineering (BE001 to BE060)
BE_PROJECTS = [
    # Cat 1: Advanced AI & Generative AI (BE001 - BE010)
    ("BE001", "Multi-Agent AI Research and Automation Platform", "BE", "Advanced AI & Generative AI", "Advanced", "8-10 Weeks", 4999, 6499,
     "Python, LangChain / CrewAI, FastAPI, React, PostgreSQL / SQLite",
     "An autonomous multi-agent system where specialized AI agents (Researcher, Writer, Reviewer, Fact-Checker) collaborate to investigate topics, synthesize data, and compile structured research reports.",
     "Complex research synthesis requires coordinating multiple analytical steps that single LLM prompts fail to execute with depth, factual rigor, and proper citation.",
     "Architect a multi-agent orchestration workflow where autonomous agents execute sequential and hierarchical tasks with memory, tool access, and peer review verification.",
     ["Autonomous task decomposition and multi-agent role delegation", "Web search and document scraping tool integration for live fact retrieval", "Cross-agent debate and hallucination verification loop", "Automated publication-ready markdown and PDF research paper compilation"],
     "Academic literature reviews, market intelligence research, and scientific literature mining.",
     "Research scholars, corporate strategy analysts, and academic faculty.",
     "Comprehensive 15-page synthesized literature reports compiled in under 4 minutes."),

    ("BE002", "Retrieval-Augmented Generation (RAG) Knowledge Assistant", "BE", "Advanced AI & Generative AI", "Advanced", "8-10 Weeks", 4499, 5999,
     "Python, ChromaDB / FAISS, LangChain, FastAPI, React",
     "An enterprise RAG assistant that ingests internal PDFs and technical manuals, computes dense vector embeddings, and answers queries with exact source citations.",
     "Standard large language models hallucinate on proprietary corporate data and cannot reference private internal documentation without continuous retraining.",
     "Implement a dense vector retrieval pipeline utilizing FAISS/ChromaDB and chunking strategies to retrieve relevant passages and synthesize accurate grounded responses.",
     ["Multi-document ingestion (PDF, DOCX, Markdown) with recursive text chunking", "High-dimensional vector embedding generation and semantic similarity search", "Hallucination-free contextual question answering with verifiable citations", "Interactive knowledge explorer with document chunk inspection"],
     "Corporate internal knowledge bases, technical support desks, and medical research archives.",
     "Enterprise employees, support engineers, and compliance auditors.",
     "Sub-second semantic search retrieval with 100% cited factual responses."),

    ("BE003", "AI-Powered Autonomous Customer Support Agent", "BE", "Advanced AI & Generative AI", "Advanced", "7-9 Weeks", 3999, 5499,
     "Python, FastAPI, OpenAI / Local LLM, Function Calling, SQLite",
     "A production-ready autonomous support agent capable of resolving complex user inquiries, querying database records, updating order statuses, and initiating refunds.",
     "Rule-based chatbots fail on complex multi-turn inquiries, while human agents are overwhelmed by repetitive operational requests like tracking and refunds.",
     "Deploy an LLM agent equipped with tool-use (Function Calling) that queries internal databases, safely executes permitted actions, and summarizes outcomes.",
     ["Multi-turn conversational memory with sentiment tracking", "Tool-use function calling to query order status, inventory, and policy rules", "Automated escalation to human supervisors on frustrated sentiment detection", "Comprehensive agent action audit log with rollbacks"],
     "E-commerce customer service, fintech account support, and SaaS user onboarding.",
     "Customer support directors, enterprise clients, and operations agents.",
     "Over 75% end-to-end resolution of tier-1 support tickets without human intervention."),

    ("BE004", "Intelligent Code Review and Bug Detection System", "BE", "Advanced AI & Generative AI", "Advanced", "8-10 Weeks", 4499, 5999,
     "Python, Tree-sitter / AST, LLM API, FastAPI, Tailwind CSS",
     "An automated code intelligence engine that parses source code ASTs, detects security vulnerabilities, identifies code smells, and suggests optimized refactored snippets.",
     "Manual peer code reviews are time-consuming and often miss subtle security flaws, memory leaks, and performance anti-patterns.",
     "Combine static abstract syntax tree (AST) analysis with transformer models to review code changes, detect CVE patterns (OWASP Top 10), and suggest idiomatic fixes.",
     ["Multi-language code parsing (Python, JavaScript, Java, C++)", "Automated detection of OWASP Top 10 vulnerabilities (SQLi, XSS, Buffer Overflow)", "Code smell detection with complexity metrics (Cyclomatic Complexity)", "Side-by-side diff view with AI-recommended refactoring suggestions"],
     "CI/CD pipelines, engineering team pull requests, and computer science grading.",
     "Software developers, security auditors, and university coding instructors.",
     "Cuts code review cycle time by 60% while catching critical security flaws early."),

    ("BE005", "AI-Based Medical Image Analysis System", "BE", "Advanced AI & Generative AI", "Advanced", "8-10 Weeks", 4999, 6999,
     "Python, PyTorch / TensorFlow, CNN / Vision Transformer, FastAPI",
     "A deep learning medical diagnostic assistant that analyzes chest X-rays and MRI scans, identifies anomalies, and generates Grad-CAM visual heatmaps for clinical review.",
     "Radiologists face severe diagnostic backlogs, leading to fatigue and delayed diagnosis of critical pulmonary and neurological conditions.",
     "Train a deep convolutional neural network (DenseNet-121 / ResNet-50) on medical imaging datasets to detect pathologies and display Grad-CAM saliency heatmaps.",
     ["DICOM / JPEG medical image upload with privacy-preserving metadata stripping", "Multi-pathology classification (Pneumonia, Tuberculosis, Cardiomegaly)", "Grad-CAM visual heatmap overlay showing regions of interest", "Structured clinical summary report generation with confidence intervals"],
     "Radiology departments, rural telemedicine centers, and diagnostic research.",
     "Consultant radiologists, pulmonologists, and clinical researchers.",
     "Over 92% diagnostic sensitivity with interpretable visual saliency maps."),

    ("BE006", "Multimodal AI Assistant Using Text, Images and Voice", "BE", "Advanced AI & Generative AI", "Advanced", "8-10 Weeks", 4999, 6499,
     "Python, Vision-Language Models, Whisper, FastAPI, WebRTC",
     "A comprehensive multimodal AI assistant capable of processing synchronized voice commands, inspecting user-uploaded images or webcam feeds, and generating spoken replies.",
     "Single-mode interfaces restrict user accessibility and cannot assist in tasks that require simultaneous visual inspection, speech interaction, and textual reasoning.",
     "Fuse Whisper automatic speech recognition, Vision-Language Models (CLIP / LLaVA), and text-to-speech synthesis into a responsive real-time multimodal loop.",
     ["Live voice interaction using Whisper speech-to-text", "Real-time image inspection and object/diagram visual reasoning", "Synthesized voice output with expressive text-to-speech audio", "Unified multi-turn conversation timeline combining voice, image, and text"],
     "Accessibility tools for the visually impaired, industrial maintenance, and smart kiosks.",
     "End consumers, accessibility users, and field service technicians.",
     "Seamless real-time multimodal interaction with under 1.5s total latency."),

    ("BE007", "AI-Powered Legal Document Analysis Platform", "BE", "Advanced AI & Generative AI", "Advanced", "8-10 Weeks", 4799, 6299,
     "Python, Spacy, Transformers, FastAPI, SQLite / PostgreSQL",
     "A specialized legal technology portal that analyzes non-disclosure agreements and commercial contracts, highlights risky indemnity clauses, and summarizes key liabilities.",
     "Legal teams spend exhausting hours reviewing lengthy contracts, risking oversight of hazardous liability clauses and unfavorable termination covenants.",
     "Implement domain-specific legal NLP models to extract contractual obligations, categorize indemnity risk levels, and summarize complex clauses into plain language.",
     ["PDF contract ingestion with section and clause segmentation", "Automated risk rating for termination, liability, and indemnity clauses", "Plain-English clause summarization and missing standard clause alerts", "Exportable contract risk audit matrix for legal counsel review"],
     "Corporate legal departments, law firms, procurement teams, and startups.",
     "Corporate legal counsel, compliance managers, and contract negotiators.",
     "Reduces contract first-pass review time from 3 hours to under 10 minutes."),

    ("BE008", "Autonomous AI-Based Software Development Assistant", "BE", "Advanced AI & Generative AI", "Advanced", "8-10 Weeks", 4999, 6999,
     "Python, FastAPI, Docker Sandboxing, LangChain, React",
     "An autonomous coding agent that accepts natural language feature specifications, generates complete multi-file project scaffolds, executes unit tests in sandboxes, and self-heals errors.",
     "Developers spend substantial time writing boilerplate code, configuring project scaffolding, and resolving initial build errors.",
     "Create a multi-step coding agent that plans architecture, writes modular code files, runs test commands inside isolated Docker sandboxes, and iterates until tests pass.",
     ["Natural language project specification parser and architecture planner", "Multi-file project scaffolding with dependency configuration", "Sandboxed execution environment for automated test runs", "Self-healing code loop: inspects tracebacks and applies automated bug fixes"],
     "Rapid prototyping, developer productivity tools, and software education.",
     "Software developers, technical founders, and coding bootcamps.",
     "Generates fully functioning, test-verified software modules in minutes."),

    ("BE009", "Intelligent Recommendation Engine Using Deep Learning", "BE", "Advanced AI & Generative AI", "Advanced", "7-9 Weeks", 3999, 5499,
     "Python, PyTorch, Two-Tower Neural Network / NCF, FastAPI, Redis",
     "An enterprise-scale neural recommendation system utilizing collaborative filtering and Two-Tower deep learning architectures to serve real-time personalized recommendations.",
     "Traditional matrix factorization algorithms struggle with user/item cold-start problems and fail to capture complex non-linear feature interactions in real time.",
     "Build a Neural Collaborative Filtering (NCF) and Two-Tower embedding network that maps user behavior and item metadata into a shared latent space for fast retrieval.",
     ["Implicit user feedback logging (clicks, dwell time, purchases)", "Two-Tower neural architecture for lightning-fast approximate nearest neighbor search", "Cold-start mitigation using auxiliary content embeddings", "Real-time personalization API serving recommendations in <50ms"],
     "Streaming media platforms, digital retail portals, and news aggregators.",
     "Data science engineers, digital product managers, and e-commerce platforms.",
     "Sub-50ms recommendation latency with significantly higher click-through rates."),

    ("BE010", "Enterprise AI Knowledge Management System", "BE", "Advanced AI & Generative AI", "Advanced", "8-10 Weeks", 4699, 6199,
     "Python, FastAPI, Vector Search, Knowledge Graph, React",
     "A hybrid knowledge intelligence platform combining dense vector search with semantic Knowledge Graphs to map organizational expertise, documents, and concepts.",
     "Large enterprises lose millions in redundant work because knowledge is siloed across departments, disconnected wikis, and unindexed internal repositories.",
     "Unify vector embeddings with Neo4j-style knowledge graph triples (Subject-Predicate-Object) to enable both semantic document search and relational concept exploration.",
     ["Multi-source document connectors (Wikis, PDFs, Code, Emails)", "Automated entity and relationship extraction creating an interactive knowledge graph", "Hybrid vector and graph retrieval for deep contextual reasoning", "Organizational expertise locator identifying subject-matter experts"],
     "R&D corporations, consulting firms, pharmaceutical researchers, and government agencies.",
     "Enterprise knowledge officers, researchers, and project directors.",
     "Breaks enterprise knowledge silos with intuitive semantic and graph discovery."),

    # Cat 2: Advanced Machine Learning & Deep Learning (BE011 - BE020)
    ("BE011", "Real-Time Object Detection Using YOLO", "BE", "Advanced Machine Learning & Deep Learning", "Advanced", "7-9 Weeks", 3899, 4999,
     "Python, Ultralytics YOLOv8, OpenCV, FastAPI, WebSocket",
     "A high-throughput computer vision pipeline processing real-time video streams to detect, track, and count multi-class objects with bounding boxes and trajectory logs.",
     "Security monitoring and industrial quality inspection suffer from human monitoring fatigue and delayed manual counting of items.",
     "Deploy a YOLOv8 real-time inference engine integrated with ByteTrack/DeepSORT for persistent object tracking and directional counting across video streams.",
     ["Webcam and RTSP IP camera live video stream ingestion", "Multi-class detection (Vehicles, Pedestrians, Equipment) at 30+ FPS", "Virtual tripwire entry/exit counting with directional analysis", "Automated alert generation for unauthorized boundary crossing"],
     "Smart city surveillance, automated warehouse counting, and security perimeters.",
     "Security operations directors, warehouse managers, and traffic engineers.",
     "Real-time 30+ FPS inference with over 90% mAP across target object classes."),

    ("BE012", "Deep Learning-Based Facial Emotion Recognition", "BE", "Advanced Machine Learning & Deep Learning", "Advanced", "7-8 Weeks", 3499, 4699,
     "Python, PyTorch, ResNet / MobileNet, OpenCV, Tailwind CSS",
     "A real-time affective computing system that detects facial expressions from video feeds and classifies emotional states (Happy, Sad, Angry, Surprised, Neutral, Fear).",
     "User experience researchers, mental wellness apps, and online educators struggle to gauge passive audience engagement and emotional reactions.",
     "Implement face detection with a lightweight convolutional neural network fine-tuned on the FER-2013 dataset to deliver real-time emotion probability distributions.",
     ["Real-time video frame face extraction and alignment", "Six-class emotional classification with live confidence percentage bars", "Temporal emotional engagement timeline across video sessions", "Aggregate sentiment reporting for educational lectures and product testing"],
     "E-learning engagement tracking, user testing labs, and mental wellness apps.",
     "UX researchers, educational psychologists, and customer experience analysts.",
     "Real-time emotion inference at 25+ FPS with detailed engagement analytics."),

    ("BE013", "Sign Language Recognition Using Computer Vision", "BE", "Advanced Machine Learning & Deep Learning", "Advanced", "8-10 Weeks", 4299, 5699,
     "Python, MediaPipe, LSTM / Transformer, OpenCV, FastAPI",
     "An assistive communication application that tracks hand landmarks in real time and translates continuous sign language gestures into audible speech and text.",
     "Deaf and hard-of-hearing individuals face persistent communication barriers when interacting with people who do not know sign language.",
     "Leverage MediaPipe Hand Landmarks to extract 21 3D coordinates per hand and pass temporal coordinate sequences through an LSTM network to classify sign phrases.",
     ["Real-time hand keypoint tracking without requiring specialized data gloves", "Recognition of alphabet fingerspelling and full dynamic sign phrases", "Instant text translation and text-to-speech audio pronunciation", "Interactive sign language learning practice mode with visual feedback"],
     "Accessibility kiosks, inclusive classrooms, and public customer service counters.",
     "Deaf community members, educators, and public service personnel.",
     "Over 92% gesture recognition accuracy in real time on standard webcams."),

    ("BE014", "Traffic Density Prediction Using Deep Learning", "BE", "Advanced Machine Learning & Deep Learning", "Advanced", "7-9 Weeks", 3699, 4899,
     "Python, TensorFlow / PyTorch, ConvLSTM, Pandas, Leaflet",
     "A spatial-temporal deep learning model forecasting urban road traffic congestion, average vehicle speeds, and congestion bottlenecks 60 minutes into the future.",
     "Static traffic light timers and reactionary traffic management worsen urban traffic gridlocks, leading to wasted fuel and emergency vehicle delays.",
     "Construct a spatial-temporal ConvLSTM network trained on urban sensor and camera count feeds to predict traffic congestion waves before they materialize.",
     ["City road network topology modeling with traffic sensor points", "Spatial-temporal traffic volume forecasting up to 60 minutes ahead", "Congestion hotspot alert map with predicted bottle-neck severity", "Smart adaptive signal timing recommendation based on predicted flow"],
     "Municipal traffic police control rooms, smart city hubs, and logistics routing.",
     "City traffic planners, municipal engineers, and navigation dispatchers.",
     "Accurate traffic congestion forecasting enabling proactive traffic signal adjustments."),

    ("BE015", "Brain Tumor Detection Using CNN", "BE", "Advanced Machine Learning & Deep Learning", "Advanced", "8-10 Weeks", 4799, 6299,
     "Python, PyTorch / Keras, ResNet50 / U-Net, FastAPI, Tailwind",
     "A clinical decision-support application analyzing brain MRI scans to segment and classify tumors (Glioma, Meningioma, Pituitary) with high diagnostic confidence.",
     "Early brain tumor detection requires painstaking examination of hundreds of MRI slice images, where subtle early lesions can be overlooked during busy clinical shifts.",
     "Train a U-Net and ResNet architecture on benchmark brain MRI datasets (BraTS) to perform both tumor classification and pixel-level lesion boundary segmentation.",
     ["MRI image slice upload with contrast adjustment and skull stripping", "Multi-class brain tumor classification with confidence scores", "Pixel-level tumor lesion segmentation overlay using U-Net", "Tumor volume estimation and radiologist reporting checklist"],
     "Neurosurgery planning, oncology departments, and medical imaging research.",
     "Neurologists, neurosurgeons, and medical imaging researchers.",
     "Over 94% classification accuracy with clear tumor contour segmentation overlays."),

    ("BE016", "Crop Disease Detection Using Computer Vision", "BE", "Advanced Machine Learning & Deep Learning", "Advanced", "7-9 Weeks", 3699, 4999,
     "Python, PyTorch / MobileNetV3, FastAPI, SQLite, PWA",
     "An agricultural diagnostic mobile web application allowing farmers to photograph diseased plant leaves and receive instant disease identification and treatment remedies.",
     "Smallholder farmers lose up to 40% of their crop yields to fungal and bacterial plant diseases due to delayed diagnosis and lack of access to agronomists.",
     "Train a lightweight MobileNetV3 model on thousands of plant leaf pathology images to run on-device or cloud inference and deliver localized organic and chemical cures.",
     ["High-resolution crop leaf photo capture and automated leaf region cropping", "Identification of 35+ crop diseases across Tomato, Potato, Corn, and Wheat", "Actionable treatment recommendations (organic, biological, chemical)", "Localized disease outbreak alert map for neighboring farmers"],
     "Agricultural extension services, rural farming cooperatives, and agribusinesses.",
     "Farmers, agricultural extension officers, and agronomy researchers.",
     "Instant field crop disease diagnosis with >95% accuracy on mobile browsers."),

    ("BE017", "Fraud Transaction Detection Using Machine Learning", "BE", "Advanced Machine Learning & Deep Learning", "Advanced", "7-9 Weeks", 3999, 5299,
     "Python, XGBoost, Scikit-learn, Imbalanced-learn, FastAPI",
     "A high-throughput fraud analytics engine utilizing XGBoost and Isolation Forests to detect fraudulent card transactions in highly imbalanced financial transaction streams.",
     "Payment processors lose billions to fraud, but naive rules-based systems trigger excessive false positives that frustrate legitimate customers.",
     "Apply SMOTE oversampling and XGBoost cost-sensitive learning to detect anomalous spending spikes, impossible geographic hops, and synthetic identity fraud.",
     ["Real-time transaction scoring against trained fraud models", "Anomaly detection using Isolation Forests for novel attack patterns", "Feature importance breakdown explaining why a transaction was flagged", "Risk rule engine with automated block, challenge, or approve decisions"],
     "Fintech payment gateways, credit card issuers, and digital banking platforms.",
     "Fraud risk officers, compliance analysts, and fintech developers.",
     "Sub-100ms transaction decisioning with >98% ROC-AUC on imbalanced datasets."),

    ("BE018", "Network Intrusion Detection Using Deep Learning", "BE", "Advanced Machine Learning & Deep Learning", "Advanced", "8-10 Weeks", 4499, 5999,
     "Python, PyTorch / TensorFlow, CIC-IDS Dataset, FastAPI, Chart.js",
     "A deep learning network security appliance monitoring PCAP and NetFlow packets to detect zero-day cyber attacks, DDoS floods, port scans, and botnet telemetry.",
     "Traditional signature-based IDS (like Snort) fail against novel polymorphic zero-day attacks and high-volume volumetric distributed denial of service floods.",
     "Construct an autoencoder and deep neural network trained on the CIC-IDS dataset to detect statistical flow anomalies and classify specific cyberattack categories.",
     ["Live network packet and NetFlow data ingestion and feature extraction", "Multi-attack classification (DDoS, Port Scan, Brute Force, Web Attack)", "Anomaly score generation detecting zero-day traffic aberrations", "Automated alert generation with IP blocking firewall trigger simulation"],
     "Enterprise security operations centers (SOC), data centers, and cloud ISPs.",
     "SOC analysts, network security engineers, and chief information security officers.",
     "Over 96% detection rate on modern multi-vector network intrusion attacks."),

    ("BE019", "Predictive Maintenance Using Machine Learning", "BE", "Advanced Machine Learning & Deep Learning", "Advanced", "7-9 Weeks", 3999, 5299,
     "Python, Scikit-learn / XGBoost, Pandas, FastAPI, Chart.js",
     "An industrial IoT analytics platform processing industrial vibration, temperature, and RPM telemetry to predict equipment failure and remaining useful life (RUL).",
     "Unplanned industrial machinery breakdowns halt production lines, costing factories millions in downtime and emergency replacement parts.",
     "Train regression and classification models on industrial sensor time-series data to predict Remaining Useful Life (RUL) and flag impending bearing/motor failures.",
     ["Industrial sensor stream ingestion (Vibration, Temperature, Pressure, RPM)", "Remaining Useful Life (RUL) estimation with degradation curve plots", "Failure mode classification (Bearing Fault, Overheating, Imbalance)", "Automated maintenance work-order generation prior to equipment failure"],
     "Manufacturing plants, wind turbine farms, aerospace, and heavy industry.",
     "Plant maintenance engineers, factory operations managers, and reliability leads.",
     "Accurate advance warning 48 hours prior to catastrophic mechanical failure."),

    ("BE020", "Human Activity Recognition Using Computer Vision", "BE", "Advanced Machine Learning & Deep Learning", "Advanced", "8-10 Weeks", 4499, 5999,
     "Python, MediaPipe / OpenPose, 3D CNN / LSTM, OpenCV, FastAPI",
     "A video surveillance system that tracks full-body skeletal keypoints across video frames to classify human actions (Walking, Running, Falling, Fighting, Reaching).",
     "Elderly care facilities and secure zones require continuous human monitoring to detect hazardous falls and physical altercations without invasive manual observation.",
     "Extract 33 skeletal body landmarks using MediaPipe and model temporal motion trajectories with an LSTM network to classify human physical activities and alert on falls.",
     ["Multi-person skeletal body keypoint tracking from standard camera video", "Classification of dynamic human actions with temporal windowing", "Instant emergency alert generation upon slip-and-fall detection", "Privacy-preserving skeletal representation without storing raw facial identities"],
     "Elderly care homes, hospital patient monitoring, and workplace safety audits.",
     "Care facility supervisors, safety auditors, and emergency medical responders.",
     "Immediate fall detection within 0.8 seconds, enabling rapid emergency response."),

    # Cat 3: Advanced Full Stack & Enterprise Development (BE021 - BE030)
    ("BE021", "AI-Powered Enterprise Resource Planning System", "BE", "Advanced Full Stack & Enterprise Development", "Advanced", "8-10 Weeks", 4999, 6999,
     "FastAPI, React / Next.js, PostgreSQL / SQLite, Redis, Tailwind",
     "A modular multi-department enterprise platform unifying procurement, inventory, human resources, accounting ledgers, and AI-driven quarterly demand forecasting.",
     "Enterprises operating disparate legacy software suffer from data fragmentation, delayed financial reconciliation, and inaccurate supply chain planning.",
     "Build an integrated modular ERP with robust role-based access control, relational transaction auditing, real-time ledger accounting, and AI demand predictions.",
     ["Multi-module architecture: HR & Payroll, Inventory, Sales, General Ledger", "Real-time double-entry accounting with automated balance sheet compilation", "Automated purchase order generation when inventory hits safety stock", "Executive business intelligence dashboard with AI quarterly forecasts"],
     "Manufacturing companies, wholesale distribution networks, and medium enterprises.",
     "Chief executive officers, chief financial officers, warehouse managers, and HR heads.",
     "Unified real-time enterprise visibility eliminating inter-department data lag."),

    ("BE022", "Microservices-Based E-Commerce Platform", "BE", "Advanced Full Stack & Enterprise Development", "Advanced", "8-10 Weeks", 4799, 6499,
     "FastAPI, Docker, RabbitMQ / Event Bus, React, SQLite / Postgres",
     "A distributed e-commerce architecture decomposed into autonomous microservices (Auth, Catalog, Cart, Order, Payment, Notification) communicating via event streams.",
     "Monolithic e-commerce applications fail to scale during seasonal flash sales and a crash in one module brings down the entire customer storefront.",
     "Implement decoupled containerized microservices communicating via asynchronous message queues (RabbitMQ/Redis) with API Gateway routing and circuit breakers.",
     ["Decoupled services: Product Catalog, Shopping Cart, Orders, Payments", "Asynchronous event-driven architecture with event bus message queues", "Resilient API Gateway with JWT validation, rate limiting, and CORS", "Fault tolerance with circuit breakers and fallback service degradation"],
     "High-scale digital retail, enterprise cloud platforms, and distributed systems labs.",
     "Cloud architects, distributed systems engineers, and e-commerce CTOs.",
     "Independent microservice scalability with zero single point of failure."),

    ("BE023", "Multi-Tenant SaaS Project Management Platform", "BE", "Advanced Full Stack & Enterprise Development", "Advanced", "8-10 Weeks", 4899, 6499,
     "FastAPI, PostgreSQL / SQLite, React, Tailwind CSS, WebSockets",
     "A collaborative SaaS workspace supporting multiple isolated corporate tenants, Kanban sprint boards, real-time team chat, time logging, and billing tiers.",
     "Modern organizations need collaborative project management platforms that guarantee strict data isolation between corporate clients while sharing infrastructure.",
     "Implement a multi-tenant database schema with tenant isolation, workspace invite workflows, interactive drag-and-drop Kanban boards, and usage-based subscriptions.",
     ["Tenant isolation ensuring zero cross-organization data leakage", "Interactive drag-and-drop Kanban boards with sprint milestone tracking", "Real-time team activity feed and task assignment notifications via WebSockets", "Subscription billing tiers with user seat limits and storage quotas"],
     "Software development agencies, corporate marketing teams, and remote consultancies.",
     "Product managers, scrum masters, software engineers, and SaaS administrators.",
     "Enterprise-grade multi-tenant collaboration with ironclad data partitioning."),

    ("BE024", "Distributed Online Examination System", "BE", "Advanced Full Stack & Enterprise Development", "Advanced", "7-9 Weeks", 3999, 5499,
     "FastAPI, React, WebRTC, WebSocket, SQLite / PostgreSQL",
     "A high-concurrency online examination platform with automated anti-cheat monitoring (browser focus loss, multi-face alerts), question shuffler, and instant grading.",
     "Remote university examinations face severe integrity challenges from unauthorized browser tab switching, proxy test-takers, and unscalable server bottlenecks.",
     "Develop a distributed testing platform with WebRTC webcam proctoring, browser blur event tracking, cryptographically randomized question delivery, and fault-tolerant autosave.",
     ["Scalable test-taking interface with continuous answer autosave to prevent data loss", "AI proctoring alerts: detects face disappearance, multiple faces, and tab switches", "Algorithmic question and option randomization per candidate to deter collusion", "Instant post-exam psychometric difficulty analysis and automated grading"],
     "National entrance examinations, university semester testing, and corporate certifications.",
     "Chief examiners, proctoring supervisors, and examination candidates.",
     "Zero-loss continuous test taking with robust automated integrity auditing."),

    ("BE025", "Real-Time Collaborative Code Editor", "BE", "Advanced Full Stack & Enterprise Development", "Advanced", "8-10 Weeks", 4699, 6299,
     "FastAPI, WebSockets, Operational Transformation / CRDT, Monaco Editor",
     "A browser-based collaborative programming IDE allowing multiple developers to edit code simultaneously, view live cursor positions, and execute code in sandboxes.",
     "Remote development teams and technical interviewers struggle with latency and edit collisions when collaborating in real time on code files.",
     "Implement Conflict-Free Replicated Data Types (CRDTs) or Operational Transformation over WebSockets integrated with Microsoft Monaco Editor and sandboxed code execution.",
     ["Simultaneous multi-user document editing with zero edit collisions", "Multi-colored live cursor indicators showing peer user selections", "Integrated Monaco Editor supporting syntax highlighting for 10+ languages", "Sandboxed server-side code execution with standard input and output display"],
     "Technical remote job interviews, pair programming, and coding classrooms.",
     "Pair programmers, technical interviewers, and student study groups.",
     "Sub-50ms synchronization latency across multiple simultaneous code collaborators."),

    ("BE026", "Intelligent Recruitment and Applicant Tracking System", "BE", "Advanced Full Stack & Enterprise Development", "Advanced", "7-9 Weeks", 3899, 5299,
     "FastAPI, React, spaCy NLP, SQLite / PostgreSQL, Tailwind CSS",
     "An enterprise hiring platform featuring automated resume parsing, candidate scoring against job requisitions, interview pipeline stages, and email automation.",
     "HR talent acquisition teams are overwhelmed by thousands of applicant resumes, leading to delayed hiring cycles and poor candidate experiences.",
     "Build an Applicant Tracking System (ATS) that extracts resume skills via NLP, ranks applicants by job fit score, and automates candidate stage progression.",
     ["Job requisition creation with custom skill weightings and knock-out questions", "Automated multi-resume ingestion with semantic match score ranking", "Kanban candidate pipeline: Sourced -> Screened -> Interview -> Offered", "Automated interview invitation scheduling and candidate feedback scorecards"],
     "Corporate HR departments, talent recruitment agencies, and hyper-growth startups.",
     "Talent acquisition leads, hiring managers, and prospective job candidates.",
     "Reduces applicant screening time by 75% while surfacing top-tier talent."),

    ("BE027", "Cloud-Based Hospital Information Management System", "BE", "Advanced Full Stack & Enterprise Development", "Advanced", "8-10 Weeks", 4899, 6699,
     "FastAPI, PostgreSQL / SQLite, React, Tailwind CSS, HL7/FHIR Mock",
     "An enterprise hospital information platform uniting inpatient admissions, electronic health records (EHR), surgical theater scheduling, pharmacy, and insurance claims.",
     "Large hospitals operating disconnected software systems risk medical prescription errors, bed allocation delays, and cumbersome insurance claim reconciliation.",
     "Deliver an enterprise hospital management platform complying with patient data privacy principles, integrating patient wards, diagnostic labs, and digital billing.",
     ["Inpatient bed management with visual ward occupancy and transfers", "Electronic Health Records (EHR) with longitudinal medical history and lab reports", "Pharmacy inventory integration with automated drug interaction alerts", "Patient billing console with insurance pre-authorization and itemized claims"],
     "Tertiary care hospitals, multi-specialty medical centers, and government health institutes.",
     "Medical superintendents, attending physicians, head nurses, and billing staff.",
     "Unified clinical workflow reducing patient admission and discharge delays by 50%."),

    ("BE028", "Smart Supply Chain Management Platform", "BE", "Advanced Full Stack & Enterprise Development", "Advanced", "8-10 Weeks", 4699, 6299,
     "FastAPI, React, PostgreSQL / SQLite, Leaflet Maps, WebSockets",
     "An end-to-end logistics visibility portal tracking shipment milestones, warehouse storage utilization, fleet locations, and estimated time of arrival (ETA).",
     "Global supply chains suffer from lack of shipment visibility, warehouse inventory bottlenecks, and inaccurate arrival estimations causing factory shutdowns.",
     "Implement an end-to-end supply chain visibility portal tracking consignments from supplier dispatch to warehouse receipt with dynamic ETA calculations.",
     ["Shipment consignment tracking with carrier milestone status updates", "Interactive live GPS fleet tracking map with transit delay alerts", "Warehouse storage bin allocation and pallet capacity telemetry", "Supplier vendor scorecard tracking on-time delivery percentages"],
     "Third-party logistics (3PL) providers, global manufacturers, and shipping lines.",
     "Supply chain directors, warehouse managers, and freight dispatchers.",
     "Real-time shipment visibility reducing transit communication inquiries by 80%."),

    ("BE029", "Real-Time Financial Transaction Monitoring System", "BE", "Advanced Full Stack & Enterprise Development", "Advanced", "8-10 Weeks", 4799, 6499,
     "FastAPI, Redis, WebSocket, Chart.js, SQLite / PostgreSQL",
     "A low-latency financial surveillance platform processing banking transaction streams, detecting compliance anomalies (AML), and visualizing market liquidity in real time.",
     "Financial regulatory compliance teams face strict penalties if money laundering or sanctioned fund transfers slip through high-speed banking settlement rails.",
     "Build an in-memory streaming transaction monitor using Redis pub/sub and WebSockets to evaluate transactions against Anti-Money Laundering (AML) velocity rules.",
     ["High-throughput transaction ingestion engine supporting 1,000+ tx/sec", "Real-time AML rule evaluation (rapid velocity spikes, round-amount structuring)", "Interactive compliance alert dashboard with one-click transaction freezes", "Live financial liquidity and settlement volume charts powered by WebSockets"],
     "Central banking regulators, fintech payment processors, and anti-fraud units.",
     "AML compliance officers, financial crime investigators, and treasury heads.",
     "Sub-10ms transaction compliance screening with zero processing bottleneck."),

    ("BE030", "Enterprise Workflow Automation Platform", "BE", "Advanced Full Stack & Enterprise Development", "Advanced", "8-10 Weeks", 4899, 6499,
     "FastAPI, React / Vue, DAG Execution Engine, SQLite / Postgres",
     "A visual drag-and-drop business process automation platform (similar to Zapier) allowing non-technical users to build conditional multi-step workflow pipelines.",
     "Corporate teams waste thousands of hours manually copying data between web forms, CRMs, spreadsheets, and notification channels.",
     "Develop a node-based workflow builder that executes Directed Acyclic Graphs (DAGs) of triggers, conditional filters, and actions with automatic retry queues.",
     ["Drag-and-drop visual workflow canvas connecting triggers and actions", "Configurable step connectors (Webhooks, Database Queries, Email, SMS)", "Conditional branching logic (if/else), loops, and data transformation", "Execution history inspector with detailed step-by-step input/output payloads"],
     "Corporate enterprise automation, digital marketing agencies, and operations teams.",
     "Business analysts, operations directors, and process automation architects.",
     "Eliminates repetitive data entry tasks with automated cross-platform workflows."),

    # Cat 4: Cybersecurity & Blockchain (BE031 - BE040)
    ("BE031", "AI-Powered Cyber Threat Intelligence Platform", "BE", "Cybersecurity & Blockchain", "Advanced", "8-10 Weeks", 4799, 6499,
     "Python, FastAPI, STIX/TAXII parser, Scikit-learn, Tailwind CSS",
     "A centralized threat intelligence hub that aggregates global threat feeds, parses Indicators of Compromise (IoCs), and uses NLP to classify hacker group tactics (MITRE ATT&CK).",
     "Security teams are flooded with thousands of disconnected threat alerts and struggle to correlate IoCs with known cyber threat actor campaigns.",
     "Build an automated threat intelligence portal that ingests STIX/TAXII feeds, normalizes IoCs (IPs, hashes, domains), and maps adversary behaviors to the MITRE ATT&CK matrix.",
     ["Automated ingestion of public and private threat feeds (AlienVault, MISP)", "Indicator of Compromise (IoC) extraction and confidence scoring", "Automated mapping of malware behavior to MITRE ATT&CK techniques", "Threat hunting dashboard with search across historical enterprise logs"],
     "Enterprise Security Operations Centers (SOC), MSSPs, and CERT teams.",
     "Threat intelligence analysts, SOC managers, and cybersecurity researchers.",
     "Transforms raw threat indicators into actionable defense rules in minutes."),

    ("BE032", "Blockchain-Based Decentralized Identity System", "BE", "Cybersecurity & Blockchain", "Advanced", "8-10 Weeks", 4999, 6999,
     "Solidity / Web3, FastAPI, Cryptographic Signatures, React",
     "A Self-Sovereign Identity (SSI) framework allowing users to own their digital credentials and prove age or qualifications using zero-knowledge cryptographic proofs.",
     "Centralized identity providers (Google, Facebook SSO) track user activity across the web and are vulnerable to catastrophic credential database breaches.",
     "Implement W3C Decentralized Identifiers (DIDs) and Verifiable Credentials on an Ethereum/Polygon compatible ledger allowing users to control their personal data.",
     ["Decentralized Identifier (DID) creation and cryptographic key pair management", "Verifiable Credential issuance by accredited authorities (Universities, Govt)", "Selective disclosure: prove attributes (e.g. over 21) without revealing full DOB", "Decentralized verification portal for employers and service providers"],
     "Digital citizenship, cross-border university admissions, and privacy-preserving KYC.",
     "Privacy-minded citizens, compliance officers, and verifying institutions.",
     "Complete user privacy preservation with cryptographically unforgeable credentials."),

    ("BE033", "Smart Contract-Based Digital Certificate Verification", "BE", "Cybersecurity & Blockchain", "Advanced", "7-9 Weeks", 4299, 5899,
     "Solidity, Web3.py, FastAPI, Ethereum Testnet / Polygon, Tailwind",
     "An immutable credential issuance platform where university graduation degrees are anchored to smart contracts, enabling instant, free employer authenticity checks.",
     "Resume fraud and fake degree mills undermine academic credibility and cost employers millions in unverified hires.",
     "Deploy Ethereum smart contracts that store immutable cryptographic hashes of university certificates, verifiable globally with zero recurring fee.",
     ["University admin portal to batch-mint digital certificate hashes on-chain", "Tamper-evident certificate generator with embedded QR code and transaction hash", "Public verification portal: drag-and-drop certificate PDF to verify on-chain", "Revocation registry allowing universities to invalidate compromised degrees"],
     "Higher education boards, professional credentialing bodies, and HR departments.",
     "University registrars, corporate background checkers, and graduates.",
     "100% tamper-proof degree verification on public blockchain ledgers."),

    ("BE034", "Advanced Network Intrusion Detection System", "BE", "Cybersecurity & Blockchain", "Advanced", "8-10 Weeks", 4699, 6299,
     "Python, Scapy, Snort Rules Engine, FastAPI, Chart.js",
     "A hybrid intrusion detection system combining signature matching with statistical traffic anomaly analysis to identify network reconnaissance, exfiltration, and exploits.",
     "Modern advanced persistent threat (APT) actors use encrypted channels and custom evasion techniques that bypass legacy firewall rules.",
     "Combine Scapy deep packet inspection with custom Snort signature rules and statistical Shannon entropy calculations to identify malicious exfiltration tunnels.",
     ["Live packet capture (PCAP) inspection with Scapy protocol decoding", "Signature matching against an extensible database of known CVE exploits", "Statistical anomaly detection flagging DNS tunneling and beaconing intervals", "Real-time attack alert console with packet hexadecimal inspection inspector"],
     "Corporate network perimeters, cloud VPC monitoring, and cybersecurity labs.",
     "Network defense engineers, SOC analysts, and security auditors.",
     "Detects both known CVE attacks and covert command-and-control exfiltration."),

    ("BE035", "Zero-Trust Security Management Platform", "BE", "Cybersecurity & Blockchain", "Advanced", "8-10 Weeks", 4899, 6699,
     "FastAPI, mTLS, JWT, SQLite / PostgreSQL, React, Tailwind CSS",
     "An enterprise zero-trust architecture enforcing continuous device posture assessment, contextual authentication, dynamic least-privilege access, and session revocation.",
     "Traditional perimeter-based security ('castle-and-moat') fails once an attacker compromises a single internal employee workstation.",
     "Implement Zero-Trust Network Access (ZTNA) principles: verify explicitly, enforce least-privilege, and continuously evaluate device risk before granting API access.",
     ["Continuous contextual authentication (IP reputation, device posture, time)", "Dynamic least-privilege policy engine granting temporary access to microservices", "Instant single-click session revocation across all enterprise endpoints", "Comprehensive policy enforcement audit log with real-time risk scores"],
     "Enterprise remote work infrastructure, defense networks, and fintech backends.",
     "Chief information security officers, cloud security architects, and IT leads.",
     "Eliminates lateral attacker movement inside corporate networks."),

    ("BE036", "Secure Cloud Data Storage Using Encryption", "BE", "Cybersecurity & Blockchain", "Advanced", "7-9 Weeks", 4199, 5699,
     "Python, Cryptography (AES-256-GCM, RSA), FastAPI, React",
     "A zero-knowledge encrypted cloud storage vault where files are encrypted on the client before transmission, ensuring cloud providers cannot view confidential data.",
     "Storing proprietary files on commercial cloud storage exposes sensitive data to subpoena, provider insider threats, and cloud data leaks.",
     "Implement zero-knowledge client-side encryption using hybrid AES-256-GCM and RSA-4096 cryptography where only the user holds the private decryption keys.",
     ["Zero-knowledge architecture: raw plaintext never leaves the client browser", "Hybrid encryption: fast AES-256-GCM payload encryption with RSA key wrapping", "Secure cryptographic key exchange for sharing encrypted files with peers", "Tamper-evident file integrity checks using SHA-512 cryptographic digests"],
     "Confidential research data, legal case files, and executive file archives.",
     "Privacy-sensitive enterprises, legal practitioners, and whistleblowers.",
     "Absolute data confidentiality with zero trust required in the storage provider."),

    ("BE037", "Digital Forensics and Cybercrime Investigation Platform", "BE", "Cybersecurity & Blockchain", "Advanced", "8-10 Weeks", 4699, 6299,
     "Python, Volatility / PyTSK, SQLite, FastAPI, Tailwind CSS",
     "A digital evidence analysis portal that ingests forensic disk images and memory dumps, reconstructs chronological timelines, and extracts deleted artifacts.",
     "Digital forensics investigators face immense backlogs manually parsing gigabytes of raw disk images and volatile RAM dumps to find evidence of cybercrimes.",
     "Build an automated forensic timeline reconstructor that parses file systems (FAT, NTFS), browser history, registry hives, and volatile memory artifacts into an interactive timeline.",
     ["Disk image and memory dump ingestion with cryptographic hash preservation", "Automated extraction of deleted files, web browser history, and USB logs", "Unified chronological investigation timeline with search and filtering", "Chain of custody tracking and court-admissible forensic report generator"],
     "Law enforcement forensic units, incident response teams, and cyber law firms.",
     "Digital forensics examiners, incident response handlers, and cyber prosecutors.",
     "Cuts forensic disk triage time by 70% while maintaining strict chain of custody."),

    ("BE038", "Blockchain-Based Supply Chain Traceability System", "BE", "Cybersecurity & Blockchain", "Advanced", "8-10 Weeks", 4899, 6499,
     "Solidity, Web3.py, FastAPI, React, QR Code Engine",
     "An end-to-end supply chain transparency ledger recording raw material provenance, temperature conditions, and custody handoffs on an immutable blockchain.",
     "Counterfeit pharmaceuticals and adulterated food products cause thousands of deaths annually because consumers and regulators lack end-to-end provenance proof.",
     "Deploy smart contracts to record each custody handoff from farm/manufacturer to consumer, verifiable by scanning a tamper-evident QR code on the packaging.",
     ["Smart contracts tracking product creation, batch numbers, and custody stages", "IoT sensor data logging (storage temperature, humidity) onto the ledger", "Public consumer portal: scan QR code to view complete verified origin timeline", "Automated counterfeit alert if an unauthorized or duplicate serial code is scanned"],
     "Pharmaceutical distribution, organic food certification, and luxury goods.",
     "Supply chain directors, food safety auditors, and end consumers.",
     "Guaranteed product authenticity and end-to-end supply chain provenance."),

    ("BE039", "Intelligent Phishing and Malware Detection Platform", "BE", "Cybersecurity & Blockchain", "Advanced", "7-9 Weeks", 3999, 5499,
     "Python, PEfile, Scikit-learn, YARA rules, FastAPI, Tailwind",
     "A dual malware and email threat analysis engine that inspects suspicious Windows PE executable files, extracts static API call features, and classifies malware families.",
     "Malicious email attachments and zero-day trojans evade traditional antivirus software by using packers, crypters, and polymorphic code techniques.",
     "Combine static PE header feature extraction (imports, sections, entropy) and YARA pattern matching with an ensemble Random Forest classifier to flag malware.",
     ["Executable file upload with static analysis (Import table, Sections, Hashes)", "Machine learning malware classification score based on behavioral import APIs", "Integrated YARA rule engine scanning for known ransomware and banking trojans", "Visual sandbox report highlighting dangerous Windows API calls"],
     "Enterprise email gateways, security triage desks, and malware analysis labs.",
     "Malware analysts, reverse engineers, and SOC tier-2 investigators.",
     "Rapid static malware triage in under 5 seconds without executing live malware."),

    ("BE040", "Privacy-Preserving Authentication System", "BE", "Cybersecurity & Blockchain", "Advanced", "8-10 Weeks", 4799, 6499,
     "Python, Cryptography, Zero-Knowledge Proofs (ZKP), FastAPI, React",
     "A zero-knowledge authentication gateway allowing users to prove knowledge of their secret password without ever transmitting or storing password hashes on the server.",
     "Server credential databases are leaked daily in corporate breaches, exposing millions of user passwords to rainbow table and brute-force cracking.",
     "Implement Zero-Knowledge Proofs (ZKP using Schnorr protocol or SRP) where authentication succeeds purely through mathematical challenge-response without transmitting secrets.",
     ["Zero-knowledge authentication handshake eliminating server-side password storage", "Mathematical resistance to eavesdropping and credential database breaches", "Time-bound cryptographic session tokens with instant revocation", "Multi-factor authentication (MFA) verification integration"],
     "High-security financial portals, defense applications, and privacy services.",
     "Security engineers, identity architects, and privacy-conscious users.",
     "Immune to server-side credential theft, rainbow tables, and interception attacks."),

    # Cat 5: Cloud Computing, IoT & Distributed Systems (BE041 - BE050)
    ("BE041", "Cloud-Native Serverless Application Platform", "BE", "Cloud Computing, IoT & Distributed Systems", "Advanced", "8-10 Weeks", 4799, 6499,
     "Python, Docker, FastAPI, Celery / Worker Queue, Redis, Tailwind",
     "A Function-as-a-Service (FaaS) execution platform that allows developers to deploy isolated code snippets that spin up in micro-containers, execute on demand, and autoscale.",
     "Developers need lightweight serverless execution environments without being locked into expensive proprietary cloud vendor pricing models.",
     "Build a self-hosted serverless platform using Docker containers and Celery task workers that executes event-driven code snippets with resource quotas and billing metrics.",
     ["Code editor for writing and deploying Python/Node functions", "Automated container spin-up and teardown per HTTP invocation", "Execution latency, memory usage telemetry, and billing metrics", "Configurable event triggers: HTTP Webhooks, Scheduled Cron, Database events"],
     "Private enterprise clouds, developer edge computing, and university cloud labs.",
     "Cloud developers, DevOps engineers, and infrastructure managers.",
     "Sub-200ms cold start execution of isolated serverless micro-functions."),

    ("BE042", "IoT-Based Smart Agriculture Monitoring System", "BE", "Cloud Computing, IoT & Distributed Systems", "Advanced", "7-9 Weeks", 3899, 5299,
     "Python, MQTT / HTTP, ESP32 Mock, FastAPI, Chart.js, SQLite",
     "An end-to-end smart farming IoT telemetry hub collecting soil moisture, ambient temperature, humidity, and sunlight data to trigger automated drip irrigation.",
     "Injudicious agricultural irrigation wastes vast quantities of water and causes soil salinity, while manual field monitoring is labor-intensive.",
     "Build an IoT cloud portal that ingests sensor streams via MQTT/HTTP, visualizes soil moisture levels in real time, and automates irrigation valve actuators.",
     ["Simulated and hardware MQTT sensor telemetry ingestion (Moisture, Temp, Lux)", "Automated threshold-based irrigation pump actuator control logic", "Weather forecast integration to delay irrigation ahead of forecasted rainfall", "Crop water requirement analytics dashboard with water conservation metrics"],
     "Precision agriculture, smart greenhouses, and water management authorities.",
     "Farmers, greenhouse operators, and agricultural researchers.",
     "Conserves up to 35% irrigation water while optimizing crop growth conditions."),

    ("BE043", "Smart City Traffic Management Using IoT and AI", "BE", "Cloud Computing, IoT & Distributed Systems", "Advanced", "8-10 Weeks", 4899, 6699,
     "Python, FastAPI, Leaflet Maps, Traffic Flow Algorithm, WebSocket",
     "A centralized smart city traffic command portal that coordinates IoT intersection sensors, predicts congestion choke points, and dynamically optimizes traffic signal timings.",
     "Rigid, pre-programmed traffic signal timings cause massive gridlocks during peak hours and leave green lights running on empty cross streets.",
     "Develop an adaptive traffic control system that aggregates live sensor counts, calculates dynamic green light durations, and clears emergency vehicle corridors.",
     ["Multi-intersection map layout with real-time vehicle queue counts", "Dynamic signal timing adjustment algorithm based on live traffic pressure", "Priority emergency corridor override: gives green waves to ambulances", "Daily congestion reduction reports and vehicle emission savings metrics"],
     "Municipal smart city traffic management centers and urban transit authorities.",
     "City traffic planners, emergency dispatchers, and municipal engineers.",
     "Reduces average intersection waiting time by 28% and clears emergency routes fast."),

    ("BE044", "Edge Computing-Based Real-Time Monitoring System", "BE", "Cloud Computing, IoT & Distributed Systems", "Advanced", "8-10 Weeks", 4699, 6299,
     "Python, FastAPI, Edge Worker Daemon, SQLite, Chart.js",
     "A distributed edge computing architecture that performs sensor data preprocessing and anomaly detection locally at edge gateways before transmitting summaries to the cloud.",
     "Transmitting continuous high-frequency raw sensor data from thousands of industrial machines overwhelms cloud bandwidth and incurs exorbitant cloud egress fees.",
     "Design a two-tier edge-cloud architecture where edge nodes run lightweight anomaly checks and filter redundant sensor noise, transmitting only critical events.",
     ["Edge node daemon simulating Raspberry Pi / industrial gateway data filtering", "Local lightweight anomaly detection triggering instant sub-second local alerts", "Bandwidth-efficient synchronization of aggregated telemetry to central cloud", "Edge gateway health monitoring, heartbeats, and remote configuration"],
     "Offshore oil rigs, mining operations, remote wind farms, and manufacturing lines.",
     "Industrial IoT engineers, edge infrastructure managers, and plant operators.",
     "Reduces cloud data transmission bandwidth by over 80% while preserving alerts."),

    ("BE045", "Kubernetes-Based Microservices Deployment Platform", "BE", "Cloud Computing, IoT & Distributed Systems", "Advanced", "8-10 Weeks", 4999, 6999,
     "Python, Kubernetes Python Client, Docker, FastAPI, React",
     "A developer-centric internal developer platform (IDP) that simplifies deploying, scaling, and monitoring containerized microservices on Kubernetes clusters.",
     "Managing Kubernetes YAML manifests, ingress controllers, and horizontal pod autoscalers is overwhelmingly complex for application developers.",
     "Create an intuitive web console that generates Kubernetes deployments, manages rolling updates, monitors pod health metrics, and visualizes service meshes.",
     ["One-click container deployment with automated manifest generation", "Visual pod replica scaler (Horizontal Pod Autoscaling) and rolling restarts", "Real-time pod logs streaming and container resource metrics (CPU/RAM)", "Ingress routing and domain SSL certificate status monitor"],
     "Software engineering teams, DevOps consultancies, and cloud training bootcamps.",
     "DevOps engineers, platform reliability leads, and software developers.",
     "Simplifies Kubernetes application management into an intuitive developer UI."),

    ("BE046", "Distributed File Storage and Management System", "BE", "Cloud Computing, IoT & Distributed Systems", "Advanced", "8-10 Weeks", 4799, 6499,
     "Python, FastAPI, Consistent Hashing, Distributed Storage Nodes",
     "A fault-tolerant distributed object store that fragments files into chunks, replicates chunks across multiple storage nodes using consistent hashing, and self-heals.",
     "Centralized file servers are single points of failure that cause catastrophic data outages if a single storage drive or power supply fails.",
     "Implement a distributed file storage cluster utilizing Consistent Hashing and replication factors to distribute file chunks across nodes with automated rebalancing.",
     ["File chunking and cryptographic content-addressable storage (CAS)", "Consistent hashing ring mapping chunks across multiple virtual storage nodes", "Automatic replication factor (3x) ensuring data availability during node failures", "Cluster management dashboard showing storage node health and disk capacity"],
     "Cloud storage infrastructures, high-availability video streaming, and archives.",
     "Storage architects, infrastructure engineers, and distributed systems students.",
     "Guaranteed data availability even during simultaneous failure of storage nodes."),

    ("BE047", "IoT-Based Smart Energy Management System", "BE", "Cloud Computing, IoT & Distributed Systems", "Advanced", "7-9 Weeks", 3999, 5499,
     "Python, MQTT, FastAPI, Chart.js, SQLite, Energy Forecaster",
     "An intelligent commercial energy telemetry platform monitoring real-time power consumption, detecting energy waste, and forecasting monthly utility bills.",
     "Commercial buildings and university campuses waste up to 30% of their electrical energy running HVAC and lighting in unoccupied zones.",
     "Ingest smart electricity meter telemetry, identify peak demand surges, correlate power consumption with building occupancy, and alert managers to energy leaks.",
     ["Sub-meter power consumption ingestion (HVAC, Lighting, Server Room)", "Real-time wattage graphs with peak demand surge alerts", "Automated detection of vampire energy drain during non-working hours", "Monthly electricity bill projection and carbon emission footprint calculation"],
     "Campus facilities, commercial office complexes, and industrial warehouses.",
     "Energy managers, facility directors, and corporate sustainability officers.",
     "Identifies energy waste, driving a 15-25% reduction in monthly electricity bills."),

    ("BE048", "Intelligent Industrial Automation Using IoT", "BE", "Cloud Computing, IoT & Distributed Systems", "Advanced", "8-10 Weeks", 4699, 6299,
     "Python, Modbus / MQTT, FastAPI, Real-time Dashboard, SQLite",
     "A smart factory telemetry hub connecting industrial machinery, monitoring PLC states, visualizing assembly line throughput, and stopping lines during anomalies.",
     "Traditional manufacturing plants suffer from blind spots on production line bottlenecks and slow human reaction to equipment safety anomalies.",
     "Build an Industrial IoT (IIoT) supervision portal that connects to industrial protocols, tracks Overall Equipment Effectiveness (OEE), and triggers safety shutdowns.",
     ["Industrial PLC state monitoring (Running, Idle, Fault, Maintenance)", "Overall Equipment Effectiveness (OEE) calculation: Availability x Performance x Quality", "Automated production line emergency trip logic on critical threshold breaches", "Batch production yield tracking and shift handover reporting"],
     "Automotive manufacturing, food packaging plants, and electronics assembly lines.",
     "Plant managers, industrial automation engineers, and quality assurance leads.",
     "Real-time OEE visibility enabling immediate response to assembly line stalls."),

    ("BE049", "Cloud-Based Real-Time Video Processing Platform", "BE", "Cloud Computing, IoT & Distributed Systems", "Advanced", "8-10 Weeks", 4899, 6699,
     "Python, FFmpeg, Celery, Redis, FastAPI, HLS Streaming",
     "A scalable cloud media processing pipeline that ingests raw video uploads, transcodes them into multi-bitrate HLS streams, extracts thumbnails, and runs content moderation.",
     "Transcoding video files into adaptive bitrates (1080p, 720p, 480p) is computationally heavy and quickly overwhelms standard single-server web backends.",
     "Construct a distributed worker pipeline using Celery and FFmpeg that shreds video jobs into parallel transcoding tasks and prepares adaptive HTTP Live Streams (HLS).",
     ["Multi-resolution video transcoding (1080p, 720p, 480p, 360p) using FFmpeg", "Automated generation of HLS (.m3u8) adaptive bitrate streaming playlists", "Video content moderation scanning keyframes for inappropriate content", "Interactive responsive video player with quality selector and bandwidth adaptation"],
     "Video-on-demand services, edtech lecture portals, and social media apps.",
     "Media engineering leads, digital content platforms, and video developers.",
     "Smooth buffer-free video playback across variable network bandwidths."),

    ("BE050", "Smart Water Quality Monitoring and Prediction System", "BE", "Cloud Computing, IoT & Distributed Systems", "Advanced", "7-9 Weeks", 3899, 5299,
     "Python, Scikit-learn, FastAPI, Leaflet Maps, SQLite",
     "An environmental IoT monitoring system tracking pH, turbidity, dissolved oxygen, and temperature to compute Water Quality Index (WQI) and predict water potability.",
     "Contaminated water supplies cause widespread health crises in rural and urban municipalities due to delayed laboratory sample testing.",
     "Deploy an IoT telemetry pipeline connecting water sensor probes, calculating real-time Water Quality Index (WQI), and predicting potability using Random Forest.",
     ["Multi-parameter sensor telemetry ingestion (pH, Turbidity, TDS, Dissolved Oxygen)", "Automated calculation of global Water Quality Index (WQI) scores", "Machine learning classification of water safety (Potable vs Non-Potable)", "Geographic water source map with instant contamination alerts for municipalities"],
     "Municipal water treatment plants, lake conservation authorities, and rural supply.",
     "Environmental health inspectors, water board engineers, and public health officials.",
     "Continuous automated water safety evaluation without waiting days for lab culture results.")
]

# Adding final 10 BE projects (BE051 - BE060)
BE_PROJECTS_FINAL = [
    # Cat 6: Advanced Data Science & Emerging Technologies (BE051 - BE060)
    ("BE051", "Real-Time Big Data Analytics Platform", "BE", "Advanced Data Science & Emerging Technologies", "Advanced", "8-10 Weeks", 4899, 6699,
     "Python, Apache Kafka Mock / Redis Streams, FastAPI, Chart.js",
     "A streaming big data analytics engine processing thousands of live transaction and click events per second with tumbling window aggregations and anomaly alerts.",
     "Traditional batch data warehouses take hours to process day-old data, leaving businesses blind to immediate operational crises and fraud waves.",
     "Implement high-throughput stream processing using Redis Streams/Kafka architecture with sliding and tumbling window aggregations and live dashboard streaming.",
     ["High-volume event ingestion stream capable of processing 2,000+ events/sec", "Real-time sliding window aggregations (1-min, 5-min, 1-hour metrics)", "Automated threshold anomaly detection and webhook notification dispatch", "Interactive low-latency streaming analytics dashboard"],
     "E-commerce monitoring, telecommunications network telemetry, and fintech ops.",
     "Big data engineers, infrastructure architects, and operational analysts.",
     "Sub-second streaming analytics transforming raw event streams into immediate insights."),

    ("BE052", "Graph Neural Network-Based Fraud Detection System", "BE", "Advanced Data Science & Emerging Technologies", "Advanced", "8-10 Weeks", 4999, 6999,
     "Python, PyTorch Geometric, NetworkX, FastAPI, Cytoscape.js",
     "A graph intelligence platform mapping financial transactions into a complex heterogeneous graph, using Graph Convolutional Networks (GCN) to detect fraud rings.",
     "Sophisticated fraud syndicates use synthetic identities and circular fund routing across dozens of mule accounts, easily evading single-transaction ML classifiers.",
     "Model accounts and transactions as nodes and edges in a graph, applying Graph Neural Networks (GCN) to uncover suspicious multi-hop circular transaction rings.",
     ["Heterogeneous financial transaction graph construction with NetworkX", "Graph Neural Network (GCN/GAT) node classification detecting mule accounts", "Interactive graph visualization explorer highlighting dense fraud subgraphs", "Fraud ring report detailing connected accounts and total laundered volume"],
     "Bank anti-fraud divisions, cryptocurrency exchange compliance, and law enforcement.",
     "Financial crime investigators, graph data scientists, and AML analysts.",
     "Uncovers coordinated multi-party fraud rings invisible to standard tabular models."),

    ("BE053", "Financial Market Prediction Using Deep Learning", "BE", "Advanced Data Science & Emerging Technologies", "Advanced", "8-10 Weeks", 4699, 6299,
     "Python, PyTorch, Bidirectional LSTM, Attention Mechanism, Plotly",
     "An algorithmic trading analysis portal utilizing Bidirectional LSTM networks with Attention mechanisms to predict market asset price trends and volatility regimes.",
     "Financial time series are notoriously non-stationary and noisy, causing standard moving average strategies to suffer heavy losses during sudden market regime shifts.",
     "Construct a deep sequence model with Bidirectional LSTM and Attention layers trained on multi-feature market data (OHLCV, Technical Indicators, Macro Data).",
     ["Automated historical market data fetching with feature engineering (RSI, ATR, MACD)", "Bidirectional LSTM with Attention model predicting next-period price direction", "Simulated backtesting engine calculating Sharpe Ratio, Max Drawdown, and Win Rate", "Interactive trading equity curve and risk exposure visualization"],
     "Quantitative hedge funds, proprietary trading desks, and fintech research.",
     "Quantitative analysts, algorithmic traders, and financial engineers.",
     "Provides statistically robust directional bias and risk metrics for asset trading."),

    ("BE054", "Large Language Model-Based Code Intelligence Platform", "BE", "Advanced Data Science & Emerging Technologies", "Advanced", "8-10 Weeks", 4999, 6999,
     "Python, Transformers / StarCoder, AST Parser, FastAPI, React",
     "A self-hosted developer copilot platform offering semantic code search, automated docstring generation, test case synthesis, and cross-language translation.",
     "Enterprise engineering teams cannot upload proprietary codebases to public commercial AI services due to strict intellectual property and data sovereignty rules.",
     "Deploy an on-premises code intelligence pipeline utilizing specialized open-weight code models to perform code explanation, unit test generation, and refactoring.",
     ["Semantic natural language code search across entire enterprise repositories", "Automated unit test generation (pytest, jest) for selected functions", "Comprehensive docstring and API documentation generator", "Code translation between languages (e.g. Python to TypeScript)"],
     "Enterprise software engineering, defense software labs, and financial IT systems.",
     "Software developers, technical leads, and engineering directors.",
     "Boosts engineering velocity by 30% without leaking proprietary source code."),

    ("BE055", "Explainable AI-Based Decision Support System", "BE", "Advanced Data Science & Emerging Technologies", "Advanced", "7-9 Weeks", 3999, 5499,
     "Python, SHAP, LIME, Scikit-learn, FastAPI, Chart.js",
     "A transparent machine learning auditing portal that calculates SHAP and LIME values to explain black-box loan approval and medical risk predictions to humans.",
     "Regulatory frameworks (GDPR, EU AI Act) mandate that automated AI decisions in credit, hiring, and healthcare must provide clear, understandable explanations.",
     "Wrap machine learning classifiers with SHAP (SHapley Additive exPlanations) and LIME to generate individual waterfall charts showing exact feature contributions.",
     ["Model-agnostic explainability suite supporting XGBoost, Random Forest, and Neural Nets", "Individual prediction waterfall plots showing positive/negative feature impacts", "Global feature importance charts revealing overall model decision patterns", "Compliance-ready decision justification summary in plain English"],
     "Banking credit risk, insurance underwriting, healthcare diagnosis, and legal AI.",
     "Credit risk officers, clinical doctors, and AI ethics compliance auditors.",
     "Eliminates AI black-box mystery, ensuring full regulatory compliance and trust."),

    ("BE056", "Real-Time Social Media Sentiment Analysis Platform", "BE", "Advanced Data Science & Emerging Technologies", "Advanced", "7-9 Weeks", 3899, 5299,
     "Python, VADER / RoBERTa, FastAPI, WordCloud, Chart.js, SQLite",
     "A brand reputation monitoring portal that scrapes social media mentions, analyzes customer sentiment polarity, and generates real-time PR crisis alerts.",
     "Brand managers learn about public relations crises hours too late because manually tracking thousands of social media comments is impossible.",
     "Deploy transformer-based sentiment analysis (RoBERTa/VADER) to analyze incoming stream data, compute sentiment polarity, and trigger alerts on sudden negative spikes.",
     ["Keyword and hashtag feed monitoring across social media streams", "Sentiment classification into Positive, Neutral, and Negative with emotion tags", "Real-time trending topics and complaint word clouds", "Automated PR crisis alert triggered when negative sentiment exceeds 30%"],
     "Brand management agencies, corporate communications, and political campaigns.",
     "Brand managers, public relations directors, and social media strategists.",
     "Instant crisis alerts within 5 minutes of a negative sentiment surge."),

    ("BE057", "Digital Twin-Based Industrial Monitoring System", "BE", "Advanced Data Science & Emerging Technologies", "Advanced", "8-10 Weeks", 4999, 6999,
     "Python, Three.js / WebGL, MQTT, FastAPI, Real-Time Physics",
     "A 3D virtual digital twin replicating an industrial robotic arm and conveyor, synchronizing physical IoT sensor movements with a live 3D browser simulation.",
     "Operators cannot physically inspect hazardous manufacturing environments (smelters, nuclear, robotic cells) to assess mechanical wear and operational status.",
     "Construct a real-time digital twin using Three.js that mirrors physical IoT telemetry in an interactive 3D model with thermal overlays and stress diagnostics.",
     ["Interactive 3D mechanical asset visualizer powered by Three.js", "Sub-second synchronization with physical sensor telemetry streams", "Thermal heatmap visualization identifying overheated motor joints", "What-if simulation mode testing machinery behavior under increased speeds"],
     "Robotics manufacturing, aerospace testing, and smart factory control rooms.",
     "Plant operations managers, robotics engineers, and digital twin architects.",
     "Enables safe, continuous visual inspection of high-hazard industrial machinery."),

    ("BE058", "Federated Learning-Based Privacy-Preserving AI System", "BE", "Advanced Data Science & Emerging Technologies", "Advanced", "8-10 Weeks", 4999, 6999,
     "Python, PyTorch, Federated Averaging (FedAvg), FastAPI, Tailwind",
     "A decentralized collaborative machine learning framework allowing multiple hospitals to train a joint disease model without ever sharing raw patient records.",
     "Healthcare institutions cannot pool patient datasets to train AI models due to strict medical data privacy laws (HIPAA) and commercial confidentiality.",
     "Implement the Federated Averaging (FedAvg) algorithm where local nodes train models on private local data, sending only mathematical model weights to a coordinator.",
     ["Multi-client federated training coordinator simulating independent hospitals", "Local gradient computation on private decentralized datasets", "Secure central model aggregation using Federated Averaging (FedAvg)", "Model convergence tracking comparing federated versus centralized accuracy"],
     "Healthcare consortia, banking fraud defense, and privacy-preserving AI labs.",
     "Medical AI researchers, privacy compliance officers, and data scientists.",
     "High-accuracy collaborative AI model trained with 100% data privacy preservation."),

    ("BE059", "AI-Powered Disaster Prediction and Early Warning System", "BE", "Advanced Data Science & Emerging Technologies", "Advanced", "8-10 Weeks", 4899, 6699,
     "Python, Scikit-learn, Leaflet Maps, Weather APIs, FastAPI",
     "A natural disaster risk analytics portal processing meteorological and hydrological satellite feeds to forecast flood and landslide risks and broadcast evacuation alerts.",
     "Communities face catastrophic losses during severe weather events due to late evacuations caused by fragmented, non-localized disaster warnings.",
     "Integrate rainfall, river gauge data, and terrain elevation models with machine learning to predict flash flood probabilities and send localized evacuation warnings.",
     ["Meteorological radar and river level telemetry data ingestion", "Flash flood and landslide susceptibility prediction algorithm", "Interactive GIS hazard risk map with flood inundation simulation zones", "Multi-tier emergency evacuation zone warning broadcast generator"],
     "Disaster management authorities, civil defense agencies, and humanitarian NGOs.",
     "Emergency response coordinators, meteorological analysts, and city mayors.",
     "Provides early evacuation warnings 6 hours ahead of flash flood cresting."),

    ("BE060", "Autonomous Multi-Agent Business Intelligence Platform", "BE", "Advanced Data Science & Emerging Technologies", "Advanced", "8-10 Weeks", 4999, 6999,
     "Python, Multi-Agent Swarm, LangChain, FastAPI, React",
     "An executive business intelligence platform where autonomous AI agents (Data Analyst, Competitor Tracker, Financial Auditor) synthesize cross-department strategies.",
     "C-suite executives wait weeks for disparate department heads to compile slide decks, resulting in delayed strategic decisions in fast-moving markets.",
     "Deploy a collaborative swarm of specialized AI agents that query enterprise databases, analyze competitor public filings, and debate strategic recommendations.",
     ["Multi-agent role specialization: Revenue Agent, Cost Auditor, Competitor Scout", "Autonomous cross-checking and debate between agents to eliminate bias", "Natural language query interface: 'What caused our Q3 margin dip in Europe?'", "Automated executive boardroom briefing generation with verified data charts"],
     "Executive boardroom strategy, venture capital due diligence, and enterprise CFOs.",
     "Chief executive officers, chief financial officers, and strategy directors.",
     "Delivers comprehensive C-suite strategic intelligence in under 3 minutes.")
]

ALL_PROJECTS = RAW_CATALOGUE + BE_PROJECTS + BE_PROJECTS_FINAL

print(f"Total projects prepared: {len(ALL_PROJECTS)}")
assert len(ALL_PROJECTS) == 120, f"Expected 120 projects, found {len(ALL_PROJECTS)}"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    # Enable WAL mode for high concurrency
    cur.execute("PRAGMA journal_mode = WAL;")

    # Drop old tables if re-initializing cleanly
    cur.executescript("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        full_name TEXT NOT NULL,
        mobile TEXT,
        college TEXT,
        course TEXT,
        academic_year TEXT,
        role TEXT DEFAULT 'student',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_code TEXT UNIQUE NOT NULL,
        title TEXT NOT NULL,
        slug TEXT UNIQUE NOT NULL,
        academic_level TEXT NOT NULL,
        category TEXT NOT NULL,
        subcategory TEXT NOT NULL,
        difficulty TEXT NOT NULL,
        duration TEXT NOT NULL,
        price INTEGER NOT NULL,
        discount_price INTEGER,
        tech_summary TEXT,
        image_url TEXT NOT NULL,
        description TEXT NOT NULL,
        problem_statement TEXT NOT NULL,
        proposed_solution TEXT NOT NULL,
        objectives TEXT NOT NULL,
        scope TEXT NOT NULL,
        real_world_apps TEXT NOT NULL,
        expected_outcomes TEXT NOT NULL,
        tech_stack_json TEXT NOT NULL,
        features_json TEXT NOT NULL,
        user_roles TEXT NOT NULL,
        architecture TEXT NOT NULL,
        database_design TEXT NOT NULL,
        api_docs TEXT NOT NULL,
        development_roadmap TEXT NOT NULL,
        academic_deliverables TEXT NOT NULL,
        is_published INTEGER DEFAULT 1,
        is_featured INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_number TEXT UNIQUE NOT NULL,
        user_id INTEGER NOT NULL,
        project_id INTEGER NOT NULL,
        amount INTEGER NOT NULL,
        status TEXT DEFAULT 'pending',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (project_id) REFERENCES projects(id)
    );

    CREATE TABLE IF NOT EXISTS payments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        project_id INTEGER NOT NULL,
        amount INTEGER NOT NULL,
        utr_reference TEXT,
        screenshot_path TEXT,
        status TEXT DEFAULT 'pending',
        verified_by TEXT,
        verified_at TIMESTAMP,
        verification_notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (order_id) REFERENCES orders(id),
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (project_id) REFERENCES projects(id)
    );

    CREATE TABLE IF NOT EXISTS payment_settings (
        id INTEGER PRIMARY KEY,
        upi_mobile TEXT NOT NULL,
        upi_id TEXT NOT NULL,
        account_name TEXT NOT NULL,
        qr_code_path TEXT NOT NULL,
        instructions TEXT NOT NULL,
        support_phone TEXT NOT NULL,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS project_resources (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id INTEGER NOT NULL,
        resource_name TEXT NOT NULL,
        resource_type TEXT NOT NULL,
        file_path TEXT NOT NULL,
        file_size TEXT NOT NULL,
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (project_id) REFERENCES projects(id)
    );

    CREATE TABLE IF NOT EXISTS wishlist (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        project_id INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(user_id, project_id),
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (project_id) REFERENCES projects(id)
    );

    CREATE TABLE IF NOT EXISTS notifications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        message TEXT NOT NULL,
        is_read INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    );
    """)

    # Seed Default Payment Settings (Configurable by Admin)
    cur.execute("SELECT COUNT(*) FROM payment_settings;")
    if cur.fetchone()[0] == 0:
        cur.execute("""
        INSERT INTO payment_settings (id, upi_mobile, upi_id, account_name, qr_code_path, instructions, support_phone)
        VALUES (1, '9876543210', 'projectverse@okaxis', 'PROJECTVERSE ACADEMIC SYSTEMS', '/static/uploads/qr/official_upi_qr.png',
        '1. Open Google Pay, PhonePe, Paytm, or BHIM.\n2. Scan the official QR code or pay to the verified UPI ID.\n3. Enter the exact project amount.\n4. Copy the 12-digit UTR/Reference number.\n5. Upload the transaction screenshot below and submit.',
        '+91 98765 43210');
        """)

    # Helper password hash
    def hash_pw(pw):
        return hashlib.sha256(pw.encode()).hexdigest()

    # Seed Admin and Demo Student
    cur.execute("SELECT COUNT(*) FROM users;")
    if cur.fetchone()[0] == 0:
        cur.execute("""
        INSERT INTO users (email, password_hash, full_name, mobile, college, course, academic_year, role)
        VALUES 
        ('admin@projectverse.com', ?, 'PROJECTVERSE Administrator', '9876543210', 'Headquarters', 'System Administration', 'Faculty', 'admin'),
        ('student@projectverse.com', ?, 'Aditya Sharma', '9812345678', 'National Institute of Technology', 'BE', 'Final Year', 'student');
        """, (hash_pw('Admin@12345'), hash_pw('Student@12345')))

    # Seed All 120 Projects
    cur.execute("SELECT COUNT(*) FROM projects;")
    if cur.fetchone()[0] == 0:
        print("Inserting 120 project records into database...")
        for p in ALL_PROJECTS:
            code, title, category, subcat, diff, dur, price, disc_price, tech_sum, desc, prob, sol, objs, scope, apps, outcomes = p
            
            slug = code.lower() + "-" + "".join(c if c.isalnum() else "-" for c in title.lower())
            slug = "-".join(filter(None, slug.split("-")))
            
            # Format image path
            sub_folder = "bca" if category == "BCA" else "be"
            img_url = f"/static/projects/{sub_folder}/{code}.webp"
            
            # Rich JSON tech stack
            tech_stack = {
                "frontend": "Tailwind CSS, React.js / HTML5, Lucide Icons",
                "backend": "Python, FastAPI",
                "database": "SQLite / PostgreSQL",
                "languages": "Python, JavaScript, SQL",
                "frameworks": "FastAPI, " + ("Scikit-Learn / PyTorch" if "AI" in subcat or "Machine" in subcat or "Deep" in subcat else "FastAPI REST"),
                "libraries": "Pydantic, Pandas, NumPy, Chart.js",
                "models": ("Domain Specialized ML / Neural Model" if "AI" in subcat or "Machine" in subcat or "Data" in subcat else "N/A - Full Stack Core"),
                "deployment": "Uvicorn, Docker, Cloud VPS / Vercel",
                "requirements": "Python 3.10+, 4GB-8GB RAM, Modern Web Browser"
            }
            
            # Rich JSON features
            features = {
                "core": [
                    "Full responsive cross-platform web interface",
                    f"Core domain processing for {title.split(' ')[0]} pipeline",
                    "Real-time database persistence and state validation",
                    "Exportable reports, summaries, and digital records"
                ],
                "advanced": [
                    "Automated error recovery and input sanity checks",
                    "Interactive data telemetry visualization via charts",
                    "Optimized algorithms for fast sub-second execution",
                    "Role-based privilege validation"
                ],
                "admin": [
                    "Administrative management console",
                    "Data ingestion, audit logs, and configuration controls",
                    "User access controls and transaction tracking"
                ],
                "user": [
                    "Intuitive user dashboard and guided workflows",
                    "Instant real-time search, filtering, and status checks",
                    "Personal activity history and report downloads"
                ],
                "optional": [
                    "Cloud storage synchronization",
                    "Push notification and email alert hooks"
                ]
            }

            user_roles = (
                "1. Student / End User: Accesses personal portal, submits inputs, and reviews system results.\n"
                "2. Operator / Faculty: Manages department workflows, verifies records, and supervises system activity.\n"
                "3. Administrator: Full system configuration, audit logs, master database oversight, and user management."
            )

            architecture = (
                f"Three-Tier Modular Architecture:\n"
                f"- Presentation Layer: Responsive client interface built with modern HTML5/Tailwind/React.\n"
                f"- Application/API Layer: High-performance Python FastAPI service providing asynchronous REST endpoints.\n"
                f"- Data Layer: Relational SQLite/PostgreSQL storage with structured foreign key relationships and index optimization."
            )

            db_design = (
                f"Tables Designed for {code}:\n"
                f"- users (id PK, name, email, role, created_at)\n"
                f"- {code.lower()}_primary_records (id PK, user_id FK, status, timestamp, telemetry_data)\n"
                f"- {code.lower()}_audit_logs (id PK, record_id FK, action, executed_by, timestamp)\n"
                f"- {code.lower()}_configurations (id PK, param_key, param_value, updated_at)"
            )

            api_docs = (
                f"Core REST API Endpoints for {code}:\n"
                f"1. GET /api/{code.lower()}/overview - Retrieves project metadata and operational status.\n"
                f"2. POST /api/{code.lower()}/process - Submits user input and returns processed results.\n"
                f"3. GET /api/{code.lower()}/history - Fetches historical execution logs with pagination.\n"
                f"4. POST /api/{code.lower()}/export - Generates formatted audit reports."
            )

            roadmap = (
                "Phase 1: Requirement Analysis & Feasibility Study (Week 1)\n"
                "Phase 2: UI/UX Wireframing & Responsive Prototypes (Week 2)\n"
                "Phase 3: Relational Database Schema Design & Normalization (Week 3)\n"
                "Phase 4: Backend API & Core Business Logic Implementation (Week 4)\n"
                "Phase 5: Frontend Component Assembly & REST Integration (Week 5)\n"
                "Phase 6: Domain Specific Algorithm / Model Integration (Week 6)\n"
                "Phase 7: End-to-End Stress & Edge-Case Testing (Week 7)\n"
                "Phase 8: Deployment & Cloud Configuration (Week 8)\n"
                "Phase 9: Comprehensive Documentation, PPT & Viva Guide (Week 9)"
            )

            deliverables = (
                "1. Complete Source Code ZIP (Clean, commented, production-ready)\n"
                "2. Database SQL Script & Sample Records\n"
                "3. Comprehensive IEEE Format Project Report (60+ Pages)\n"
                "4. Software Requirements Specification (SRS) Document\n"
                "5. Professional Presentation Slides (PPT - 25+ Slides)\n"
                "6. Step-by-Step Installation & Execution Manual\n"
                "7. Complete Viva Voce Questions & Answers Guide (50+ Q&A)"
            )

            # Feature first 4 projects of each category on homepage
            num_part = int(code[3:]) if code.startswith("BCA") else int(code[2:])
            is_feat = 1 if num_part <= 4 else 0

            objs_str = "\n".join(objs) if isinstance(objs, list) else objs

            cur.execute("""
            INSERT INTO projects (
                project_code, title, slug, academic_level, category, subcategory, difficulty, duration,
                price, discount_price, tech_summary, image_url, description, problem_statement,
                proposed_solution, objectives, scope, real_world_apps, expected_outcomes,
                tech_stack_json, features_json, user_roles, architecture, database_design,
                api_docs, development_roadmap, academic_deliverables, is_published, is_featured
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1, ?)
            """, (
                code, title, slug, category, category, subcat, diff, dur,
                price, disc_price, tech_sum, img_url, desc, prob,
                sol, objs_str, scope, apps, outcomes,
                json.dumps(tech_stack), json.dumps(features), user_roles, architecture,
                db_design, api_docs, roadmap, deliverables, is_feat
            ))

        # Seed sample starter deliverables for every project
        cur.execute("SELECT id, project_code, title FROM projects;")
        projects_rows = cur.fetchall()
        for p_id, p_code, p_title in projects_rows:
            # We seed 5 real academic deliverable records per project
            resources = [
                ("Full Source Code ZIP Package", "source_code", f"/static/uploads/resources/{p_code}_source_code.zip", "18.4 MB", "Complete runnable source code with frontend, backend, and config files."),
                ("IEEE Standard Project Report", "documentation", f"/static/uploads/resources/{p_code}_project_report.pdf", "4.2 MB", "Complete 65-page formatted academic report ready for college submission."),
                ("Software Requirements Specification (SRS)", "srs", f"/static/uploads/resources/{p_code}_srs_document.pdf", "2.1 MB", "Detailed IEEE-format SRS specification outlining functional and non-functional requirements."),
                ("Project Presentation Slides (PPT)", "presentation", f"/static/uploads/resources/{p_code}_presentation.pptx", "6.8 MB", "25 polished presentation slides covering problem, architecture, demo, and results."),
                ("Viva Voce Preparation Guide", "viva_guide", f"/static/uploads/resources/{p_code}_viva_qa.pdf", "1.5 MB", "50+ frequently asked viva questions with detailed model answers.")
            ]
            for r_name, r_type, r_path, r_size, r_desc in resources:
                cur.execute("""
                INSERT INTO project_resources (project_id, resource_name, resource_type, file_path, file_size, description)
                VALUES (?, ?, ?, ?, ?, ?)
                """, (p_id, r_name, r_type, r_path, r_size, r_desc))

        # Seed a sample approved purchase for the demo student so they can immediately see purchased projects
        # Let's assign BCA001 to student (user_id = 2)
        cur.execute("""
        INSERT INTO orders (order_number, user_id, project_id, amount, status)
        VALUES ('ORD-PV-2026-001', 2, 1, 1899, 'approved');
        """)
        order_id = cur.lastrowid
        cur.execute("""
        INSERT INTO payments (order_id, user_id, project_id, amount, utr_reference, screenshot_path, status, verified_by, verified_at, verification_notes)
        VALUES (?, 2, 1, 1899, 'UTR492817293810', '/static/uploads/screenshots/sample_receipt.png', 'approved', 'admin@projectverse.com', CURRENT_TIMESTAMP, 'Payment verified via Axis Bank UPI. Deliverables unlocked.');
        """, (order_id,))

        # Add a notification for the student
        cur.execute("""
        INSERT INTO notifications (user_id, title, message)
        VALUES (2, 'Order Approved: BCA001 Unlocked!', 'Your payment for AI-Powered Resume Analyzer has been verified. You can now download all academic deliverables.');
        """)

    conn.commit()
    conn.close()
    print("Database initialization complete! 120 projects, payment settings, demo users and resources ready.")

if __name__ == "__main__":
    init_db()
