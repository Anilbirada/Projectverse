/**
 * PROJECTVERSE - Enterprise Frontend Single Page Application Controller
 * Version: 4.0.0 (Production Release)
 * Architecture: Vanilla Modern ES6+ Modular Class
 * Features:
 *  - 90 Unique Projects Catalogue across 6 Academic Streams (BCA, B.Com, B.Tech, MCA, M.Tech, IIT Research)
 *  - Comprehensive 9-Tab Project Specifications Modal (DFD, UML, 3NF Schemas, APIs, Roadmaps, Deliverables)
 *  - Pre-Sales Project Enquiries & Capstone Enrollment Requests with Email Dispatch to aniladani843@gmail.com
 *  - Verified Deliverables Unlocked Downloads & Official GST Invoices
 *  - Full Administrative Control Center (90 Projects CRUD, Enquiries, Requests, Orders, Email Logs, UPI)
 *  - Direct UPI Checkout (Payee: ANIL, 8431712924-3@ybl) & Permanent WhatsApp Support (+91 8431712924)
 */

class ProjectverseApp {
  constructor() {
    this.token = localStorage.getItem('pv_token') || null;
    this.user = JSON.parse(localStorage.getItem('pv_user') || 'null');
    
    // Core Datasets
    this.allProjects = [];
    this.featuredProjects = [];
    this.trendingProjects = [];
    this.mentorsList = [];
    this.categoriesList = [];
    this.wishlist = new Set(JSON.parse(localStorage.getItem('pv_wishlist') || '[]'));
    
    // Runtime UI State
    this.currentView = 'home';
    this.selectedProject = null;
    this.checkoutProject = null;
    this.searchDebounceTimer = null;
    // Production mode initialized

    // Advanced Multi-Filter State
    this.filters = {
      q: '',
      category: '',
      domain: '',
      difficulty: '',
      timeline: '',
      sort: 'default'
    };

    // Admin Telemetry & Workspace State
    this.adminData = {
      stats: {},
      projects: [],
      enrollments: [],
      students: [],
      mentors: [],
      payments: [],
      images: [],
      upi: {},
      support: {}
    };

    this.init();
  }

  async init() {
    this.updateNavAuth();
    this.bindHashRouter();

    // Parallel bootstrap of datasets
    await Promise.all([
      this.fetchStats(),
      this.fetchSections(),
      this.fetchAllProjects(),
      this.fetchCategories()
    ]);

    // Handle initial bookmark/route
    this.handleRoute();

    // Render Lucide icons
    if (window.lucide) {
      window.lucide.createIcons();
    }
  }

  // ================= ROUTING & SPA VIEW MANAGEMENT =================

  bindHashRouter() {
    window.addEventListener('hashchange', () => this.handleRoute());
  }

  handleRoute() {
    const hash = window.location.hash.replace('#', '') || 'home';

    if (hash === 'catalogue' || hash.startsWith('catalogue')) {
      this.navigate('catalogue');
    } else if (hash === 'help-desk') {
      this.navigate('help-desk');
    } else if (hash === 'student-dashboard') {
      if (!this.user) {
        this.openAuthModal('login');
        this.navigate('home');
      } else {
        this.navigate('student-dashboard');
      }
    } else if (hash === 'admin') {
      if (!this.user || !['admin', 'super_admin', 'project_manager'].includes(this.user.role)) {
        this.showToast('Administrator privileges required. Please sign in.', 'error');
        this.openAuthModal('login');
        this.navigate('home');
      } else {
        this.navigate('admin');
      }
    } else if (hash.startsWith('project/')) {
      const code = hash.split('/')[1];
      this.openProjectDetails(code);
    } else {
      this.navigate('home');
      if (['how-it-works', 'about', 'contact'].includes(hash)) {
        setTimeout(() => {
          const el = document.getElementById(hash);
          if (el) el.scrollIntoView({ behavior: 'smooth' });
        }, 100);
      }
    }
  }

  navigate(viewName, scrollTarget = null) {
    this.currentView = viewName;

    const views = {
      'home': document.getElementById('view-home'),
      'catalogue': document.getElementById('view-catalogue'),
      'student-dashboard': document.getElementById('view-student-dashboard'),
      'admin': document.getElementById('view-admin'),
      'help-desk': document.getElementById('view-help-desk')
    };

    Object.entries(views).forEach(([name, container]) => {
      if (container) {
        container.classList.toggle('hidden', name !== viewName);
      }
    });

    if (viewName === 'catalogue') {
      this.renderCatalogue();
      window.scrollTo({ top: 0, behavior: 'smooth' });
    } else if (viewName === 'help-desk') {
      this.loadHelpDesk();
      window.scrollTo({ top: 0, behavior: 'smooth' });
    } else if (viewName === 'student-dashboard') {
      this.loadStudentDashboard();
      window.scrollTo({ top: 0, behavior: 'smooth' });
    } else if (viewName === 'admin') {
      this.loadAdminDashboard();
      window.scrollTo({ top: 0, behavior: 'smooth' });
    } else if (viewName === 'home') {
      if (scrollTarget) {
        const el = document.getElementById(scrollTarget);
        if (el) el.scrollIntoView({ behavior: 'smooth' });
      } else {
        window.scrollTo({ top: 0, behavior: 'smooth' });
      }
    }

    if (window.lucide) window.lucide.createIcons();
  }

  toggleMobileMenu() {
    const m = document.getElementById('mobile-menu');
    if (m) m.classList.toggle('hidden');
  }

  // ================= API UTILITY LAYER =================

  async apiRequest(endpoint, options = {}) {
    const headers = options.headers || {};
    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`;
    }
    options.headers = headers;

    try {
      const res = await fetch(endpoint, options);
      if (!res.ok) {
        const err = await res.json().catch(() => ({ detail: 'Network response was not ok' }));
        throw new Error(err.detail || 'An unexpected error occurred');
      }
      return await res.json();
    } catch (e) {
      console.error(`API Error on ${endpoint}:`, e);
      throw e;
    }
  }

  // ================= DATA FETCHING & TELEMETRY =================

  async fetchStats() {
    try {
      const data = await this.apiRequest('/api/stats');

      // Update Homepage / Marketplace Metrics
      const statProjectsEl = document.getElementById('stat-counter-projects');
      if (statProjectsEl) statProjectsEl.innerText = data.total_projects || 90;

      const statStudentsEl = document.getElementById('stat-counter-students');
      if (statStudentsEl) statStudentsEl.innerText = data.total_students || 0;
    } catch (e) {
      console.warn("Could not load platform stats:", e);
    }
  }

  async fetchCategories() {
    try {
      this.categoriesList = await this.apiRequest('/api/categories');
    } catch (e) {
      console.warn("Could not load categories:", e);
    }
  }

  async fetchSections() {
    try {
      const sections = await this.apiRequest('/api/projects/sections');
      this.featuredProjects = sections.featured || [];
      this.trendingProjects = sections.trending || [];
      this.mentorsList = sections.mentors || [];

      this.renderHomeFeatured();
      this.renderHomeTrending();
      this.renderHomeMentors();
    } catch (e) {
      console.warn("Could not load homepage sections:", e);
    }
  }

  async fetchAllProjects() {
    try {
      const data = await this.apiRequest('/api/projects?limit=150');
      this.allProjects = data.projects || [];
      
      const countLabel = document.getElementById('catalogue-count-label');
      if (countLabel) countLabel.innerText = this.allProjects.length;

      if (this.currentView === 'catalogue') {
        this.renderCatalogue();
      }
    } catch (e) {
      console.warn("Could not load catalogue projects:", e);
    }
  }

  // ================= HOMEPAGE SHOWCASE RENDERING =================

  renderHomeFeatured() {
    const container = document.getElementById('home-featured-grid');
    if (!container) return;
    if (this.featuredProjects.length === 0) {
      container.innerHTML = `<div class="col-span-3 text-center py-6 text-slate-400 text-xs">Featured projects will appear here.</div>`;
      return;
    }
    container.innerHTML = this.featuredProjects.map(p => this.createProjectCardHTML(p)).join('');
    if (window.lucide) window.lucide.createIcons();
  }

  renderHomeTrending() {
    const container = document.getElementById('home-trending-grid');
    if (!container) return;
    if (this.trendingProjects.length === 0) {
      container.innerHTML = `<div class="col-span-3 text-center py-6 text-slate-400 text-xs">Trending projects will appear here.</div>`;
      return;
    }
    container.innerHTML = this.trendingProjects.map(p => this.createProjectCardHTML(p)).join('');
    if (window.lucide) window.lucide.createIcons();
  }

  renderHomeMentors() {
    const container = document.getElementById('home-mentors-list');
    if (!container) return;
    if (this.mentorsList.length === 0) {
      container.innerHTML = `<div class="text-slate-400 text-xs">Faculty advisors loading...</div>`;
      return;
    }
    container.innerHTML = this.mentorsList.map(m => `
      <div class="p-3 bg-slate-900/60 rounded-2xl border border-slate-700/60 flex items-center justify-between text-xs">
        <div class="flex items-center gap-3">
          <div class="w-9 h-9 rounded-xl bg-purple-500/20 text-purple-300 border border-purple-500/30 flex items-center justify-center font-bold">
            ${m.full_name.split(' ').map(n => n[0]).join('')}
          </div>
          <div>
            <h5 class="font-bold text-slate-200 text-xs sm:text-sm">${m.full_name}</h5>
            <p class="text-[11px] text-slate-400">${m.designation} • ${m.department}</p>
          </div>
        </div>
        <span class="px-2.5 py-1 rounded-full text-[10px] font-bold bg-emerald-950 text-emerald-400 border border-emerald-800/40">
          ${m.specialization}
        </span>
      </div>
    `).join('');
    if (window.lucide) window.lucide.createIcons();
  }

  openFindMyProjectModal() {
    this.navigate('catalogue');
    const filterInput = document.getElementById('filter-search');
    if (filterInput) {
      filterInput.focus();
    }
    this.showToast('Select your academic stream below or search your required project title', 'info');
  }

  // ================= 90 PROJECTS CATALOGUE & MULTI-FILTER =================

  setCategoryFilter(cat) {
    this.filters.category = cat;
    
    // Update Filter Pills UI
    const pills = [
      { id: 'cat-pill-all', key: '' },
      { id: 'cat-pill-bca', key: 'BCA' },
      { id: 'cat-pill-bcom', key: 'B.Com' },
      { id: 'cat-pill-btech', key: 'B.Tech' },
      { id: 'cat-pill-mca', key: 'MCA' },
      { id: 'cat-pill-mtech', key: 'M.Tech' },
      { id: 'cat-pill-iit', key: 'IIT-Level / Research-Grade' }
    ];

    pills.forEach(p => {
      const el = document.getElementById(p.id);
      if (el) {
        const isActive = this.filters.category === p.key;
        el.className = isActive 
          ? 'px-4 py-2 rounded-xl text-xs font-bold whitespace-nowrap bg-brand-navy text-white shadow-sm transition-all'
          : 'px-4 py-2 rounded-xl text-xs font-bold whitespace-nowrap bg-white text-slate-700 hover:bg-purple-50 hover:text-purple-700 border border-slate-200 transition-all';
      }
    });

    this.renderCatalogue();
  }

  filterByLevel(cat) {
    this.filters.category = cat;
    this.navigate('catalogue');
    this.setCategoryFilter(cat);
  }

  filterByDomain(domain) {
    this.filters.domain = domain;
    const domSelect = document.getElementById('filter-domain');
    if (domSelect) domSelect.value = domain;
    this.navigate('catalogue');
    this.renderCatalogue();
  }

  debounceSearch() {
    clearTimeout(this.searchDebounceTimer);
    this.searchDebounceTimer = setTimeout(() => {
      const val = document.getElementById('filter-search')?.value.trim() || '';
      this.filters.q = val;
      this.renderCatalogue();
    }, 250);
  }

  handleHeroSearch() {
    const q = document.getElementById('hero-search-input')?.value.trim() || '';
    this.filters.q = q;
    const filterInput = document.getElementById('filter-search');
    if (filterInput) filterInput.value = q;
    this.navigate('catalogue');
    this.renderCatalogue();
  }

  applyFilters() {
    this.filters.domain = document.getElementById('filter-domain')?.value || '';
    this.filters.difficulty = document.getElementById('filter-difficulty')?.value || '';
    this.filters.timeline = document.getElementById('filter-timeline')?.value || '';
    this.filters.sort = document.getElementById('filter-sort')?.value || 'default';
    this.renderCatalogue();
  }

  resetFilters() {
    this.filters = {
      q: '',
      category: '',
      domain: '',
      difficulty: '',
      timeline: '',
      sort: 'default'
    };

    const sIn = document.getElementById('filter-search');
    if (sIn) sIn.value = '';
    const domIn = document.getElementById('filter-domain');
    if (domIn) domIn.value = '';
    const diffIn = document.getElementById('filter-difficulty');
    if (diffIn) diffIn.value = '';
    const timeIn = document.getElementById('filter-timeline');
    if (timeIn) timeIn.value = '';
    const sortIn = document.getElementById('filter-sort');
    if (sortIn) sortIn.value = 'default';

    this.setCategoryFilter('');
  }

  getFilteredProjects() {
    return this.allProjects.filter(p => {
      if (this.filters.category && p.academic_level !== this.filters.category) return false;
      if (this.filters.domain && (!p.domain || !p.domain.toLowerCase().includes(this.filters.domain.toLowerCase()))) return false;
      if (this.filters.difficulty && p.difficulty !== this.filters.difficulty) return false;
      if (this.filters.timeline && (!p.timeline || !p.timeline.toLowerCase().includes(this.filters.timeline.toLowerCase()))) return false;

      if (this.filters.q) {
        const q = this.filters.q.toLowerCase();
        const code = (p.project_code || '').toLowerCase();
        const title = (p.title || '').toLowerCase();
        const tech = (p.tech_summary || '').toLowerCase();
        const desc = (p.description || '').toLowerCase();
        const dom = (p.domain || '').toLowerCase();
        if (!code.includes(q) && !title.includes(q) && !tech.includes(q) && !desc.includes(q) && !dom.includes(q)) {
          return false;
        }
      }
      return true;
    }).sort((a, b) => {
      if (this.filters.sort === 'price_asc') return a.price - b.price;
      if (this.filters.sort === 'price_desc') return b.price - a.price;
      if (this.filters.sort === 'name') return a.title.localeCompare(b.title);
      if (this.filters.sort === 'popularity') return (b.popularity_score || 0) - (a.popularity_score || 0);
      if (this.filters.sort === 'newest') return b.id - a.id;
      return a.id - b.id;
    });
  }

  renderCatalogue() {
    const container = document.getElementById('catalogue-grid');
    const emptyBox = document.getElementById('catalogue-empty');
    const countLabel = document.getElementById('catalogue-count-label');
    if (!container) return;

    const filtered = this.getFilteredProjects();
    if (countLabel) countLabel.innerText = `${filtered.length} of ${this.allProjects.length}`;

    if (filtered.length === 0) {
      container.innerHTML = '';
      if (emptyBox) emptyBox.classList.remove('hidden');
      return;
    }

    if (emptyBox) emptyBox.classList.add('hidden');
    container.innerHTML = filtered.map(p => this.createProjectCardHTML(p)).join('');

    if (window.lucide) window.lucide.createIcons();
  }

  createProjectCardHTML(p) {
    const isSaved = this.wishlist.has(p.id);

    // Color Badges per Academic Category
    let badgeClass = 'bg-blue-50 text-blue-700 border-blue-200';
    if (p.academic_level === 'B.Com') badgeClass = 'bg-emerald-50 text-emerald-700 border-emerald-200';
    if (p.academic_level === 'B.Tech') badgeClass = 'bg-cyan-50 text-cyan-800 border-cyan-200';
    if (p.academic_level === 'MCA') badgeClass = 'bg-indigo-50 text-indigo-700 border-indigo-200';
    if (p.academic_level === 'M.Tech') badgeClass = 'bg-amber-50 text-amber-800 border-amber-200';
    if (p.academic_level === 'IIT-Level / Research-Grade') badgeClass = 'bg-rose-50 text-rose-700 border-rose-200';

    const waCardMsg = `Hello PROJECTVERSE,\n\nI am interested in:\nProject Code: ${p.project_code}\nTitle: ${p.title}\nCategory: ${p.academic_level}\n\nPlease share synopsis, deliverables, and guidance.\nThank you!`;

    return `
      <div class="bg-white rounded-3xl border border-slate-200 overflow-hidden shadow-sm hover:shadow-xl transition-all duration-300 card-hover flex flex-col group">
        
        <!-- Thumbnail & Visual Overlay -->
        <div class="relative aspect-video overflow-hidden bg-slate-900 cursor-pointer" onclick="app.openProjectDetails('${p.project_code}')">
          <img src="${p.image_url}" alt="${p.title}" loading="lazy" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
               onerror="this.src='/static/projects/btech/BTECH001.webp'">
          <div class="absolute inset-0 bg-gradient-to-t from-slate-950/80 via-transparent to-transparent"></div>
          
          <div class="absolute top-3 left-3 flex items-center gap-1.5 flex-wrap">
            <span class="px-2.5 py-0.5 rounded-lg font-mono font-bold text-[11px] bg-slate-900/90 text-cyan-300 border border-cyan-500/30">
              ${p.project_code}
            </span>
            <span class="px-2.5 py-0.5 rounded-lg font-bold text-[10px] ${badgeClass} border">
              ${p.academic_level}
            </span>
          </div>

          <!-- Wishlist Bookmark Toggle -->
          <button onclick="event.stopPropagation(); app.toggleWishlist(${p.id});" 
                  class="absolute top-3 right-3 p-2 rounded-full ${isSaved ? 'bg-brand-purple text-white' : 'bg-slate-900/80 text-slate-300 hover:text-white'} transition-colors" title="Save Project">
            <i data-lucide="bookmark" class="w-3.5 h-3.5 ${isSaved ? 'fill-current' : ''}"></i>
          </button>

          <div class="absolute bottom-2.5 left-3 right-3 flex items-center justify-between text-[11px] text-slate-300">
            <span class="flex items-center gap-1 font-medium"><i data-lucide="clock" class="w-3 h-3 text-cyan-400"></i> ${p.timeline || p.duration || '6-8 Weeks'}</span>
            <span class="font-bold text-slate-200 tracking-wider text-[10px] uppercase">${p.difficulty}</span>
          </div>
        </div>

        <!-- Card Body -->
        <div class="p-5 flex flex-col flex-grow justify-between space-y-4">
          <div class="space-y-2">
            <div class="flex items-center justify-between">
              <span class="text-[10px] font-bold uppercase tracking-wider text-brand-purple block line-clamp-1">
                ${p.domain || p.subcategory}
              </span>
              ${p.is_trending ? `<span class="px-2 py-0.5 rounded text-[9px] font-black bg-cyan-100 text-cyan-800">TRENDING</span>` : ''}
            </div>

            <h4 class="font-extrabold text-slate-900 text-sm sm:text-base leading-snug line-clamp-2 hover:text-brand-purple transition-colors cursor-pointer" onclick="app.openProjectDetails('${p.project_code}')">
              ${p.title}
            </h4>

            <p class="text-xs text-slate-500 line-clamp-2 leading-relaxed">
              ${p.description}
            </p>

            <!-- Tech summary tags -->
            <div class="pt-1 flex flex-wrap gap-1 text-[10px] text-slate-600 font-mono">
              <span class="px-2 py-0.5 rounded bg-slate-100 line-clamp-1 max-w-full">
                ${p.tech_summary || 'Full Stack & Database'}
              </span>
            </div>
          </div>

          <!-- Price & Actions Row -->
          <div class="pt-3 border-t border-slate-100 flex items-center justify-between gap-2">
            <div>
              <span class="text-[10px] text-slate-400 uppercase block font-semibold">Academic License</span>
              <div class="flex items-baseline gap-1.5 font-mono">
                <span class="text-lg font-black text-slate-900">₹${p.price.toLocaleString()}</span>
                ${p.discount_price ? `<span class="text-xs text-slate-400 line-through">₹${p.discount_price.toLocaleString()}</span>` : ''}
              </div>
            </div>

            <div class="flex items-center gap-1.5 flex-wrap justify-end">
              <button onclick="app.openProjectDetails('${p.project_code}')" class="px-3 py-2 rounded-xl text-xs font-semibold border border-slate-200 hover:bg-slate-50 text-slate-700 transition-colors">
                Details
              </button>
              <button onclick="app.openProjectEnquiryModal('${p.project_code}')" class="px-3 py-2 rounded-xl text-xs font-bold bg-amber-500 hover:bg-amber-600 text-slate-950 transition-colors shadow-sm">
                Enquire
              </button>
              <button onclick="app.openProjectRequestModal('${p.project_code}')" class="px-3 py-2 rounded-xl text-xs font-bold bg-cyan-500 hover:bg-cyan-600 text-slate-950 transition-colors shadow-sm">
                Request
              </button>
              <a href="https://wa.me/918431712924?text=${encodeURIComponent(waCardMsg)}" target="_blank" rel="noopener noreferrer" class="p-2 rounded-xl bg-emerald-50 hover:bg-emerald-100 text-emerald-700 border border-emerald-200 transition-colors" title="Ask on WhatsApp">
                <i data-lucide="message-circle" class="w-4 h-4"></i>
              </a>
            </div>
          </div>

        </div>

      </div>
    `;
  }

  // ================= PROJECT DETAILS MODAL (9 FULL TABS) =================

  async openProjectDetails(codeOrId) {
    try {
      const p = await this.apiRequest(`/api/projects/${codeOrId}`);
      this.selectedProject = p;

      // Header Elements
      document.getElementById('modal-project-code').innerText = p.project_code;
      document.getElementById('modal-project-level').innerText = p.academic_level;
      document.getElementById('modal-project-domain').innerText = p.domain || p.subcategory;
      document.getElementById('modal-project-difficulty').innerText = (p.difficulty || 'Intermediate').toUpperCase();
      document.getElementById('modal-project-timeline').innerText = (p.timeline || p.duration || '6-8 WEEKS').toUpperCase();
      document.getElementById('modal-project-title').innerText = p.title;
      document.getElementById('modal-project-price').innerText = `₹${p.price.toLocaleString()}`;
      document.getElementById('modal-project-discount').innerText = p.discount_price ? `₹${p.discount_price.toLocaleString()}` : '';

      // Image
      const imgEl = document.getElementById('modal-project-img');
      if (imgEl) imgEl.src = p.image_url;

      // Tab 1: Overview
      document.getElementById('modal-desc').innerText = p.description || '';
      document.getElementById('modal-problem').innerText = p.problem_statement || 'Standard manual academic / commercial bottlenecks.';
      document.getElementById('modal-solution').innerText = p.proposed_solution || 'Modular, automated, verified digital architecture.';
      document.getElementById('modal-objectives').innerText = p.objectives || '1. Build robust data pipeline.\n2. Develop secure APIs.\n3. Integrate responsive user interface.\n4. Validate deliverables.';
      document.getElementById('modal-apps').innerText = p.real_world_apps || 'Enterprise deployments, college systems, educational defense.';
      document.getElementById('modal-users').innerText = p.target_users || 'Students, faculty evaluators, administrators.';

      // Tab 2: Tech Stack
      const ts = p.tech_stack || {};
      const techHTML = Object.entries(ts).map(([key, val]) => `
        <div class="p-3.5 rounded-2xl bg-slate-50 border border-slate-200">
          <span class="text-[10px] font-bold uppercase tracking-wider text-slate-500 block">${key.replace('_', ' ')}</span>
          <span class="text-xs font-semibold text-slate-900 font-mono mt-0.5 block">${val}</span>
        </div>
      `).join('');
      document.getElementById('modal-tech-grid').innerHTML = techHTML || `<p class="text-xs text-slate-500">${p.tech_summary}</p>`;

      // Tab 3: Features & Modules
      const modules = p.core_modules || [];
      const modHTML = modules.length > 0 ? modules.map((m, idx) => `
        <div class="p-4 rounded-2xl bg-slate-50 border border-slate-200 space-y-1.5">
          <div class="flex items-center gap-2">
            <span class="w-5 h-5 rounded-md bg-purple-100 text-brand-purple text-[10px] font-mono font-bold flex items-center justify-center">${idx + 1}</span>
            <h5 class="font-bold text-xs text-slate-900">${m.name || m.module_name || 'Module ' + (idx + 1)}</h5>
          </div>
          <p class="text-xs text-slate-600 leading-relaxed">${m.description || m.details || ''}</p>
        </div>
      `).join('') : '<p class="text-xs text-slate-500">Standard modular breakdown provided with complete source package.</p>';
      document.getElementById('modal-modules-container').innerHTML = modHTML;

      const f = p.features || {};
      const featHTML = Object.entries(f).map(([cat, list]) => `
        <div class="p-4 rounded-2xl bg-slate-50 border border-slate-200 space-y-2">
          <span class="text-xs font-bold text-brand-purple uppercase tracking-wider block">${cat} Features</span>
          <ul class="space-y-1.5 text-xs text-slate-700">
            ${(list || []).map(item => `<li class="flex items-start gap-2"><i data-lucide="check" class="w-3.5 h-3.5 text-emerald-500 flex-shrink-0 mt-0.5"></i> <span>${item}</span></li>`).join('')}
          </ul>
        </div>
      `).join('');
      document.getElementById('modal-features-container').innerHTML = featHTML;

      // Tab 4: Architecture & DFD/UML
      document.getElementById('modal-architecture-text').innerText = p.architecture || 'Layered 3-tier architecture with decoupled presentation, application, and persistence layers.';
      document.getElementById('modal-dfd-text').innerText = p.dfd_description || 'Level 0 Context Diagram: External entities interact through secure gateway.\nLevel 1 Diagram: Subsystem processes handle authentication, verification, and transaction logging.';
      document.getElementById('modal-uml-text').innerText = p.uml_description || 'UML Class Diagram: Entity relationship classes with strict encapsulation.\nSequence Diagram: Chronological lifecycle of request dispatching and verified response handling.';

      // Tab 5: Database Design
      document.getElementById('modal-database-text').innerText = p.database_design || 'Relational 3NF normalized schema designed for integrity and query optimization.';

      // Tab 6: API Documentation
      document.getElementById('modal-api-text').innerText = p.api_docs || 'GET /api/v1/health -> { "status": "ok" }\nPOST /api/v1/action -> { "success": true }';

      // Tab 7: Roadmap
      document.getElementById('modal-roadmap-text').innerText = p.development_roadmap || 'Sprint 1: Architecture & DB Setup\nSprint 2: Core Module Implementation\nSprint 3: Testing & IEEE Documentation';

      // Tab 8: Prerequisites & Outcomes
      document.getElementById('modal-prereqs-text').innerText = p.prerequisites || 'Basic understanding of programming, databases, and core course curriculum.';
      document.getElementById('modal-outcomes-text').innerText = p.learning_outcomes || 'Hands-on practical development skills, thesis writing, and viva defense proficiency.';

      // Tab 9: Deliverables & Testing
      const delivHTML = (p.resources || []).map(r => `
        <div class="p-3.5 rounded-2xl bg-slate-50 border border-slate-200 flex items-center justify-between">
          <div class="flex items-center gap-3">
            <div class="w-9 h-9 rounded-xl bg-purple-100 text-brand-purple flex items-center justify-center font-bold">
              <i data-lucide="file-check" class="w-4 h-4"></i>
            </div>
            <div>
              <h5 class="font-bold text-slate-800 text-xs sm:text-sm">${r.resource_name}</h5>
              <p class="text-[11px] text-slate-500">${r.description || 'Verified deliverable'} • Format: ${r.file_type || 'ZIP'} (${r.file_size})</p>
            </div>
          </div>
          <span class="px-2.5 py-1 rounded-md text-[10px] font-bold bg-slate-200 text-slate-700">Verified Academic Deliverable</span>
        </div>
      `).join('');
      document.getElementById('modal-deliverables-list').innerHTML = delivHTML;
      document.getElementById('modal-testing-text').innerText = p.testing_requirements || 'Unit test suite with 80%+ branch coverage, integration validation, and user acceptance scripts.';

      // Dynamic WhatsApp Enquiry Link
      const waBtn = document.getElementById('modal-whatsapp-enquiry-btn');
      if (waBtn) {
        const waMsg = `Hello PROJECTVERSE,\n\nI need academic guidance on:\nProject Code: ${p.project_code}\nTitle: ${p.title}\nCategory: ${p.academic_level}\n\nPlease share the detailed synopsis and deliverable package details.`;
        waBtn.href = `https://wa.me/918431712924?text=${encodeURIComponent(waMsg)}`;
      }

      // Reset to Tab 1
      this.setModalTab('overview');

      document.getElementById('modal-project-details').classList.remove('hidden');
      if (window.lucide) window.lucide.createIcons();

    } catch (e) {
      this.showToast('Could not load project details', 'error');
    }
  }

  closeProjectDetails() {
    document.getElementById('modal-project-details').classList.add('hidden');
  }

  setModalTab(tabId) {
    const tabs = ['overview', 'tech', 'features', 'architecture', 'database', 'api', 'roadmap', 'prerequisites', 'deliverables'];
    tabs.forEach(t => {
      const btn = document.getElementById(`tab-modal-${t}`);
      const content = document.getElementById(`modal-tab-${t}`);
      if (btn) btn.className = t === tabId ? 'py-3.5 tab-active whitespace-nowrap' : 'py-3.5 text-slate-600 hover:text-slate-900 whitespace-nowrap';
      if (content) content.classList.toggle('hidden', t !== tabId);
    });
    if (window.lucide) window.lucide.createIcons();
  }

  openProjectRequestFromModal() {
    if (!this.selectedProject) return;
    this.closeProjectDetails();
    this.openProjectRequestModal(this.selectedProject.project_code);
  }

  openCheckoutFromModal() {
    if (!this.selectedProject) return;
    this.closeProjectDetails();
    this.openCheckout(this.selectedProject.project_code);
  }

  // ================= STUDENT CAPSTONE ENROLLMENT REQUEST =================

  openProjectRequestModal(codeOrId) {
    if (!this.user) {
      this.showToast('Please sign in or register to request capstone project enrollment', 'info');
      this.openAuthModal('login');
      return;
    }

    const proj = this.allProjects.find(p => p.project_code === codeOrId || p.id == codeOrId);
    if (!proj) return;

    this.selectedProject = proj;
    document.getElementById('req-modal-project-title').innerText = proj.title;
    document.getElementById('req-modal-project-code').innerText = `${proj.project_code} • ${proj.academic_level}`;
    document.getElementById('req-modal-project-id').value = proj.id;
    document.getElementById('req-team-members').value = '';
    document.getElementById('req-remarks').value = '';
    this.toggleTeamFields(false);

    document.getElementById('modal-project-request').classList.remove('hidden');
    if (window.lucide) window.lucide.createIcons();
  }

  closeProjectRequestModal() {
    document.getElementById('modal-project-request').classList.add('hidden');
  }

  toggleTeamFields(isTeam) {
    const box = document.getElementById('req-team-members-container');
    if (box) box.classList.toggle('hidden', !isTeam);
  }

  async submitProjectEnrollmentRequest() {
    const projectId = document.getElementById('req-modal-project-id').value;
    const mode = document.querySelector('input[name="req-mode"]:checked')?.value || 'Individual';
    const teamMembers = document.getElementById('req-team-members').value.trim();
    const remarks = document.getElementById('req-remarks').value.trim();

    const submitBtn = document.getElementById('req-submit-btn');
    submitBtn.disabled = true;
    submitBtn.innerText = 'Submitting Request...';

    try {
      const res = await this.apiRequest('/api/student/enroll-request', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          project_id: parseInt(projectId),
          team_mode: mode,
          team_members: teamMembers,
          remarks: remarks
        })
      });

      this.closeProjectRequestModal();
      this.showToast(res.message || 'Capstone project request submitted! Faculty mentor will review your enrollment.', 'success');
      this.navigate('student-dashboard');

    } catch (e) {
      this.showToast(e.message || 'Failed to submit request', 'error');
    } finally {
      submitBtn.disabled = false;
      submitBtn.innerText = 'Submit Enrollment Request';
    }
  }

  // ================= WISHLIST =================

  async toggleWishlist(projectId) {
    if (!this.user) {
      this.showToast('Please sign in to bookmark academic projects', 'info');
      this.openAuthModal('login');
      return;
    }

    try {
      const res = await this.apiRequest(`/api/student/wishlist/${projectId}`, { method: 'POST' });
      if (res.saved) {
        this.wishlist.add(projectId);
        this.showToast('Project bookmarked to your list', 'success');
      } else {
        this.wishlist.delete(projectId);
        this.showToast('Project removed from bookmark list', 'info');
      }
      localStorage.setItem('pv_wishlist', JSON.stringify([...this.wishlist]));
      this.updateWishlistCount();
      if (this.currentView === 'catalogue') this.renderCatalogue();
    } catch (e) {
      this.showToast('Failed to update wishlist', 'error');
    }
  }

  updateWishlistCount() {
    const el = document.getElementById('nav-wishlist-count');
    if (el) {
      el.innerText = this.wishlist.size;
      el.classList.toggle('hidden', this.wishlist.size === 0);
    }
  }

  // ================= UPI CHECKOUT & PAYMENT FLOW =================

  async openCheckout(codeOrId) {
    if (!this.user) {
      this.showToast('Please sign in or register before completing project purchase', 'info');
      this.openAuthModal('login');
      return;
    }

    try {
      const [proj, settings] = await Promise.all([
        this.apiRequest(`/api/projects/${codeOrId}`),
        this.apiRequest('/api/payment-settings')
      ]);

      this.checkoutProject = proj;

      document.getElementById('checkout-project-code').innerText = proj.project_code;
      document.getElementById('checkout-project-title').innerText = proj.title;
      document.getElementById('checkout-amount').innerText = `₹${proj.price.toLocaleString()}`;

      document.getElementById('checkout-qr-img').src = settings.qr_code_path || '/static/uploads/qr/projectverse-upi-qr.png';
      document.getElementById('checkout-account-name').innerText = settings.account_name;
      document.getElementById('checkout-upi-id').innerText = settings.upi_id;
      document.getElementById('checkout-upi-phone').innerText = `Mobile: ${settings.upi_mobile}`;
      document.getElementById('checkout-utr').value = '';

      const dlQr = document.getElementById('checkout-download-qr');
      if (dlQr) dlQr.href = settings.qr_code_path || '/static/uploads/qr/projectverse-upi-qr.png';

      const upiIntentBtn = document.getElementById('checkout-upi-intent-btn');
      if (upiIntentBtn) {
        upiIntentBtn.href = `upi://pay?pa=${encodeURIComponent(settings.upi_id)}&pn=${encodeURIComponent(settings.account_name)}&am=${proj.price}&cu=INR&tn=${encodeURIComponent(proj.project_code)}`;
      }

      const checkoutWaBtn = document.getElementById('checkout-whatsapp-btn');
      if (checkoutWaBtn) {
        const payWaMsg = `Hello PROJECTVERSE,\n\nI need payment assistance for:\nProject: ${proj.project_code} - ${proj.title}\nAmount: Rs ${proj.price}\n\nPlease guide me through UPI verification.`;
        checkoutWaBtn.href = `https://wa.me/918431712924?text=${encodeURIComponent(payWaMsg)}`;
      }

      document.getElementById('modal-checkout').classList.remove('hidden');
      if (window.lucide) window.lucide.createIcons();

    } catch (e) {
      this.showToast('Failed to initialize checkout', 'error');
    }
  }

  closeCheckout() {
    document.getElementById('modal-checkout').classList.add('hidden');
  }

  copyUpiId() {
    const upi = document.getElementById('checkout-upi-id').innerText;
    navigator.clipboard.writeText(upi);
    this.showToast(`Copied UPI ID: ${upi}`, 'success');
  }

  async submitPayment() {
    const utr = document.getElementById('checkout-utr').value.trim();
    const screenshotInput = document.getElementById('checkout-screenshot');

    if (!utr || utr.length < 6) {
      this.showToast('Please enter a valid 12-digit UPI transaction reference (UTR)', 'error');
      return;
    }

    const btn = document.getElementById('checkout-submit-btn');
    btn.disabled = true;
    btn.innerHTML = `<span class="animate-spin mr-2">⏳</span> Submitting Payment...`;

    try {
      const formData = new FormData();
      formData.append('project_id', this.checkoutProject.id);
      formData.append('utr_reference', utr);
      if (screenshotInput.files && screenshotInput.files[0]) {
        formData.append('screenshot', screenshotInput.files[0]);
      }

      const res = await this.apiRequest('/api/orders/create', {
        method: 'POST',
        body: formData
      });

      this.closeCheckout();
      this.showToast(`Order ${res.order_number} submitted! Admin will audit the UTR and unlock deliverables shortly.`, 'success');
      this.navigate('student-dashboard');

    } catch (e) {
      this.showToast(e.message || 'Payment submission failed', 'error');
    } finally {
      btn.disabled = false;
      btn.innerHTML = `<i data-lucide="shield-check" class="w-4 h-4"></i> Submit for Verification`;
      if (window.lucide) window.lucide.createIcons();
    }
  }

  // ================= STUDENT DASHBOARD (ENROLLED, MENTORS, PROGRESS) =================

  async loadStudentDashboard() {
    if (!this.user) {
      this.navigate('home');
      this.openAuthModal('login');
      return;
    }

    try {
      const data = await this.apiRequest('/api/student/dashboard');
      const student = data.student || this.user;

      // User profile display
      const initialEl = document.getElementById('dash-user-initial');
      const nameEl = document.getElementById('dash-user-name');
      const colEl = document.getElementById('dash-user-college');
      const emailEl = document.getElementById('dash-user-email');
      const roleEl = document.getElementById('dash-user-role');

      if (initialEl) initialEl.innerText = (student.name || student.full_name || 'S')[0].toUpperCase();
      if (nameEl) nameEl.innerText = student.name || student.full_name || 'Student';
      if (colEl) colEl.innerText = `${student.college_name || student.college || 'Academic Scholar'} • ${student.course || 'Degree Program'}`;
      if (emailEl) emailEl.innerText = student.email;
      if (roleEl) roleEl.innerText = (student.role || 'student').toUpperCase();

      // Pre-fill Profile Settings Form
      const pName = document.getElementById('prof-name');
      const pPhone = document.getElementById('prof-phone');
      const pCollege = document.getElementById('prof-college');
      const pCourse = document.getElementById('prof-course');
      if (pName) pName.value = student.name || student.full_name || '';
      if (pPhone) pPhone.value = student.phone || '';
      if (pCollege) pCollege.value = student.college_name || student.college || '';
      if (pCourse) pCourse.value = student.course || '';

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

      // 3. Render Orders & Invoices
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

    } catch (e) {
      this.showToast('Could not load student dashboard', 'error');
    }
  }

  setDashboardTab(tabId) {
    const tabs = ['enquiries', 'requests', 'orders', 'profile'];
    tabs.forEach(t => {
      const btn = document.getElementById(`tab-dash-${t}`);
      const content = document.getElementById(`dash-tab-content-${t}`);
      if (btn) btn.className = t === tabId ? 'py-3 tab-active flex items-center gap-2 font-semibold' : 'py-3 text-slate-500 hover:text-slate-800 flex items-center gap-2 font-semibold';
      if (content) content.classList.toggle('hidden', t !== tabId);
    });
    if (window.lucide) window.lucide.createIcons();
  }

  async handleCreateTicket() {
    const subject = document.getElementById('ticket-subject').value.trim();
    const category = document.getElementById('ticket-category').value;
    const message = document.getElementById('ticket-message').value.trim();

    try {
      await this.apiRequest('/api/support/ticket', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ subject, category, message })
      });
      this.showToast('Support ticket submitted! Faculty will assist shortly.', 'success');
      document.getElementById('ticket-subject').value = '';
      document.getElementById('ticket-message').value = '';
      this.loadStudentDashboard();
    } catch (e) {
      this.showToast('Failed to submit ticket', 'error');
    }
  }

  // ================= ADMIN DASHBOARD & ADVANCED OPERATIONS =================

  async loadAdminDashboard() {
    if (!this.user || !['admin', 'super_admin', 'project_manager'].includes(this.user.role)) {
      this.openAuthModal('login');
      this.showToast('Please sign in with your administrator credentials.', 'info');
      return;
    }

    try {
      await this.refreshAdminData();
    } catch (e) {
      this.showToast('Failed to load admin telemetry', 'error');
    }
  }

  async refreshAdminData() {
    const [stats, projectsData, enrollments, students, mentors, payments, images, upi, support] = await Promise.all([
      this.apiRequest('/api/admin/stats'),
      this.apiRequest('/api/projects?limit=150'),
      this.apiRequest('/api/admin/enrollments'),
      this.apiRequest('/api/admin/students'),
      this.apiRequest('/api/admin/mentors'),
      this.apiRequest('/api/admin/payments'),
      this.apiRequest('/api/admin/images-audit'),
      this.apiRequest('/api/payment-settings'),
      this.apiRequest('/api/support-settings')
    ]);

    this.adminData = {
      stats,
      projects: projectsData.projects || [],
      enrollments: enrollments || [],
      students: students || [],
      mentors: mentors || [],
      payments: payments || [],
      images: images || [],
      upi,
      support
    };

    // Update Telemetry Metrics
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
    this.populateSupportSettings();

    if (window.lucide) window.lucide.createIcons();
  }

    setAdminTab(tabId) {
    const tabs = ['enquiries', 'requests', 'orders', 'projects', 'students', 'email-logs', 'payments', 'mentors', 'pricing', 'upi'];
    tabs.forEach(t => {
      const btn = document.getElementById(`tab-adm-${t}`);
      const content = document.getElementById(`adm-tab-${t}`);
      if (btn) btn.className = t === tabId ? 'py-3 tab-active flex items-center gap-1.5 whitespace-nowrap' : 'py-3 text-slate-600 hover:text-slate-900 flex items-center gap-1.5 whitespace-nowrap';
      if (content) content.classList.toggle('hidden', t !== tabId);
    });
    if (window.lucide) window.lucide.createIcons();
  }

  renderAdminProjectsTable() {
    const tbody = document.getElementById('adm-projects-table-body');
    const projects = this.adminData.projects || [];
    if (!tbody) return;

    tbody.innerHTML = projects.map(p => `
      <tr class="hover:bg-slate-50">
        <td class="py-2.5 px-4 font-mono font-bold text-cyan-700">${p.project_code}</td>
        <td class="py-2.5 px-4 font-medium text-slate-900 line-clamp-1">${p.title}</td>
        <td class="py-2.5 px-4 font-semibold text-slate-600">${p.academic_level}</td>
        <td class="py-2.5 px-4 text-slate-500">${p.domain || p.subcategory}</td>
        <td class="py-2.5 px-4 font-mono font-bold text-slate-900">₹${p.price.toLocaleString()}</td>
        <td class="py-2.5 px-4"><span class="px-2 py-0.5 rounded text-[10px] font-bold bg-slate-100 text-slate-700">${p.difficulty}</span></td>
        <td class="py-2.5 px-4 text-right space-x-1.5 whitespace-nowrap">
          <button onclick="app.openAdminProjectModal(${p.id})" class="px-2.5 py-1 bg-slate-100 hover:bg-slate-200 text-slate-800 rounded-lg text-xs font-semibold">
            Edit
          </button>
          <button onclick="app.deleteProject(${p.id}, '${p.project_code}')" class="px-2.5 py-1 bg-red-50 hover:bg-red-100 text-red-700 rounded-lg text-xs font-semibold">
            Delete
          </button>
        </td>
      </tr>
    `).join('');
  }

  filterAdminProjectsTable() {
    const q = (document.getElementById('adm-project-search')?.value || '').toLowerCase();
    const rows = document.querySelectorAll('#adm-projects-table-body tr');
    rows.forEach(r => {
      const text = r.innerText.toLowerCase();
      r.style.display = text.includes(q) ? '' : 'none';
    });
  }

  openAdminProjectModal(projectId = null) {
    const titleEl = document.getElementById('adm-project-modal-title');
    const idInput = document.getElementById('adm-p-id');

    if (projectId) {
      const p = this.adminData.projects.find(item => item.id == projectId);
      if (!p) return;
      titleEl.innerText = `Edit Project (${p.project_code})`;
      idInput.value = p.id;
      document.getElementById('adm-p-code').value = p.project_code;
      document.getElementById('adm-p-level').value = p.academic_level;
      document.getElementById('adm-p-title').value = p.title;
      document.getElementById('adm-p-domain').value = p.domain || p.subcategory;
      document.getElementById('adm-p-diff').value = p.difficulty || 'Intermediate';
      document.getElementById('adm-p-price').value = p.price;
      document.getElementById('adm-p-tech').value = p.tech_summary || '';
      document.getElementById('adm-p-desc').value = p.description || '';
    } else {
      titleEl.innerText = 'Add New Academic Project';
      idInput.value = '';
      document.getElementById('adm-p-code').value = '';
      document.getElementById('adm-p-level').value = 'B.Tech';
      document.getElementById('adm-p-title').value = '';
      document.getElementById('adm-p-domain').value = 'Artificial Intelligence';
      document.getElementById('adm-p-diff').value = 'Intermediate';
      document.getElementById('adm-p-price').value = 999;
      document.getElementById('adm-p-tech').value = '';
      document.getElementById('adm-p-desc').value = '';
    }

    document.getElementById('modal-admin-project').classList.remove('hidden');
  }

  closeAdminProjectModal() {
    document.getElementById('modal-admin-project').classList.add('hidden');
  }

  async handleSaveAdminProject() {
    const id = document.getElementById('adm-p-id').value;
    const price = parseInt(document.getElementById('adm-p-price').value);

    if (isNaN(price) || price < 799) {
      this.showToast('Rule: Minimum project price is ₹799', 'error');
      return;
    }

    const payload = {
      project_code: document.getElementById('adm-p-code').value.trim(),
      academic_level: document.getElementById('adm-p-level').value,
      title: document.getElementById('adm-p-title').value.trim(),
      domain: document.getElementById('adm-p-domain').value.trim(),
      difficulty: document.getElementById('adm-p-diff').value,
      price: price,
      tech_summary: document.getElementById('adm-p-tech').value.trim(),
      description: document.getElementById('adm-p-desc').value.trim()
    };

    try {
      if (id) {
        await this.apiRequest(`/api/admin/projects/${id}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
        this.showToast('Project updated successfully', 'success');
      } else {
        await this.apiRequest('/api/admin/projects/create', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
        this.showToast('New project created successfully', 'success');
      }
      this.closeAdminProjectModal();
      await this.refreshAdminData();
      await this.fetchAllProjects();
    } catch (e) {
      this.showToast(e.message || 'Failed to save project', 'error');
    }
  }

  async deleteProject(id, code) {
    if (!confirm(`Are you sure you want to delete project ${code}? This will remove it from the catalogue.`)) return;

    try {
      await this.apiRequest(`/api/admin/projects/${id}`, { method: 'DELETE' });
      this.showToast(`Project ${code} deleted`, 'info');
      await this.refreshAdminData();
      await this.fetchAllProjects();
    } catch (e) {
      this.showToast('Delete failed: ' + e.message, 'error');
    }
  }

  openAdminCsvModal() {
    document.getElementById('modal-admin-csv').classList.remove('hidden');
  }

  closeAdminCsvModal() {
    document.getElementById('modal-admin-csv').classList.add('hidden');
  }

  async handleCsvImport() {
    const input = document.getElementById('adm-csv-input');
    if (!input.files || !input.files[0]) return;

    const btn = document.getElementById('adm-csv-submit-btn');
    btn.disabled = true;
    btn.innerText = 'Importing CSV...';

    try {
      const formData = new FormData();
      formData.append('csv_file', input.files[0]);

      const res = await this.apiRequest('/api/admin/projects/import-csv', {
        method: 'POST',
        body: formData
      });

      this.closeAdminCsvModal();
      this.showToast(`Imported ${res.imported_count} projects from CSV. Total: ${res.total_catalogue}`, 'success');
      await this.refreshAdminData();
      await this.fetchAllProjects();
    } catch (e) {
      this.showToast('CSV import failed: ' + e.message, 'error');
    } finally {
      btn.disabled = false;
      btn.innerText = 'Upload & Import Projects';
    }
  }

  // --- Admin Enrollment Requests & Mentorship ---

  renderAdminEnrollments() {
    const tbody = document.getElementById('adm-enrollments-table-body');
    const filter = document.getElementById('adm-enroll-filter')?.value || '';
    const enrollments = (this.adminData.enrollments || []).filter(e => !filter || e.status === filter);
    if (!tbody) return;

    if (enrollments.length === 0) {
      tbody.innerHTML = `<tr><td colspan="7" class="py-8 text-center text-slate-500">No enrollment records matching criteria.</td></tr>`;
      return;
    }

    tbody.innerHTML = enrollments.map(e => `
      <tr class="hover:bg-slate-50">
        <td class="py-3 px-4">
          <span class="font-bold text-slate-900 block">${e.student_name}</span>
          <span class="text-[11px] text-slate-500">${e.college} (${e.course})</span>
        </td>
        <td class="py-3 px-4">
          <span class="font-mono font-bold text-cyan-700">${e.project_code}</span>
          <span class="text-xs text-slate-700 block line-clamp-1">${e.title}</span>
        </td>
        <td class="py-3 px-4">
          <span class="px-2 py-0.5 rounded text-[10px] font-bold ${e.team_mode === 'Team' ? 'bg-purple-100 text-brand-purple' : 'bg-slate-100 text-slate-700'}">
            ${e.team_mode || 'Individual'}
          </span>
        </td>
        <td class="py-3 px-4">
          <span class="font-semibold text-slate-800 text-xs">${e.mentor_name || 'Unassigned'}</span>
        </td>
        <td class="py-3 px-4">
          <div class="space-y-1">
            <span class="text-[11px] font-semibold text-slate-700">${e.current_milestone || 'Setup'} (${e.progress_percent || 0}%)</span>
            <div class="w-24 bg-slate-200 rounded-full h-1.5">
              <div class="bg-brand-purple h-1.5 rounded-full" style="width: ${e.progress_percent || 0}%"></div>
            </div>
          </div>
        </td>
        <td class="py-3 px-4">
          <span class="px-2 py-0.5 rounded text-[10px] font-bold ${e.status === 'approved' ? 'bg-emerald-100 text-emerald-800' : 'bg-amber-100 text-amber-800'}">
            ${e.status.toUpperCase()}
          </span>
        </td>
        <td class="py-3 px-4 text-right space-x-1 whitespace-nowrap">
          ${e.status === 'pending' ? `
            <button onclick="app.actionEnrollment(${e.id}, 'approved')" class="px-2.5 py-1 bg-emerald-600 hover:bg-emerald-700 text-white rounded text-xs font-bold">Approve</button>
            <button onclick="app.actionEnrollment(${e.id}, 'rejected')" class="px-2.5 py-1 bg-red-600 hover:bg-red-700 text-white rounded text-xs font-bold">Reject</button>
          ` : `
            <button onclick="app.promptAssignMentor(${e.id})" class="px-2 py-1 bg-purple-50 hover:bg-purple-100 text-brand-purple rounded text-xs font-semibold">Mentor</button>
            <button onclick="app.promptUpdateProgress(${e.id}, ${e.progress_percent || 0})" class="px-2 py-1 bg-cyan-50 hover:bg-cyan-100 text-cyan-800 rounded text-xs font-semibold">Progress</button>
          `}
        </td>
      </tr>
    `).join('');
  }

  async actionEnrollment(id, action) {
    try {
      await this.apiRequest(`/api/admin/enrollments/${id}/action`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ action })
      });
      this.showToast(`Enrollment request ${action}`, 'success');
      await this.refreshAdminData();
    } catch (e) {
      this.showToast('Action failed: ' + e.message, 'error');
    }
  }

  async promptAssignMentor(enrollmentId) {
    const mentors = this.adminData.mentors || [];
    if (mentors.length === 0) {
      this.showToast('No mentors available in roster', 'error');
      return;
    }
    const mentorListStr = mentors.map((m, i) => `${i + 1}. ${m.full_name} (${m.specialization})`).join('\n');
    const selection = prompt(`Assign Mentor to Enrollment ID ${enrollmentId}:\n\n${mentorListStr}\n\nEnter Mentor Number (1-${mentors.length}):`);
    if (!selection) return;

    const idx = parseInt(selection) - 1;
    if (isNaN(idx) || idx < 0 || idx >= mentors.length) {
      this.showToast('Invalid mentor selection', 'error');
      return;
    }

    try {
      await this.apiRequest(`/api/admin/enrollments/${enrollmentId}/assign-mentor`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ mentor_id: mentors[idx].id })
      });
      this.showToast(`Assigned mentor ${mentors[idx].full_name}`, 'success');
      await this.refreshAdminData();
    } catch (e) {
      this.showToast('Failed to assign mentor: ' + e.message, 'error');
    }
  }

  async promptUpdateProgress(enrollmentId, currentPercent) {
    const newPercent = prompt(`Update Progress Percentage (0-100):`, currentPercent);
    if (newPercent === null) return;
    const pVal = parseInt(newPercent);
    if (isNaN(pVal) || pVal < 0 || pVal > 100) {
      this.showToast('Enter valid percentage between 0 and 100', 'error');
      return;
    }

    const milestone = prompt(`Enter Current Milestone Name:`, 'Module Development & Testing');
    if (!milestone) return;

    try {
      await this.apiRequest(`/api/admin/enrollments/${enrollmentId}/progress`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ progress_percent: pVal, current_milestone: milestone })
      });
      this.showToast('Milestone progress updated!', 'success');
      await this.refreshAdminData();
    } catch (e) {
      this.showToast('Update failed: ' + e.message, 'error');
    }
  }

  // --- Admin Student Roster ---

  renderAdminStudents() {
    this.filterStudentRoster();
  }

  filterStudentRoster() {
    const q = document.getElementById('adm-student-search')?.value.trim().toLowerCase() || '';
    const students = (this.adminData ? this.adminData.students : []) || [];
    const tbody = document.getElementById('adm-students-table-body');
    if (!tbody) return;

    const filtered = students.filter(s => {
      if (!q) return true;
      return (s.full_name || s.name || '').toLowerCase().includes(q) ||
             (s.email || '').toLowerCase().includes(q) ||
             (s.college || s.college_name || '').toLowerCase().includes(q) ||
             (s.course || '').toLowerCase().includes(q);
    });

    if (filtered.length === 0) {
      tbody.innerHTML = `<tr><td colspan="7" class="py-8 text-center text-xs text-slate-500">No registered students found.</td></tr>`;
      return;
    }

    tbody.innerHTML = filtered.map(s => `
      <tr class="hover:bg-slate-50">
        <td class="py-2.5 px-4 font-bold text-slate-900">${s.full_name || s.name}</td>
        <td class="py-2.5 px-4 font-mono text-slate-600 text-[11px]">${s.email}</td>
        <td class="py-2.5 px-4 text-slate-800 text-xs">${s.college || s.college_name || 'N/A'}</td>
        <td class="py-2.5 px-4"><span class="px-2 py-0.5 rounded text-[10px] font-bold bg-slate-100 text-slate-800">${s.course || 'B.Tech'}</span></td>
        <td class="py-2.5 px-4 text-slate-600 text-xs">${s.specialization || 'General'}</td>
        <td class="py-2.5 px-4 font-semibold text-brand-purple text-xs">${s.orders_count || 0}</td>
        <td class="py-2.5 px-4">
          <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-100 text-emerald-900 border border-emerald-300">
            VERIFIED USER
          </span>
        </td>
      </tr>
    `).join('');
  }

  // --- Admin Mentors Roster ---

  renderAdminMentors() {
    const grid = document.getElementById('adm-mentors-grid');
    const mentors = this.adminData.mentors || [];
    if (!grid) return;

    grid.innerHTML = mentors.map(m => `
      <div class="bg-slate-50 rounded-2xl border border-slate-200 p-5 space-y-3">
        <div class="flex items-center justify-between">
          <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-purple-100 text-brand-purple">${m.department}</span>
          <span class="text-xs text-slate-500 font-mono">${m.active_students}/${m.capacity} active</span>
        </div>
        <div>
          <h4 class="font-extrabold text-slate-900 text-sm">${m.full_name}</h4>
          <p class="text-xs text-slate-500">${m.designation}</p>
        </div>
        <div class="pt-2 border-t border-slate-200 text-xs text-slate-700">
          <span class="font-semibold text-slate-900">Specialization:</span> ${m.specialization}
        </div>
      </div>
    `).join('');
  }

  async openAddMentorModal() {
    const name = prompt('Enter Mentor Full Name (e.g. Dr. Ramesh Gupta):');
    if (!name) return;
    const email = prompt('Enter Mentor Official Email:');
    if (!email) return;
    const dept = prompt('Enter Academic Department (e.g. Computer Science & Engineering):');
    if (!dept) return;
    const spec = prompt('Enter Technical Specialization (e.g. Deep Learning & Edge AI):');
    if (!spec) return;

    try {
      await this.apiRequest('/api/admin/mentors/create', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          full_name: name,
          email: email,
          department: dept,
          designation: 'Faculty Advisor',
          specialization: spec,
          capacity: 25
        })
      });
      this.showToast('Mentor added to faculty roster!', 'success');
      await this.refreshAdminData();
    } catch (e) {
      this.showToast('Failed to add mentor: ' + e.message, 'error');
    }
  }

  // --- Admin Payment Verification ---

  renderAdminPayments() {
    const tbody = document.getElementById('adm-payments-table-body');
    const payments = this.adminData.payments || [];
    if (!tbody) return;

    if (payments.length === 0) {
      tbody.innerHTML = `<tr><td colspan="7" class="py-6 text-center text-slate-500">No payment records found.</td></tr>`;
      return;
    }

    tbody.innerHTML = payments.map(p => `
      <tr class="hover:bg-slate-50">
        <td class="py-3 px-4">
          <span class="font-bold text-slate-900 block">${p.student_name}</span>
          <span class="text-[11px] text-slate-500">${p.student_college || p.student_email}</span>
        </td>
        <td class="py-3 px-4">
          <span class="font-mono font-bold text-cyan-700">${p.project_code}</span>
          <span class="text-xs text-slate-700 block line-clamp-1">${p.project_title}</span>
        </td>
        <td class="py-3 px-4 font-mono font-bold">₹${p.amount.toLocaleString()}</td>
        <td class="py-3 px-4 font-mono text-slate-800 font-semibold">${p.utr_reference}</td>
        <td class="py-3 px-4">
          ${p.screenshot_path ? `<a href="${p.screenshot_path}" target="_blank" class="text-brand-purple hover:underline text-xs font-semibold flex items-center gap-1"><i data-lucide="external-link" class="w-3 h-3"></i> View Receipt</a>` : '—'}
        </td>
        <td class="py-3 px-4">
          <span class="px-2 py-0.5 rounded text-[10px] font-bold ${p.status === 'approved' ? 'bg-emerald-100 text-emerald-800' : 'bg-amber-100 text-amber-800'}">
            ${p.status.toUpperCase()}
          </span>
        </td>
        <td class="py-3 px-4 text-right space-x-1.5 whitespace-nowrap">
          ${p.status === 'pending' ? `
            <button onclick="app.verifyPayment(${p.id}, 'approved')" class="px-3 py-1 bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg text-xs font-bold shadow-sm">
              Approve
            </button>
            <button onclick="app.verifyPayment(${p.id}, 'rejected')" class="px-3 py-1 bg-red-600 hover:bg-red-700 text-white rounded-lg text-xs font-bold shadow-sm">
              Reject
            </button>
          ` : `
            <span class="text-[11px] text-slate-400">Verified by ${p.verified_by || 'Admin'}</span>
          `}
        </td>
      </tr>
    `).join('');
  }

  async verifyPayment(paymentId, action) {
    const notes = prompt(`Enter verification audit notes for this ${action} decision:`, action === 'approved' ? 'UPI confirmed via bank statement. Deliverables unlocked.' : 'UTR reference mismatch.');
    if (notes === null) return;

    try {
      await this.apiRequest(`/api/admin/payments/${paymentId}/verify`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ action, notes })
      });
      this.showToast(`Payment successfully ${action}`, 'success');
      await this.refreshAdminData();
    } catch (e) {
      this.showToast('Verification failed: ' + e.message, 'error');
    }
  }

  // --- Admin Pricing (Minimum ₹799 Rule) ---

  renderAdminPricing() {
    const tbody = document.getElementById('adm-pricing-table-body');
    const projects = this.adminData.projects || [];
    if (!tbody) return;

    tbody.innerHTML = projects.map(p => `
      <tr class="hover:bg-slate-50">
        <td class="py-2.5 px-4 font-bold text-slate-900">${p.project_code}</td>
        <td class="py-2.5 px-4 font-sans font-medium text-slate-800 line-clamp-1">${p.title}</td>
        <td class="py-2.5 px-4 font-sans"><span class="px-2 py-0.5 rounded text-[10px] font-bold bg-purple-100 text-brand-purple">${p.academic_level}</span></td>
        <td class="py-2.5 px-4 font-bold text-slate-900">₹${p.price.toLocaleString()}</td>
        <td class="py-2.5 px-4">
          <input type="number" id="adm-price-input-${p.id}" value="${p.price}" min="799" class="w-24 px-2 py-1 rounded border border-slate-300 text-xs">
        </td>
        <td class="py-2.5 px-4">
          <button onclick="app.saveProjectPrice(${p.id})" class="px-2.5 py-1 bg-slate-800 hover:bg-slate-900 text-white rounded text-xs font-semibold">
            Update
          </button>
        </td>
      </tr>
    `).join('');
  }

  async saveProjectPrice(projectId) {
    const input = document.getElementById(`adm-price-input-${projectId}`);
    const newPrice = parseInt(input.value);

    if (isNaN(newPrice) || newPrice < 799) {
      this.showToast('Pricing Rule: Minimum project price is ₹799', 'error');
      return;
    }

    try {
      await this.apiRequest(`/api/admin/projects/${projectId}/price`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ price: newPrice })
      });
      this.showToast('Price updated successfully', 'success');
      await this.fetchAllProjects();
      await this.refreshAdminData();
    } catch (e) {
      this.showToast(e.message || 'Failed to update price', 'error');
    }
  }

  // --- Admin Images Audit (90 Bespoke Artworks) ---

  renderAdminImages() {
    const container = document.getElementById('adm-images-grid');
    const images = this.adminData.images || [];
    if (!container) return;

    container.innerHTML = images.map(img => `
      <div class="bg-slate-50 rounded-2xl border border-slate-200 overflow-hidden p-3 space-y-2">
        <div class="aspect-video bg-slate-900 rounded-xl overflow-hidden relative group">
          <img src="${img.image_url}" alt="${img.title}" class="w-full h-full object-cover">
          <label class="absolute inset-0 bg-slate-950/70 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center cursor-pointer text-white text-xs font-bold gap-1">
            <i data-lucide="upload" class="w-4 h-4"></i> Replace Image
            <input type="file" accept="image/*" class="hidden" onchange="app.uploadProjectImage(${img.id}, this)">
          </label>
        </div>
        <div>
          <div class="flex items-center justify-between text-xs">
            <span class="font-mono font-bold text-cyan-700">${img.project_code}</span>
            <span class="text-[10px] text-emerald-600 font-semibold font-mono">${img.size_kb} KB</span>
          </div>
          <h5 class="font-bold text-slate-800 text-xs line-clamp-1 mt-0.5">${img.title}</h5>
        </div>
      </div>
    `).join('');
  }

  async uploadProjectImage(projectId, fileInput) {
    if (!fileInput.files || !fileInput.files[0]) return;
    const file = fileInput.files[0];

    const formData = new FormData();
    formData.append('image_file', file);

    try {
      this.showToast('Uploading replacement project artwork...', 'info');
      await this.apiRequest(`/api/admin/projects/${projectId}/image`, {
        method: 'POST',
        body: formData
      });
      this.showToast('Artwork updated successfully!', 'success');
      await this.refreshAdminData();
    } catch (e) {
      this.showToast('Failed to upload image: ' + e.message, 'error');
    }
  }

  // --- Admin UPI Configuration ---

  populateUpiSettings() {
    const upi = this.adminData.upi || {};
    const phone = document.getElementById('adm-upi-phone');
    if (phone) phone.value = upi.upi_mobile || '8431712924';
    const id = document.getElementById('adm-upi-id');
    if (id) id.value = upi.upi_id || '8431712924-3@ybl';
    const name = document.getElementById('adm-upi-name');
    if (name) name.value = upi.account_name || 'ANIL';
    const instr = document.getElementById('adm-upi-instructions');
    if (instr) instr.value = upi.instructions || 'Scan official QR code or pay to 8431712924-3@ybl. After transaction, submit 12-digit UTR reference for instant verification.';
    const preview = document.getElementById('adm-qr-preview');
    if (preview) preview.src = upi.qr_code_path || '/static/uploads/qr/projectverse-upi-qr.png';
  }

  async saveUpiSettings() {
    const payload = {
      upi_mobile: document.getElementById('adm-upi-phone').value,
      upi_id: document.getElementById('adm-upi-id').value,
      account_name: document.getElementById('adm-upi-name').value,
      instructions: document.getElementById('adm-upi-instructions').value
    };

    try {
      await this.apiRequest('/api/admin/payment-settings', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      this.showToast('Official UPI payment settings saved!', 'success');
    } catch (e) {
      this.showToast('Failed to save UPI settings: ' + e.message, 'error');
    }
  }

  async uploadQrCode(input) {
    if (!input.files || !input.files[0]) return;
    const formData = new FormData();
    formData.append('qr_file', input.files[0]);

    try {
      this.showToast('Uploading UPI QR Code...', 'info');
      const res = await this.apiRequest('/api/admin/payment-settings/qr', {
        method: 'POST',
        body: formData
      });
      document.getElementById('adm-qr-preview').src = res.qr_code_path;
      this.showToast('QR Code updated successfully!', 'success');
    } catch (e) {
      this.showToast('Failed to upload QR code: ' + e.message, 'error');
    }
  }

  // --- Admin Support & WhatsApp Settings ---

  populateSupportSettings() {
    const s = this.adminData.support || {};
    const wa = document.getElementById('adm-support-whatsapp');
    if (wa) wa.value = s.whatsapp_number || '918431712924';
    const label = document.getElementById('adm-support-label');
    if (label) label.value = s.support_label || 'Official Academic Support';
    const gen = document.getElementById('adm-support-template-general');
    if (gen) gen.value = s.template_general || 'Hello PROJECTVERSE, I need academic project assistance.';
    const proj = document.getElementById('adm-support-template-project');
    if (proj) proj.value = s.template_project || 'Hello PROJECTVERSE, I need information about project {code}: {title}.';
    const pay = document.getElementById('adm-support-template-payment');
    if (pay) pay.value = s.template_payment || 'Hello PROJECTVERSE, I need help with payment for project {code}: {title} (Rs {price}).';
  }

  async saveSupportSettings() {
    const payload = {
      whatsapp_number: document.getElementById('adm-support-whatsapp').value.trim(),
      support_label: document.getElementById('adm-support-label').value.trim(),
      template_general: document.getElementById('adm-support-template-general').value.trim(),
      template_project: document.getElementById('adm-support-template-project').value.trim(),
      template_payment: document.getElementById('adm-support-template-payment').value.trim()
    };

    try {
      await this.apiRequest('/api/admin/support-settings', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      this.showToast('WhatsApp & Support settings updated successfully!', 'success');
      await this.refreshAdminData();
    } catch (e) {
      this.showToast('Failed to save support settings: ' + e.message, 'error');
    }
  }

  // ================= HELP DESK & FAQS =================

  async loadHelpDesk() {
    try {
      const faqs = await this.apiRequest('/api/faqs');
      this.faqsList = faqs;
      this.renderHelpDeskFaqs(faqs);
    } catch (e) {
      console.error('Failed to load FAQs:', e);
    }
  }

  renderHelpDeskFaqs(faqs) {
    const container = document.getElementById('help-desk-faq-container');
    if (!container) return;
    if (!faqs || faqs.length === 0) {
      container.innerHTML = `<div class="p-6 text-center text-xs text-slate-500">No matching questions found.</div>`;
      return;
    }
    container.innerHTML = faqs.map((f, idx) => `
      <details class="group bg-slate-50 border border-slate-200 rounded-2xl overflow-hidden transition-all duration-200 open:bg-white open:shadow-sm open:border-purple-200">
        <summary class="flex items-center justify-between p-4 sm:p-5 text-sm font-bold text-slate-800 cursor-pointer list-none select-none hover:text-brand-purple">
          <span class="flex items-center gap-2.5">
            <span class="w-6 h-6 rounded-lg bg-purple-100 text-brand-purple flex items-center justify-center text-xs font-mono font-bold flex-shrink-0">${idx + 1}</span>
            <span>${f.question}</span>
          </span>
          <i data-lucide="chevron-down" class="w-4 h-4 text-slate-400 group-open:rotate-180 transition-transform"></i>
        </summary>
        <div class="px-5 pb-5 pt-1 text-xs sm:text-sm text-slate-600 leading-relaxed border-t border-slate-100 mt-1 whitespace-pre-line">
          ${f.answer}
          <div class="mt-3 pt-3 border-t border-slate-100 flex items-center justify-between text-xs">
            <span class="text-[11px] text-slate-400 font-medium">Category: ${f.category}</span>
            <a href="https://wa.me/918431712924?text=${encodeURIComponent('Hello PROJECTVERSE, I have a question regarding: ' + f.question)}" target="_blank" class="text-emerald-600 hover:text-emerald-700 font-bold flex items-center gap-1">
              Ask Faculty on WhatsApp →
            </a>
          </div>
        </div>
      </details>
    `).join('');
    if (window.lucide) window.lucide.createIcons();
  }

  filterFaqs() {
    const query = (document.getElementById('faq-search-input')?.value || '').toLowerCase().trim();
    if (!this.faqsList) return;
    if (!query) {
      this.renderHelpDeskFaqs(this.faqsList);
      return;
    }
    const filtered = this.faqsList.filter(f => 
      f.question.toLowerCase().includes(query) || 
      f.answer.toLowerCase().includes(query) || 
      f.category.toLowerCase().includes(query)
    );
    this.renderHelpDeskFaqs(filtered);
  }

  // ================= AUTHENTICATION MODALS & MULTI-ROLE =================

  openAuthModal(mode = 'login') {
    this.switchAuthMode(mode);
    document.getElementById('modal-auth').classList.remove('hidden');
    if (window.lucide) window.lucide.createIcons();
  }

  closeAuthModal() {
    document.getElementById('modal-auth').classList.add('hidden');
  }

  switchAuthMode(mode) {
    const isLogin = mode === 'login';
    const titleEl = document.getElementById('auth-modal-title');
    const loginForm = document.getElementById('auth-login-form');
    const registerForm = document.getElementById('auth-register-form');
    const tabLogin = document.getElementById('auth-tab-login');
    const tabRegister = document.getElementById('auth-tab-register');

    if (titleEl) {
      titleEl.innerText = isLogin ? 'Student & Staff Login' : 'Student Capstone Registration';
    }
    if (loginForm) {
      loginForm.classList.toggle('hidden', !isLogin);
    }
    if (registerForm) {
      registerForm.classList.toggle('hidden', isLogin);
    }
    if (tabLogin && tabRegister) {
      if (isLogin) {
        tabLogin.className = 'flex-1 py-2 rounded-lg transition-all text-center font-bold bg-white text-slate-900 shadow-sm';
        tabRegister.className = 'flex-1 py-2 rounded-lg transition-all text-center font-medium text-slate-500 hover:text-slate-800';
      } else {
        tabRegister.className = 'flex-1 py-2 rounded-lg transition-all text-center font-bold bg-white text-slate-900 shadow-sm';
        tabLogin.className = 'flex-1 py-2 rounded-lg transition-all text-center font-medium text-slate-500 hover:text-slate-800';
      }
    }
    if (window.lucide) window.lucide.createIcons();
  }


  async handleLogin() {
    const email = document.getElementById('login-email').value.trim();
    const password = document.getElementById('login-password').value;

    try {
      const res = await this.apiRequest('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      });

      this.token = res.token;
      this.user = res.user;
      localStorage.setItem('pv_token', res.token);
      localStorage.setItem('pv_user', JSON.stringify(res.user));

      this.updateNavAuth();
      this.closeAuthModal();
      this.showToast(`Welcome back, ${res.user.full_name}!`, 'success');

      if (['admin', 'super_admin', 'project_manager'].includes(res.user.role)) {
        this.navigate('admin');
      } else {
        this.navigate('student-dashboard');
      }

    } catch (e) {
      this.showToast(e.message || 'Login failed. Check your email & password.', 'error');
    }
  }

  async handleRegister() {
    const payload = {
      full_name: document.getElementById('reg-name').value.trim(),
      email: document.getElementById('reg-email').value.trim(),
      mobile: document.getElementById('reg-mobile').value.trim(),
      college: document.getElementById('reg-college').value.trim(),
      university: document.getElementById('reg-university').value.trim(),
      course: document.getElementById('reg-course').value,
      academic_year: document.getElementById('reg-year').value,
      specialization: document.getElementById('reg-specialization')?.value.trim() || '',
      preferred_tech: document.getElementById('reg-tech')?.value.trim() || '',
      team_mode: document.querySelector('input[name="reg-mode"]:checked')?.value || 'Individual',
      password: document.getElementById('reg-password').value
    };

    try {
      const res = await this.apiRequest('/api/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      this.token = res.token;
      this.user = res.user;
      localStorage.setItem('pv_token', res.token);
      localStorage.setItem('pv_user', JSON.stringify(res.user));

      this.updateNavAuth();
      this.closeAuthModal();
      this.showToast(`Registration complete! Welcome to PROJECTVERSE.`, 'success');
      this.navigate('catalogue');

    } catch (e) {
      this.showToast(e.message || 'Registration failed', 'error');
    }
  }

  logout() {
    this.token = null;
    this.user = null;
    localStorage.removeItem('pv_token');
    localStorage.removeItem('pv_user');
    this.updateNavAuth();
    this.showToast('You have been logged out.', 'info');
    this.navigate('home');
  }

  updateNavAuth() {
    const container = document.getElementById('nav-auth-container');
    if (!container) return;

    if (this.user) {
      const isAdmin = ['admin', 'super_admin', 'project_manager'].includes(this.user.role);
      container.innerHTML = `
        <div class="flex items-center gap-2">
          ${isAdmin ? `
            <button onclick="app.navigate('admin')" class="px-3 py-1.5 rounded-xl text-xs font-bold bg-rose-50 text-rose-700 border border-rose-200 hover:bg-rose-100 flex items-center gap-1">
              <i data-lucide="shield" class="w-3.5 h-3.5"></i> Admin Control
            </button>
          ` : `
            <button onclick="app.navigate('student-dashboard')" class="px-3 py-1.5 rounded-xl text-xs font-bold bg-purple-50 text-brand-purple border border-purple-200 hover:bg-purple-100 flex items-center gap-1">
              <i data-lucide="user" class="w-3.5 h-3.5"></i> My Capstone
            </button>
          `}
          <button onclick="app.logout()" class="p-2 text-slate-500 hover:text-red-600 rounded-lg" title="Sign Out">
            <i data-lucide="log-out" class="w-4 h-4"></i>
          </button>
        </div>
      `;
    } else {
      container.innerHTML = `
        <button onclick="app.openAuthModal('login')" class="px-4 py-2 rounded-xl text-xs font-bold text-slate-700 hover:bg-slate-100 transition-colors">
          Log In
        </button>
        <button onclick="app.openAuthModal('register')" class="px-4 py-2 rounded-xl text-xs font-bold bg-brand-purple hover:bg-purple-700 text-white shadow-sm transition-all">
          Register
        </button>
      `;
    }

    const mobileContainer = document.getElementById('mobile-auth-container');
    if (mobileContainer) {
      if (this.user) {
        const isAdmin = ['admin', 'super_admin', 'project_manager'].includes(this.user.role);
        mobileContainer.innerHTML = `
          <div class="flex items-center gap-2">
            ${isAdmin ? `
              <button onclick="app.navigate('admin'); app.toggleMobileMenu();" class="flex-1 py-2 rounded-xl text-xs font-bold bg-rose-50 text-rose-700 border border-rose-200 text-center flex items-center justify-center gap-1">
                <i data-lucide="shield" class="w-3.5 h-3.5"></i> Admin
              </button>
            ` : `
              <button onclick="app.navigate('student-dashboard'); app.toggleMobileMenu();" class="flex-1 py-2 rounded-xl text-xs font-bold bg-purple-50 text-brand-purple border border-purple-200 text-center flex items-center justify-center gap-1">
                <i data-lucide="user" class="w-3.5 h-3.5"></i> My Capstone
              </button>
            `}
            <button onclick="app.logout(); app.toggleMobileMenu();" class="py-2 px-3 text-xs font-semibold text-slate-500 hover:text-red-600 rounded-xl bg-slate-100" title="Sign Out">
              Sign Out
            </button>
          </div>
        `;
      } else {
        mobileContainer.innerHTML = `
          <div class="flex items-center gap-2">
            <button onclick="app.openAuthModal('login'); app.toggleMobileMenu();" class="flex-1 py-2 rounded-xl text-xs font-bold text-slate-700 bg-slate-100 hover:bg-slate-200 text-center">
              Log In
            </button>
            <button onclick="app.openAuthModal('register'); app.toggleMobileMenu();" class="flex-1 py-2 rounded-xl text-xs font-bold bg-brand-purple hover:bg-purple-700 text-white shadow-sm text-center">
              Register
            </button>
          </div>
        `;
      }
    }

    this.updateWishlistCount();
    if (window.lucide) window.lucide.createIcons();
  }

  // ================= NOTIFICATION TOAST =================

  showToast(message, type = 'info') {
    const toast = document.getElementById('toast');
    const toastTitle = document.getElementById('toast-title');
    const toastMessage = document.getElementById('toast-message');
    const toastIcon = document.getElementById('toast-icon');

    if (!toast) return;

    toastTitle.innerText = type.toUpperCase();
    toastMessage.innerText = message;

    if (type === 'error') {
      toastIcon.className = 'text-rose-400 flex-shrink-0';
      toastIcon.innerHTML = `<i data-lucide="alert-triangle" class="w-5 h-5"></i>`;
    } else if (type === 'success') {
      toastIcon.className = 'text-emerald-400 flex-shrink-0';
      toastIcon.innerHTML = `<i data-lucide="check-circle-2" class="w-5 h-5"></i>`;
    } else {
      toastIcon.className = 'text-cyan-400 flex-shrink-0';
      toastIcon.innerHTML = `<i data-lucide="info" class="w-5 h-5"></i>`;
    }

    toast.classList.remove('translate-y-24', 'opacity-0');
    toast.classList.add('translate-y-0', 'opacity-100');

    if (window.lucide) window.lucide.createIcons();

    setTimeout(() => {
      toast.classList.remove('translate-y-0', 'opacity-100');
      toast.classList.add('translate-y-24', 'opacity-0');
    }, 4000);
  }

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


}

// Global Application Instance
let app;
window.addEventListener('DOMContentLoaded', () => {
  app = new ProjectverseApp();
  window.app = app;
});
