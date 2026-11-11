import re

with open('static/js/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# 1. Update Constructor to initialize partner auth state
ctor_target = "this.user = JSON.parse(localStorage.getItem('pv_user') || 'null');"
ctor_replacement = """this.user = JSON.parse(localStorage.getItem('pv_user') || 'null');
    this.partnerToken = localStorage.getItem('pv_partner_token') || null;
    this.partnerUser = JSON.parse(localStorage.getItem('pv_partner_user') || 'null');"""

if ctor_target in js and 'this.partnerToken' not in js:
    js = js.replace(ctor_target, ctor_replacement, 1)

# 2. Add URL referral tracking in init()
init_target = 'await Promise.all(['
init_replacement = """// Check & track URL referral attribution (?ref=CODE)
    this.checkAndTrackUrlReferral();

    await Promise.all(["""

if init_target in js and 'checkAndTrackUrlReferral' not in js:
    js = js.replace(init_target, init_replacement, 1)

# 3. Add partner-dashboard to hash router & navigate()
route_target = "} else if (hash === 'student-dashboard') {"
route_replacement = """} else if (hash === 'partner-dashboard') {
      if (!this.partnerToken) {
        this.openPartnerModal('login');
        this.navigate('home');
      } else {
        this.navigate('partner-dashboard');
      }
    } else if (hash === 'student-dashboard') {"""

if route_target in js and 'partner-dashboard' not in js:
    js = js.replace(route_target, route_replacement, 1)

# In navigate()
views_target = "'help-desk': document.getElementById('view-help-desk')"
views_replacement = """'help-desk': document.getElementById('view-help-desk'),
      'partner-dashboard': document.getElementById('view-partner-dashboard')"""

if views_target in js and "'partner-dashboard':" not in js:
    js = js.replace(views_target, views_replacement, 1)

# Add trigger in navigate()
nav_action_target = "if (viewName === 'catalogue') {"
nav_action_replacement = """if (viewName === 'partner-dashboard') {
      this.loadPartnerDashboard();
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
    if (viewName === 'catalogue') {"""

if nav_action_target in js and "viewName === 'partner-dashboard'" not in js:
    js = js.replace(nav_action_target, nav_action_replacement, 1)

# 4. Update setAdminTab to include 'referrals'
old_set_admin_tab = """  setAdminTab(tabId) {
    const tabs = ['enquiries', 'requests', 'orders', 'projects', 'students', 'email-logs', 'payments', 'mentors', 'pricing', 'upi'];
    tabs.forEach(t => {
      const btn = document.getElementById(`tab-adm-${t}`);
      const content = document.getElementById(`adm-tab-${t}`);
      if (btn) btn.className = t === tabId ? 'py-3 tab-active flex items-center gap-1.5 whitespace-nowrap' : 'py-3 text-slate-600 hover:text-slate-900 flex items-center gap-1.5 whitespace-nowrap';
      if (content) content.classList.toggle('hidden', t !== tabId);
    });
    if (window.lucide) window.lucide.createIcons();
  }"""

new_set_admin_tab = """  setAdminTab(tabId) {
    const tabs = ['enquiries', 'requests', 'orders', 'projects', 'students', 'email-logs', 'payments', 'mentors', 'pricing', 'upi', 'support', 'referrals'];
    tabs.forEach(t => {
      const btn = document.getElementById(`tab-adm-${t}`);
      const content = document.getElementById(`adm-tab-${t}`);
      if (btn) btn.className = t === tabId ? 'py-3 tab-active flex items-center gap-1.5 whitespace-nowrap' : 'py-3 text-slate-600 hover:text-slate-900 flex items-center gap-1.5 whitespace-nowrap';
      if (content) content.classList.toggle('hidden', t !== tabId);
    });
    if (tabId === 'referrals') this.loadAdminReferrals();
    if (window.lucide) window.lucide.createIcons();
  }"""

if old_set_admin_tab in js:
    js = js.replace(old_set_admin_tab, new_set_admin_tab)

# 5. In openAuthModal, pre-fill referral code if stored
auth_modal_target = "this.switchAuthMode(mode);"
auth_modal_replacement = """this.switchAuthMode(mode);
    if (mode === 'register') {
      const storedRef = localStorage.getItem('pv_referral_code');
      const refInput = document.getElementById('reg-referral-code');
      const refBadge = document.getElementById('reg-ref-badge');
      if (storedRef && refInput) {
        refInput.value = storedRef;
        if (refBadge) refBadge.classList.remove('hidden');
      }
    }"""

if auth_modal_target in js and 'storedRef' not in js:
    js = js.replace(auth_modal_target, auth_modal_replacement, 1)

# 6. In handleRegister, pass referral_code
reg_payload_target = "password: document.getElementById('reg-password').value"
reg_payload_replacement = """password: document.getElementById('reg-password').value,
      referral_code: document.getElementById('reg-referral-code')?.value.trim() || localStorage.getItem('pv_referral_code') || ''"""

if reg_payload_target in js and 'referral_code:' not in js:
    js = js.replace(reg_payload_target, reg_payload_replacement, 1)

# 7. Insert all Referral Partner & Admin Referral Methods INSIDE ProjectverseApp class
referral_methods = '''

  // =========================================================================
  // REFERRAL PARTNER & 25% COMMISSION SYSTEM METHODS
  // =========================================================================

  async checkAndTrackUrlReferral() {
    try {
      const params = new URLSearchParams(window.location.search);
      const refCode = params.get('ref') || params.get('referral');
      if (!refCode) return;

      const cleanCode = refCode.trim().toUpperCase();
      const valRes = await this.apiRequest(`/api/referrals/validate-code/${cleanCode}`);
      if (valRes && valRes.valid) {
        localStorage.setItem('pv_referral_code', cleanCode);
        localStorage.setItem('pv_referral_time', new Date().toISOString());

        // Track click asynchronously
        this.apiRequest('/api/referrals/track-click', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            referral_code: cleanCode,
            referrer_url: document.referrer || '',
            landing_page: window.location.pathname + window.location.search
          })
        }).catch(err => console.warn('Referral click tracking error:', err));

        this.showToast(`✨ Referral code ${cleanCode} active! Flat 25% partner benefits tracked.`, 'success');
      }
    } catch (e) {
      console.warn('Referral URL check note:', e.message);
    }
  }

  // Partner Modal Controls
  openPartnerModal(mode = 'register') {
    this.switchPartnerAuthMode(mode);
    const modal = document.getElementById('modal-partner-auth');
    if (modal) modal.classList.remove('hidden');
    if (window.lucide) window.lucide.createIcons();
  }

  closePartnerModal() {
    const modal = document.getElementById('modal-partner-auth');
    if (modal) modal.classList.add('hidden');
  }

  switchPartnerAuthMode(mode) {
    const isRegister = mode === 'register';
    const titleEl = document.getElementById('partner-modal-title');
    const regForm = document.getElementById('partner-register-form');
    const loginForm = document.getElementById('partner-login-form');
    const tabRegister = document.getElementById('partner-tab-register');
    const tabLogin = document.getElementById('partner-tab-login');

    if (titleEl) {
      titleEl.innerText = isRegister ? 'Become a Partner (Earn 25%)' : 'Partner Sign In';
    }
    if (regForm) regForm.classList.toggle('hidden', !isRegister);
    if (loginForm) loginForm.classList.toggle('hidden', isRegister);

    if (tabRegister && tabLogin) {
      if (isRegister) {
        tabRegister.className = 'flex-1 py-2 rounded-lg transition-all text-center font-bold bg-white text-slate-900 shadow-sm';
        tabLogin.className = 'flex-1 py-2 rounded-lg transition-all text-center font-medium text-slate-500 hover:text-slate-800';
      } else {
        tabLogin.className = 'flex-1 py-2 rounded-lg transition-all text-center font-bold bg-white text-slate-900 shadow-sm';
        tabRegister.className = 'flex-1 py-2 rounded-lg transition-all text-center font-medium text-slate-500 hover:text-slate-800';
      }
    }
    if (window.lucide) window.lucide.createIcons();
  }

  togglePartnerRegMethod(method) {
    const upiBox = document.getElementById('partner-reg-upi-box');
    const bankBox = document.getElementById('partner-reg-bank-box');
    const isUpi = method === 'UPI';
    if (upiBox) upiBox.classList.toggle('hidden', !isUpi);
    if (bankBox) bankBox.classList.toggle('hidden', isUpi);
  }

  async handlePartnerRegister() {
    const method = document.getElementById('partner-reg-method').value;
    const payload = {
      full_name: document.getElementById('partner-reg-name').value.trim(),
      email: document.getElementById('partner-reg-email').value.trim(),
      mobile: document.getElementById('partner-reg-mobile').value.trim(),
      college_name: document.getElementById('partner-reg-college')?.value.trim() || '',
      city: document.getElementById('partner-reg-city').value.trim(),
      payment_method: method,
      upi_id: method === 'UPI' ? document.getElementById('partner-reg-upi').value.trim() : '',
      bank_account_number: method === 'BANK_TRANSFER' ? document.getElementById('partner-reg-bank-acc').value.trim() : '',
      bank_ifsc: method === 'BANK_TRANSFER' ? document.getElementById('partner-reg-bank-ifsc').value.trim().toUpperCase() : '',
      bank_account_name: method === 'BANK_TRANSFER' ? document.getElementById('partner-reg-bank-name').value.trim() : '',
      password: document.getElementById('partner-reg-password').value
    };

    try {
      const res = await this.apiRequest('/api/referrals/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      this.closePartnerModal();
      this.showToast('Application submitted! Admin will verify and activate your account shortly.', 'success');
    } catch (e) {
      this.showToast(e.message || 'Partner registration failed', 'error');
    }
  }

  async handlePartnerLogin() {
    const email = document.getElementById('partner-login-email').value.trim();
    const password = document.getElementById('partner-login-password').value;

    try {
      const res = await this.apiRequest('/api/referrals/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      });

      this.partnerToken = res.token;
      this.partnerUser = res.partner;
      localStorage.setItem('pv_partner_token', res.token);
      localStorage.setItem('pv_partner_user', JSON.stringify(res.partner));

      this.closePartnerModal();
      this.showToast(`Welcome back, ${res.partner.full_name}!`, 'success');
      this.navigate('partner-dashboard');
    } catch (e) {
      this.showToast(e.message || 'Partner login failed. Make sure your account is approved.', 'error');
    }
  }

  partnerLogout() {
    this.partnerToken = null;
    this.partnerUser = null;
    localStorage.removeItem('pv_partner_token');
    localStorage.removeItem('pv_partner_user');
    this.showToast('Signed out from Partner Dashboard.', 'info');
    this.navigate('home');
  }

  // Dedicated Partner Dashboard Loading
  async loadPartnerDashboard() {
    if (!this.partnerToken) {
      this.openPartnerModal('login');
      this.navigate('home');
      return;
    }

    try {
      const res = await this.apiRequest('/api/referrals/partner/dashboard', {
        headers: { 'Authorization': `Bearer ${this.partnerToken}` }
      });

      const partner = res.partner || {};
      const stats = res.stats || {};
      const commissions = res.commissions || [];
      const payouts = res.payout_requests || [];

      // Render Partner info & badge
      const nameEl = document.getElementById('partner-dash-name');
      const codeEl = document.getElementById('partner-dash-code');
      const linkInput = document.getElementById('partner-dash-link-input');
      const statusBadge = document.getElementById('partner-dash-status-badge');

      if (nameEl) nameEl.innerText = partner.full_name || 'Partner';
      if (codeEl) codeEl.innerText = partner.referral_code || '---';
      if (statusBadge) statusBadge.innerText = partner.status || 'APPROVED';

      const fullUrl = `${window.location.origin}/?ref=${partner.referral_code || ''}`;
      if (linkInput) linkInput.value = fullUrl;

      // Render 6 KPI Cards
      const setTxt = (id, val) => { const el = document.getElementById(id); if (el) el.innerText = val; };
      setTxt('partner-stat-clicks', stats.total_clicks || 0);
      setTxt('partner-stat-registrations', stats.total_registrations || 0);
      setTxt('partner-stat-sales', stats.total_sales || 0);
      setTxt('partner-stat-conversion', `${stats.conversion_rate_percentage || 0}%`);
      setTxt('partner-stat-approved', `₹${Number(stats.approved_balance || 0).toLocaleString('en-IN')}`);
      setTxt('partner-stat-paid', `₹${Number(stats.paid_balance || 0).toLocaleString('en-IN')}`);
      setTxt('partner-stat-total-earned', `₹${Number(stats.total_earnings || 0).toLocaleString('en-IN')} total earned`);

      // Store current approved balance for modal
      this.partnerApprovedBalance = stats.approved_balance || 0;
      this.partnerMinPayout = stats.minimum_payout_amount || 500;

      // Render Commissions Table
      const commTbody = document.getElementById('partner-dash-commissions-tbody');
      if (commTbody) {
        if (commissions.length === 0) {
          commTbody.innerHTML = '<tr><td colspan="6" class="py-6 text-center text-slate-400">No commissions recorded yet. Share your referral link to earn!</td></tr>';
        } else {
          commTbody.innerHTML = commissions.map(c => `
            <tr class="hover:bg-slate-50/80">
              <td class="py-2.5 px-3 text-slate-500">${(c.created_at || '').substring(0, 10)}</td>
              <td class="py-2.5 px-3 font-mono font-bold text-slate-800">${c.order_number}</td>
              <td class="py-2.5 px-3 text-slate-700 font-medium">${c.project_title || c.project_code || 'Academic Project'}</td>
              <td class="py-2.5 px-3 text-right font-mono text-slate-600">₹${Number(c.order_amount).toLocaleString('en-IN')}</td>
              <td class="py-2.5 px-3 text-right font-mono font-black text-emerald-600">+₹${Number(c.commission_amount).toLocaleString('en-IN')}</td>
              <td class="py-2.5 px-3 text-center">
                <span class="px-2 py-0.5 rounded text-[10px] font-bold ${c.status === 'APPROVED' ? 'bg-emerald-100 text-emerald-800' : c.status === 'PAID' ? 'bg-blue-100 text-blue-800' : 'bg-rose-100 text-rose-800'}">
                  ${c.status}
                </span>
              </td>
            </tr>
          `).join('');
        }
      }

      // Render Payouts List
      const payoutsList = document.getElementById('partner-dash-payouts-list');
      if (payoutsList) {
        if (payouts.length === 0) {
          payoutsList.innerHTML = '<p class="text-xs text-slate-400 py-3 text-center">No payout requests yet.</p>';
        } else {
          payoutsList.innerHTML = payouts.map(p => `
            <div class="p-2.5 rounded-xl border border-slate-100 bg-slate-50 flex items-center justify-between text-xs">
              <div>
                <span class="font-bold font-mono text-slate-900">₹${Number(p.amount).toLocaleString('en-IN')}</span>
                <span class="text-[10px] text-slate-400 block">${(p.created_at || '').substring(0, 10)} via ${p.payment_method}</span>
              </div>
              <span class="px-2 py-0.5 rounded text-[10px] font-bold ${p.status === 'PAID' ? 'bg-emerald-100 text-emerald-800' : p.status === 'PENDING' ? 'bg-amber-100 text-amber-800' : 'bg-rose-100 text-rose-800'}">
                ${p.status}
              </span>
            </div>
          `).join('');
        }
      }

      // Populate Payout Profile Form
      const methSelect = document.getElementById('partner-cfg-method');
      const upiInput = document.getElementById('partner-cfg-upi');
      const accInput = document.getElementById('partner-cfg-bank-acc');
      const ifscInput = document.getElementById('partner-cfg-bank-ifsc');
      const nameInput = document.getElementById('partner-cfg-bank-name');

      if (methSelect) methSelect.value = partner.payment_method || 'UPI';
      this.togglePartnerPayoutMethodInputs(partner.payment_method || 'UPI');
      if (upiInput) upiInput.value = partner.upi_id || '';
      if (accInput) accInput.value = partner.bank_account_number || '';
      if (ifscInput) ifscInput.value = partner.bank_ifsc || '';
      if (nameInput) nameInput.value = partner.bank_account_name || '';

      if (window.lucide) window.lucide.createIcons();
    } catch (e) {
      this.showToast('Failed to load partner dashboard: ' + e.message, 'error');
    }
  }

  togglePartnerPayoutMethodInputs(method) {
    const upiBox = document.getElementById('partner-cfg-upi-box');
    const bankBox = document.getElementById('partner-cfg-bank-box');
    const isUpi = method === 'UPI';
    if (upiBox) upiBox.classList.toggle('hidden', !isUpi);
    if (bankBox) bankBox.classList.toggle('hidden', isUpi);
  }

  copyPartnerLink() {
    const input = document.getElementById('partner-dash-link-input');
    if (!input || !input.value) return;
    navigator.clipboard.writeText(input.value).then(() => {
      this.showToast('Referral link copied to clipboard!', 'success');
    }).catch(() => {
      input.select();
      document.execCommand('copy');
      this.showToast('Referral link copied!', 'success');
    });
  }

  sharePartnerLink(platform) {
    const input = document.getElementById('partner-dash-link-input');
    const url = input ? encodeURIComponent(input.value) : encodeURIComponent(window.location.origin);
    const text = encodeURIComponent('Explore 90+ verified final-year BCA, B.Tech, MCA, and M.Tech academic projects on PROJECTVERSE with complete source code & IEEE reports: ');

    let shareUrl = '';
    if (platform === 'whatsapp') {
      shareUrl = `https://api.whatsapp.com/send?text=${text}${url}`;
    } else if (platform === 'telegram') {
      shareUrl = `https://t.me/share/url?url=${url}&text=${text}`;
    } else if (platform === 'twitter') {
      shareUrl = `https://twitter.com/intent/tweet?text=${text}&url=${url}`;
    } else if (platform === 'email') {
      shareUrl = `mailto:?subject=${encodeURIComponent('Verified College Projects on PROJECTVERSE')}&body=${text}${url}`;
    }

    if (shareUrl) window.open(shareUrl, '_blank');
  }

  openPayoutModal() {
    const balEl = document.getElementById('payout-modal-balance');
    const amtInput = document.getElementById('payout-amount-input');
    const modal = document.getElementById('modal-partner-payout');
    if (balEl) balEl.innerText = `₹${Number(this.partnerApprovedBalance || 0).toLocaleString('en-IN')}`;
    if (amtInput) amtInput.value = Math.max(0, Math.floor(this.partnerApprovedBalance || 0));
    if (modal) modal.classList.remove('hidden');
    if (window.lucide) window.lucide.createIcons();
  }

  closePayoutModal() {
    const modal = document.getElementById('modal-partner-payout');
    if (modal) modal.classList.add('hidden');
  }

  async submitPayoutRequest() {
    const amount = parseFloat(document.getElementById('payout-amount-input').value);
    const method = document.getElementById('payout-method-select').value;
    const details = document.getElementById('payout-details-input').value.trim();

    if (!amount || amount <= 0) {
      this.showToast('Please enter a valid payout amount', 'error');
      return;
    }

    try {
      const res = await this.apiRequest('/api/referrals/partner/payout-request', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.partnerToken}`
        },
        body: JSON.stringify({ amount, payment_method: method, payout_details: details })
      });

      this.closePayoutModal();
      this.showToast(res.message || 'Payout request submitted successfully!', 'success');
      this.loadPartnerDashboard();
    } catch (e) {
      this.showToast(e.message || 'Payout request failed', 'error');
    }
  }

  async handleUpdatePartnerProfile() {
    const method = document.getElementById('partner-cfg-method').value;
    const payload = {
      payment_method: method,
      upi_id: method === 'UPI' ? document.getElementById('partner-cfg-upi').value.trim() : '',
      bank_account_number: method === 'BANK_TRANSFER' ? document.getElementById('partner-cfg-bank-acc').value.trim() : '',
      bank_ifsc: method === 'BANK_TRANSFER' ? document.getElementById('partner-cfg-bank-ifsc').value.trim().toUpperCase() : '',
      bank_account_name: method === 'BANK_TRANSFER' ? document.getElementById('partner-cfg-bank-name').value.trim() : ''
    };

    try {
      const res = await this.apiRequest('/api/referrals/partner/profile', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.partnerToken}`
        },
        body: JSON.stringify(payload)
      });
      this.showToast('Payout details updated successfully!', 'success');
    } catch (e) {
      this.showToast(e.message || 'Failed to update payout details', 'error');
    }
  }

  // ==========================================
  // ADMIN REFERRAL MANAGEMENT CENTER
  // ==========================================

  async loadAdminReferrals() {
    try {
      const statsRes = await this.apiRequest('/api/admin/referrals/stats');
      const stats = statsRes.stats || {};

      const setTxt = (id, val) => { const el = document.getElementById(id); if (el) el.innerText = val; };
      setTxt('adm-ref-stat-partners', stats.total_partners || 0);
      setTxt('adm-ref-stat-pending-partners', `${stats.pending_partners || 0} Pending`);
      setTxt('adm-ref-stat-sales', stats.total_conversions || 0);
      setTxt('adm-ref-stat-clicks', `${stats.total_clicks || 0} Clicks`);
      setTxt('adm-ref-stat-earned', `₹${Number(stats.total_commission_earned || 0).toLocaleString('en-IN')}`);
      setTxt('adm-ref-stat-pending-payouts', stats.pending_payout_requests || 0);
      setTxt('adm-ref-stat-pending-payout-amt', `₹${Number(stats.pending_payout_amount || 0).toLocaleString('en-IN')}`);
      setTxt('adm-ref-badge-payouts', stats.pending_payout_requests || 0);
      setTxt('adm-badge-partners', stats.total_partners || 0);

      this.renderAdminPartnersTable();
    } catch (e) {
      console.warn('Admin referral telemetry note:', e.message);
    }
  }

  setAdminReferralSubTab(subTabId) {
    const subtabs = ['partners', 'commissions', 'payouts', 'clicks', 'settings'];
    subtabs.forEach(t => {
      const btn = document.getElementById(`tab-adm-ref-${t}`);
      const pane = document.getElementById(`adm-ref-subtab-${t}`);
      if (btn) btn.className = t === subTabId ? 'py-3 tab-active flex items-center gap-1.5 whitespace-nowrap' : 'py-3 text-slate-600 hover:text-slate-900 flex items-center gap-1.5 whitespace-nowrap';
      if (pane) pane.classList.toggle('hidden', t !== subTabId);
    });

    if (subTabId === 'partners') this.renderAdminPartnersTable();
    else if (subTabId === 'commissions') this.renderAdminCommissionsTable();
    else if (subTabId === 'payouts') this.renderAdminPayoutsTable();
    else if (subTabId === 'clicks') this.renderAdminClicksTable();
    else if (subTabId === 'settings') this.loadAdminReferralSettings();

    if (window.lucide) window.lucide.createIcons();
  }

  async renderAdminPartnersTable() {
    const tbody = document.getElementById('adm-ref-partners-tbody');
    if (!tbody) return;
    const filterStatus = document.getElementById('adm-ref-filter-partner-status')?.value || 'ALL';

    try {
      const url = filterStatus !== 'ALL' ? `/api/admin/referrals/partners?status=${filterStatus}` : '/api/admin/referrals/partners';
      const res = await this.apiRequest(url);
      const partners = res.partners || [];

      if (partners.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" class="py-6 text-center text-slate-400">No referral partners found matching criteria.</td></tr>';
        return;
      }

      tbody.innerHTML = partners.map(p => {
        const isPending = p.status === 'PENDING';
        const isApproved = p.status === 'APPROVED';
        return `
          <tr class="hover:bg-slate-50/80">
            <td class="py-2.5 px-3">
              <span class="font-bold text-slate-900 block">${p.full_name}</span>
              <span class="text-[10px] text-slate-400">${p.city || 'India'} ${p.college_name ? '• ' + p.college_name : ''}</span>
            </td>
            <td class="py-2.5 px-3">
              <span class="text-slate-800 block">${p.email}</span>
              <span class="text-[10px] text-slate-500 font-mono">${p.mobile}</span>
            </td>
            <td class="py-2.5 px-3 text-xs">
              <span class="font-semibold text-slate-700 block">${p.payment_method}</span>
              <span class="text-[10px] font-mono text-slate-500">${p.upi_id || p.bank_account_number || 'Not provided'}</span>
            </td>
            <td class="py-2.5 px-3">
              <span class="px-2 py-0.5 rounded font-mono font-bold text-[11px] bg-purple-50 text-brand-purple border border-purple-200">
                ${p.referral_code || 'Pending'}
              </span>
            </td>
            <td class="py-2.5 px-3 text-right">
              <span class="font-bold text-slate-800 block">${p.total_sales || 0} sales</span>
              <span class="text-[10px] text-emerald-600 font-mono font-semibold">₹${Number(p.total_earned || 0).toLocaleString('en-IN')}</span>
            </td>
            <td class="py-2.5 px-3 text-center">
              <span class="px-2 py-0.5 rounded text-[10px] font-bold ${isApproved ? 'bg-emerald-100 text-emerald-800' : isPending ? 'bg-amber-100 text-amber-800' : 'bg-rose-100 text-rose-800'}">
                ${p.status}
              </span>
            </td>
            <td class="py-2.5 px-3 text-right">
              <div class="flex items-center justify-end gap-1.5">
                ${isPending ? `
                  <button onclick="app.updatePartnerStatus(${p.id}, 'APPROVED')" class="px-2.5 py-1 bg-emerald-600 hover:bg-emerald-700 text-white rounded text-[10px] font-bold shadow-sm">
                    Approve
                  </button>
                  <button onclick="app.updatePartnerStatus(${p.id}, 'REJECTED')" class="px-2.5 py-1 bg-rose-600 hover:bg-rose-700 text-white rounded text-[10px] font-bold shadow-sm">
                    Reject
                  </button>
                ` : isApproved ? `
                  <button onclick="app.updatePartnerStatus(${p.id}, 'SUSPENDED')" class="px-2 py-1 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded text-[10px] font-semibold">
                    Suspend
                  </button>
                ` : `
                  <button onclick="app.updatePartnerStatus(${p.id}, 'APPROVED')" class="px-2 py-1 bg-emerald-50 hover:bg-emerald-100 text-emerald-800 rounded text-[10px] font-bold">
                    Re-Activate
                  </button>
                `}
              </div>
            </td>
          </tr>
        `;
      }).join('');

      if (window.lucide) window.lucide.createIcons();
    } catch (e) {
      tbody.innerHTML = `<tr><td colspan="7" class="py-4 text-center text-xs text-rose-500">Failed to load partners: ${e.message}</td></tr>`;
    }
  }

  async updatePartnerStatus(id, newStatus) {
    try {
      const res = await this.apiRequest(`/api/admin/referrals/partners/${id}/status`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status: newStatus })
      });
      this.showToast(`Partner status updated to ${newStatus}`, 'success');
      this.loadAdminReferrals();
    } catch (e) {
      this.showToast('Failed to update status: ' + e.message, 'error');
    }
  }

  async renderAdminCommissionsTable() {
    const tbody = document.getElementById('adm-ref-commissions-tbody');
    if (!tbody) return;
    const filterStatus = document.getElementById('adm-ref-filter-comm-status')?.value || 'ALL';

    try {
      const url = filterStatus !== 'ALL' ? `/api/admin/referrals/commissions?status=${filterStatus}` : '/api/admin/referrals/commissions';
      const res = await this.apiRequest(url);
      const commissions = res.commissions || [];

      if (commissions.length === 0) {
        tbody.innerHTML = '<tr><td colspan="8" class="py-6 text-center text-slate-400">No commissions matching filter.</td></tr>';
        return;
      }

      tbody.innerHTML = commissions.map(c => `
        <tr class="hover:bg-slate-50/80">
          <td class="py-2.5 px-3 text-slate-500">${(c.created_at || '').substring(0, 10)}</td>
          <td class="py-2.5 px-3 font-mono font-bold text-slate-900">${c.order_number}</td>
          <td class="py-2.5 px-3">
            <span class="font-bold text-slate-900 block">${c.partner_name}</span>
            <span class="text-[10px] text-slate-400">${c.partner_email}</span>
          </td>
          <td class="py-2.5 px-3">
            <span class="font-semibold text-slate-800 block">${c.project_title || c.project_code}</span>
            <span class="text-[10px] text-slate-500">${c.student_name || 'Student'}</span>
          </td>
          <td class="py-2.5 px-3 text-right font-mono text-slate-600">₹${Number(c.order_amount).toLocaleString('en-IN')}</td>
          <td class="py-2.5 px-3 text-right font-mono font-black text-emerald-600">₹${Number(c.commission_amount).toLocaleString('en-IN')}</td>
          <td class="py-2.5 px-3 text-center">
            <span class="px-2 py-0.5 rounded text-[10px] font-bold ${c.status === 'APPROVED' ? 'bg-emerald-100 text-emerald-800' : c.status === 'PAID' ? 'bg-blue-100 text-blue-800' : 'bg-rose-100 text-rose-800'}">
              ${c.status}
            </span>
          </td>
          <td class="py-2.5 px-3 text-right">
            ${c.status === 'APPROVED' ? `
              <button onclick="app.openAdminReverseCommissionModal(${c.id})" class="px-2 py-1 bg-rose-50 hover:bg-rose-100 text-rose-700 rounded text-[10px] font-bold">
                Reverse
              </button>
            ` : '<span class="text-slate-400 text-[10px]">—</span>'}
          </td>
        </tr>
      `).join('');

      if (window.lucide) window.lucide.createIcons();
    } catch (e) {
      tbody.innerHTML = `<tr><td colspan="8" class="py-4 text-center text-xs text-rose-500">Failed to load commissions: ${e.message}</td></tr>`;
    }
  }

  openAdminReverseCommissionModal(id) {
    document.getElementById('adm-rev-comm-id').value = id;
    const modal = document.getElementById('modal-admin-reverse-commission');
    if (modal) modal.classList.remove('hidden');
  }

  closeAdminReverseCommissionModal() {
    const modal = document.getElementById('modal-admin-reverse-commission');
    if (modal) modal.classList.add('hidden');
  }

  async submitAdminReverseCommission() {
    const id = document.getElementById('adm-rev-comm-id').value;
    const notes = document.getElementById('adm-rev-notes').value.trim();

    try {
      await this.apiRequest(`/api/admin/referrals/commissions/${id}/status`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status: 'REVERSED', notes })
      });
      this.closeAdminReverseCommissionModal();
      this.showToast('Commission reversed successfully.', 'success');
      this.renderAdminCommissionsTable();
      this.loadAdminReferrals();
    } catch (e) {
      this.showToast('Failed to reverse commission: ' + e.message, 'error');
    }
  }

  async renderAdminPayoutsTable() {
    const tbody = document.getElementById('adm-ref-payouts-tbody');
    if (!tbody) return;
    const filterStatus = document.getElementById('adm-ref-filter-payout-status')?.value || 'ALL';

    try {
      const url = filterStatus !== 'ALL' ? `/api/admin/referrals/payout-requests?status=${filterStatus}` : '/api/admin/referrals/payout-requests';
      const res = await this.apiRequest(url);
      const payouts = res.payout_requests || [];

      if (payouts.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" class="py-6 text-center text-slate-400">No payout requests matching filter.</td></tr>';
        return;
      }

      tbody.innerHTML = payouts.map(p => {
        const isPending = p.status === 'PENDING';
        return `
          <tr class="hover:bg-slate-50/80">
            <td class="py-2.5 px-3 text-slate-500">${(p.created_at || '').substring(0, 10)}</td>
            <td class="py-2.5 px-3 font-mono font-bold text-slate-900">${p.request_number}</td>
            <td class="py-2.5 px-3">
              <span class="font-bold text-slate-900 block">${p.partner_name}</span>
              <span class="text-[10px] text-slate-400">${p.partner_email}</span>
            </td>
            <td class="py-2.5 px-3 text-xs">
              <span class="font-semibold text-slate-700 block">${p.payment_method}</span>
              <span class="text-[10px] font-mono text-slate-500">${p.payout_details}</span>
            </td>
            <td class="py-2.5 px-3 text-right font-mono font-black text-slate-900">₹${Number(p.amount).toLocaleString('en-IN')}</td>
            <td class="py-2.5 px-3 text-center">
              <span class="px-2 py-0.5 rounded text-[10px] font-bold ${p.status === 'PAID' ? 'bg-emerald-100 text-emerald-800' : isPending ? 'bg-amber-100 text-amber-800' : 'bg-rose-100 text-rose-800'}">
                ${p.status}
              </span>
            </td>
            <td class="py-2.5 px-3 text-right">
              ${isPending ? `
                <button onclick="app.openAdminProcessPayoutModal(${p.id}, '${p.partner_name.replace(/'/g, "\\'")}', ${p.amount}, '${p.payment_method}', '${p.payout_details.replace(/'/g, "\\'")}')" class="px-3 py-1 bg-emerald-600 hover:bg-emerald-700 text-white rounded text-[10px] font-bold shadow-sm">
                  Process & Settle
                </button>
              ` : `
                <span class="text-[10px] font-mono text-slate-500">${p.settlement_reference || 'Settled'}</span>
              `}
            </td>
          </tr>
        `;
      }).join('');

      if (window.lucide) window.lucide.createIcons();
    } catch (e) {
      tbody.innerHTML = `<tr><td colspan="7" class="py-4 text-center text-xs text-rose-500">Failed to load payouts: ${e.message}</td></tr>`;
    }
  }

  openAdminProcessPayoutModal(id, partnerName, amount, method, details) {
    document.getElementById('adm-payout-id').value = id;
    document.getElementById('adm-payout-partner-name').innerText = partnerName;
    document.getElementById('adm-payout-amount').innerText = `₹${Number(amount).toLocaleString('en-IN')}`;
    document.getElementById('adm-payout-dest').innerText = `${method}: ${details}`;
    document.getElementById('adm-payout-utr').value = `BANK-UTR-${Date.now().toString().slice(-8)}`;

    const modal = document.getElementById('modal-admin-process-payout');
    if (modal) modal.classList.remove('hidden');
  }

  closeAdminProcessPayoutModal() {
    const modal = document.getElementById('modal-admin-process-payout');
    if (modal) modal.classList.add('hidden');
  }

  toggleAdminPayoutFields(action) {
    const utrBox = document.getElementById('adm-payout-utr-box');
    if (utrBox) utrBox.classList.toggle('hidden', action !== 'approve');
  }

  async submitAdminProcessPayout() {
    const id = document.getElementById('adm-payout-id').value;
    const action = document.getElementById('adm-payout-action').value;
    const utr = document.getElementById('adm-payout-utr').value.trim();
    const notes = document.getElementById('adm-payout-notes').value.trim();

    if (action === 'approve' && !utr) {
      this.showToast('Please enter the Bank UTR / Reference number for audit trail.', 'error');
      return;
    }

    try {
      const res = await this.apiRequest(`/api/admin/referrals/payout-requests/${id}/process`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ action, utr_reference: utr, notes })
      });

      this.closeAdminProcessPayoutModal();
      this.showToast(res.message || 'Payout processed successfully!', 'success');
      this.renderAdminPayoutsTable();
      this.loadAdminReferrals();
    } catch (e) {
      this.showToast('Failed to process payout: ' + e.message, 'error');
    }
  }

  async renderAdminClicksTable() {
    const tbody = document.getElementById('adm-ref-clicks-tbody');
    if (!tbody) return;

    try {
      const res = await this.apiRequest('/api/admin/referrals/clicks?limit=50');
      const clicks = res.clicks || [];

      if (clicks.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5" class="py-6 text-center text-slate-400">No clicks recorded yet.</td></tr>';
        return;
      }

      tbody.innerHTML = clicks.map(c => `
        <tr class="hover:bg-slate-50/80">
          <td class="py-2.5 px-3 text-slate-500">${(c.created_at || '').substring(0, 19)}</td>
          <td class="py-2.5 px-3">
            <span class="px-2 py-0.5 rounded font-mono font-bold text-[11px] bg-purple-50 text-brand-purple border border-purple-200">
              ${c.referral_code}
            </span>
          </td>
          <td class="py-2.5 px-3 font-semibold text-slate-800">${c.partner_name || 'Partner'}</td>
          <td class="py-2.5 px-3 text-[11px] font-mono text-slate-500">${c.ip_address || '---'}</td>
          <td class="py-2.5 px-3 text-slate-600 truncate max-w-xs" title="${c.referrer_url || 'Direct'}">${c.referrer_url || 'Direct Visit'}</td>
        </tr>
      `).join('');
    } catch (e) {
      tbody.innerHTML = `<tr><td colspan="5" class="py-4 text-center text-xs text-rose-500">Failed to load clicks: ${e.message}</td></tr>`;
    }
  }

  async loadAdminReferralSettings() {
    try {
      const res = await this.apiRequest('/api/admin/referrals/settings');
      const s = res.settings || {};

      const setVal = (id, val) => { const el = document.getElementById(id); if (el) el.value = val; };
      setVal('adm-ref-cfg-rate', s.commission_rate_percentage || 25.0);
      setVal('adm-ref-cfg-window', s.attribution_window_days || 30);
      setVal('adm-ref-cfg-minpayout', s.minimum_payout_amount || 500.0);

      const autoApproveEl = document.getElementById('adm-ref-cfg-autoapprove');
      if (autoApproveEl) autoApproveEl.checked = s.auto_approve_partners === '1';

      const excludeTaxEl = document.getElementById('adm-ref-cfg-excludetax');
      if (excludeTaxEl) excludeTaxEl.checked = s.exclude_tax_from_commission !== '0';
    } catch (e) {
      console.warn('Referral settings load note:', e.message);
    }
  }

  async saveReferralSettings() {
    const payload = {
      commission_rate_percentage: parseFloat(document.getElementById('adm-ref-cfg-rate').value),
      attribution_window_days: parseInt(document.getElementById('adm-ref-cfg-window').value),
      minimum_payout_amount: parseFloat(document.getElementById('adm-ref-cfg-minpayout').value),
      auto_approve_partners: document.getElementById('adm-ref-cfg-autoapprove').checked,
      exclude_tax_from_commission: document.getElementById('adm-ref-cfg-excludetax').checked
    };

    try {
      const res = await this.apiRequest('/api/admin/referrals/settings', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      this.showToast('Affiliate engine settings updated successfully!', 'success');
    } catch (e) {
      this.showToast('Failed to update settings: ' + e.message, 'error');
    }
  }

  exportReferralsCsv() {
    const token = this.token;
    if (!token) return;
    window.open(`/api/admin/referrals/export?token=${token}`, '_blank');
  }
'''

# Find the last closing brace of the ProjectverseApp class
app_inst_target = """// Global Application Instance
let app;
window.addEventListener('DOMContentLoaded', () => {
  app = new ProjectverseApp();
  window.app = app;
});"""

parts = js.split(app_inst_target)
if len(parts) == 2:
    class_body = parts[0].rstrip()
    last_brace_idx = class_body.rfind('}')
    new_class_body = class_body[:last_brace_idx] + '\n\n' + referral_methods + '\n\n}'
    js = new_class_body + '\n\n' + app_inst_target + '\n'
else:
    print("Warning: could not split by app_inst_target")

with open('static/js/app.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("patch_referrals_app_js.py completed successfully!")
