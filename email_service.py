"""
PROJECTVERSE - Production Email Notification Service
Handles server-side transactional email delivery for business notifications to aniladani843@gmail.com
Features:
- SMTP over TLS/SSL (supports Gmail App Password, SendGrid, Resend, Amazon SES, or custom SMTP)
- Zero-exposure: all credentials read from environment variables (.env)
- Non-blocking background dispatch
- Full persistence in email_logs table
- Safe failure handling: customer enquiries and orders never fail if SMTP temporarily errors
- Retry mechanism for administrator
"""
import os
import smtplib
import sqlite3
import threading
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

DB_PATH = os.getenv("PROJECTVERSE_DB", "projectverse.db")
PRIMARY_NOTIFICATION_EMAIL = os.getenv("NOTIFICATION_EMAIL", "aniladani843@gmail.com")
ADMIN_DASHBOARD_URL = os.getenv("ADMIN_DASHBOARD_URL", "http://localhost:8000/#admin")

def log_email_to_db(event_type, recipient, subject, preview, status, error_msg=None):
    try:
        conn = sqlite3.connect(DB_PATH, timeout=30.0)
        conn.execute("PRAGMA busy_timeout=30000")
        cur = conn.cursor()
        cur.execute("""
        INSERT INTO email_logs (event_type, recipient_email, subject, body_preview, status, error_message, sent_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            event_type,
            recipient,
            subject,
            preview[:500] if preview else "",
            status,
            error_msg[:500] if error_msg else None,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S") if status == "SENT" else None
        ))
        log_id = cur.lastrowid
        conn.commit()
        conn.close()
        return log_id
    except Exception as e:
        print(f"[Email Logger Error]: {e}")
        return None

def send_smtp_message(recipient, subject, html_content, text_content):
    host = os.getenv("SMTP_HOST", "smtp.gmail.com")
    port = int(os.getenv("SMTP_PORT", "587"))
    user = os.getenv("SMTP_USER", "")
    password = os.getenv("SMTP_PASSWORD", "")
    from_email = os.getenv("SMTP_FROM_EMAIL", user or "notifications@projectverse.com")
    from_name = os.getenv("SMTP_FROM_NAME", "PROJECTVERSE Official")

    if not user or not password:
        raise ValueError("SMTP_USER or SMTP_PASSWORD is not configured in server environment variables.")

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f"{from_name} <{from_email}>"
    msg["To"] = recipient

    part1 = MIMEText(text_content, "plain")
    part2 = MIMEText(html_content, "html")
    msg.attach(part1)
    msg.attach(part2)

    if port == 465:
        with smtplib.SMTP_SSL(host, port, timeout=15) as server:
            server.login(user, password)
            server.sendmail(from_email, [recipient], msg.as_string())
    else:
        with smtplib.SMTP(host, port, timeout=15) as server:
            server.starttls()
            server.login(user, password)
            server.sendmail(from_email, [recipient], msg.as_string())

def dispatch_email_async(event_type, recipient, subject, html_content, text_content):
    def _worker():
        try:
            send_smtp_message(recipient, subject, html_content, text_content)
            log_email_to_db(event_type, recipient, subject, text_content, "SENT")
            print(f"[EMAIL SUCCESS] Delivered {event_type} notification to {recipient}")
        except Exception as e:
            err_msg = str(e)
            log_email_to_db(event_type, recipient, subject, text_content, "FAILED", err_msg)
            print(f"[EMAIL NOTICE] Could not dispatch to {recipient} ({event_type}): {err_msg}")

    t = threading.Thread(target=_worker, daemon=True)
    t.start()

# ================= TEMPLATES FOR THE 9 REQUIRED EVENTS =================

def notify_new_project_enquiry(enquiry_data):
    """
    Template matching user exact requirement:
    Subject: NEW PROJECT ENQUIRY – PROJECTVERSE
    """
    cust_name = enquiry_data.get("customer_name", "N/A")
    email = enquiry_data.get("customer_email", "N/A")
    phone = enquiry_data.get("customer_phone", "N/A")
    college = enquiry_data.get("college_name", "N/A")
    course = enquiry_data.get("course", "N/A")
    proj_name = enquiry_data.get("project_title", "N/A")
    proj_id = enquiry_data.get("project_code", "N/A")
    tech = enquiry_data.get("technology", "N/A")
    enq_id = enquiry_data.get("enquiry_number", "N/A")
    sub_date = enquiry_data.get("date", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    message = enquiry_data.get("message", "N/A")

    subject = f"NEW PROJECT ENQUIRY – PROJECTVERSE ({proj_id})"
    
    text_content = f"""A new customer has submitted a project enquiry.

Customer Name: {cust_name}
Email: {email}
Phone: {phone}
College: {college}
Course: {course}
Project Name: {proj_name}
Project ID: {proj_id}
Technology: {tech}
Enquiry ID: {enq_id}
Date: {sub_date}
Message: {message}

Admin Dashboard: {ADMIN_DASHBOARD_URL}
"""

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head><meta charset="utf-8"></head>
    <body style="font-family: Arial, sans-serif; background-color: #f8fafc; padding: 20px; color: #1e293b;">
      <div style="max-width: 600px; margin: 0 auto; background: #ffffff; border-radius: 12px; border: 1px solid #e2e8f0; overflow: hidden;">
        <div style="background: #0f172a; padding: 24px; text-align: center; color: #ffffff;">
          <h2 style="margin: 0; font-size: 20px; letter-spacing: 1px;">PROJECT<span style="color: #38bdf8;">VERSE</span></h2>
          <p style="margin: 4px 0 0; font-size: 13px; color: #94a3b8;">New Customer Project Enquiry Notification</p>
        </div>
        <div style="padding: 24px;">
          <div style="background: #eff6ff; border-left: 4px solid #3b82f6; padding: 12px 16px; margin-bottom: 20px;">
            <strong style="color: #1e40af; font-size: 14px;">Enquiry Reference: {enq_id}</strong>
          </div>
          <table style="width: 100%; border-collapse: collapse; font-size: 14px;">
            <tr><td style="padding: 8px 0; color: #64748b; width: 140px;">Customer Name:</td><td style="padding: 8px 0; font-weight: bold; color: #0f172a;">{cust_name}</td></tr>
            <tr><td style="padding: 8px 0; color: #64748b;">Email Address:</td><td style="padding: 8px 0; font-family: monospace; color: #2563eb;"><a href="mailto:{email}">{email}</a></td></tr>
            <tr><td style="padding: 8px 0; color: #64748b;">Phone / Mobile:</td><td style="padding: 8px 0; font-weight: bold;"><a href="tel:{phone}">{phone}</a> | <a href="https://wa.me/{phone.replace('+', '').replace(' ', '')}" style="color: #16a34a; text-decoration: none;">Chat on WhatsApp →</a></td></tr>
            <tr><td style="padding: 8px 0; color: #64748b;">College / Univ:</td><td style="padding: 8px 0;">{college} ({course})</td></tr>
            <tr><td style="padding: 8px 0; color: #64748b;">Project Title:</td><td style="padding: 8px 0; font-weight: bold; color: #7c3aed;">{proj_id} – {proj_name}</td></tr>
            <tr><td style="padding: 8px 0; color: #64748b;">Technology:</td><td style="padding: 8px 0; font-family: monospace;">{tech}</td></tr>
            <tr><td style="padding: 8px 0; color: #64748b;">Submission Date:</td><td style="padding: 8px 0; color: #64748b;">{sub_date}</td></tr>
          </table>
          <div style="margin-top: 20px; padding: 16px; background: #f1f5f9; border-radius: 8px; font-size: 14px;">
            <strong style="color: #334155; display: block; margin-bottom: 6px;">Customer Requirements / Message:</strong>
            <p style="margin: 0; color: #1e293b; line-height: 1.5; white-space: pre-wrap;">{message}</p>
          </div>
          <div style="margin-top: 24px; text-align: center;">
            <a href="{ADMIN_DASHBOARD_URL}" style="display: inline-block; background: #7c3aed; color: #ffffff; padding: 12px 28px; border-radius: 8px; font-weight: bold; text-decoration: none; font-size: 14px;">Open Admin Dashboard</a>
          </div>
        </div>
        <div style="background: #f8fafc; padding: 16px; text-align: center; border-top: 1px solid #e2e8f0; font-size: 12px; color: #94a3b8;">
          PROJECTVERSE Automated Transactional Gateway • Sent to {PRIMARY_NOTIFICATION_EMAIL}
        </div>
      </div>
    </body>
    </html>
    """
    dispatch_email_async("new_enquiry", PRIMARY_NOTIFICATION_EMAIL, subject, html_content, text_content)

def notify_new_project_request(req_data):
    req_num = req_data.get("request_number", "N/A")
    student_name = req_data.get("student_name", "N/A")
    email = req_data.get("student_email", "N/A")
    phone = req_data.get("student_phone", "N/A")
    college = req_data.get("college_name", "N/A")
    course = req_data.get("course", "N/A")
    proj_code = req_data.get("project_code", "N/A")
    proj_title = req_data.get("project_title", "N/A")
    deadline = req_data.get("deadline", "N/A")
    mode = req_data.get("team_mode", "Individual")
    team = req_data.get("team_members", "None")
    reqs = req_data.get("requirements", "N/A")

    subject = f"NEW PROJECT REQUEST – PROJECTVERSE ({proj_code} - {req_num})"
    text_content = f"""New Capstone Project Request Submitted:
Request ID: {req_num}
Student Name: {student_name}
Email: {email}
Phone: {phone}
College: {college} ({course})
Project: {proj_code} - {proj_title}
Project Mode: {mode}
Team Members: {team}
Required Deadline: {deadline}
Requirements: {reqs}

Admin Dashboard: {ADMIN_DASHBOARD_URL}
"""
    html_content = f"""
    <div style="font-family: Arial, sans-serif; padding: 20px; background: #f8fafc;">
      <div style="max-width: 600px; margin: 0 auto; background: #ffffff; border-radius: 12px; border: 1px solid #e2e8f0; padding: 24px;">
        <h2 style="color: #0f172a; margin-top: 0;">Capstone Project Enrollment Request ({req_num})</h2>
        <p><strong>Student:</strong> {student_name} (<a href="mailto:{email}">{email}</a> | {phone})</p>
        <p><strong>College:</strong> {college} • {course}</p>
        <p><strong>Project:</strong> <span style="color: #7c3aed; font-weight: bold;">{proj_code} – {proj_title}</span></p>
        <p><strong>Mode:</strong> {mode} | <strong>Members:</strong> {team}</p>
        <p><strong>Deadline:</strong> {deadline}</p>
        <div style="background: #f1f5f9; padding: 12px; border-radius: 8px;"><strong>Requirements:</strong><br>{reqs}</div>
        <div style="margin-top: 20px;"><a href="{ADMIN_DASHBOARD_URL}" style="background: #0284c7; color: white; padding: 10px 20px; border-radius: 6px; text-decoration: none; font-weight: bold;">Review & Approve in Admin Panel</a></div>
      </div>
    </div>
    """
    dispatch_email_async("new_request", PRIMARY_NOTIFICATION_EMAIL, subject, html_content, text_content)

def notify_new_registration(user_data):
    name = user_data.get("full_name", "N/A")
    email = user_data.get("email", "N/A")
    phone = user_data.get("mobile", "N/A")
    college = user_data.get("college", "N/A")
    course = user_data.get("course", "N/A")
    year = user_data.get("academic_year", "N/A")

    subject = f"NEW CUSTOMER REGISTRATION – PROJECTVERSE ({name})"
    text_content = f"""A new student account has registered on PROJECTVERSE.
Name: {name}
Email: {email}
Phone: {phone}
College: {college}
Course: {course} ({year})

Admin Dashboard: {ADMIN_DASHBOARD_URL}
"""
    html_content = f"""
    <div style="font-family: Arial, sans-serif; padding: 20px; background: #f8fafc;">
      <div style="max-width: 600px; margin: 0 auto; background: #ffffff; border-radius: 12px; border: 1px solid #e2e8f0; padding: 24px;">
        <h3 style="color: #0f172a; margin-top: 0;">New Student Registered</h3>
        <p><strong>Name:</strong> {name}</p>
        <p><strong>Email:</strong> {email}</p>
        <p><strong>Phone:</strong> {phone}</p>
        <p><strong>College:</strong> {college} ({course} - {year})</p>
        <div style="margin-top: 15px;"><a href="{ADMIN_DASHBOARD_URL}" style="background: #7c3aed; color: white; padding: 10px 20px; border-radius: 6px; text-decoration: none; font-weight: bold;">View in Admin Panel</a></div>
      </div>
    </div>
    """
    dispatch_email_async("new_registration", PRIMARY_NOTIFICATION_EMAIL, subject, html_content, text_content)

def notify_new_order(order_data):
    ord_num = order_data.get("order_number", "N/A")
    cust_name = order_data.get("customer_name", "N/A")
    email = order_data.get("customer_email", "N/A")
    phone = order_data.get("customer_phone", "N/A")
    proj_code = order_data.get("project_code", "N/A")
    proj_title = order_data.get("project_title", "N/A")
    amount = order_data.get("amount", 0)
    utr = order_data.get("utr_reference", "Pending")

    subject = f"NEW ORDER & PAYMENT SUBMISSION – PROJECTVERSE ({ord_num})"
    text_content = f"""New Customer Order Received:
Order Number: {ord_num}
Customer Name: {cust_name}
Email: {email}
Phone: {phone}
Project: {proj_code} - {proj_title}
Amount: Rs {amount:,}
UTR Reference: {utr}

Admin Dashboard: {ADMIN_DASHBOARD_URL}
"""
    html_content = f"""
    <div style="font-family: Arial, sans-serif; padding: 20px; background: #f8fafc;">
      <div style="max-width: 600px; margin: 0 auto; background: #ffffff; border-radius: 12px; border: 1px solid #e2e8f0; padding: 24px;">
        <h3 style="color: #16a34a; margin-top: 0;">New Order Submitted ({ord_num})</h3>
        <p><strong>Customer:</strong> {cust_name} ({email} | {phone})</p>
        <p><strong>Project:</strong> {proj_code} - {proj_title}</p>
        <p><strong>Amount:</strong> Rs {amount:,}</p>
        <p><strong>UTR Reference:</strong> <span style="font-family: monospace; font-weight: bold;">{utr}</span></p>
        <div style="margin-top: 15px;"><a href="{ADMIN_DASHBOARD_URL}" style="background: #16a34a; color: white; padding: 10px 20px; border-radius: 6px; text-decoration: none; font-weight: bold;">Audit Payment & Deliverables</a></div>
      </div>
    </div>
    """
    dispatch_email_async("new_order", PRIMARY_NOTIFICATION_EMAIL, subject, html_content, text_content)

def notify_payment_verified(order_data):
    ord_num = order_data.get("order_number", "N/A")
    cust_name = order_data.get("customer_name", "N/A")
    email = order_data.get("customer_email", "N/A")
    amount = order_data.get("amount", 0)
    proj_code = order_data.get("project_code", "N/A")

    subject = f"PAYMENT VERIFIED & DELIVERABLES UNLOCKED – PROJECTVERSE ({ord_num})"
    text_content = f"""Payment has been successfully verified for Order {ord_num}.
Customer: {cust_name} ({email})
Project: {proj_code}
Amount: Rs {amount:,}
Status: VERIFIED & DELIVERABLES UNLOCKED
"""
    html_content = f"<p>{text_content}</p>"
    dispatch_email_async("payment_verified", PRIMARY_NOTIFICATION_EMAIL, subject, html_content, text_content)

def notify_contact_message(msg_data):
    name = msg_data.get("name", "N/A")
    email = msg_data.get("email", "N/A")
    phone = msg_data.get("phone", "N/A")
    subj = msg_data.get("subject", "N/A")
    body = msg_data.get("message", "N/A")

    subject = f"NEW CONTACT MESSAGE – PROJECTVERSE: {subj}"
    text_content = f"""New Business Contact Form Message:
Name: {name}
Email: {email}
Phone: {phone}
Subject: {subj}
Message:
{body}

Admin Dashboard: {ADMIN_DASHBOARD_URL}
"""
    html_content = f"<div style='font-family: Arial, sans-serif; padding: 20px;'><p><strong>From:</strong> {name} ({email} | {phone})</p><p><strong>Subject:</strong> {subj}</p><blockquote style='background:#f1f5f9; padding: 10px; border-left: 3px solid #7c3aed;'>{body}</blockquote></div>"
    dispatch_email_async("contact_message", PRIMARY_NOTIFICATION_EMAIL, subject, html_content, text_content)

def notify_support_ticket(ticket_data):
    t_num = ticket_data.get("ticket_number", "N/A")
    user_name = ticket_data.get("user_name", "Student")
    cat = ticket_data.get("category", "General")
    subj = ticket_data.get("subject", "N/A")
    msg = ticket_data.get("message", "N/A")

    subject = f"NEW SUPPORT TICKET – PROJECTVERSE ({t_num})"
    text_content = f"""New Academic Support Ticket Created:
Ticket Number: {t_num}
Student: {user_name}
Category: {cat}
Subject: {subj}
Message: {msg}

Admin Dashboard: {ADMIN_DASHBOARD_URL}
"""
    html_content = f"<div style='font-family: Arial, sans-serif; padding: 20px;'><h3>Support Ticket {t_num}</h3><p><strong>Student:</strong> {user_name}</p><p><strong>Category:</strong> {cat}</p><p><strong>Subject:</strong> {subj}</p><p>{msg}</p></div>"
    dispatch_email_async("support_ticket", PRIMARY_NOTIFICATION_EMAIL, subject, html_content, text_content)

# ================= REFERRAL PARTNER & 25% COMMISSION NOTIFICATIONS =================

def notify_partner_application_received(partner_data):
    name = partner_data.get("full_name", "Partner")
    email = partner_data.get("email")
    if not email:
        return
    subject = "PROJECTVERSE Referral Partner Application Received – Under Review"
    text_content = f"""Dear {name},

Thank you for applying to become an official PROJECTVERSE Referral Partner!
Your application has been received and is currently under review by our administration team.

Once approved, you will receive your unique referral code and tracking link to start earning 25% commission on every successful academic project referral.

Best regards,
PROJECTVERSE Partner Operations Team
Website: http://localhost:8000
"""
    html_content = f"""
    <div style="font-family: Arial, sans-serif; padding: 20px; background: #f8fafc;">
      <div style="max-width: 600px; margin: 0 auto; background: #ffffff; border-radius: 12px; border: 1px solid #e2e8f0; padding: 24px;">
        <h3 style="color: #0f172a; margin-top: 0;">Referral Partner Application Received</h3>
        <p>Dear <strong>{name}</strong>,</p>
        <p>Thank you for applying to become an official <strong>PROJECTVERSE Referral Partner</strong>. Your account registration is under administrative verification.</p>
        <div style="background: #f1f5f9; padding: 14px; border-radius: 8px; font-size: 14px; color: #334155;">
          <strong>Next Steps:</strong>
          <ul style="margin: 8px 0 0 20px; padding: 0;">
            <li>Our team verifies partner contact and payout details within 24 hours.</li>
            <li>Upon approval, your unique <strong>Referral Tracking Link</strong> will activate.</li>
            <li>Earn a flat <strong>25% commission</strong> on every completed project purchase.</li>
          </ul>
        </div>
        <p style="margin-top: 20px; font-size: 13px; color: #64748b;">Questions? Contact partner support at support@projectverse.com</p>
      </div>
    </div>
    """
    dispatch_email_async("partner_applied", email, subject, html_content, text_content)

def notify_admin_new_partner_registration(partner_data):
    name = partner_data.get("full_name", "N/A")
    email = partner_data.get("email", "N/A")
    mobile = partner_data.get("mobile", "N/A")
    college = partner_data.get("college_name", "N/A")
    city = partner_data.get("city", "N/A")
    payout_method = partner_data.get("preferred_payment_method", "UPI")
    upi = partner_data.get("upi_id", "N/A")

    subject = f"NEW REFERRAL PARTNER REGISTRATION – {name}"
    text_content = f"""A new referral partner has registered on PROJECTVERSE.

Partner Name: {name}
Email: {email}
Mobile: {mobile}
College/City: {college} ({city})
Payout Method: {payout_method} ({upi})

Admin Dashboard: {ADMIN_DASHBOARD_URL}
"""
    html_content = f"""
    <div style="font-family: Arial, sans-serif; padding: 20px; background: #f8fafc;">
      <div style="max-width: 600px; margin: 0 auto; background: #ffffff; border-radius: 12px; border: 1px solid #e2e8f0; padding: 24px;">
        <h3 style="color: #7c3aed; margin-top: 0;">New Referral Partner Registration</h3>
        <p><strong>Partner:</strong> {name} (<a href="mailto:{email}">{email}</a> | {mobile})</p>
        <p><strong>College / City:</strong> {college} • {city}</p>
        <p><strong>Payout Details:</strong> {payout_method} – {upi}</p>
        <div style="margin-top: 20px;">
          <a href="{ADMIN_DASHBOARD_URL}" style="background: #7c3aed; color: #ffffff; padding: 10px 20px; border-radius: 6px; text-decoration: none; font-weight: bold; font-size: 14px;">Review & Approve in Admin Panel</a>
        </div>
      </div>
    </div>
    """
    dispatch_email_async("admin_new_partner", PRIMARY_NOTIFICATION_EMAIL, subject, html_content, text_content)

def notify_partner_status_update(partner_data, status, ref_code=""):
    name = partner_data.get("full_name", "Partner")
    email = partner_data.get("email")
    if not email:
        return

    if status == "APPROVED":
        subject = "🎉 CONGRATULATIONS: Your PROJECTVERSE Partner Account is Approved!"
        text_content = f"""Dear {name},

Great news! Your PROJECTVERSE Referral Partner account has been APPROVED!
Your unique Referral Code: {ref_code}
Your Referral URL: http://localhost:8000/?ref={ref_code}

You earn a flat 25% commission on every verified project purchase made through your link!
Log into your Partner Dashboard at http://localhost:8000/#partner to track clicks, sales, and payouts.

Best regards,
PROJECTVERSE Partner Team
"""
        html_content = f"""
        <div style="font-family: Arial, sans-serif; padding: 20px; background: #f8fafc;">
          <div style="max-width: 600px; margin: 0 auto; background: #ffffff; border-radius: 12px; border: 1px solid #e2e8f0; padding: 24px;">
            <h2 style="color: #16a34a; margin-top: 0;">🎉 You are now an Official Referral Partner!</h2>
            <p>Dear <strong>{name}</strong>,</p>
            <p>Your referral partner application has been <strong>APPROVED</strong> by PROJECTVERSE administration.</p>
            <div style="background: #ecfdf5; border: 1px solid #a7f3d0; border-radius: 8px; padding: 16px; margin: 20px 0;">
              <p style="margin: 0 0 6px 0; font-size: 13px; color: #065f46;"><strong>YOUR UNIQUE REFERRAL CODE:</strong></p>
              <h3 style="margin: 0 0 12px 0; font-family: monospace; color: #047857; font-size: 24px; letter-spacing: 2px;">{ref_code}</h3>
              <p style="margin: 0; font-size: 13px; color: #065f46;"><strong>YOUR REFERRAL LINK:</strong><br>
                <a href="http://localhost:8000/?ref={ref_code}" style="color: #059669; word-break: break-all; font-weight: bold;">http://localhost:8000/?ref={ref_code}</a>
              </p>
            </div>
            <p style="font-size: 14px; color: #334155;">Share this link with BCA, B.Com, B.Tech, MCA, and M.Tech students. You will earn a <strong>flat 25% commission</strong> on every verified project sale!</p>
            <div style="margin-top: 24px; text-align: center;">
              <a href="http://localhost:8000/#partner" style="background: #16a34a; color: #ffffff; padding: 12px 24px; border-radius: 8px; text-decoration: none; font-weight: bold;">Open Partner Dashboard</a>
            </div>
          </div>
        </div>
        """
    else:
        subject = f"PROJECTVERSE Partner Account Status: {status}"
        text_content = f"Dear {name},\nYour PROJECTVERSE referral partner account status has been updated to: {status}.\nIf you have questions, please contact support@projectverse.com."
        html_content = f"<div style='font-family: Arial, sans-serif; padding: 20px;'><h3>Partner Account Status: {status}</h3><p>Dear {name}, your referral account status is now <strong>{status}</strong>.</p></div>"

    dispatch_email_async("partner_status_change", email, subject, html_content, text_content)

def notify_partner_new_referred_student(partner_data, student_data):
    partner_name = partner_data.get("full_name", "Partner")
    partner_email = partner_data.get("email")
    if not partner_email:
        return
    student_name = student_data.get("full_name", "A student")
    college = student_data.get("college", "University")
    course = student_data.get("course", "Academic Program")

    subject = f"New Student Registered via Your Referral Link! ({student_name})"
    text_content = f"""Dear {partner_name},

Great news! {student_name} from {college} ({course}) just registered an account using your referral link!
When they complete their academic project purchase, 25% commission will automatically be credited to your account.

Track all your referrals on your Partner Dashboard: http://localhost:8000/#partner
"""
    html_content = f"""
    <div style="font-family: Arial, sans-serif; padding: 20px; background: #f8fafc;">
      <div style="max-width: 600px; margin: 0 auto; background: #ffffff; border-radius: 12px; border: 1px solid #e2e8f0; padding: 24px;">
        <h3 style="color: #2563eb; margin-top: 0;">New Student Referral Registered!</h3>
        <p>Dear <strong>{partner_name}</strong>,</p>
        <p><strong>{student_name}</strong> from <strong>{college}</strong> ({course}) has registered on PROJECTVERSE via your referral link.</p>
        <p>You will earn your <strong>25% commission</strong> immediately when they purchase their project!</p>
        <div style="margin-top: 20px;">
          <a href="http://localhost:8000/#partner" style="background: #2563eb; color: #ffffff; padding: 10px 20px; border-radius: 6px; text-decoration: none; font-weight: bold;">View Partner Telemetry</a>
        </div>
      </div>
    </div>
    """
    dispatch_email_async("partner_new_student", partner_email, subject, html_content, text_content)

def notify_partner_commission_earned(partner_data, order_data):
    partner_name = partner_data.get("full_name", "Partner")
    partner_email = partner_data.get("email")
    if not partner_email:
        return
    order_num = order_data.get("order_number", "N/A")
    proj_title = order_data.get("project_title", "Academic Project")
    order_amount = order_data.get("order_amount", 0)
    comm_amount = order_data.get("commission_amount", 0)

    subject = f"💰 Commission Earned: Rs {comm_amount:,} on Order {order_num}!"
    text_content = f"""Dear {partner_name},

Congratulations! Your referred student just purchased '{proj_title}'.
Order Number: {order_num}
Sale Amount: Rs {order_amount:,}
Your 25% Commission: Rs {comm_amount:,}
Status: APPROVED (Ready for payout)

View your earnings: http://localhost:8000/#partner
"""
    html_content = f"""
    <div style="font-family: Arial, sans-serif; padding: 20px; background: #f8fafc;">
      <div style="max-width: 600px; margin: 0 auto; background: #ffffff; border-radius: 12px; border: 1px solid #e2e8f0; padding: 24px;">
        <h2 style="color: #16a34a; margin-top: 0;">💰 You Earned Rs {comm_amount:,} Commission!</h2>
        <p>Dear <strong>{partner_name}</strong>,</p>
        <p>A customer referred by your link has successfully completed their payment for <strong>{proj_title}</strong>.</p>
        <table style="width: 100%; border-collapse: collapse; margin: 16px 0; font-size: 14px;">
          <tr><td style="padding: 6px 0; color: #64748b;">Order Number:</td><td style="font-family: monospace; font-weight: bold;">{order_num}</td></tr>
          <tr><td style="padding: 6px 0; color: #64748b;">Sale Amount:</td><td>Rs {order_amount:,}</td></tr>
          <tr><td style="padding: 6px 0; color: #64748b;">Commission Rate:</td><td>25%</td></tr>
          <tr><td style="padding: 6px 0; color: #64748b; font-weight: bold;">Your Earning:</td><td style="color: #16a34a; font-weight: bold; font-size: 18px;">Rs {comm_amount:,}</td></tr>
        </table>
        <p style="font-size: 13px; color: #475569;">This commission has been added to your available payout balance.</p>
        <div style="margin-top: 20px; text-align: center;">
          <a href="http://localhost:8000/#partner" style="background: #16a34a; color: #ffffff; padding: 12px 24px; border-radius: 8px; text-decoration: none; font-weight: bold;">View Earnings on Dashboard</a>
        </div>
      </div>
    </div>
    """
    dispatch_email_async("partner_commission", partner_email, subject, html_content, text_content)

def notify_partner_commission_reversed(partner_data, order_data):
    partner_name = partner_data.get("full_name", "Partner")
    partner_email = partner_data.get("email")
    if not partner_email:
        return
    order_num = order_data.get("order_number", "N/A")
    comm_amount = order_data.get("commission_amount", 0)

    subject = f"Notice: Commission Reversal on Order {order_num}"
    text_content = f"""Dear {partner_name},
The purchase for Order {order_num} was cancelled or refunded. In accordance with platform policy, the commission of Rs {comm_amount:,} has been reversed.
"""
    html_content = f"<div style='font-family: Arial, sans-serif; padding: 20px;'><h3>Commission Reversal Notice</h3><p>Dear {partner_name}, Order {order_num} was cancelled or refunded. The commission of Rs {comm_amount:,} has been reversed.</p></div>"
    dispatch_email_async("commission_reversed", partner_email, subject, html_content, text_content)

def notify_admin_payout_requested(payout_data):
    partner_name = payout_data.get("partner_name", "Partner")
    req_num = payout_data.get("request_number", "N/A")
    amount = payout_data.get("amount", 0)
    method = payout_data.get("payment_method", "UPI")
    details = payout_data.get("payout_details", "N/A")

    subject = f"REFERRAL PAYOUT REQUESTED – {req_num} (Rs {amount:,})"
    text_content = f"""Referral Partner Payout Request Submitted:
Request ID: {req_num}
Partner: {partner_name}
Amount: Rs {amount:,}
Method: {method}
Details: {details}

Admin Dashboard: {ADMIN_DASHBOARD_URL}
"""
    html_content = f"""
    <div style="font-family: Arial, sans-serif; padding: 20px;">
      <h3>Referral Payout Request ({req_num})</h3>
      <p><strong>Partner:</strong> {partner_name}</p>
      <p><strong>Amount:</strong> Rs {amount:,}</p>
      <p><strong>Method & Account:</strong> {method} ({details})</p>
      <a href="{ADMIN_DASHBOARD_URL}" style="display:inline-block; padding: 10px 20px; background: #0284c7; color: white; border-radius: 6px; text-decoration: none;">Process Payout in Admin Panel</a>
    </div>
    """
    dispatch_email_async("admin_payout_req", PRIMARY_NOTIFICATION_EMAIL, subject, html_content, text_content)

def notify_partner_payout_processed(partner_data, transaction_data):
    partner_name = partner_data.get("full_name", "Partner")
    partner_email = partner_data.get("email")
    if not partner_email:
        return
    amount = transaction_data.get("amount", 0)
    utr = transaction_data.get("utr_reference", "N/A")
    method = transaction_data.get("payment_method", "UPI")
    date_str = transaction_data.get("date", datetime.now().strftime("%Y-%m-%d"))

    subject = f"✅ Payout Processed: Rs {amount:,} Settled via {method}!"
    text_content = f"""Dear {partner_name},

Your referral commission payout has been successfully transferred!
Amount: Rs {amount:,}
Settlement Method: {method}
Transaction UTR / Ref: {utr}
Date: {date_str}

Thank you for being a valued PROJECTVERSE Partner!
Dashboard: http://localhost:8000/#partner
"""
    html_content = f"""
    <div style="font-family: Arial, sans-serif; padding: 20px; background: #f8fafc;">
      <div style="max-width: 600px; margin: 0 auto; background: #ffffff; border-radius: 12px; border: 1px solid #e2e8f0; padding: 24px;">
        <h2 style="color: #16a34a; margin-top: 0;">✅ Payout Transferred: Rs {amount:,}</h2>
        <p>Dear <strong>{partner_name}</strong>,</p>
        <p>We are pleased to inform you that your referral commission payout has been processed and transferred to your account.</p>
        <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 16px; margin: 16px 0;">
          <p style="margin: 4px 0;">Amount Paid: <strong style="color: #16a34a; font-size: 18px;">Rs {amount:,}</strong></p>
          <p style="margin: 4px 0;">Payment Method: <strong>{method}</strong></p>
          <p style="margin: 4px 0;">Bank UTR / Reference: <strong style="font-family: monospace;">{utr}</strong></p>
          <p style="margin: 4px 0;">Settlement Date: <strong>{date_str}</strong></p>
        </div>
        <p style="font-size: 13px; color: #64748b;">Keep sharing your link to earn more 25% commissions on PROJECTVERSE projects!</p>
        <div style="margin-top: 20px;">
          <a href="http://localhost:8000/#partner" style="background: #16a34a; color: #ffffff; padding: 10px 20px; border-radius: 6px; text-decoration: none; font-weight: bold;">View Payout History</a>
        </div>
      </div>
    </div>
    """
    dispatch_email_async("partner_payout_done", partner_email, subject, html_content, text_content)

