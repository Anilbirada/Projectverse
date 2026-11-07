import re

with open('static/js/app.js', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Remove demo mode property from constructor
code = code.replace("this.currentDemoMode = 1;", "// Production mode initialized")

# 2. Update renderProjectCard to include Enquire button
card_action_old = """              <button onclick="app.openProjectDetails('${p.project_code}')" class="px-3 py-2 rounded-xl text-xs font-semibold border border-slate-200 hover:bg-slate-50 text-slate-700 transition-colors">
                Details
              </button>
              <button onclick="app.openProjectRequestModal('${p.project_code}')" class="px-3 py-2 rounded-xl text-xs font-bold bg-cyan-500 hover:bg-cyan-600 text-slate-950 transition-colors shadow-sm">
                Request
              </button>"""

card_action_new = """              <button onclick="app.openProjectDetails('${p.project_code}')" class="px-3 py-2 rounded-xl text-xs font-semibold border border-slate-200 hover:bg-slate-50 text-slate-700 transition-colors">
                Details
              </button>
              <button onclick="app.openProjectEnquiryModal('${p.project_code}')" class="px-3 py-2 rounded-xl text-xs font-bold bg-amber-500 hover:bg-amber-600 text-slate-950 transition-colors shadow-sm">
                Enquire
              </button>
              <button onclick="app.openProjectRequestModal('${p.project_code}')" class="px-3 py-2 rounded-xl text-xs font-bold bg-cyan-500 hover:bg-cyan-600 text-slate-950 transition-colors shadow-sm">
                Request
              </button>"""

if card_action_old in code:
    code = code.replace(card_action_old, card_action_new)
    print("Added Enquire button to project cards.")

# 3. Clean statistics display
old_stats_func = """    const statDemoBadge = document.getElementById('hero-demo-badge');
    if (statDemoBadge) {
      statDemoBadge.innerText = data.badge_text || (data.demo_mode ? "Illustrative Demo Statistics" : "Verified Academic Platform");
      statDemoBadge.className = data.demo_mode 
        ? "inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-amber-500/20 text-amber-300 text-xs font-semibold border border-amber-500/30 backdrop-blur-sm"
        : "inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-emerald-500/20 text-emerald-300 text-xs font-semibold border border-emerald-500/30 backdrop-blur-sm";
    }"""

if old_stats_func in code:
    code = code.replace(old_stats_func, "// Production statistics loaded directly")
    print("Cleaned hero demo badge code.")

# 4. Remove fillDemoCredentials method
code = re.sub(r'fillDemoCredentials\(role\)\s*\{[^}]*\}', '', code)

# 5. Remove updateDemoModeUI, toggleDemoMode, resetDemoData
code = re.sub(r'updateDemoModeUI\(demoMode\)\s*\{.*?(?=setAdminTab|\Z)', '', code, flags=re.DOTALL)

# 6. Update setDashboardTab
new_setDashboardTab = """  setDashboardTab(tabId) {
    const tabs = ['enquiries', 'requests', 'orders', 'profile'];
    tabs.forEach(t => {
      const btn = document.getElementById(`tab-dash-${t}`);
      const content = document.getElementById(`dash-tab-content-${t}`);
      if (btn) btn.className = t === tabId ? 'py-3 tab-active flex items-center gap-2 font-semibold' : 'py-3 text-slate-500 hover:text-slate-800 flex items-center gap-2 font-semibold';
      if (content) content.classList.toggle('hidden', t !== tabId);
    });
    if (window.lucide) window.lucide.createIcons();
  }"""

code = re.sub(r'setDashboardTab\(tabId\)\s*\{[^}]*\}', new_setDashboardTab, code)

# 7. Update setAdminTab
new_setAdminTab = """  setAdminTab(tabId) {
    const tabs = ['enquiries', 'requests', 'orders', 'projects', 'students', 'email-logs', 'payments', 'mentors', 'pricing', 'upi'];
    tabs.forEach(t => {
      const btn = document.getElementById(`tab-adm-${t}`);
      const content = document.getElementById(`adm-tab-${t}`);
      if (btn) btn.className = t === tabId ? 'py-3 tab-active flex items-center gap-1.5 whitespace-nowrap' : 'py-3 text-slate-600 hover:text-slate-900 flex items-center gap-1.5 whitespace-nowrap';
      if (content) content.classList.toggle('hidden', t !== tabId);
    });
    if (window.lucide) window.lucide.createIcons();
  }"""

code = re.sub(r'setAdminTab\(tabId\)\s*\{.*?renderAdminProjectsTable', new_setAdminTab + '\n\n  renderAdminProjectsTable', code, flags=re.DOTALL)

with open('static/js/app.js', 'w', encoding='utf-8') as f:
    f.write(code)

print("First phase of app.js patch complete.")
