import re

with open('static/js/app.js', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update loadStudentDashboard to render Enquiries, Requests, Orders, and Profile
old_load_student_dash = '''  async loadStudentDashboard() {
    if (!this.user) {
      this.navigate('home');
      this.openAuthModal('login');
      return;
    }

    try {
      const data = await this.apiRequest('/api/student/dashboard');

      // Populate User Banner
      document.getElementById('dash-user-name').innerText = data.student.name;
      document.getElementById('dash-user-college').innerText = `${data.student.college_name || 'Student'} • ${data.student.course || 'B.Tech'}`;
      document.getElementById('dash-user-email').innerText = data.student.email;
      document.getElementById('dash-user-initial').innerText = (data.student.name || 'S')[0].toUpperCase();
      document.getElementById('dash-user-role').innerText = data.student.role.toUpperCase();

      // Render Enrolled Projects Cards
      const container = document.getElementById('dash-enrolled-container');
      const enrollments = data.enrollments || [];
      document.getElementById('dash-enrolled-count').innerText = enrollments.length;'''

new_load_student_dash = '''  async loadStudentDashboard() {
    if (!this.user) {
      this.navigate('home');
      this.openAuthModal('login');
      return;
    }

    try {
      const data = await this.apiRequest('/api/student/dashboard');

      // Populate User Banner
      document.getElementById('dash-user-name').innerText = data.student.name;
      document.getElementById('dash-user-college').innerText = `${data.student.college_name || 'Academic Scholar'} • ${data.student.course || 'Degree Program'}`;
      document.getElementById('dash-user-email').innerText = data.student.email;
      document.getElementById('dash-user-initial').innerText = (data.student.name || 'S')[0].toUpperCase();
      document.getElementById('dash-user-role').innerText = data.student.role.toUpperCase();

      // Populate Profile Tab Form Fields
      const pName = document.getElementById('prof-name');
      const pPhone = document.getElementById('prof-phone');
      const pCollege = document.getElementById('prof-college');
      const pCourse = document.getElementById('prof-course');
      if (pName) pName.value = data.student.name || '';
      if (pPhone) pPhone.value = data.student.phone || '';
      if (pCollege) pCollege.value = data.student.college_name || '';
      if (pCourse) pCourse.value = data.student.course || '';

      // 1. Render Enquiries
      const enquiriesContainer = document.getElementById('dash-enquiries-container');
      const enquiries = data.enquiries || [];
      const enqCountEl = document.getElementById('dash-enquiries-count');
      if (enqCountEl) enqCountEl.innerText = enquiries.length;

      if (enquiriesContainer) {
        if (enquiries.length === 0) {
          enquiriesContainer.innerHTML = `<div class="p-8 bg-slate-50 rounded-2xl border border-slate-200 text-center text-xs text-slate-500">You haven't submitted any project enquiries yet. Browse 90 projects and click 'Enquire' on any project!</div>`;
        } else {
          enquiriesContainer.innerHTML = enquiries.map(e => `
            <div class="p-4 bg-slate-50 rounded-2xl border border-slate-200 space-y-2">
              <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-2 border-b border-slate-200">
                <div>
                  <span class="px-2 py-0.5 rounded font-mono text-[10px] font-black bg-cyan-100 text-cyan-800">${e.project_code}</span>
                  <span class="font-bold text-slate-900 text-sm ml-1.5">${e.project_title}</span>
                </div>
                <div class="flex items-center gap-2">
                  <span class="font-mono text-xs text-slate-500">${e.enquiry_number}</span>
                  <span class="px-2 py-0.5 rounded text-[10px] font-bold ${e.status === 'CONVERTED' ? 'bg-emerald-100 text-emerald-800' : 'bg-amber-100 text-amber-800'}">${e.status}</span>
                </div>
              </div>
              <p class="text-xs text-slate-600">${e.message}</p>
              <div class="flex items-center justify-between pt-1 text-[11px] text-slate-400">
                <span>Submitted: ${(e.created_at || '').substring(0, 16)}</span>
                <a href="https://wa.me/918431712924?text=${encodeURIComponent(`Hello Projectverse, following up on enquiry ${e.enquiry_number} for ${e.project_code}`)}" target="_blank" class="text-emerald-600 font-semibold hover:underline flex items-center gap-1">
                  Follow up on WhatsApp →
                </a>
              </div>
            </div>
          `).join('');
        }
      }

      // 2. Render Requests
      const requestsContainer = document.getElementById('dash-requests-container');
      const requests = data.requests || [];
      const reqCountEl = document.getElementById('dash-requests-count');
      if (reqCountEl) reqCountEl.innerText = requests.length;

      if (requestsContainer) {
        if (requests.length === 0) {
          requestsContainer.innerHTML = `<div class="p-8 bg-slate-50 rounded-2xl border border-slate-200 text-center text-xs text-slate-500">No capstone enrollment requests submitted yet.</div>`;
        } else {
          requestsContainer.innerHTML = requests.map(r => `
            <div class="p-4 bg-slate-50 rounded-2xl border border-slate-200 space-y-3">
              <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-2 border-b border-slate-200">
                <div>
                  <span class="px-2 py-0.5 rounded font-mono text-[10px] font-black bg-purple-100 text-purple-800">${r.project_code}</span>
                  <span class="font-bold text-slate-900 text-sm ml-1.5">${r.project_title}</span>
                </div>
                <div class="flex items-center gap-2">
                  <span class="font-mono text-xs text-slate-500">${r.request_number}</span>
                  <span class="px-2 py-0.5 rounded text-[10px] font-bold ${r.status === 'APPROVED' ? 'bg-emerald-100 text-emerald-800' : 'bg-amber-100 text-amber-800'}">${r.status}</span>
                </div>
              </div>
              <div class="grid grid-cols-1 sm:grid-cols-3 gap-2 text-xs">
                <div><span class="text-slate-400">Mode:</span> <span class="font-semibold text-slate-700">${r.team_mode || 'Individual'}</span></div>
                <div><span class="text-slate-400">Deadline:</span> <span class="font-semibold text-slate-700">${r.deadline || '8 Weeks'}</span></div>
                <div><span class="text-slate-400">Mentor:</span> <span class="font-semibold text-purple-700">${r.mentor_name || 'Assigned after approval'}</span></div>
              </div>
              <!-- Progress Bar -->
              <div>
                <div class="flex items-center justify-between text-xs mb-1">
                  <span class="font-bold text-slate-700">Project Progress</span>
                  <span class="font-mono font-bold text-brand-purple">${r.progress_percentage || 0}%</span>
                </div>
                <div class="w-full bg-slate-200 h-2 rounded-full overflow-hidden">
                  <div class="bg-gradient-to-r from-brand-purple to-cyan-500 h-full rounded-full transition-all duration-500" style="width: ${r.progress_percentage || 0}%"></div>
                </div>
              </div>
            </div>
          `).join('');
        }
      }

      // 3. Render Orders
      const ordersContainer = document.getElementById('dash-orders-container');
      const orders = data.orders || [];
      const ordCountEl = document.getElementById('dash-orders-count');
      if (ordCountEl) ordCountEl.innerText = orders.length;

      if (ordersContainer) {
        if (orders.length === 0) {
          ordersContainer.innerHTML = `<div class="p-8 bg-slate-50 rounded-2xl border border-slate-200 text-center text-xs text-slate-500">No project purchases or UPI orders found.</div>`;
        } else {
          ordersContainer.innerHTML = `
            <table class="w-full text-left text-xs">
              <thead class="bg-slate-50 text-slate-600 font-semibold uppercase text-[10px] border-b border-slate-200">
                <tr>
                  <th class="py-3 px-3">Order Number</th>
                  <th class="py-3 px-3">Project Title</th>
                  <th class="py-3 px-3">Amount</th>
                  <th class="py-3 px-3">UTR Reference</th>
                  <th class="py-3 px-3">Status</th>
                  <th class="py-3 px-3 text-right">Tax Invoice</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-100 font-mono">
                ${orders.map(o => `
                  <tr>
                    <td class="py-3 px-3 font-bold text-slate-900">${o.order_number}</td>
                    <td class="py-3 px-3 font-sans font-medium text-slate-800">${o.project_code} - ${o.title}</td>
                    <td class="py-3 px-3 font-bold text-slate-900">₹${(o.amount || 0).toLocaleString()}</td>
                    <td class="py-3 px-3 text-slate-600">${o.utr_reference || '—'}</td>
                    <td class="py-3 px-3">
                      <span class="px-2 py-0.5 rounded text-[10px] font-bold ${o.order_status === 'approved' ? 'bg-emerald-100 text-emerald-800' : 'bg-amber-100 text-amber-800'}">
                        ${(o.order_status || 'PENDING').toUpperCase()}
                      </span>
                    </td>
                    <td class="py-3 px-3 text-right">
                      ${o.invoice_number ? `
                        <a href="/api/invoices/${o.invoice_number}" target="_blank" class="px-2.5 py-1 rounded bg-purple-50 hover:bg-purple-100 text-brand-purple font-bold text-xs border border-purple-200 inline-flex items-center gap-1 font-sans">
                          <i data-lucide="file-text" class="w-3.5 h-3.5"></i> ${o.invoice_number}
                        </a>
                      ` : '<span class="text-slate-400 font-sans text-xs">Generated upon verification</span>'}
                    </td>
                  </tr>
                `).join('')}
              </tbody>
            </table>
          `;
        }
      }

      if (window.lucide) window.lucide.createIcons();
      return;
    } catch (e) {
      this.showToast('Could not load student dashboard', 'error');
    }
  }

  /* legacy dashboard stub */
  legacyLoadStudentDashboard() {
'''

if old_load_student_dash in content:
    content = content.replace(old_load_student_dash, new_load_student_dash)
    print("Replaced loadStudentDashboard with real Enquiries, Requests, Orders, Invoices, and Profile.")

# 2. Update refreshAdminData
old_refresh_admin = '''    // Update Telemetry Metrics
    document.getElementById('admin-stat-projects').innerText = stats.total_projects;
    document.getElementById('admin-stat-students').innerText = stats.total_students;
    document.getElementById('admin-stat-pending').innerText = stats.pending_payments;
    document.getElementById('admin-stat-revenue').innerText = `₹${stats.verified_revenue.toLocaleString()}`;
    
    const genuineSub = document.getElementById('admin-stat-genuine-sub');
    if (genuineSub) {
      genuineSub.innerText = `${stats.genuine_students_count || 1} Genuine (${stats.demo_students_count || 0} Demo)`;
    }

    // Update Demo Controller Banner
    this.updateDemoModeUI(stats.demo_mode);

    // Render Admin Views
    this.renderAdminProjectsTable();
    this.renderAdminEnrollments();
    this.renderAdminStudents();
    this.renderAdminMentors();
    this.renderAdminPayments();
    this.renderAdminPricing();
    this.renderAdminImages();
    this.populateUpiSettings();
    this.populateSupportSettings();'''

new_refresh_admin = '''    // Update Telemetry Metrics
    if (document.getElementById('admin-stat-projects')) document.getElementById('admin-stat-projects').innerText = stats.total_projects || 90;
    if (document.getElementById('admin-stat-students')) document.getElementById('admin-stat-students').innerText = stats.total_students || 0;
    if (document.getElementById('admin-stat-enquiries')) document.getElementById('admin-stat-enquiries').innerText = stats.new_enquiries || 0;
    if (document.getElementById('admin-stat-requests')) document.getElementById('admin-stat-requests').innerText = stats.pending_requests || 0;
    if (document.getElementById('admin-stat-pending')) document.getElementById('admin-stat-pending').innerText = stats.pending_payments || 0;
    if (document.getElementById('admin-stat-revenue')) document.getElementById('admin-stat-revenue').innerText = `₹${(stats.verified_revenue || 0).toLocaleString()}`;

    // Render All Admin Views
    this.fetchAdminNotifications();
    this.renderAdminEnquiries();
    this.renderAdminRequests();
    this.renderAdminOrders();
    this.renderAdminProjectsTable();
    this.renderAdminStudents();
    this.renderAdminEmailLogs();
    this.renderAdminMentors();
    this.renderAdminPayments();
    this.renderAdminPricing();
    this.populateUpiSettings();
    this.populateSupportSettings();'''

if old_refresh_admin in content:
    content = content.replace(old_refresh_admin, new_refresh_admin)
    print("Updated refreshAdminData for production telemetry and new admin views.")

# 3. Append the new production methods at the end of ProjectVerseApp class
methods_to_append = '''
  // ==========================================
  // PROJECT ENQUIRY (CUSTOMER WORKFLOW)
  // ==========================================

  openProjectEnquiryModal(codeOrId) {
    const proj = (this.allProjects || []).find(p => p.project_code === codeOrId || p.id == codeOrId);
    if (!proj) return;

    this.selectedProject = proj;
    const titleEl = document.getElementById('enq-modal-project-title');
    const codeEl = document.getElementById('enq-modal-project-code');
    const priceEl = document.getElementById('enq-modal-project-price');
    const idEl = document.getElementById('enq-modal-project-id');

    if (titleEl) titleEl.innerText = proj.title;
    if (codeEl) codeEl.innerText = `${proj.project_code} • ${proj.academic_level}`;
    if (priceEl) priceEl.innerText = `Starting ₹${proj.price.toLocaleString()}`;
    if (idEl) idEl.value = proj.id;

    if (this.user) {
      const nameInput = document.getElementById('enq-name');
      const emailInput = document.getElementById('enq-email');
      const phoneInput = document.getElementById('enq-phone');
      const collegeInput = document.getElementById('enq-college');
      const courseInput = document.getElementById('enq-course');

      if (nameInput) nameInput.value = this.user.name || '';
      if (emailInput) emailInput.value = this.user.email || '';
      if (phoneInput) phoneInput.value = this.user.phone || '';
      if (collegeInput) collegeInput.value = this.user.college_name || '';
      if (courseInput) courseInput.value = this.user.course || '';
    }

    const modal = document.getElementById('modal-project-enquiry');
    if (modal) modal.classList.remove('hidden');
    if (window.lucide) window.lucide.createIcons();
  }

  closeProjectEnquiryModal() {
    const modal = document.getElementById('modal-project-enquiry');
    if (modal) modal.classList.add('hidden');
  }

  openProjectEnquiryFromModal() {
    if (!this.selectedProject) return;
    this.closeProjectDetails();
    this.openProjectEnquiryModal(this.selectedProject.project_code);
  }

  async submitProjectEnquiry() {
    const name = document.getElementById('enq-name').value.trim();
    const email = document.getElementById('enq-email').value.trim();
    const phone = document.getElementById('enq-phone').value.trim();
    const college = document.getElementById('enq-college').value.trim();
    const course = document.getElementById('enq-course').value.trim();
    const tech = document.getElementById('enq-tech').value.trim();
    const message = document.getElementById('enq-message').value.trim();
    const projectId = document.getElementById('enq-modal-project-id').value;

    const btn = document.getElementById('enq-submit-btn');
    btn.disabled = true;
    btn.innerText = 'Submitting Enquiry...';

    try {
      const res = await this.apiRequest('/api/enquiries/create', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          customer_name: name,
          customer_email: email,
          customer_phone: phone,
          college_name: college,
          course: course,
          project_id: projectId ? parseInt(projectId) : null,
          technology: tech || 'General',
          message: message
        })
      });

      this.closeProjectEnquiryModal();
      this.showToast(res.message || `Enquiry ${res.enquiry_number} submitted! Notification emailed to academic owner.`, 'success');

      document.getElementById('enq-message').value = '';

      if (this.user) {
        this.loadStudentDashboard();
      }
    } catch (e) {
      this.showToast('Failed to submit enquiry: ' + e.message, 'error');
    } finally {
      btn.disabled = false;
      btn.innerHTML = `<i data-lucide="send" class="w-4 h-4"></i> Submit Enquiry for Immediate Response`;
      if (window.lucide) window.lucide.createIcons();
    }
  }

  // ==========================================
  // ADMIN NOTIFICATION CENTRE
  // ==========================================

  toggleAdminNotifDropdown() {
    const dd = document.getElementById('adm-notif-dropdown');
    if (dd) dd.classList.toggle('hidden');
  }

  async fetchAdminNotifications() {
    try {
      const res = await this.apiRequest('/api/admin/notifications');
      const notifs = res.notifications || [];
      const unreadCount = res.unread_count || 0;

      const badge = document.getElementById('adm-notif-count');
      if (badge) {
        badge.innerText = unreadCount;
        badge.classList.toggle('hidden', unreadCount === 0);
      }

      const list = document.getElementById('adm-notif-list');
      if (list) {
        if (notifs.length === 0) {
          list.innerHTML = `<p class="text-slate-400 text-center py-2 text-xs">No notifications</p>`;
        } else {
          list.innerHTML = notifs.slice(0, 10).map(n => `
            <div class="p-2 rounded-xl ${n.is_read ? 'bg-slate-50' : 'bg-purple-50/80 border border-purple-200'} space-y-1 cursor-pointer" onclick="app.markAdminNotifRead(${n.id})">
              <div class="flex items-center justify-between">
                <span class="font-bold text-[11px] text-slate-900">${n.title}</span>
                <span class="text-[9px] text-slate-400 font-mono">${(n.created_at || '').substring(11, 16)}</span>
              </div>
              <p class="text-[11px] text-slate-600 line-clamp-2">${n.message}</p>
            </div>
          `).join('');
        }
      }
    } catch (e) {}
  }

  async markAdminNotifRead(id) {
    try {
      await this.apiRequest(`/api/admin/notifications/${id}/read`, { method: 'POST' });
      this.fetchAdminNotifications();
    } catch (e) {}
  }

  async markAllNotificationsRead() {
    try {
      await this.apiRequest('/api/admin/notifications/read-all', { method: 'POST' });
      this.fetchAdminNotifications();
      this.showToast('All notifications marked as read', 'success');
    } catch (e) {}
  }

  // ==========================================
  // ADMIN ENQUIRIES MANAGEMENT
  // ==========================================

  async renderAdminEnquiries() {
    const tbody = document.getElementById('adm-enquiries-table-body');
    if (!tbody) return;

    const statusFilter = document.getElementById('adm-enquiry-status-filter')?.value || 'ALL';
    const q = document.getElementById('adm-enquiry-search')?.value.trim().toLowerCase() || '';

    try {
      const url = `/api/admin/enquiries${statusFilter !== 'ALL' ? '?status=' + statusFilter : ''}`;
      const res = await this.apiRequest(url);
      let enquiries = res.enquiries || [];

      if (q) {
        enquiries = enquiries.filter(e => 
          (e.customer_name || '').toLowerCase().includes(q) ||
          (e.customer_phone || '').includes(q) ||
          (e.project_title || '').toLowerCase().includes(q) ||
          (e.project_code || '').toLowerCase().includes(q) ||
          (e.enquiry_number || '').toLowerCase().includes(q)
        );
      }

      const badge = document.getElementById('adm-badge-enquiries');
      if (badge) badge.innerText = enquiries.length;
      const kpiEnq = document.getElementById('admin-stat-enquiries');
      if (kpiEnq) kpiEnq.innerText = res.new_count !== undefined ? res.new_count : enquiries.filter(e => e.status === 'NEW').length;

      if (enquiries.length === 0) {
        tbody.innerHTML = `<tr><td colspan="8" class="py-8 text-center text-xs text-slate-500">No enquiries found for current filter.</td></tr>`;
        return;
      }

      tbody.innerHTML = enquiries.map(e => {
        const waMsg = `Hello ${e.customer_name}, regarding your Projectverse enquiry (${e.enquiry_number}) for project ${e.project_code} - ${e.project_title}: `;
        const waUrl = `https://wa.me/${(e.customer_phone || '').replace(/[^0-9]/g, '')}?text=${encodeURIComponent(waMsg)}`;
        const statusColors = {
          'NEW': 'bg-amber-100 text-amber-900 border-amber-300',
          'CONTACTED': 'bg-blue-100 text-blue-900 border-blue-300',
          'IN_DISCUSSION': 'bg-purple-100 text-purple-900 border-purple-300',
          'CONVERTED': 'bg-emerald-100 text-emerald-900 border-emerald-300',
          'CLOSED': 'bg-slate-100 text-slate-800 border-slate-300'
        };

        return `
          <tr class="hover:bg-slate-50/80">
            <td class="py-3 px-3 font-mono">
              <span class="font-bold text-slate-900 block">${e.enquiry_number}</span>
              <span class="text-[10px] text-slate-400">${(e.created_at || '').substring(0, 16)}</span>
            </td>
            <td class="py-3 px-3">
              <span class="font-bold text-slate-900 block">${e.customer_name}</span>
              <span class="text-[11px] text-slate-500 font-mono block">${e.customer_email}</span>
              <span class="text-[11px] text-emerald-700 font-mono font-semibold">${e.customer_phone}</span>
            </td>
            <td class="py-3 px-3 text-[11px]">
              <span class="font-semibold text-slate-700 block">${e.college_name || 'N/A'}</span>
              <span class="text-slate-500">${e.course || 'N/A'}</span>
            </td>
            <td class="py-3 px-3">
              <span class="px-1.5 py-0.5 rounded font-mono text-[10px] font-black bg-cyan-100 text-cyan-800 mr-1">${e.project_code}</span>
              <span class="font-medium text-slate-800 line-clamp-1">${e.project_title}</span>
              <span class="text-[10px] text-purple-700 font-mono block mt-0.5">Stack: ${e.technology || 'General'}</span>
            </td>
            <td class="py-3 px-3 text-[11px] text-slate-600 max-w-xs">
              <p class="line-clamp-2" title="${e.message}">${e.message}</p>
            </td>
            <td class="py-3 px-3">
              <select onchange="app.updateEnquiryStatus(${e.id}, this.value)" class="px-2 py-1 rounded-lg border text-[11px] font-bold ${statusColors[e.status] || 'border-slate-300'}">
                <option value="NEW" ${e.status === 'NEW' ? 'selected' : ''}>NEW</option>
                <option value="CONTACTED" ${e.status === 'CONTACTED' ? 'selected' : ''}>CONTACTED</option>
                <option value="IN_DISCUSSION" ${e.status === 'IN_DISCUSSION' ? 'selected' : ''}>IN DISCUSSION</option>
                <option value="CONVERTED" ${e.status === 'CONVERTED' ? 'selected' : ''}>CONVERTED</option>
                <option value="CLOSED" ${e.status === 'CLOSED' ? 'selected' : ''}>CLOSED</option>
              </select>
            </td>
            <td class="py-3 px-3">
              <div class="flex items-center gap-1">
                <input type="text" id="adm-enq-notes-${e.id}" value="${e.admin_notes || ''}" placeholder="Add notes..." class="px-2 py-1 text-[11px] rounded border border-slate-200 w-28">
                <button onclick="app.saveEnquiryNotes(${e.id})" class="px-2 py-1 bg-slate-800 text-white rounded text-[10px] font-bold hover:bg-slate-900" title="Save Note">Save</button>
              </div>
            </td>
            <td class="py-3 px-3 text-right">
              <a href="${waUrl}" target="_blank" class="p-2 rounded-xl bg-emerald-50 hover:bg-emerald-100 text-emerald-700 border border-emerald-200 inline-flex items-center gap-1 text-[11px] font-bold" title="WhatsApp Customer">
                <i data-lucide="message-circle" class="w-3.5 h-3.5"></i> Chat
              </a>
            </td>
          </tr>
        `;
      }).join('');

      if (window.lucide) window.lucide.createIcons();
    } catch (e) {
      tbody.innerHTML = `<tr><td colspan="8" class="py-4 text-center text-xs text-rose-500">Failed to load enquiries: ${e.message}</td></tr>`;
    }
  }

  async updateEnquiryStatus(id, newStatus) {
    try {
      await this.apiRequest(`/api/admin/enquiries/${id}/status`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status: newStatus })
      });
      this.showToast(`Enquiry status updated to ${newStatus}`, 'success');
      this.renderAdminEnquiries();
    } catch (e) {
      this.showToast('Failed to update enquiry status: ' + e.message, 'error');
    }
  }

  async saveEnquiryNotes(id) {
    const input = document.getElementById(`adm-enq-notes-${id}`);
    const notes = input ? input.value.trim() : '';
    try {
      await this.apiRequest(`/api/admin/enquiries/${id}/status`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ admin_notes: notes })
      });
      this.showToast('Enquiry notes saved successfully', 'success');
    } catch (e) {
      this.showToast('Failed to save notes: ' + e.message, 'error');
    }
  }

  // ==========================================
  // ADMIN CAPSTONE REQUESTS MANAGEMENT
  // ==========================================

  async renderAdminRequests() {
    const tbody = document.getElementById('adm-requests-table-body');
    if (!tbody) return;

    const statusFilter = document.getElementById('adm-request-status-filter')?.value || 'ALL';

    try {
      const url = `/api/admin/requests${statusFilter !== 'ALL' ? '?status=' + statusFilter : ''}`;
      const res = await this.apiRequest(url);
      const requests = res.requests || [];
      const mentors = res.mentors || (this.adminData ? this.adminData.mentors : []) || [];

      const badge = document.getElementById('adm-badge-requests');
      if (badge) badge.innerText = requests.length;
      const kpiReq = document.getElementById('admin-stat-requests');
      if (kpiReq) kpiReq.innerText = requests.filter(r => r.status === 'NEW' || r.status === 'PENDING').length;

      if (requests.length === 0) {
        tbody.innerHTML = `<tr><td colspan="8" class="py-8 text-center text-xs text-slate-500">No project requests found.</td></tr>`;
        return;
      }

      tbody.innerHTML = requests.map(r => `
        <tr class="hover:bg-slate-50/80">
          <td class="py-3 px-3 font-mono">
            <span class="font-bold text-slate-900 block">${r.request_number}</span>
            <span class="text-[10px] text-slate-400">${(r.created_at || '').substring(0, 16)}</span>
          </td>
          <td class="py-3 px-3">
            <span class="font-bold text-slate-900 block">${r.student_name}</span>
            <span class="text-[11px] text-slate-500 font-mono block">${r.student_email}</span>
            <span class="text-[11px] text-emerald-700 font-mono font-semibold">${r.student_phone}</span>
          </td>
          <td class="py-3 px-3">
            <span class="px-1.5 py-0.5 rounded font-mono text-[10px] font-black bg-cyan-100 text-cyan-800 mr-1">${r.project_code}</span>
            <span class="font-medium text-slate-800 line-clamp-1">${r.project_title}</span>
          </td>
          <td class="py-3 px-3 text-[11px]">
            <span class="px-2 py-0.5 rounded text-[10px] font-semibold bg-slate-100 text-slate-700">${r.team_mode || 'Individual'}</span>
            <span class="text-slate-500 block mt-0.5">Due: ${r.deadline || '8 Weeks'}</span>
          </td>
          <td class="py-3 px-3">
            <span class="px-2 py-0.5 rounded text-[10px] font-bold ${r.status === 'APPROVED' ? 'bg-emerald-100 text-emerald-900' : (r.status === 'REJECTED' ? 'bg-rose-100 text-rose-900' : 'bg-amber-100 text-amber-900')}">
              ${r.status}
            </span>
          </td>
          <td class="py-3 px-3 text-[11px]">
            <select onchange="app.assignMentorToRequest(${r.id}, this.value)" class="px-2 py-1 rounded border border-slate-200 text-[11px] bg-white">
              <option value="">-- Assign Faculty --</option>
              ${mentors.map(m => `<option value="${m.id}" ${r.mentor_id == m.id ? 'selected' : ''}>${m.name} (${m.department})</option>`).join('')}
            </select>
          </td>
          <td class="py-3 px-3">
            <div class="flex items-center gap-1.5">
              <input type="number" min="0" max="100" id="adm-req-prog-${r.id}" value="${r.progress_percentage || 0}" class="w-14 px-2 py-1 text-xs rounded border border-slate-200 text-center font-mono">
              <span class="text-xs font-bold text-slate-500">%</span>
              <button onclick="app.updateRequestProgress(${r.id})" class="p-1 rounded bg-slate-100 hover:bg-slate-200 text-slate-700" title="Save Progress"><i data-lucide="check" class="w-3.5 h-3.5"></i></button>
            </div>
          </td>
          <td class="py-3 px-3 text-right">
            <div class="flex items-center justify-end gap-1">
              <button onclick="app.updateRequestStatus(${r.id}, 'APPROVED')" class="px-2 py-1 bg-emerald-600 hover:bg-emerald-700 text-white rounded text-[10px] font-bold" title="Approve Request">Approve</button>
              <button onclick="app.updateRequestStatus(${r.id}, 'REJECTED')" class="px-2 py-1 bg-rose-600 hover:bg-rose-700 text-white rounded text-[10px] font-bold" title="Reject Request">Reject</button>
            </div>
          </td>
        </tr>
      `).join('');

      if (window.lucide) window.lucide.createIcons();
    } catch (e) {
      tbody.innerHTML = `<tr><td colspan="8" class="py-4 text-center text-xs text-rose-500">Failed to load requests: ${e.message}</td></tr>`;
    }
  }

  async updateRequestStatus(id, action) {
    try {
      await this.apiRequest(`/api/admin/requests/${id}/action`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ action: action })
      });
      this.showToast(`Request marked as ${action}`, 'success');
      this.renderAdminRequests();
    } catch (e) {
      this.showToast('Failed to update request: ' + e.message, 'error');
    }
  }

  async assignMentorToRequest(id, mentorId) {
    if (!mentorId) return;
    try {
      await this.apiRequest(`/api/admin/requests/${id}/assign-mentor`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ mentor_id: parseInt(mentorId) })
      });
      this.showToast('Faculty mentor assigned successfully', 'success');
    } catch (e) {
      this.showToast('Failed to assign mentor: ' + e.message, 'error');
    }
  }

  async updateRequestProgress(id) {
    const input = document.getElementById(`adm-req-prog-${id}`);
    const pct = input ? parseInt(input.value) : 0;
    try {
      await this.apiRequest(`/api/admin/requests/${id}/progress`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ progress_percentage: pct, milestone_notes: `Milestone updated to ${pct}%` })
      });
      this.showToast(`Progress updated to ${pct}%`, 'success');
    } catch (e) {
      this.showToast('Failed to update progress: ' + e.message, 'error');
    }
  }

  // ==========================================
  // ADMIN ORDERS & INVOICES MANAGEMENT
  // ==========================================

  async renderAdminOrders() {
    const tbody = document.getElementById('adm-orders-table-body');
    if (!tbody) return;

    try {
      const payments = await this.apiRequest('/api/admin/payments');
      if (payments.length === 0) {
        tbody.innerHTML = `<tr><td colspan="9" class="py-8 text-center text-xs text-slate-500">No customer orders submitted yet.</td></tr>`;
        return;
      }

      tbody.innerHTML = payments.map(p => {
        const isApproved = p.status === 'approved' || p.status === 'verified';
        return `
          <tr class="hover:bg-slate-50/80">
            <td class="py-3 px-3 font-mono font-bold text-slate-900">${p.order_number || ('ORD-' + p.id)}</td>
            <td class="py-3 px-3">
              <span class="font-bold text-slate-900 block">${p.student_name || 'Customer'}</span>
              <span class="text-[11px] text-slate-500 font-mono">${p.student_email || '—'}</span>
            </td>
            <td class="py-3 px-3">
              <span class="font-medium text-slate-800 line-clamp-1">${p.project_title || 'Academic Project'}</span>
              <span class="text-[10px] text-cyan-800 font-mono">${p.project_code || '—'}</span>
            </td>
            <td class="py-3 px-3 font-mono font-black text-slate-900">₹${(p.amount || 0).toLocaleString()}</td>
            <td class="py-3 px-3 font-mono text-xs font-semibold text-purple-700">${p.utr_reference || '—'}</td>
            <td class="py-3 px-3">
              ${p.screenshot_url ? `<a href="${p.screenshot_url}" target="_blank" class="text-xs text-cyan-600 hover:underline font-semibold flex items-center gap-1"><i data-lucide="image" class="w-3.5 h-3.5"></i> Proof</a>` : '<span class="text-slate-400 text-xs">—</span>'}
            </td>
            <td class="py-3 px-3">
              <span class="px-2 py-0.5 rounded text-[10px] font-bold ${isApproved ? 'bg-emerald-100 text-emerald-900' : 'bg-amber-100 text-amber-900'}">
                ${(p.status || 'pending').toUpperCase()}
              </span>
            </td>
            <td class="py-3 px-3 font-mono text-xs">
              ${p.invoice_number ? `
                <a href="/api/invoices/${p.invoice_number}" target="_blank" class="px-2 py-1 rounded bg-purple-50 text-brand-purple hover:bg-purple-100 font-bold border border-purple-200 inline-flex items-center gap-1">
                  <i data-lucide="file-text" class="w-3.5 h-3.5"></i> ${p.invoice_number}
                </a>
              ` : (isApproved ? `
                <button onclick="app.generateInvoice(${p.id})" class="px-2 py-1 bg-brand-purple hover:bg-purple-700 text-white rounded text-[10px] font-bold flex items-center gap-1">
                  <i data-lucide="plus" class="w-3 h-3"></i> Generate
                </button>
              ` : '<span class="text-slate-400 text-[10px]">Awaiting Approval</span>')}
            </td>
            <td class="py-3 px-3 text-right">
              ${!isApproved ? `
                <div class="flex items-center justify-end gap-1">
                  <button onclick="app.verifyPayment(${p.id}, 'approved')" class="px-2 py-1 bg-emerald-600 hover:bg-emerald-700 text-white rounded text-[10px] font-bold">Verify</button>
                  <button onclick="app.verifyPayment(${p.id}, 'rejected')" class="px-2 py-1 bg-rose-600 hover:bg-rose-700 text-white rounded text-[10px] font-bold">Reject</button>
                </div>
              ` : '<span class="text-emerald-700 text-xs font-bold">Verified</span>'}
            </td>
          </tr>
        `;
      }).join('');

      if (window.lucide) window.lucide.createIcons();
    } catch (e) {
      tbody.innerHTML = `<tr><td colspan="9" class="py-4 text-center text-xs text-rose-500">Failed to load orders: ${e.message}</td></tr>`;
    }
  }

  async generateInvoice(orderId) {
    try {
      const res = await this.apiRequest(`/api/admin/orders/${orderId}/generate-invoice`, { method: 'POST' });
      this.showToast(`Invoice ${res.invoice_number} generated successfully!`, 'success');
      this.renderAdminOrders();
      window.open(`/api/invoices/${res.invoice_number}`, '_blank');
    } catch (e) {
      this.showToast('Failed to generate invoice: ' + e.message, 'error');
    }
  }

  // ==========================================
  // ADMIN EMAIL NOTIFICATION LOGS
  // ==========================================

  async renderAdminEmailLogs() {
    const tbody = document.getElementById('adm-email-logs-table-body');
    if (!tbody) return;

    try {
      const res = await this.apiRequest('/api/admin/email-logs');
      const logs = res.logs || [];

      if (logs.length === 0) {
        tbody.innerHTML = `<tr><td colspan="7" class="py-8 text-center text-xs text-slate-500">No email logs recorded yet. Automated alerts will show here.</td></tr>`;
        return;
      }

      tbody.innerHTML = logs.map(l => {
        const isSent = l.status === 'SENT';
        return `
          <tr class="hover:bg-slate-50/80">
            <td class="py-2.5 px-3 text-[11px] text-slate-600">${(l.created_at || '').substring(0, 19)}</td>
            <td class="py-2.5 px-3 font-semibold text-slate-800 text-xs">${l.event_type}</td>
            <td class="py-2.5 px-3 text-brand-purple font-medium text-xs">${l.recipient_email}</td>
            <td class="py-2.5 px-3 text-slate-700 text-xs max-w-xs truncate" title="${l.subject}">${l.subject}</td>
            <td class="py-2.5 px-3">
              <span class="px-2 py-0.5 rounded text-[10px] font-bold ${isSent ? 'bg-emerald-100 text-emerald-900 border border-emerald-300' : 'bg-rose-100 text-rose-900 border border-rose-300'}">
                ${l.status}
              </span>
            </td>
            <td class="py-2.5 px-3 text-[10px] text-slate-500 max-w-xs truncate" title="${l.error_message || 'Delivered successfully'}">${l.error_message || 'Delivered via SMTP'}</td>
            <td class="py-2.5 px-3 text-right">
              ${!isSent ? `
                <button onclick="app.retryEmailLog(${l.id})" class="px-2.5 py-1 bg-rose-600 hover:bg-rose-700 text-white rounded text-[10px] font-bold shadow-sm flex items-center gap-1 ml-auto">
                  <i data-lucide="rotate-ccw" class="w-3 h-3"></i> Retry
                </button>
              ` : '<span class="text-slate-400 text-[10px]">—</span>'}
            </td>
          </tr>
        `;
      }).join('');

      if (window.lucide) window.lucide.createIcons();
    } catch (e) {
      tbody.innerHTML = `<tr><td colspan="7" class="py-4 text-center text-xs text-rose-500">Failed to load email logs: ${e.message}</td></tr>`;
    }
  }

  async retryEmailLog(id) {
    try {
      this.showToast('Retrying email delivery...', 'info');
      const res = await this.apiRequest(`/api/admin/email-logs/${id}/retry`, { method: 'POST' });
      this.showToast(res.message || 'Email delivery retry completed', 'success');
      this.renderAdminEmailLogs();
    } catch (e) {
      this.showToast('Retry attempt failed: ' + e.message, 'error');
    }
  }

  // ==========================================
  // PROFILE & PASSWORD MANAGEMENT
  // ==========================================

  async handleUpdateProfile() {
    const name = document.getElementById('prof-name').value.trim();
    const phone = document.getElementById('prof-phone').value.trim();
    const college = document.getElementById('prof-college').value.trim();
    const course = document.getElementById('prof-course').value.trim();

    try {
      const res = await this.apiRequest('/api/student/profile', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, phone, college_name: college, course })
      });
      this.showToast('Profile updated successfully!', 'success');
      if (this.user) {
        this.user.name = name;
        this.user.phone = phone;
        this.user.college_name = college;
        this.user.course = course;
        this.updateAuthUI();
      }
    } catch (e) {
      this.showToast('Failed to update profile: ' + e.message, 'error');
    }
  }

  async handleChangePassword() {
    const oldPassword = document.getElementById('pwd-old').value;
    const newPassword = document.getElementById('pwd-new').value;
    const confirmPassword = document.getElementById('pwd-confirm').value;

    if (newPassword !== confirmPassword) {
      this.showToast('New passwords do not match!', 'error');
      return;
    }

    try {
      await this.apiRequest('/api/student/change-password', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ old_password: oldPassword, new_password: newPassword })
      });
      this.showToast('Password changed successfully!', 'success');
      document.getElementById('pwd-old').value = '';
      document.getElementById('pwd-new').value = '';
      document.getElementById('pwd-confirm').value = '';
    } catch (e) {
      this.showToast('Failed to change password: ' + e.message, 'error');
    }
  }
'''

# Place methods right before the closing brace of class ProjectVerseApp
last_brace_index = content.rfind('}')
if last_brace_index != -1:
    content = content[:last_brace_index] + methods_to_append + '\n' + content[last_brace_index:]
    print("Appended production methods to ProjectVerseApp class.")

with open('static/js/app.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("append_methods_to_app_js.py completed.")
