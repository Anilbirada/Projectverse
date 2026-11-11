import re

with open('static/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Add "Refer & Earn 25%" button in desktop navbar
nav_target = '<div id="nav-auth-container" class="flex items-center gap-2">'
nav_replacement = '''<!-- Refer & Earn 25% CTA -->
        <button onclick="app.openPartnerModal()" class="hidden md:inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-bold bg-emerald-50 text-emerald-700 hover:bg-emerald-100 border border-emerald-200 shadow-sm transition-all" title="Become a Referral Partner & Earn 25% Commission">
          <i data-lucide="gift" class="w-3.5 h-3.5 text-emerald-600"></i>
          <span>Refer & Earn 25%</span>
        </button>

        <div id="nav-auth-container" class="flex items-center gap-2">'''

if nav_target in html and 'Refer & Earn 25%' not in html:
    html = html.replace(nav_target, nav_replacement, 1)
    print("Added desktop navbar Refer & Earn button.")

# 2. Add in mobile menu
mobile_target = '<div id="mobile-auth-container" class="pt-2 border-t border-slate-100">'
mobile_replacement = '''<div class="pt-2 border-t border-slate-100">
        <button onclick="app.openPartnerModal(); app.toggleMobileMenu();" class="w-full text-left font-bold text-emerald-700 py-1 flex items-center gap-2 text-xs">
          <i data-lucide="gift" class="w-4 h-4 text-emerald-600"></i>
          <span>Refer & Earn 25% Commission</span>
        </button>
      </div>
      <div id="mobile-auth-container" class="pt-2 border-t border-slate-100">'''

if mobile_target in html and 'Refer & Earn 25% Commission' not in html:
    html = html.replace(mobile_target, mobile_replacement, 1)
    print("Added mobile menu Refer & Earn button.")

# 3. Add Referral Code input in student registration form
reg_pwd_target = '''        <div>
          <label class="block text-xs font-semibold text-slate-700 mb-1">Create Password *</label>
          <input type="password" id="reg-password" required minlength="6" placeholder="At least 6 characters" class="w-full px-3 py-2 rounded-xl border border-slate-300 text-xs sm:text-sm">
        </div>'''

reg_pwd_replacement = '''        <div>
          <label class="block text-xs font-semibold text-slate-700 mb-1">Referral Code (Optional)</label>
          <div class="relative">
            <input type="text" id="reg-referral-code" placeholder="e.g. ANIL001" class="w-full px-3 py-2 rounded-xl border border-slate-300 text-xs sm:text-sm uppercase font-mono tracking-wider">
            <span id="reg-ref-badge" class="hidden absolute right-2.5 top-2 text-[10px] font-bold text-emerald-600 bg-emerald-50 px-2 py-0.5 rounded-md border border-emerald-200">Applied</span>
          </div>
        </div>
        <div>
          <label class="block text-xs font-semibold text-slate-700 mb-1">Create Password *</label>
          <input type="password" id="reg-password" required minlength="6" placeholder="At least 6 characters" class="w-full px-3 py-2 rounded-xl border border-slate-300 text-xs sm:text-sm">
        </div>'''

if reg_pwd_target in html and 'id="reg-referral-code"' not in html:
    html = html.replace(reg_pwd_target, reg_pwd_replacement, 1)
    print("Added referral code input to student registration form.")

# 4. Add Admin Navigation Tab button for Referrals
admin_tabs_target = '''          <button onclick="app.setAdminTab('support')" id="tab-adm-support" class="py-3 text-slate-600 hover:text-slate-900 flex items-center gap-1.5 whitespace-nowrap">
            <i data-lucide="message-square" class="w-4 h-4"></i> Support Settings
          </button>'''

admin_tabs_replacement = '''          <button onclick="app.setAdminTab('referrals')" id="tab-adm-referrals" class="py-3 text-slate-600 hover:text-slate-900 flex items-center gap-1.5 whitespace-nowrap">
            <i data-lucide="share-2" class="w-4 h-4 text-emerald-600"></i> Referral Partners (25%) (<span id="adm-badge-partners">0</span>)
          </button>
          <button onclick="app.setAdminTab('support')" id="tab-adm-support" class="py-3 text-slate-600 hover:text-slate-900 flex items-center gap-1.5 whitespace-nowrap">
            <i data-lucide="message-square" class="w-4 h-4"></i> Support Settings
          </button>'''

if admin_tabs_target in html and 'tab-adm-referrals' not in html:
    html = html.replace(admin_tabs_target, admin_tabs_replacement, 1)
    print("Added admin tab button for referrals.")

# 5. Add Admin Referrals Content Pane (Subtabs: Partners, Commissions, Payout Requests, Clicks, Settings)
admin_support_pane = '''        <!-- Admin Tab 9: WhatsApp & Support Settings -->'''

admin_referrals_pane = '''        <!-- Admin Tab: Referral Partners & 25% Commission Management -->
        <div id="adm-tab-referrals" class="hidden space-y-6">
          <div class="flex flex-wrap items-center justify-between gap-4 bg-white p-5 rounded-2xl border border-slate-200 shadow-sm">
            <div>
              <h3 class="text-lg font-bold text-slate-900 flex items-center gap-2">
                <i data-lucide="share-2" class="w-5 h-5 text-emerald-600"></i>
                Referral Partner & 25% Commission Command Center
              </h3>
              <p class="text-xs text-slate-500 mt-0.5">Manage partner approvals, commission ledgers, automated payouts, and affiliate settings.</p>
            </div>
            <div class="flex items-center gap-2">
              <button onclick="app.exportReferralsCsv()" class="px-3.5 py-2 rounded-xl text-xs font-bold bg-slate-900 hover:bg-slate-800 text-white flex items-center gap-1.5 shadow-sm transition-all">
                <i data-lucide="download" class="w-3.5 h-3.5 text-cyan-400"></i> Export CSV Report
              </button>
              <button onclick="app.loadAdminReferrals()" class="px-3.5 py-2 rounded-xl text-xs font-bold bg-white hover:bg-slate-50 border border-slate-200 text-slate-700 flex items-center gap-1.5 shadow-sm">
                <i data-lucide="refresh-cw" class="w-3.5 h-3.5"></i> Refresh
              </button>
            </div>
          </div>

          <!-- Referral Admin KPI Summary Cards -->
          <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div class="bg-white p-4 rounded-2xl border border-slate-200 shadow-sm">
              <span class="text-[11px] font-bold text-slate-500 uppercase tracking-wider block">Total Partners</span>
              <div class="mt-1 flex items-baseline justify-between">
                <span class="text-2xl sm:text-3xl font-black text-slate-900" id="adm-ref-stat-partners">0</span>
                <span class="text-[11px] font-semibold text-amber-600" id="adm-ref-stat-pending-partners">0 Pending</span>
              </div>
            </div>
            <div class="bg-white p-4 rounded-2xl border border-slate-200 shadow-sm">
              <span class="text-[11px] font-bold text-slate-500 uppercase tracking-wider block">Referred Sales</span>
              <div class="mt-1 flex items-baseline justify-between">
                <span class="text-2xl sm:text-3xl font-black text-emerald-600" id="adm-ref-stat-sales">0</span>
                <span class="text-[11px] font-semibold text-slate-500" id="adm-ref-stat-clicks">0 Clicks</span>
              </div>
            </div>
            <div class="bg-white p-4 rounded-2xl border border-slate-200 shadow-sm">
              <span class="text-[11px] font-bold text-slate-500 uppercase tracking-wider block">Total 25% Earned</span>
              <div class="mt-1">
                <span class="text-2xl sm:text-3xl font-black text-brand-purple" id="adm-ref-stat-earned">₹0</span>
                <span class="text-[11px] font-medium text-slate-500 block">All-time Commission</span>
              </div>
            </div>
            <div class="bg-white p-4 rounded-2xl border border-slate-200 shadow-sm">
              <span class="text-[11px] font-bold text-slate-500 uppercase tracking-wider block">Pending Payouts</span>
              <div class="mt-1 flex items-baseline justify-between">
                <span class="text-2xl sm:text-3xl font-black text-rose-600" id="adm-ref-stat-pending-payouts">0</span>
                <span class="text-[11px] font-semibold text-rose-600" id="adm-ref-stat-pending-payout-amt">₹0</span>
              </div>
            </div>
          </div>

          <!-- Referral Admin Sub-Tabs Navigation -->
          <div class="flex border-b border-slate-200 gap-4 font-semibold text-xs overflow-x-auto bg-white px-4 rounded-t-2xl">
            <button onclick="app.setAdminReferralSubTab('partners')" id="tab-adm-ref-partners" class="py-3 tab-active flex items-center gap-1.5 whitespace-nowrap">
              <i data-lucide="users" class="w-3.5 h-3.5"></i> Partner Roster
            </button>
            <button onclick="app.setAdminReferralSubTab('commissions')" id="tab-adm-ref-commissions" class="py-3 text-slate-600 hover:text-slate-900 flex items-center gap-1.5 whitespace-nowrap">
              <i data-lucide="percent" class="w-3.5 h-3.5"></i> 25% Commission Ledger
            </button>
            <button onclick="app.setAdminReferralSubTab('payouts')" id="tab-adm-ref-payouts" class="py-3 text-slate-600 hover:text-slate-900 flex items-center gap-1.5 whitespace-nowrap">
              <i data-lucide="credit-card" class="w-3.5 h-3.5"></i> Payout Requests (<span id="adm-ref-badge-payouts">0</span>)
            </button>
            <button onclick="app.setAdminReferralSubTab('clicks')" id="tab-adm-ref-clicks" class="py-3 text-slate-600 hover:text-slate-900 flex items-center gap-1.5 whitespace-nowrap">
              <i data-lucide="mouse-pointer" class="w-3.5 h-3.5"></i> Traffic & Clicks
            </button>
            <button onclick="app.setAdminReferralSubTab('settings')" id="tab-adm-ref-settings" class="py-3 text-slate-600 hover:text-slate-900 flex items-center gap-1.5 whitespace-nowrap">
              <i data-lucide="sliders" class="w-3.5 h-3.5"></i> Commission Settings
            </button>
          </div>

          <!-- SUB-TAB 1: PARTNERS ROSTER -->
          <div id="adm-ref-subtab-partners" class="bg-white rounded-b-2xl border border-slate-200 p-5 shadow-sm space-y-4">
            <div class="flex items-center justify-between">
              <span class="text-xs font-bold text-slate-700 uppercase tracking-wider">Registered Referral Partners</span>
              <div class="flex items-center gap-2">
                <select id="adm-ref-filter-partner-status" onchange="app.renderAdminPartnersTable()" class="px-3 py-1.5 rounded-xl border border-slate-300 text-xs bg-white">
                  <option value="ALL">All Statuses</option>
                  <option value="PENDING">Pending Review</option>
                  <option value="APPROVED">Approved Active</option>
                  <option value="REJECTED">Rejected</option>
                  <option value="SUSPENDED">Suspended</option>
                </select>
              </div>
            </div>
            <div class="overflow-x-auto">
              <table class="w-full text-left border-collapse">
                <thead>
                  <tr class="border-b border-slate-200 text-[11px] font-bold text-slate-500 uppercase tracking-wider">
                    <th class="py-2.5 px-3">Partner</th>
                    <th class="py-2.5 px-3">Contact</th>
                    <th class="py-2.5 px-3">Payout Details</th>
                    <th class="py-2.5 px-3">Referral Code</th>
                    <th class="py-2.5 px-3 text-right">Sales / Earned</th>
                    <th class="py-2.5 px-3 text-center">Status</th>
                    <th class="py-2.5 px-3 text-right">Actions</th>
                  </tr>
                </thead>
                <tbody id="adm-ref-partners-tbody" class="divide-y divide-slate-100 text-xs">
                  <tr><td colspan="7" class="py-6 text-center text-slate-400">Loading partners...</td></tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- SUB-TAB 2: COMMISSIONS LEDGER -->
          <div id="adm-ref-subtab-commissions" class="hidden bg-white rounded-b-2xl border border-slate-200 p-5 shadow-sm space-y-4">
            <div class="flex items-center justify-between">
              <span class="text-xs font-bold text-slate-700 uppercase tracking-wider">Automated 25% Commission Ledger</span>
              <select id="adm-ref-filter-comm-status" onchange="app.renderAdminCommissionsTable()" class="px-3 py-1.5 rounded-xl border border-slate-300 text-xs bg-white">
                <option value="ALL">All Statuses</option>
                <option value="APPROVED">Approved</option>
                <option value="PAID">Paid</option>
                <option value="REVERSED">Reversed</option>
              </select>
            </div>
            <div class="overflow-x-auto">
              <table class="w-full text-left border-collapse">
                <thead>
                  <tr class="border-b border-slate-200 text-[11px] font-bold text-slate-500 uppercase tracking-wider">
                    <th class="py-2.5 px-3">Date</th>
                    <th class="py-2.5 px-3">Order #</th>
                    <th class="py-2.5 px-3">Partner</th>
                    <th class="py-2.5 px-3">Project / Student</th>
                    <th class="py-2.5 px-3 text-right">Net Sale</th>
                    <th class="py-2.5 px-3 text-right">Commission (25%)</th>
                    <th class="py-2.5 px-3 text-center">Status</th>
                    <th class="py-2.5 px-3 text-right">Actions</th>
                  </tr>
                </thead>
                <tbody id="adm-ref-commissions-tbody" class="divide-y divide-slate-100 text-xs">
                  <tr><td colspan="8" class="py-6 text-center text-slate-400">Loading commissions...</td></tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- SUB-TAB 3: PAYOUT REQUESTS -->
          <div id="adm-ref-subtab-payouts" class="hidden bg-white rounded-b-2xl border border-slate-200 p-5 shadow-sm space-y-4">
            <div class="flex items-center justify-between">
              <span class="text-xs font-bold text-slate-700 uppercase tracking-wider">Partner Payout Queue</span>
              <select id="adm-ref-filter-payout-status" onchange="app.renderAdminPayoutsTable()" class="px-3 py-1.5 rounded-xl border border-slate-300 text-xs bg-white">
                <option value="ALL">All Statuses</option>
                <option value="PENDING">Pending Settlement</option>
                <option value="PAID">Paid (Settled)</option>
                <option value="REJECTED">Rejected</option>
              </select>
            </div>
            <div class="overflow-x-auto">
              <table class="w-full text-left border-collapse">
                <thead>
                  <tr class="border-b border-slate-200 text-[11px] font-bold text-slate-500 uppercase tracking-wider">
                    <th class="py-2.5 px-3">Date</th>
                    <th class="py-2.5 px-3">Request #</th>
                    <th class="py-2.5 px-3">Partner</th>
                    <th class="py-2.5 px-3">Method & Details</th>
                    <th class="py-2.5 px-3 text-right">Amount (₹)</th>
                    <th class="py-2.5 px-3 text-center">Status</th>
                    <th class="py-2.5 px-3 text-right">Settlement Action</th>
                  </tr>
                </thead>
                <tbody id="adm-ref-payouts-tbody" class="divide-y divide-slate-100 text-xs">
                  <tr><td colspan="7" class="py-6 text-center text-slate-400">Loading payouts...</td></tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- SUB-TAB 4: CLICKS & TRAFFIC -->
          <div id="adm-ref-subtab-clicks" class="hidden bg-white rounded-b-2xl border border-slate-200 p-5 shadow-sm space-y-4">
            <span class="text-xs font-bold text-slate-700 uppercase tracking-wider block">Live Referral Traffic Stream</span>
            <div class="overflow-x-auto">
              <table class="w-full text-left border-collapse">
                <thead>
                  <tr class="border-b border-slate-200 text-[11px] font-bold text-slate-500 uppercase tracking-wider">
                    <th class="py-2.5 px-3">Timestamp</th>
                    <th class="py-2.5 px-3">Referral Code</th>
                    <th class="py-2.5 px-3">Partner</th>
                    <th class="py-2.5 px-3">Visitor IP / Device</th>
                    <th class="py-2.5 px-3">Referrer</th>
                  </tr>
                </thead>
                <tbody id="adm-ref-clicks-tbody" class="divide-y divide-slate-100 text-xs">
                  <tr><td colspan="5" class="py-6 text-center text-slate-400">Loading clicks...</td></tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- SUB-TAB 5: COMMISSION SETTINGS -->
          <div id="adm-ref-subtab-settings" class="hidden bg-white rounded-b-2xl border border-slate-200 p-6 shadow-sm space-y-4 max-w-2xl">
            <h4 class="font-bold text-slate-900 text-sm">Affiliate & Commission Engine Parameters</h4>
            <form onsubmit="event.preventDefault(); app.saveReferralSettings();" class="space-y-4">
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label class="block text-xs font-semibold text-slate-700 mb-1">Commission Rate (%)</label>
                  <input type="number" id="adm-ref-cfg-rate" step="0.1" min="1" max="100" required class="w-full px-3 py-2 rounded-xl border border-slate-300 text-xs sm:text-sm font-bold text-emerald-700">
                  <p class="text-[10px] text-slate-500 mt-1">Default: 25.0% on net eligible project sale amount.</p>
                </div>
                <div>
                  <label class="block text-xs font-semibold text-slate-700 mb-1">Attribution Window (Days)</label>
                  <input type="number" id="adm-ref-cfg-window" min="1" max="365" required class="w-full px-3 py-2 rounded-xl border border-slate-300 text-xs sm:text-sm">
                  <p class="text-[10px] text-slate-500 mt-1">Cookie attribution window (standard: 30 days).</p>
                </div>
              </div>
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label class="block text-xs font-semibold text-slate-700 mb-1">Minimum Payout Threshold (₹)</label>
                  <input type="number" id="adm-ref-cfg-minpayout" min="100" max="50000" required class="w-full px-3 py-2 rounded-xl border border-slate-300 text-xs sm:text-sm">
                  <p class="text-[10px] text-slate-500 mt-1">Minimum approved balance to request payout (default: ₹500).</p>
                </div>
                <div class="space-y-3 pt-2">
                  <label class="flex items-center gap-2 text-xs font-semibold text-slate-700 cursor-pointer">
                    <input type="checkbox" id="adm-ref-cfg-autoapprove" class="rounded text-brand-purple">
                    <span>Auto-Approve Partner Registrations</span>
                  </label>
                  <label class="flex items-center gap-2 text-xs font-semibold text-slate-700 cursor-pointer">
                    <input type="checkbox" id="adm-ref-cfg-excludetax" checked class="rounded text-brand-purple">
                    <span>Exclude GST Tax from Commission Base</span>
                  </label>
                </div>
              </div>
              <button type="submit" class="px-6 py-2.5 bg-brand-purple hover:bg-purple-700 text-white font-bold rounded-xl text-xs sm:text-sm shadow-md transition-all">
                Save Affiliate Settings
              </button>
            </form>
          </div>
        </div>

'''

if admin_support_pane in html and 'adm-tab-referrals' not in html:
    html = html.replace(admin_support_pane, admin_referrals_pane + admin_support_pane, 1)
    print("Added admin referrals pane.")

# 6. Add Dedicated Referral Partner Dashboard SPA View (View 6)
view_dash_target = '''  </main>'''

partner_dashboard_view = '''    <!-- ================= VIEW 6: REFERRAL PARTNER DASHBOARD ================= -->
    <div id="view-partner-dashboard" class="hidden min-h-screen py-10 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto space-y-8 animate-in fade-in duration-200">
      
      <!-- Partner Hero Banner -->
      <div class="relative bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 rounded-3xl p-6 sm:p-8 text-white shadow-xl overflow-hidden border border-indigo-900/40">
        <div class="absolute -right-10 -bottom-10 w-64 h-64 bg-emerald-500/10 rounded-full blur-3xl pointer-events-none"></div>
        <div class="relative z-10 flex flex-wrap items-center justify-between gap-4">
          <div>
            <div class="flex items-center gap-2 mb-1">
              <span class="px-2.5 py-0.5 rounded-full text-[10px] font-black uppercase tracking-wider bg-emerald-400 text-slate-950">Official Partner</span>
              <span id="partner-dash-status-badge" class="px-2.5 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wider bg-emerald-500/20 text-emerald-300 border border-emerald-400/30">Active</span>
            </div>
            <h1 class="text-2xl sm:text-3xl font-extrabold tracking-tight">
              Welcome back, <span id="partner-dash-name" class="text-cyan-300">Partner</span>!
            </h1>
            <p class="text-slate-400 text-xs sm:text-sm mt-1">
              Earn a flat <span class="font-bold text-white">25% automatic commission</span> on every academic project purchase made through your link.
            </p>
          </div>
          <div class="flex items-center gap-3">
            <button onclick="app.openPayoutModal()" class="px-4 py-2.5 bg-gradient-to-r from-emerald-500 to-teal-500 hover:from-emerald-400 hover:to-teal-400 text-slate-950 font-bold rounded-xl text-xs sm:text-sm shadow-lg shadow-emerald-500/25 transition-all flex items-center gap-2">
              <i data-lucide="wallet" class="w-4 h-4"></i> Request Payout
            </button>
            <button onclick="app.partnerLogout()" class="px-3.5 py-2.5 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-xl text-xs font-semibold transition-colors">
              Sign Out
            </button>
          </div>
        </div>
      </div>

      <!-- Unique Referral Link & Share Card -->
      <div class="bg-white rounded-3xl border border-slate-200 p-6 sm:p-7 shadow-sm space-y-4">
        <div class="flex flex-wrap items-center justify-between gap-2">
          <div>
            <h3 class="text-base font-bold text-slate-900 flex items-center gap-2">
              <i data-lucide="link" class="w-4 h-4 text-brand-purple"></i> Your Unique Referral Link
            </h3>
            <p class="text-xs text-slate-500 mt-0.5">Share this link with classmates, students, WhatsApp groups, and campus channels.</p>
          </div>
          <div class="text-right">
            <span class="text-xs text-slate-500">Your Referral Code:</span>
            <span id="partner-dash-code" class="ml-1.5 px-3 py-1 rounded-lg font-mono font-black text-sm bg-purple-50 text-brand-purple border border-purple-200">ANIL001</span>
          </div>
        </div>

        <div class="flex flex-wrap sm:flex-nowrap items-center gap-2">
          <input type="text" id="partner-dash-link-input" readonly class="flex-1 px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl font-mono text-xs sm:text-sm text-slate-800 focus:outline-none">
          <button onclick="app.copyPartnerLink()" class="px-5 py-3 bg-brand-purple hover:bg-purple-700 text-white font-bold rounded-xl text-xs sm:text-sm shadow-md transition-all flex items-center gap-1.5 whitespace-nowrap">
            <i data-lucide="copy" class="w-4 h-4"></i> Copy Link
          </button>
        </div>

        <!-- 1-Click Social Share Buttons -->
        <div class="pt-3 border-t border-slate-100 flex flex-wrap items-center gap-2 text-xs">
          <span class="font-semibold text-slate-600 mr-1">Instant Share:</span>
          <button onclick="app.sharePartnerLink('whatsapp')" class="px-3.5 py-2 rounded-xl bg-emerald-500 hover:bg-emerald-600 text-white font-bold flex items-center gap-1.5 shadow-sm transition-all">
            <i data-lucide="message-circle" class="w-4 h-4"></i> WhatsApp
          </button>
          <button onclick="app.sharePartnerLink('telegram')" class="px-3.5 py-2 rounded-xl bg-sky-500 hover:bg-sky-600 text-white font-bold flex items-center gap-1.5 shadow-sm transition-all">
            <i data-lucide="send" class="w-4 h-4"></i> Telegram
          </button>
          <button onclick="app.sharePartnerLink('twitter')" class="px-3.5 py-2 rounded-xl bg-slate-900 hover:bg-black text-white font-bold flex items-center gap-1.5 shadow-sm transition-all">
            <i data-lucide="twitter" class="w-4 h-4"></i> X / Twitter
          </button>
          <button onclick="app.sharePartnerLink('email')" class="px-3.5 py-2 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-700 font-bold flex items-center gap-1.5 transition-all">
            <i data-lucide="mail" class="w-4 h-4"></i> Email
          </button>
        </div>
      </div>

      <!-- Partner 6-KPI Metric Telemetry -->
      <div class="grid grid-cols-2 lg:grid-cols-6 gap-3 sm:gap-4">
        <div class="bg-white p-4 rounded-2xl border border-slate-200 shadow-sm">
          <span class="text-[10px] font-bold text-slate-500 uppercase tracking-wider block">Total Clicks</span>
          <span class="text-2xl font-black text-slate-900 mt-1 block" id="partner-stat-clicks">0</span>
          <span class="text-[10px] text-slate-400">Visitors referred</span>
        </div>
        <div class="bg-white p-4 rounded-2xl border border-slate-200 shadow-sm">
          <span class="text-[10px] font-bold text-slate-500 uppercase tracking-wider block">Registrations</span>
          <span class="text-2xl font-black text-blue-600 mt-1 block" id="partner-stat-registrations">0</span>
          <span class="text-[10px] text-slate-400">Attributed students</span>
        </div>
        <div class="bg-white p-4 rounded-2xl border border-slate-200 shadow-sm">
          <span class="text-[10px] font-bold text-slate-500 uppercase tracking-wider block">Purchases</span>
          <span class="text-2xl font-black text-emerald-600 mt-1 block" id="partner-stat-sales">0</span>
          <span class="text-[10px] text-slate-400">Verified orders</span>
        </div>
        <div class="bg-white p-4 rounded-2xl border border-slate-200 shadow-sm">
          <span class="text-[10px] font-bold text-slate-500 uppercase tracking-wider block">Conversion</span>
          <span class="text-2xl font-black text-cyan-600 mt-1 block" id="partner-stat-conversion">0%</span>
          <span class="text-[10px] text-slate-400">Sales / clicks</span>
        </div>
        <div class="bg-white p-4 rounded-2xl border border-slate-200 shadow-sm">
          <span class="text-[10px] font-bold text-slate-500 uppercase tracking-wider block">Available Balance</span>
          <span class="text-2xl font-black text-emerald-600 mt-1 block" id="partner-stat-approved">₹0</span>
          <span class="text-[10px] text-emerald-700 font-semibold">Ready for payout</span>
        </div>
        <div class="bg-white p-4 rounded-2xl border border-slate-200 shadow-sm">
          <span class="text-[10px] font-bold text-slate-500 uppercase tracking-wider block">Total Paid</span>
          <span class="text-2xl font-black text-slate-900 mt-1 block" id="partner-stat-paid">₹0</span>
          <span class="text-[10px] text-slate-400" id="partner-stat-total-earned">₹0 total earned</span>
        </div>
      </div>

      <!-- Partner Tables: Commission Ledger & Payout History -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        <!-- Left: Commissions History (2 Cols) -->
        <div class="lg:col-span-2 bg-white rounded-3xl border border-slate-200 p-6 shadow-sm space-y-4">
          <div class="flex items-center justify-between">
            <h3 class="text-base font-bold text-slate-900 flex items-center gap-2">
              <i data-lucide="percent" class="w-4 h-4 text-emerald-600"></i>
              Your 25% Commissions Ledger
            </h3>
            <span class="text-xs text-slate-400">Automatic credit on verified orders</span>
          </div>
          <div class="overflow-x-auto">
            <table class="w-full text-left border-collapse">
              <thead>
                <tr class="border-b border-slate-200 text-[11px] font-bold text-slate-500 uppercase tracking-wider">
                  <th class="py-2.5 px-3">Date</th>
                  <th class="py-2.5 px-3">Order #</th>
                  <th class="py-2.5 px-3">Project</th>
                  <th class="py-2.5 px-3 text-right">Net Sale</th>
                  <th class="py-2.5 px-3 text-right">25% Commission</th>
                  <th class="py-2.5 px-3 text-center">Status</th>
                </tr>
              </thead>
              <tbody id="partner-dash-commissions-tbody" class="divide-y divide-slate-100 text-xs">
                <tr><td colspan="6" class="py-6 text-center text-slate-400">No commissions recorded yet. Share your link to start earning!</td></tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Right: Payout Requests & Payment Profile -->
        <div class="space-y-6">
          <div class="bg-white rounded-3xl border border-slate-200 p-6 shadow-sm space-y-4">
            <div class="flex items-center justify-between">
              <h3 class="text-base font-bold text-slate-900 flex items-center gap-2">
                <i data-lucide="credit-card" class="w-4 h-4 text-brand-purple"></i>
                Payout Requests
              </h3>
              <button onclick="app.openPayoutModal()" class="text-xs font-bold text-brand-purple hover:underline">+ Request</button>
            </div>
            <div class="space-y-2 max-h-60 overflow-y-auto pr-1" id="partner-dash-payouts-list">
              <p class="text-xs text-slate-400 py-3 text-center">No payout requests yet.</p>
            </div>
          </div>

          <!-- Edit Payout Details -->
          <div class="bg-white rounded-3xl border border-slate-200 p-6 shadow-sm space-y-4">
            <h3 class="text-base font-bold text-slate-900 flex items-center gap-2">
              <i data-lucide="settings" class="w-4 h-4 text-slate-600"></i> Payout Settings
            </h3>
            <form onsubmit="event.preventDefault(); app.handleUpdatePartnerProfile();" class="space-y-3">
              <div>
                <label class="block text-xs font-semibold text-slate-700 mb-1">Preferred Method</label>
                <select id="partner-cfg-method" onchange="app.togglePartnerPayoutMethodInputs(this.value)" class="w-full px-3 py-2 rounded-xl border border-slate-300 text-xs bg-white">
                  <option value="UPI">UPI ID (Instant Transfer)</option>
                  <option value="BANK_TRANSFER">Direct Bank Transfer (NEFT/IMPS)</option>
                </select>
              </div>
              <div id="partner-cfg-upi-box">
                <label class="block text-xs font-semibold text-slate-700 mb-1">UPI ID</label>
                <input type="text" id="partner-cfg-upi" placeholder="yourname@okaxis" class="w-full px-3 py-2 rounded-xl border border-slate-300 text-xs font-mono">
              </div>
              <div id="partner-cfg-bank-box" class="hidden space-y-2">
                <div>
                  <label class="block text-xs font-semibold text-slate-700 mb-1">Bank Account Number</label>
                  <input type="text" id="partner-cfg-bank-acc" placeholder="Account Number" class="w-full px-3 py-2 rounded-xl border border-slate-300 text-xs font-mono">
                </div>
                <div class="grid grid-cols-2 gap-2">
                  <div>
                    <label class="block text-xs font-semibold text-slate-700 mb-1">IFSC Code</label>
                    <input type="text" id="partner-cfg-bank-ifsc" placeholder="HDFC0001234" class="w-full px-3 py-2 rounded-xl border border-slate-300 text-xs font-mono uppercase">
                  </div>
                  <div>
                    <label class="block text-xs font-semibold text-slate-700 mb-1">Holder Name</label>
                    <input type="text" id="partner-cfg-bank-name" placeholder="Name as per Passbook" class="w-full px-3 py-2 rounded-xl border border-slate-300 text-xs">
                  </div>
                </div>
              </div>
              <button type="submit" class="w-full py-2.5 bg-slate-900 hover:bg-slate-800 text-white font-bold rounded-xl text-xs shadow-sm transition-all">
                Update Payout Details
              </button>
            </form>
          </div>
        </div>

      </div>

    </div>
'''

if view_dash_target in html and 'id="view-partner-dashboard"' not in html:
    html = html.replace(view_dash_target, partner_dashboard_view + view_dash_target, 1)
    print("Added dedicated partner dashboard view.")

# 7. Add Referral Partner Auth Modal (#modal-partner-auth) & Partner Payout Modal & Admin Settlement Modal
modals_end_target = '''</body>'''

partner_modals = '''  <!-- ================= REFERRAL PARTNER AUTH MODAL (LOGIN / REGISTER) ================= -->
  <div id="modal-partner-auth" class="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-sm hidden flex items-center justify-center p-3 sm:p-4 overflow-y-auto">
    <div class="bg-white rounded-3xl max-w-lg w-full p-6 sm:p-8 shadow-2xl border border-slate-200 space-y-4 my-auto animate-in fade-in zoom-in-95 duration-200">
      
      <div class="flex items-center justify-between pb-3 border-b border-slate-100">
        <div>
          <span class="px-2 py-0.5 rounded text-[10px] font-black uppercase bg-emerald-100 text-emerald-800">Affiliate Program</span>
          <h3 id="partner-modal-title" class="font-extrabold text-slate-900 text-xl mt-0.5">Become a Partner (Earn 25%)</h3>
        </div>
        <button onclick="app.closePartnerModal()" class="text-slate-400 hover:text-slate-600">
          <i data-lucide="x" class="w-5 h-5"></i>
        </button>
      </div>

      <!-- Segmented Tab Switcher -->
      <div class="flex rounded-xl bg-slate-100 p-1 text-xs font-semibold">
        <button type="button" id="partner-tab-register" onclick="app.switchPartnerAuthMode('register')" class="flex-1 py-2 rounded-lg transition-all text-center font-bold bg-white text-slate-900 shadow-sm">
          Partner Registration
        </button>
        <button type="button" id="partner-tab-login" onclick="app.switchPartnerAuthMode('login')" class="flex-1 py-2 rounded-lg transition-all text-center font-medium text-slate-500 hover:text-slate-800">
          Partner Sign In
        </button>
      </div>

      <!-- PARTNER REGISTRATION FORM -->
      <form id="partner-register-form" onsubmit="event.preventDefault(); app.handlePartnerRegister();" class="space-y-3 max-h-[70vh] overflow-y-auto pr-1">
        <div class="p-3 bg-emerald-50 rounded-xl border border-emerald-200 text-xs text-emerald-900">
          <p class="font-bold flex items-center gap-1.5"><i data-lucide="sparkles" class="w-3.5 h-3.5 text-emerald-600"></i> 25% Flat Commission on Every Sale</p>
          <p class="mt-0.5 text-slate-600">Get your unique link, real-time attribution tracking, and fast UPI/Bank payouts.</p>
        </div>
        <div>
          <label class="block text-xs font-semibold text-slate-700 mb-1">Full Name *</label>
          <input type="text" id="partner-reg-name" required placeholder="Rajesh Kumar" class="w-full px-3 py-2 rounded-xl border border-slate-300 text-xs sm:text-sm">
        </div>
        <div class="grid grid-cols-2 gap-2">
          <div>
            <label class="block text-xs font-semibold text-slate-700 mb-1">Email Address *</label>
            <input type="email" id="partner-reg-email" required placeholder="rajesh@gmail.com" class="w-full px-3 py-2 rounded-xl border border-slate-300 text-xs sm:text-sm">
          </div>
          <div>
            <label class="block text-xs font-semibold text-slate-700 mb-1">Mobile Number *</label>
            <input type="tel" id="partner-reg-mobile" required placeholder="9876543210" class="w-full px-3 py-2 rounded-xl border border-slate-300 text-xs sm:text-sm">
          </div>
        </div>
        <div class="grid grid-cols-2 gap-2">
          <div>
            <label class="block text-xs font-semibold text-slate-700 mb-1">College Name (Optional)</label>
            <input type="text" id="partner-reg-college" placeholder="IIT / NIT / RVCE" class="w-full px-3 py-2 rounded-xl border border-slate-300 text-xs sm:text-sm">
          </div>
          <div>
            <label class="block text-xs font-semibold text-slate-700 mb-1">City *</label>
            <input type="text" id="partner-reg-city" required placeholder="Bangalore" class="w-full px-3 py-2 rounded-xl border border-slate-300 text-xs sm:text-sm">
          </div>
        </div>
        <div>
          <label class="block text-xs font-semibold text-slate-700 mb-1">Payout Method *</label>
          <select id="partner-reg-method" onchange="app.togglePartnerRegMethod(this.value)" class="w-full px-3 py-2 rounded-xl border border-slate-300 text-xs sm:text-sm bg-white">
            <option value="UPI">UPI ID (Google Pay, PhonePe, Paytm)</option>
            <option value="BANK_TRANSFER">Direct Bank Account Transfer</option>
          </select>
        </div>
        <div id="partner-reg-upi-box">
          <label class="block text-xs font-semibold text-slate-700 mb-1">UPI ID *</label>
          <input type="text" id="partner-reg-upi" placeholder="yourname@okaxis" class="w-full px-3 py-2 rounded-xl border border-slate-300 text-xs sm:text-sm font-mono">
        </div>
        <div id="partner-reg-bank-box" class="hidden space-y-2">
          <div>
            <label class="block text-xs font-semibold text-slate-700 mb-1">Bank Account Number *</label>
            <input type="text" id="partner-reg-bank-acc" placeholder="Account Number" class="w-full px-3 py-2 rounded-xl border border-slate-300 text-xs font-mono">
          </div>
          <div class="grid grid-cols-2 gap-2">
            <div>
              <label class="block text-xs font-semibold text-slate-700 mb-1">IFSC Code *</label>
              <input type="text" id="partner-reg-bank-ifsc" placeholder="HDFC0001234" class="w-full px-3 py-2 rounded-xl border border-slate-300 text-xs font-mono uppercase">
            </div>
            <div>
              <label class="block text-xs font-semibold text-slate-700 mb-1">Account Holder Name *</label>
              <input type="text" id="partner-reg-bank-name" placeholder="Name as per Bank" class="w-full px-3 py-2 rounded-xl border border-slate-300 text-xs">
            </div>
          </div>
        </div>
        <div>
          <label class="block text-xs font-semibold text-slate-700 mb-1">Create Password *</label>
          <input type="password" id="partner-reg-password" required minlength="6" placeholder="At least 6 characters" class="w-full px-3 py-2 rounded-xl border border-slate-300 text-xs sm:text-sm">
        </div>
        <p class="text-[11px] text-slate-500">
          Admin verifies applications within 2 hours. You will receive an activation email with your unique link.
        </p>
        <button type="submit" class="w-full py-3 bg-emerald-600 hover:bg-emerald-700 text-white font-bold rounded-xl text-sm shadow-md transition-all">
          Submit Partner Application
        </button>
      </form>

      <!-- PARTNER SIGN IN FORM -->
      <form id="partner-login-form" onsubmit="event.preventDefault(); app.handlePartnerLogin();" class="hidden space-y-3.5">
        <div>
          <label class="block text-xs font-semibold text-slate-700 mb-1">Partner Email Address</label>
          <input type="email" id="partner-login-email" required placeholder="rajesh@gmail.com" class="w-full px-3.5 py-2.5 rounded-xl border border-slate-300 text-sm">
        </div>
        <div>
          <label class="block text-xs font-semibold text-slate-700 mb-1">Password</label>
          <input type="password" id="partner-login-password" required placeholder="••••••••" class="w-full px-3.5 py-2.5 rounded-xl border border-slate-300 text-sm">
        </div>
        <button type="submit" class="w-full py-3 bg-emerald-600 hover:bg-emerald-700 text-white font-bold rounded-xl text-sm shadow-md transition-all">
          Sign In to Partner Dashboard
        </button>
        <p class="text-xs text-center text-slate-600">
          Want to become an affiliate partner? <a href="#" onclick="app.switchPartnerAuthMode('register')" class="text-emerald-600 font-semibold hover:underline">Apply here</a>
        </p>
      </form>

    </div>
  </div>

  <!-- ================= PARTNER PAYOUT REQUEST MODAL ================= -->
  <div id="modal-partner-payout" class="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-sm hidden flex items-center justify-center p-3 sm:p-4 overflow-y-auto">
    <div class="bg-white rounded-3xl max-w-md w-full p-6 shadow-2xl border border-slate-200 space-y-4 my-auto animate-in fade-in zoom-in-95 duration-200">
      <div class="flex items-center justify-between pb-3 border-b border-slate-100">
        <h3 class="font-extrabold text-slate-900 text-lg">Request Commission Payout</h3>
        <button onclick="app.closePayoutModal()" class="text-slate-400 hover:text-slate-600">
          <i data-lucide="x" class="w-5 h-5"></i>
        </button>
      </div>
      <div class="p-3 bg-emerald-50 rounded-xl border border-emerald-200 flex items-center justify-between">
        <span class="text-xs font-semibold text-emerald-900">Available Approved Balance:</span>
        <span id="payout-modal-balance" class="text-lg font-black text-emerald-700 font-mono">₹0</span>
      </div>
      <form onsubmit="event.preventDefault(); app.submitPayoutRequest();" class="space-y-3">
        <div>
          <label class="block text-xs font-semibold text-slate-700 mb-1">Payout Amount (₹) *</label>
          <input type="number" id="payout-amount-input" step="1" min="100" required class="w-full px-3 py-2 rounded-xl border border-slate-300 text-sm font-bold text-slate-900">
          <p class="text-[10px] text-slate-500 mt-1">Minimum payout threshold is ₹500.</p>
        </div>
        <div>
          <label class="block text-xs font-semibold text-slate-700 mb-1">Payment Method</label>
          <select id="payout-method-select" class="w-full px-3 py-2 rounded-xl border border-slate-300 text-xs bg-white">
            <option value="UPI">UPI ID</option>
            <option value="BANK_TRANSFER">Bank Account (NEFT/IMPS)</option>
          </select>
        </div>
        <div>
          <label class="block text-xs font-semibold text-slate-700 mb-1">Payout Account / UPI ID *</label>
          <input type="text" id="payout-details-input" required placeholder="yourname@okaxis or Bank Details" class="w-full px-3 py-2 rounded-xl border border-slate-300 text-xs font-mono">
        </div>
        <button type="submit" class="w-full py-3 bg-emerald-600 hover:bg-emerald-700 text-white font-bold rounded-xl text-sm shadow-md transition-all">
          Submit Payout Request
        </button>
      </form>
    </div>
  </div>

  <!-- ================= ADMIN PROCESS PAYOUT MODAL ================= -->
  <div id="modal-admin-process-payout" class="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-sm hidden flex items-center justify-center p-3 sm:p-4 overflow-y-auto">
    <div class="bg-white rounded-3xl max-w-md w-full p-6 shadow-2xl border border-slate-200 space-y-4 my-auto">
      <div class="flex items-center justify-between pb-3 border-b border-slate-100">
        <h3 class="font-extrabold text-slate-900 text-lg">Process Partner Payout</h3>
        <button onclick="app.closeAdminProcessPayoutModal()" class="text-slate-400 hover:text-slate-600">
          <i data-lucide="x" class="w-5 h-5"></i>
        </button>
      </div>
      <input type="hidden" id="adm-payout-id">
      <div class="p-3 bg-slate-50 rounded-xl border border-slate-200 text-xs space-y-1">
        <div><span class="text-slate-500">Partner:</span> <span id="adm-payout-partner-name" class="font-bold text-slate-800"></span></div>
        <div><span class="text-slate-500">Amount:</span> <span id="adm-payout-amount" class="font-bold text-emerald-600 font-mono"></span></div>
        <div><span class="text-slate-500">Destination:</span> <span id="adm-payout-dest" class="font-mono text-slate-700"></span></div>
      </div>
      <form onsubmit="event.preventDefault(); app.submitAdminProcessPayout();" class="space-y-3">
        <div>
          <label class="block text-xs font-semibold text-slate-700 mb-1">Action *</label>
          <select id="adm-payout-action" onchange="app.toggleAdminPayoutFields(this.value)" class="w-full px-3 py-2 rounded-xl border border-slate-300 text-xs bg-white">
            <option value="approve">Mark as PAID (Settled via Bank / UPI)</option>
            <option value="reject">Reject Request (Refund balance to partner)</option>
          </select>
        </div>
        <div id="adm-payout-utr-box">
          <label class="block text-xs font-semibold text-slate-700 mb-1">Bank UTR / Transaction Reference *</label>
          <input type="text" id="adm-payout-utr" placeholder="HDFC-UTR-8431712924-XXXX" class="w-full px-3 py-2 rounded-xl border border-slate-300 text-xs font-mono uppercase">
        </div>
        <div>
          <label class="block text-xs font-semibold text-slate-700 mb-1">Admin Notes / Settlement Remarks</label>
          <input type="text" id="adm-payout-notes" placeholder="Settled via HDFC Bank UPI" class="w-full px-3 py-2 rounded-xl border border-slate-300 text-xs">
        </div>
        <button type="submit" class="w-full py-2.5 bg-brand-purple hover:bg-purple-700 text-white font-bold rounded-xl text-xs sm:text-sm shadow-md transition-all">
          Confirm Settlement
        </button>
      </form>
    </div>
  </div>

  <!-- ================= ADMIN REVERSE COMMISSION MODAL ================= -->
  <div id="modal-admin-reverse-commission" class="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-sm hidden flex items-center justify-center p-3 sm:p-4 overflow-y-auto">
    <div class="bg-white rounded-3xl max-w-md w-full p-6 shadow-2xl border border-slate-200 space-y-4 my-auto">
      <div class="flex items-center justify-between pb-3 border-b border-slate-100">
        <h3 class="font-extrabold text-slate-900 text-lg">Reverse Commission</h3>
        <button onclick="app.closeAdminReverseCommissionModal()" class="text-slate-400 hover:text-slate-600">
          <i data-lucide="x" class="w-5 h-5"></i>
        </button>
      </div>
      <input type="hidden" id="adm-rev-comm-id">
      <p class="text-xs text-rose-600 bg-rose-50 p-3 rounded-xl border border-rose-200">
        Warning: This will set the commission status to REVERSED and deduct the commission amount from the partner's balance.
      </p>
      <form onsubmit="event.preventDefault(); app.submitAdminReverseCommission();" class="space-y-3">
        <div>
          <label class="block text-xs font-semibold text-slate-700 mb-1">Reason for Reversal *</label>
          <textarea id="adm-rev-notes" required rows="3" placeholder="Order cancelled or student refund issued" class="w-full px-3 py-2 rounded-xl border border-slate-300 text-xs"></textarea>
        </div>
        <button type="submit" class="w-full py-2.5 bg-rose-600 hover:bg-rose-700 text-white font-bold rounded-xl text-xs sm:text-sm shadow-md transition-all">
          Confirm Reversal
        </button>
      </form>
    </div>
  </div>
'''

if modals_end_target in html and 'modal-partner-auth' not in html:
    html = html.replace(modals_end_target, partner_modals + modals_end_target, 1)
    print("Added partner modals.")

with open('static/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("index.html successfully updated with referral system!")
