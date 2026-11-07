import re

with open('static/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Remove topbar demo pill
content = re.sub(r'<span id="topbar-demo-pill"[^>]*>.*?</span>', '', content)

# 2. Update stats demo banner
content = re.sub(
    r'<!-- Reactive Demo Mode Transparency Badge -->\s*<div id="stat-demo-banner".*?</div>\s*</div>',
    '''<div class="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-xl bg-emerald-50 border border-emerald-300 text-emerald-900 text-xs font-semibold shadow-sm">
              <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
              <span>100% Genuine Database Records</span>
            </div>
          </div>''',
    content,
    flags=re.DOTALL
)

# 3. Update students counter labels
content = re.sub(
    r'<div class="text-3xl sm:text-4xl font-black text-brand-purple" id="stat-counter-students">520\+</div>\s*<p class="text-xs font-bold text-slate-600 mt-1 uppercase tracking-wider" id="stat-student-label">Demo Student Records</p>\s*<p class="text-\[11px\] text-amber-600 font-medium" id="stat-student-sublabel">Illustrative Sample Data</p>',
    '''<div class="text-3xl sm:text-4xl font-black text-brand-purple" id="stat-counter-students">0</div>
              <p class="text-xs font-bold text-slate-600 mt-1 uppercase tracking-wider" id="stat-student-label">Registered Students</p>
              <p class="text-[11px] text-emerald-600 font-medium" id="stat-student-sublabel">Genuine Verified Accounts</p>''',
    content
)

# 4. Remove quick-fill demo credentials in modal-auth
content = re.sub(
    r'<!-- Quick Fill Demo Accounts -->\s*<div class="p-3 bg-purple-50 rounded-xl border border-purple-200.*?</div>\s*</div>',
    '',
    content,
    flags=re.DOTALL
)

# 5. Remove Demo Data Transparency card in admin view
content = re.sub(
    r'<!-- DEMO MODE TRANSPARENCY CARD \(Essential Requirement\) -->\s*<div class="bg-white rounded-2xl border border-amber-300.*?</div>\s*</div>',
    '',
    content,
    flags=re.DOTALL
)

# 6. Update Admin Header with Notification Bell
old_adm_header_buttons = '''          <div class="flex items-center gap-2">
            <button onclick="app.refreshAdminData()" class="px-4 py-2 bg-white hover:bg-slate-50 border border-slate-200 text-slate-700 text-xs font-semibold rounded-xl flex items-center gap-1.5 shadow-sm">
              <i data-lucide="refresh-cw" class="w-3.5 h-3.5"></i> Refresh Data
            </button>
            <button onclick="app.openAdminProjectModal()" class="px-4 py-2 bg-brand-purple hover:bg-purple-700 text-white text-xs font-bold rounded-xl flex items-center gap-1.5 shadow-sm">
              <i data-lucide="plus-circle" class="w-3.5 h-3.5"></i> Add New Project
            </button>
            <button onclick="app.openAdminCsvModal()" class="px-4 py-2 bg-slate-800 hover:bg-slate-900 text-white text-xs font-bold rounded-xl flex items-center gap-1.5 shadow-sm">
              <i data-lucide="upload" class="w-3.5 h-3.5"></i> Import CSV
            </button>
          </div>'''

new_adm_header_buttons = '''          <div class="flex items-center gap-2">
            <!-- Admin Notification Centre -->
            <div class="relative">
              <button onclick="app.toggleAdminNotifDropdown()" id="adm-notif-bell" class="relative p-2.5 rounded-xl bg-white hover:bg-slate-50 border border-slate-200 text-slate-700 shadow-sm transition-colors" title="Notifications">
                <i data-lucide="bell" class="w-4 h-4"></i>
                <span id="adm-notif-count" class="hidden absolute -top-1 -right-1 w-4 h-4 rounded-full bg-rose-600 text-white text-[10px] font-black flex items-center justify-center">0</span>
              </button>
              <div id="adm-notif-dropdown" class="hidden absolute right-0 mt-2 w-80 bg-white rounded-2xl shadow-xl border border-slate-200 z-50 p-3 space-y-2">
                <div class="flex items-center justify-between pb-2 border-b border-slate-100">
                  <span class="text-xs font-bold text-slate-900">Live Business Alerts</span>
                  <button onclick="app.markAllNotificationsRead()" class="text-[11px] font-semibold text-brand-purple hover:underline">Mark All Read</button>
                </div>
                <div id="adm-notif-list" class="max-h-60 overflow-y-auto space-y-2 text-xs">
                  <p class="text-slate-400 text-center py-2">No unread notifications</p>
                </div>
              </div>
            </div>

            <button onclick="app.refreshAdminData()" class="px-3.5 py-2 bg-white hover:bg-slate-50 border border-slate-200 text-slate-700 text-xs font-semibold rounded-xl flex items-center gap-1.5 shadow-sm">
              <i data-lucide="refresh-cw" class="w-3.5 h-3.5"></i> Refresh
            </button>
            <button onclick="app.openAdminProjectModal()" class="px-3.5 py-2 bg-brand-purple hover:bg-purple-700 text-white text-xs font-bold rounded-xl flex items-center gap-1.5 shadow-sm">
              <i data-lucide="plus-circle" class="w-3.5 h-3.5"></i> Add Project
            </button>
            <button onclick="app.openAdminCsvModal()" class="px-3.5 py-2 bg-slate-800 hover:bg-slate-900 text-white text-xs font-bold rounded-xl flex items-center gap-1.5 shadow-sm">
              <i data-lucide="upload" class="w-3.5 h-3.5"></i> Import CSV
            </button>
          </div>'''

if old_adm_header_buttons in content:
    content = content.replace(old_adm_header_buttons, new_adm_header_buttons)
    print("Replaced Admin Header Buttons.")

# 7. Update Admin KPI Metric Cards (6 Live Business Metrics)
old_kpi_cards = '''        <!-- Admin KPI Metric Cards -->
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
          
          <div class="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm">
            <span class="text-xs font-bold text-slate-500 uppercase tracking-wider">Catalogue Projects</span>
            <div class="flex items-baseline justify-between mt-2">
              <span class="text-3xl font-black text-slate-900" id="admin-stat-projects">90</span>
              <span class="text-xs font-semibold text-blue-600">6 Categories</span>
            </div>
          </div>

          <div class="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm">
            <span class="text-xs font-bold text-slate-500 uppercase tracking-wider">Student Registrations</span>
            <div class="flex items-baseline justify-between mt-2">
              <span class="text-3xl font-black text-purple-600" id="admin-stat-students">540</span>
              <span class="text-xs font-semibold text-amber-600" id="admin-stat-genuine-sub">1 Genuine</span>
            </div>
          </div>

          <div class="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm">
            <span class="text-xs font-bold text-slate-500 uppercase tracking-wider">Pending UPI Payments</span>
            <div class="flex items-baseline justify-between mt-2">
              <span class="text-3xl font-black text-amber-600" id="admin-stat-pending">0</span>
              <span class="text-xs font-semibold text-amber-600 animate-pulse">Review Queue</span>
            </div>
          </div>

          <div class="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm">
            <span class="text-xs font-bold text-slate-500 uppercase tracking-wider">Verified Revenue</span>
            <div class="flex items-baseline justify-between mt-2">
              <span class="text-3xl font-black text-emerald-600" id="admin-stat-revenue">₹0</span>
              <span class="text-xs font-semibold text-emerald-600">Approved UPI</span>
            </div>
          </div>

        </div>'''

new_kpi_cards = '''        <!-- Admin KPI Metric Cards (6 Live Genuine Business Metrics) -->
        <div class="grid grid-cols-2 md:grid-cols-6 gap-3 sm:gap-4">
          
          <div class="bg-white p-4 rounded-2xl border border-slate-200 shadow-sm">
            <span class="text-[11px] font-bold text-slate-500 uppercase tracking-wider block">Total Projects</span>
            <div class="mt-1">
              <span class="text-2xl sm:text-3xl font-black text-slate-900" id="admin-stat-projects">90</span>
              <span class="text-[11px] font-medium text-blue-600 block">6 Streams</span>
            </div>
          </div>

          <div class="bg-white p-4 rounded-2xl border border-slate-200 shadow-sm">
            <span class="text-[11px] font-bold text-slate-500 uppercase tracking-wider block">Real Students</span>
            <div class="mt-1">
              <span class="text-2xl sm:text-3xl font-black text-purple-600" id="admin-stat-students">0</span>
              <span class="text-[11px] font-medium text-purple-600 block">Active Profiles</span>
            </div>
          </div>

          <div class="bg-white p-4 rounded-2xl border border-slate-200 shadow-sm">
            <span class="text-[11px] font-bold text-slate-500 uppercase tracking-wider block">New Enquiries</span>
            <div class="mt-1">
              <span class="text-2xl sm:text-3xl font-black text-amber-500" id="admin-stat-enquiries">0</span>
              <span class="text-[11px] font-medium text-amber-600 block">Unread Leads</span>
            </div>
          </div>

          <div class="bg-white p-4 rounded-2xl border border-slate-200 shadow-sm">
            <span class="text-[11px] font-bold text-slate-500 uppercase tracking-wider block">Project Requests</span>
            <div class="mt-1">
              <span class="text-2xl sm:text-3xl font-black text-blue-500" id="admin-stat-requests">0</span>
              <span class="text-[11px] font-medium text-blue-600 block">Pending Review</span>
            </div>
          </div>

          <div class="bg-white p-4 rounded-2xl border border-slate-200 shadow-sm">
            <span class="text-[11px] font-bold text-slate-500 uppercase tracking-wider block">Pending UPI</span>
            <div class="mt-1">
              <span class="text-2xl sm:text-3xl font-black text-cyan-600" id="admin-stat-pending">0</span>
              <span class="text-[11px] font-medium text-cyan-600 block">Payment Queue</span>
            </div>
          </div>

          <div class="bg-white p-4 rounded-2xl border border-slate-200 shadow-sm">
            <span class="text-[11px] font-bold text-slate-500 uppercase tracking-wider block">Verified Revenue</span>
            <div class="mt-1">
              <span class="text-2xl sm:text-3xl font-black text-emerald-600" id="admin-stat-revenue">₹0</span>
              <span class="text-[11px] font-medium text-emerald-600 block">Approved UPI</span>
            </div>
          </div>

        </div>'''

if old_kpi_cards in content:
    content = content.replace(old_kpi_cards, new_kpi_cards)
    print("Replaced KPI Metric Cards.")

# 8. Update Admin Navigation Tabs
old_adm_tabs = '''        <!-- Admin Navigation Tabs -->
        <div class="flex border-b border-slate-300 gap-6 font-semibold text-sm overflow-x-auto">
          <button onclick="app.setAdminTab('projects')" id="tab-adm-projects" class="py-3 tab-active flex items-center gap-1.5 whitespace-nowrap">
            <i data-lucide="layers" class="w-4 h-4"></i> Project Management (90 Projects)
          </button>
          <button onclick="app.setAdminTab('enrollments')" id="tab-adm-enrollments" class="py-3 text-slate-600 hover:text-slate-900 flex items-center gap-1.5 whitespace-nowrap">
            <i data-lucide="clipboard-check" class="w-4 h-4"></i> Enrollment Requests & Mentorship
          </button>
          <button onclick="app.setAdminTab('students')" id="tab-adm-students" class="py-3 text-slate-600 hover:text-slate-900 flex items-center gap-1.5 whitespace-nowrap">
            <i data-lucide="users" class="w-4 h-4"></i> Student Roster (540+ Records)
          </button>
          <button onclick="app.setAdminTab('mentors')" id="tab-adm-mentors" class="py-3 text-slate-600 hover:text-slate-900 flex items-center gap-1.5 whitespace-nowrap">
            <i data-lucide="user-check" class="w-4 h-4"></i> Mentors Roster
          </button>
          <button onclick="app.setAdminTab('payments')" id="tab-adm-payments" class="py-3 text-slate-600 hover:text-slate-900 flex items-center gap-1.5 whitespace-nowrap">
            <i data-lucide="check-circle" class="w-4 h-4"></i> Payment Verification
          </button>
          <button onclick="app.setAdminTab('pricing')" id="tab-adm-pricing" class="py-3 text-slate-600 hover:text-slate-900 flex items-center gap-1.5 whitespace-nowrap">
            <i data-lucide="tag" class="w-4 h-4"></i> Pricing Manager (Min ₹799)
          </button>
          <button onclick="app.setAdminTab('images')" id="tab-adm-images" class="py-3 text-slate-600 hover:text-slate-900 flex items-center gap-1.5 whitespace-nowrap">
            <i data-lucide="image" class="w-4 h-4"></i> Image Audit (90 Artworks)
          </button>
          <button onclick="app.setAdminTab('upi')" id="tab-adm-upi" class="py-3 text-slate-600 hover:text-slate-900 flex items-center gap-1.5 whitespace-nowrap">
            <i data-lucide="qr-code" class="w-4 h-4"></i> UPI Settings
          </button>
          <button onclick="app.setAdminTab('support')" id="tab-adm-support" class="py-3 text-slate-600 hover:text-slate-900 flex items-center gap-1.5 whitespace-nowrap">
            <i data-lucide="message-square" class="w-4 h-4"></i> WhatsApp Settings
          </button>
        </div>'''

new_adm_tabs = '''        <!-- Admin Navigation Tabs -->
        <div class="flex border-b border-slate-300 gap-6 font-semibold text-sm overflow-x-auto">
          <button onclick="app.setAdminTab('enquiries')" id="tab-adm-enquiries" class="py-3 tab-active flex items-center gap-1.5 whitespace-nowrap">
            <i data-lucide="help-circle" class="w-4 h-4 text-amber-500"></i> Project Enquiries (<span id="adm-badge-enquiries">0</span>)
          </button>
          <button onclick="app.setAdminTab('requests')" id="tab-adm-requests" class="py-3 text-slate-600 hover:text-slate-900 flex items-center gap-1.5 whitespace-nowrap">
            <i data-lucide="clipboard-list" class="w-4 h-4 text-blue-500"></i> Project Requests (<span id="adm-badge-requests">0</span>)
          </button>
          <button onclick="app.setAdminTab('orders')" id="tab-adm-orders" class="py-3 text-slate-600 hover:text-slate-900 flex items-center gap-1.5 whitespace-nowrap">
            <i data-lucide="receipt" class="w-4 h-4 text-emerald-500"></i> Orders & Invoices
          </button>
          <button onclick="app.setAdminTab('projects')" id="tab-adm-projects" class="py-3 text-slate-600 hover:text-slate-900 flex items-center gap-1.5 whitespace-nowrap">
            <i data-lucide="layers" class="w-4 h-4 text-purple-500"></i> Projects (90)
          </button>
          <button onclick="app.setAdminTab('students')" id="tab-adm-students" class="py-3 text-slate-600 hover:text-slate-900 flex items-center gap-1.5 whitespace-nowrap">
            <i data-lucide="users" class="w-4 h-4 text-indigo-500"></i> Registered Students
          </button>
          <button onclick="app.setAdminTab('email-logs')" id="tab-adm-email-logs" class="py-3 text-slate-600 hover:text-slate-900 flex items-center gap-1.5 whitespace-nowrap">
            <i data-lucide="mail" class="w-4 h-4 text-rose-500"></i> Email Logs (Owner Alert)
          </button>
          <button onclick="app.setAdminTab('payments')" id="tab-adm-payments" class="py-3 text-slate-600 hover:text-slate-900 flex items-center gap-1.5 whitespace-nowrap">
            <i data-lucide="check-circle" class="w-4 h-4 text-emerald-600"></i> Payment Verification
          </button>
          <button onclick="app.setAdminTab('mentors')" id="tab-adm-mentors" class="py-3 text-slate-600 hover:text-slate-900 flex items-center gap-1.5 whitespace-nowrap">
            <i data-lucide="user-check" class="w-4 h-4"></i> Mentors
          </button>
          <button onclick="app.setAdminTab('pricing')" id="tab-adm-pricing" class="py-3 text-slate-600 hover:text-slate-900 flex items-center gap-1.5 whitespace-nowrap">
            <i data-lucide="tag" class="w-4 h-4"></i> Pricing (Min ₹799)
          </button>
          <button onclick="app.setAdminTab('upi')" id="tab-adm-upi" class="py-3 text-slate-600 hover:text-slate-900 flex items-center gap-1.5 whitespace-nowrap">
            <i data-lucide="qr-code" class="w-4 h-4"></i> UPI & Settings
          </button>
        </div>'''

if old_adm_tabs in content:
    content = content.replace(old_adm_tabs, new_adm_tabs)
    print("Replaced Admin Tabs Navigation.")

# 9. Insert Admin Panes for Enquiries, Requests, Orders, and Email Logs before adm-tab-projects
new_admin_panes = '''        <!-- Admin Tab 1: Project Enquiries Management -->
        <div id="adm-tab-enquiries" class="space-y-4">
          <div class="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm space-y-4">
            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
              <div>
                <h3 class="text-base font-bold text-slate-900">Customer Project Enquiries</h3>
                <p class="text-xs text-slate-500">Live pre-sales inquiries with instant email alerts to aniladani843@gmail.com and WhatsApp follow-up.</p>
              </div>
              <div class="flex items-center gap-2">
                <select id="adm-enquiry-status-filter" onchange="app.renderAdminEnquiries()" class="px-3 py-1.5 rounded-lg border border-slate-200 text-xs bg-white font-medium">
                  <option value="ALL">All Statuses</option>
                  <option value="NEW" selected>NEW (Unprocessed)</option>
                  <option value="CONTACTED">CONTACTED</option>
                  <option value="IN_DISCUSSION">IN DISCUSSION</option>
                  <option value="CONVERTED">CONVERTED</option>
                  <option value="CLOSED">CLOSED</option>
                </select>
                <input type="text" id="adm-enquiry-search" oninput="app.renderAdminEnquiries()" placeholder="Search name, phone, project..." class="px-3 py-1.5 rounded-lg border border-slate-200 text-xs">
              </div>
            </div>
            
            <div class="overflow-x-auto max-h-[600px] overflow-y-auto">
              <table class="w-full text-left text-xs">
                <thead class="bg-slate-50 text-slate-600 font-semibold uppercase text-[10px] sticky top-0 border-b border-slate-200">
                  <tr>
                    <th class="py-3 px-3">Enquiry ID & Date</th>
                    <th class="py-3 px-3">Customer Info</th>
                    <th class="py-3 px-3">College & Course</th>
                    <th class="py-3 px-3">Project Enquired</th>
                    <th class="py-3 px-3">Requirements Message</th>
                    <th class="py-3 px-3">Status</th>
                    <th class="py-3 px-3">Admin Notes</th>
                    <th class="py-3 px-3 text-right">Actions</th>
                  </tr>
                </thead>
                <tbody id="adm-enquiries-table-body" class="divide-y divide-slate-100">
                  <!-- Populated by app.js -->
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- Admin Tab 2: Project Requests & Capstone Mentorship -->
        <div id="adm-tab-requests" class="hidden space-y-4">
          <div class="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm space-y-4">
            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
              <div>
                <h3 class="text-base font-bold text-slate-900">Capstone Project Enrollment Requests</h3>
                <p class="text-xs text-slate-500">Academic capstone requests, mentor assignment, and project progress milestone updates.</p>
              </div>
              <div class="flex items-center gap-2">
                <select id="adm-request-status-filter" onchange="app.renderAdminRequests()" class="px-3 py-1.5 rounded-lg border border-slate-200 text-xs bg-white font-medium">
                  <option value="ALL">All Statuses</option>
                  <option value="NEW" selected>NEW / PENDING</option>
                  <option value="APPROVED">APPROVED</option>
                  <option value="IN_PROGRESS">IN PROGRESS</option>
                  <option value="COMPLETED">COMPLETED</option>
                  <option value="REJECTED">REJECTED</option>
                </select>
              </div>
            </div>
            
            <div class="overflow-x-auto max-h-[600px] overflow-y-auto">
              <table class="w-full text-left text-xs">
                <thead class="bg-slate-50 text-slate-600 font-semibold uppercase text-[10px] sticky top-0 border-b border-slate-200">
                  <tr>
                    <th class="py-3 px-3">Request ID & Date</th>
                    <th class="py-3 px-3">Student Details</th>
                    <th class="py-3 px-3">Project & Code</th>
                    <th class="py-3 px-3">Mode & Timeline</th>
                    <th class="py-3 px-3">Status</th>
                    <th class="py-3 px-3">Assigned Mentor</th>
                    <th class="py-3 px-3">Progress</th>
                    <th class="py-3 px-3 text-right">Actions</th>
                  </tr>
                </thead>
                <tbody id="adm-requests-table-body" class="divide-y divide-slate-100">
                  <!-- Populated by app.js -->
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- Admin Tab 3: Orders & Invoices Management -->
        <div id="adm-tab-orders" class="hidden space-y-4">
          <div class="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm space-y-4">
            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
              <div>
                <h3 class="text-base font-bold text-slate-900">Customer UPI Orders & Official GST Invoices</h3>
                <p class="text-xs text-slate-500">Verify payments, generate tax invoices (INV-XXXX), and download printable PDF/HTML receipts.</p>
              </div>
            </div>
            
            <div class="overflow-x-auto max-h-[600px] overflow-y-auto">
              <table class="w-full text-left text-xs">
                <thead class="bg-slate-50 text-slate-600 font-semibold uppercase text-[10px] sticky top-0 border-b border-slate-200">
                  <tr>
                    <th class="py-3 px-3">Order Number</th>
                    <th class="py-3 px-3">Customer</th>
                    <th class="py-3 px-3">Project Title</th>
                    <th class="py-3 px-3">Amount (₹)</th>
                    <th class="py-3 px-3">UTR Reference</th>
                    <th class="py-3 px-3">Screenshot</th>
                    <th class="py-3 px-3">Payment Status</th>
                    <th class="py-3 px-3">Invoice</th>
                    <th class="py-3 px-3 text-right">Actions</th>
                  </tr>
                </thead>
                <tbody id="adm-orders-table-body" class="divide-y divide-slate-100">
                  <!-- Populated by app.js -->
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- Admin Tab 6: Email Notification Audit Logs -->
        <div id="adm-tab-email-logs" class="hidden space-y-4">
          <div class="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm space-y-4">
            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
              <div>
                <h3 class="text-base font-bold text-slate-900">Email Notification Delivery Logs</h3>
                <p class="text-xs text-slate-500">Audit trail of automated alerts sent to owner (aniladani843@gmail.com) with retry capability.</p>
              </div>
              <button onclick="app.renderAdminEmailLogs()" class="px-3 py-1.5 rounded-lg border border-slate-200 hover:bg-slate-50 text-slate-700 text-xs font-semibold flex items-center gap-1">
                <i data-lucide="refresh-cw" class="w-3.5 h-3.5"></i> Refresh Logs
              </button>
            </div>
            
            <div class="overflow-x-auto max-h-[600px] overflow-y-auto">
              <table class="w-full text-left text-xs">
                <thead class="bg-slate-50 text-slate-600 font-semibold uppercase text-[10px] sticky top-0 border-b border-slate-200">
                  <tr>
                    <th class="py-3 px-3">Timestamp</th>
                    <th class="py-3 px-3">Event Type</th>
                    <th class="py-3 px-3">Recipient Email</th>
                    <th class="py-3 px-3">Subject</th>
                    <th class="py-3 px-3">Delivery Status</th>
                    <th class="py-3 px-3">Error / Diagnostics</th>
                    <th class="py-3 px-3 text-right">Action</th>
                  </tr>
                </thead>
                <tbody id="adm-email-logs-table-body" class="divide-y divide-slate-100 font-mono">
                  <!-- Populated by app.js -->
                </tbody>
              </table>
            </div>
          </div>
        </div>
'''

target_projects_tab = '<!-- Admin Tab 1: Project Management (90 Projects CRUD) -->'
if target_projects_tab in content:
    content = content.replace(target_projects_tab, new_admin_panes + '\n        <!-- Admin Tab 4: Project Management (90 Projects CRUD) -->')
    print("Inserted new Admin Panes.")

# Also update adm-tab-projects to hidden by default since enquiries is now the first tab
content = content.replace(
    '<div id="adm-tab-projects" class="space-y-4">',
    '<div id="adm-tab-projects" class="hidden space-y-4">'
)

# 10. Clean up Students Roster Table in admin view (remove demo filters)
old_student_filter = '''                <select id="adm-student-roster-filter" onchange="app.filterStudentRoster()" class="px-3 py-1.5 rounded-lg border border-slate-200 text-xs bg-white font-medium">
                  <option value="all">All Records (Genuine + Demo)</option>
                  <option value="genuine">Genuine Registrations Only</option>
                  <option value="demo">Demo Records Only (540)</option>
                </select>'''

new_student_filter = '''                <input type="text" id="adm-student-search" oninput="app.filterStudentRoster()" placeholder="Search student name, email, college..." class="px-3 py-1.5 rounded-lg border border-slate-200 text-xs">'''

if old_student_filter in content:
    content = content.replace(old_student_filter, new_student_filter)
    print("Updated Student Roster filter.")

# 11. Add Project Enquiry Modal
modal_enquiry_html = '''  <!-- ================= DEDICATED PROJECT ENQUIRY MODAL ================= -->
  <div id="modal-project-enquiry" class="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-sm hidden flex items-center justify-center p-3 sm:p-4 overflow-y-auto">
    <div class="bg-white rounded-3xl max-w-lg w-full p-6 sm:p-8 shadow-2xl border border-slate-200 space-y-4 my-auto animate-in fade-in zoom-in-95 duration-200">
      <div class="flex items-center justify-between pb-3 border-b border-slate-100">
        <div>
          <span class="text-xs font-bold text-amber-600 uppercase">Pre-Sales & Customization</span>
          <h3 class="font-extrabold text-slate-900 text-xl mt-0.5">Enquire About This Project</h3>
        </div>
        <button onclick="app.closeProjectEnquiryModal()" class="text-slate-400 hover:text-slate-600">
          <i data-lucide="x" class="w-5 h-5"></i>
        </button>
      </div>

      <div class="p-3.5 bg-amber-50 rounded-xl border border-amber-200 text-xs text-amber-950 space-y-1">
        <span class="font-bold block" id="enq-modal-project-title">Selected Project</span>
        <div class="flex items-center justify-between">
          <span class="text-[11px] text-amber-800 font-mono" id="enq-modal-project-code">CODE</span>
          <span class="text-[11px] font-bold text-amber-900" id="enq-modal-project-price">₹799+</span>
        </div>
      </div>

      <form onsubmit="event.preventDefault(); app.submitProjectEnquiry();" class="space-y-3">
        <input type="hidden" id="enq-modal-project-id">

        <div>
          <label class="block text-xs font-semibold text-slate-700 mb-1">Full Name *</label>
          <input type="text" id="enq-name" required placeholder="e.g. Rahul Sharma" class="w-full px-3 py-2 rounded-xl border border-slate-300 text-xs">
        </div>

        <div class="grid grid-cols-2 gap-2">
          <div>
            <label class="block text-xs font-semibold text-slate-700 mb-1">Email Address *</label>
            <input type="email" id="enq-email" required placeholder="rahul@college.edu" class="w-full px-3 py-2 rounded-xl border border-slate-300 text-xs">
          </div>
          <div>
            <label class="block text-xs font-semibold text-slate-700 mb-1">Mobile / WhatsApp *</label>
            <input type="tel" id="enq-phone" required placeholder="9876543210" class="w-full px-3 py-2 rounded-xl border border-slate-300 text-xs">
          </div>
        </div>

        <div class="grid grid-cols-2 gap-2">
          <div>
            <label class="block text-xs font-semibold text-slate-700 mb-1">College / University</label>
            <input type="text" id="enq-college" placeholder="e.g. Delhi Technical Univ" class="w-full px-3 py-2 rounded-xl border border-slate-300 text-xs">
          </div>
          <div>
            <label class="block text-xs font-semibold text-slate-700 mb-1">Course / Branch</label>
            <input type="text" id="enq-course" placeholder="e.g. B.Tech CSE / BCA" class="w-full px-3 py-2 rounded-xl border border-slate-300 text-xs">
          </div>
        </div>

        <div>
          <label class="block text-xs font-semibold text-slate-700 mb-1">Preferred Technology / Stack</label>
          <input type="text" id="enq-tech" placeholder="e.g. Python Django, React + FastAPI, Java Spring" class="w-full px-3 py-2 rounded-xl border border-slate-300 text-xs">
        </div>

        <div>
          <label class="block text-xs font-semibold text-slate-700 mb-1">Customization Requirements or Question *</label>
          <textarea id="enq-message" rows="3" required placeholder="Describe what customization, synopsis assistance, or delivery timeline you need..." class="w-full px-3 py-2 rounded-xl border border-slate-300 text-xs"></textarea>
        </div>

        <button type="submit" id="enq-submit-btn" class="w-full py-3 bg-amber-500 hover:bg-amber-600 text-slate-950 font-bold rounded-xl text-xs sm:text-sm shadow-md transition-all flex items-center justify-center gap-2">
          <i data-lucide="send" class="w-4 h-4"></i> Submit Enquiry for Immediate Response
        </button>
      </form>
    </div>
  </div>
'''

target_modal_request = '<!-- ================= STUDENT PROJECT ENROLLMENT REQUEST MODAL ================= -->'
if target_modal_request in content:
    content = content.replace(target_modal_request, modal_enquiry_html + '\n  ' + target_modal_request)
    print("Inserted modal-project-enquiry.")

# 12. Add Enquire Button in Project Details Modal
old_modal_action_bar = '''          <div class="flex flex-wrap items-center gap-2.5">
            <button id="modal-request-btn" onclick="app.openProjectRequestFromModal()" class="px-4 py-2.5 rounded-xl bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold text-xs sm:text-sm shadow-md transition-all flex items-center gap-1.5">
              <i data-lucide="send" class="w-4 h-4"></i> Request Project
            </button>
            <a id="modal-whatsapp-enquiry-btn" href="https://wa.me/918431712924" target="_blank" rel="noopener noreferrer" class="px-4 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white text-xs sm:text-sm font-bold flex items-center gap-2 shadow-md shadow-emerald-600/30 transition-all">
              <i data-lucide="message-circle" class="w-4 h-4"></i> Ask on WhatsApp
            </a>
            <button id="modal-buy-btn" onclick="app.openCheckoutFromModal()" class="px-5 py-2.5 rounded-xl bg-gradient-to-r from-brand-purple to-purple-600 hover:opacity-95 text-white text-xs sm:text-sm font-bold shadow-lg shadow-purple-500/25 transition-all flex items-center gap-2">
              <i data-lucide="zap" class="w-4 h-4"></i> Buy Now (UPI)
            </button>
          </div>'''

new_modal_action_bar = '''          <div class="flex flex-wrap items-center gap-2.5">
            <button id="modal-enquire-btn" onclick="app.openProjectEnquiryFromModal()" class="px-4 py-2.5 rounded-xl bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold text-xs sm:text-sm shadow-md transition-all flex items-center gap-1.5">
              <i data-lucide="help-circle" class="w-4 h-4"></i> Enquire Now
            </button>
            <button id="modal-request-btn" onclick="app.openProjectRequestFromModal()" class="px-4 py-2.5 rounded-xl bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold text-xs sm:text-sm shadow-md transition-all flex items-center gap-1.5">
              <i data-lucide="send" class="w-4 h-4"></i> Request Capstone
            </button>
            <a id="modal-whatsapp-enquiry-btn" href="https://wa.me/918431712924" target="_blank" rel="noopener noreferrer" class="px-4 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white text-xs sm:text-sm font-bold flex items-center gap-2 shadow-md shadow-emerald-600/30 transition-all">
              <i data-lucide="message-circle" class="w-4 h-4"></i> WhatsApp
            </a>
            <button id="modal-buy-btn" onclick="app.openCheckoutFromModal()" class="px-5 py-2.5 rounded-xl bg-gradient-to-r from-brand-purple to-purple-600 hover:opacity-95 text-white text-xs sm:text-sm font-bold shadow-lg shadow-purple-500/25 transition-all flex items-center gap-2">
              <i data-lucide="zap" class="w-4 h-4"></i> Buy Now (UPI)
            </button>
          </div>'''

if old_modal_action_bar in content:
    content = content.replace(old_modal_action_bar, new_modal_action_bar)
    print("Updated Project Details Modal Action Bar with Enquire button.")

# 13. Update Customer Dashboard Navigation Tabs & Panes
old_dash_tabs = '''        <!-- Dashboard Navigation Tabs -->
        <div class="flex border-b border-slate-200 gap-6 font-semibold text-sm overflow-x-auto">
          <button onclick="app.setDashboardTab('enrolled')" id="tab-dash-enrolled" class="py-3 tab-active flex items-center gap-2 whitespace-nowrap">
            <i data-lucide="layers" class="w-4 h-4"></i> Enrolled Projects (<span id="dash-enrolled-count">0</span>)
          </button>
          <button onclick="app.setDashboardTab('orders')" id="tab-dash-orders" class="py-3 text-slate-500 hover:text-slate-800 flex items-center gap-2 whitespace-nowrap">
            <i data-lucide="receipt" class="w-4 h-4"></i> Requests & UPI Orders
          </button>
          <button onclick="app.setDashboardTab('support')" id="tab-dash-support" class="py-3 text-slate-500 hover:text-slate-800 flex items-center gap-2 whitespace-nowrap">
            <i data-lucide="life-buoy" class="w-4 h-4"></i> Support Tickets
          </button>
          <button onclick="app.setDashboardTab('notifications')" id="tab-dash-notifications" class="py-3 text-slate-500 hover:text-slate-800 flex items-center gap-2 whitespace-nowrap">
            <i data-lucide="bell" class="w-4 h-4"></i> Notifications
          </button>
        </div>'''

new_dash_tabs = '''        <!-- Dashboard Navigation Tabs (Customer Self-Service) -->
        <div class="flex border-b border-slate-200 gap-6 font-semibold text-sm overflow-x-auto">
          <button onclick="app.setDashboardTab('enquiries')" id="tab-dash-enquiries" class="py-3 tab-active flex items-center gap-2 whitespace-nowrap">
            <i data-lucide="help-circle" class="w-4 h-4 text-amber-500"></i> My Enquiries (<span id="dash-enquiries-count">0</span>)
          </button>
          <button onclick="app.setDashboardTab('requests')" id="tab-dash-requests" class="py-3 text-slate-500 hover:text-slate-800 flex items-center gap-2 whitespace-nowrap">
            <i data-lucide="clipboard-list" class="w-4 h-4 text-blue-500"></i> My Project Requests (<span id="dash-requests-count">0</span>)
          </button>
          <button onclick="app.setDashboardTab('orders')" id="tab-dash-orders" class="py-3 text-slate-500 hover:text-slate-800 flex items-center gap-2 whitespace-nowrap">
            <i data-lucide="receipt" class="w-4 h-4 text-emerald-500"></i> My Orders & Invoices (<span id="dash-orders-count">0</span>)
          </button>
          <button onclick="app.setDashboardTab('profile')" id="tab-dash-profile" class="py-3 text-slate-500 hover:text-slate-800 flex items-center gap-2 whitespace-nowrap">
            <i data-lucide="user-cog" class="w-4 h-4 text-purple-500"></i> Profile & Security
          </button>
        </div>'''

if old_dash_tabs in content:
    content = content.replace(old_dash_tabs, new_dash_tabs)
    print("Replaced Customer Dashboard Tabs.")

# Replace Dashboard Panes
old_dash_panes = '''        <!-- Dashboard Tab 1: Enrolled Projects (with progress milestones & mentor info) -->
        <div id="dash-tab-content-enrolled" class="space-y-6">
          <div id="dash-enrolled-container" class="space-y-4">
            <!-- Populated by app.js -->
          </div>
        </div>

        <!-- Dashboard Tab 2: Requests & UPI Orders -->
        <div id="dash-tab-content-orders" class="hidden space-y-4">
          <div id="dash-orders-container" class="bg-white rounded-2xl border border-slate-200 overflow-hidden shadow-sm">
            <!-- Table populated by app.js -->
          </div>
        </div>

        <!-- Dashboard Tab 3: Support Tickets -->
        <div id="dash-tab-content-support" class="hidden space-y-4">
          <div class="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm space-y-4">
            <div class="flex items-center justify-between pb-3 border-b border-slate-100">
              <h4 class="font-bold text-slate-900 text-sm">Raise an Academic Support Ticket</h4>
            </div>
            <form onsubmit="event.preventDefault(); app.handleCreateTicket();" class="space-y-3">
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <div>
                  <label class="block text-xs font-semibold text-slate-700 mb-1">Subject</label>
                  <input type="text" id="ticket-subject" required placeholder="e.g. Need assistance importing MySQL database" class="w-full px-3 py-2 rounded-xl border border-slate-300 text-xs">
                </div>
                <div>
                  <label class="block text-xs font-semibold text-slate-700 mb-1">Category</label>
                  <select id="ticket-category" class="w-full px-3 py-2 rounded-xl border border-slate-300 text-xs bg-white">
                    <option value="Technical Code Setup">Technical Code Setup</option>
                    <option value="Project Selection Guidance">Project Selection Guidance</option>
                    <option value="Documentation & IEEE Format">Documentation & IEEE Format</option>
                    <option value="UPI Payment Verification">UPI Payment Verification</option>
                  </select>
                </div>
              </div>
              <div>
                <label class="block text-xs font-semibold text-slate-700 mb-1">Message Description</label>
                <textarea id="ticket-message" rows="3" required placeholder="Describe your question or error details..." class="w-full px-3 py-2 rounded-xl border border-slate-300 text-xs"></textarea>
              </div>
              <button type="submit" class="px-5 py-2.5 bg-brand-purple hover:bg-purple-700 text-white font-bold rounded-xl text-xs transition-colors">
                Submit Support Ticket
              </button>
            </form>
          </div>
          <div id="dash-tickets-container" class="space-y-3"></div>
        </div>

        <!-- Dashboard Tab 4: Notifications -->
        <div id="dash-tab-content-notifications" class="hidden space-y-3">
          <div id="dash-notifications-container" class="space-y-2">
            <!-- Populated by app.js -->
          </div>
        </div>'''

new_dash_panes = '''        <!-- Dashboard Tab 1: My Enquiries -->
        <div id="dash-tab-content-enquiries" class="space-y-4">
          <div class="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm space-y-4">
            <div class="flex items-center justify-between pb-3 border-b border-slate-100">
              <h4 class="font-bold text-slate-900 text-base">My Project Enquiries</h4>
              <button onclick="app.navigate('catalogue')" class="px-3.5 py-1.5 bg-brand-purple text-white text-xs font-bold rounded-xl flex items-center gap-1.5">
                <i data-lucide="plus-circle" class="w-3.5 h-3.5"></i> Enquire for Project
              </button>
            </div>
            <div id="dash-enquiries-container" class="space-y-3">
              <!-- Populated by app.js -->
            </div>
          </div>
        </div>

        <!-- Dashboard Tab 2: My Project Requests -->
        <div id="dash-tab-content-requests" class="hidden space-y-4">
          <div class="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm space-y-4">
            <h4 class="font-bold text-slate-900 text-base">My Capstone Enrollment Requests</h4>
            <div id="dash-requests-container" class="space-y-3">
              <!-- Populated by app.js -->
            </div>
          </div>
        </div>

        <!-- Dashboard Tab 3: My Orders & Official Invoices -->
        <div id="dash-tab-content-orders" class="hidden space-y-4">
          <div class="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm space-y-4">
            <h4 class="font-bold text-slate-900 text-base">My Project Orders & GST Invoices</h4>
            <div id="dash-orders-container" class="overflow-x-auto">
              <!-- Populated by app.js -->
            </div>
          </div>
        </div>

        <!-- Dashboard Tab 4: Profile & Security -->
        <div id="dash-tab-content-profile" class="hidden space-y-6">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <!-- Profile Info Form -->
            <div class="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm space-y-4">
              <h4 class="font-bold text-slate-900 text-base pb-2 border-b border-slate-100">Update Profile Information</h4>
              <form onsubmit="event.preventDefault(); app.handleUpdateProfile();" class="space-y-3">
                <div>
                  <label class="block text-xs font-semibold text-slate-700 mb-1">Full Name</label>
                  <input type="text" id="prof-name" required class="w-full px-3 py-2 rounded-xl border border-slate-300 text-xs">
                </div>
                <div>
                  <label class="block text-xs font-semibold text-slate-700 mb-1">Phone Number</label>
                  <input type="tel" id="prof-phone" class="w-full px-3 py-2 rounded-xl border border-slate-300 text-xs">
                </div>
                <div>
                  <label class="block text-xs font-semibold text-slate-700 mb-1">College / University</label>
                  <input type="text" id="prof-college" class="w-full px-3 py-2 rounded-xl border border-slate-300 text-xs">
                </div>
                <div>
                  <label class="block text-xs font-semibold text-slate-700 mb-1">Course / Branch</label>
                  <input type="text" id="prof-course" class="w-full px-3 py-2 rounded-xl border border-slate-300 text-xs">
                </div>
                <button type="submit" class="px-5 py-2.5 bg-brand-purple hover:bg-purple-700 text-white font-bold rounded-xl text-xs transition-colors">
                  Save Profile Changes
                </button>
              </form>
            </div>

            <!-- Change Password Form -->
            <div class="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm space-y-4">
              <h4 class="font-bold text-slate-900 text-base pb-2 border-b border-slate-100">Change Account Password</h4>
              <form onsubmit="event.preventDefault(); app.handleChangePassword();" class="space-y-3">
                <div>
                  <label class="block text-xs font-semibold text-slate-700 mb-1">Current Password</label>
                  <input type="password" id="pwd-old" required class="w-full px-3 py-2 rounded-xl border border-slate-300 text-xs">
                </div>
                <div>
                  <label class="block text-xs font-semibold text-slate-700 mb-1">New Password (Min 6 chars)</label>
                  <input type="password" id="pwd-new" required minlength="6" class="w-full px-3 py-2 rounded-xl border border-slate-300 text-xs">
                </div>
                <div>
                  <label class="block text-xs font-semibold text-slate-700 mb-1">Confirm New Password</label>
                  <input type="password" id="pwd-confirm" required minlength="6" class="w-full px-3 py-2 rounded-xl border border-slate-300 text-xs">
                </div>
                <button type="submit" class="px-5 py-2.5 bg-slate-900 hover:bg-slate-800 text-white font-bold rounded-xl text-xs transition-colors">
                  Update Password
                </button>
              </form>
            </div>
          </div>
        </div>'''

if old_dash_panes in content:
    content = content.replace(old_dash_panes, new_dash_panes)
    print("Replaced Customer Dashboard Panes.")

with open('static/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("update_html.py completed successfully.")
