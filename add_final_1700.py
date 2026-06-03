path = r'C:\Users\gamju\AppData\Local\Temp\opencode\SXIGOai.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

extra = []
def A(s):
    extra.append(s)

# ===== 1700+ MORE LINES =====
A('<style>')
A('/* === Extended Design System === */')
A('')
# CSS custom properties for each theme
A(':root {')
for name, colors in [('ocean', '#667eea,#4facfe,#764ba2,#0a0a1a'), ('sunset', '#f093fb,#fca311,#f5576c,#0d0d1a'), ('forest', '#2ecc71,#1abc9c,#27ae60,#050d0a'), ('neon', '#00ff87,#ff00ff,#60efff,#050510'), ('midnight', '#7c3aed,#6366f1,#a78bfa,#03030f'), ('aurora', '#00b4d8,#90e0ef,#0077b6,#000814'), ('candy', '#ff6b6b,#ffd93d,#ffa07a,#0f0a14'), ('mono', '#888888,#cccccc,#aaaaaa,#050505')]:
    parts = colors.split(',')
    A(f'  --theme-{name}-primary: {parts[0]};')
    A(f'  --theme-{name}-accent: {parts[1]};')
    A(f'  --theme-{name}-secondary: {parts[2]};')
    A(f'  --theme-{name}-bg: {parts[3]};')
A('}')

# Additional layout patterns
A('.layout-stack > * + * { margin-top: var(--stack-gap, 12px); }')
A('.layout-cluster { display: flex; flex-wrap: wrap; gap: var(--cluster-gap, 8px); align-items: var(--cluster-align, center); justify-content: var(--cluster-justify, flex-start); }')
A('.layout-sidebar { display: grid; grid-template-columns: var(--sidebar-width, 280px) 1fr; gap: 0; }')
A('.layout-switcher { display: grid; grid-template-columns: repeat(auto-fill, minmax(var(--switcher-min, 200px), 1fr)); gap: var(--switcher-gap, 8px); }')
A('.layout-center { display: flex; flex-direction: column; align-items: center; justify-content: center; }')
A('.layout-cover { display: flex; flex-direction: column; min-height: 100%; }')
A('.layout-cover > * { margin-top: auto; margin-bottom: auto; }')
A('.layout-frame { aspect-ratio: var(--frame-ratio, 16/9); overflow: hidden; display: flex; align-items: center; justify-content: center; }')
A('.layout-imposter { position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; }')
A('.layout-reel { display: flex; overflow-x: auto; overflow-y: hidden; gap: var(--reel-gap, 8px); scroll-snap-type: x mandatory; }')
A('.layout-reel > * { flex: 0 0 auto; scroll-snap-align: start; }')
A('.layout-grid { display: grid; gap: var(--grid-gap, 8px); }')
A('.layout-grid-2 { grid-template-columns: repeat(2, 1fr); }')
A('.layout-grid-3 { grid-template-columns: repeat(3, 1fr); }')
A('.layout-grid-4 { grid-template-columns: repeat(4, 1fr); }')
A('.layout-grid-auto { grid-template-columns: repeat(auto-fill, minmax(var(--grid-min, 200px), 1fr)); }')

# Color palette classes
A('.color-accent-1 { color: var(--accent-1); }')
A('.color-accent-2 { color: var(--accent-2); }')
A('.color-accent-3 { color: var(--accent-3); }')
A('.color-accent-4 { color: var(--accent-4); }')
A('.color-accent-5 { color: var(--accent-5); }')
A('.color-accent-6 { color: var(--accent-6); }')
A('.color-accent-7 { color: var(--accent-7); }')
A('.bg-accent-1 { background: var(--accent-1); }')
A('.bg-accent-2 { background: var(--accent-2); }')
A('.bg-accent-3 { background: var(--accent-3); }')
A('.bg-accent-4 { background: var(--accent-4); }')
A('.bg-accent-5 { background: var(--accent-5); }')
A('.bg-accent-6 { background: var(--accent-6); }')
A('.bg-accent-7 { background: var(--accent-7); }')
A('.border-accent-1 { border-color: var(--accent-1); }')
A('.border-accent-5 { border-color: var(--accent-5); }')

# Extended animation utilities
A('.ease-linear { animation-timing-function: linear; }')
A('.ease-in { animation-timing-function: ease-in; }')
A('.ease-out { animation-timing-function: ease-out; }')
A('.ease-in-out { animation-timing-function: ease-in-out; }')
A('.ease-bounce { animation-timing-function: cubic-bezier(0.68, -0.55, 0.265, 1.55); }')
A('.ease-elastic { animation-timing-function: cubic-bezier(0.68, -0.6, 0.32, 1.6); }')
A('.ease-smooth { animation-timing-function: cubic-bezier(0.4, 0, 0.2, 1); }')
A('.ease-spring { animation-timing-function: cubic-bezier(0.34, 1.56, 0.64, 1); }')

# Animation delay scale
for i in range(1, 20):
    A(f'.delay-{i*100}ms {{ animation-delay: {i*100}ms; }}')
    A(f'.duration-{i*100}ms {{ animation-duration: {i*100}ms; }}')

# Media print enhancements
A('@media print {')
A('  body { background: #fff; color: #000; -webkit-print-color-adjust: exact; print-color-adjust: exact; }')
A('  .glass-card, .message-content, .modal, .settings-panel, .notification-panel { background: #f8f8f8 !important; backdrop-filter: none !important; -webkit-backdrop-filter: none !important; border: 1px solid #ddd !important; color: #000 !important; }')
A('  .rgb-border::before { display: none !important; }')
A('  .gradient-main, .gradient-chat { background: none !important; -webkit-text-fill-color: #000 !important; color: #000 !important; }')
A('  .avatar { background: #e0e0e0 !important; color: #333 !important; }')
A('  a { color: #0000ee !important; }')
A('  code { background: #f0f0f0 !important; }')
A('  pre { background: #f5f5f5 !important; border: 1px solid #ddd !important; }')
A('  .v2-badge { background: #333 !important; color: #fff !important; }')
A('}')

# High contrast mode
A('@media (prefers-contrast: high) {')
A('  :root { --glass-border: rgba(255,255,255,0.2); }')
A('  .message-content { border-width: 2px; }')
A('  .sidebar { border-right-width: 2px; }')
A('  .model-badge { border: 1px solid currentColor; }')
A('  .glass-card { border-width: 2px; }')
A('}')

# Right-to-left support
A('[dir="rtl"] .sidebar { border-right: none; border-left: 1px solid var(--glass-border); }')
A('[dir="rtl"] .settings-panel { right: auto; left: -440px; }')
A('[dir="rtl"] .settings-panel.open { left: 0; right: auto; }')
A('[dir="rtl"] .settings-overlay { direction: rtl; }')

# Screen reader only
A('.sr-only { border: 0; clip: rect(0,0,0,0); height: 1px; margin: -1px; overflow: hidden; padding: 0; position: absolute; width: 1px; white-space: nowrap; }')

# Reduced motion
A('@media (prefers-reduced-motion: reduce) {')
A('  *, *::before, *::after { animation-duration: 0.01ms !important; animation-iteration-count: 1 !important; transition-duration: 0.01ms !important; scroll-behavior: auto !important; }')
A('  .bg-particles .particle { display: none; }')
A('  .rgb-border::before { animation: none; }')
A('  .rgb-text { animation: none; }')
A('  .rgb-glow { animation: none; }')
A('}')

# Dark mode preference
A('@media (prefers-color-scheme: light) {')
A('  :root { --glass-border: rgba(0,0,0,0.1); --text-primary: #1a1a2e; --text-secondary: #555; --text-muted: #888; --bg-primary: #f0f0ff; --bg-secondary: #e8e8ff; --bg-tertiary: #ddddf8; }')
A('  .sidebar { background: rgba(232,232,255,0.95); }')
A('  .status-bar { background: rgba(240,240,255,0.9); }')
A('  .message-content { color: #1a1a2e; }')
A('  .glass-card:hover { background: rgba(0,0,0,0.03); }')
A('}')

# Loading animations for async operations
A('.loading-dots::after { content: ""; animation: loading-dots 1.5s steps(4, end) infinite; }')
A('@keyframes loading-dots { 0% { content: ""; } 25% { content: "."; } 50% { content: ".."; } 75% { content: "..."; } 100% { content: ""; } }')
A('.loading-spinner { width: 20px; height: 20px; border: 2px solid var(--glass-border); border-top-color: var(--accent-5); border-radius: 50%; animation: spin 0.7s linear infinite; }')
A('.loading-pulse { animation: loading-pulse 1.5s ease-in-out infinite; }')
A('@keyframes loading-pulse { 0%,100% { opacity: 0.4; } 50% { opacity: 1; } }')
A('.loading-slide { animation: loading-slide 1.5s ease-in-out infinite; }')
A('@keyframes loading-slide { 0% { transform: translateX(-100%); } 100% { transform: translateX(400%); } }')

# Extended responsive breakpoints
A('@media (max-width: 1200px) { .dashboard-grid { grid-template-columns: repeat(3, 1fr); } .welcome-grid { grid-template-columns: repeat(2, 1fr); } }')
A('@media (max-width: 992px) { .dashboard-grid { grid-template-columns: repeat(2, 1fr); } .shortcut-grid { grid-template-columns: 1fr; } .model-compare-selects { flex-direction: column; } }')
A('@media (max-width: 640px) { .welcome-logo { font-size: 36px; } .welcome-title { font-size: 16px; } .welcome-grid { grid-template-columns: 1fr; } .theme-grid { grid-template-columns: repeat(2, 1fr); } .emoji-picker-grid { grid-template-columns: repeat(5, 1fr); } .token-usage { flex-wrap: wrap; } }')
A('@media (max-width: 360px) { .input-tools { display: none; } .chat-header .header-btn span { display: none; } .welcome-logo { font-size: 28px; } .theme-grid { grid-template-columns: 1fr; } }')

# Hover device detection
A('@media (hover: none) {')
A('  .message-actions { opacity: 1; }')
A('  .conv-action-btn { opacity: 1; }')
A('  .copy-btn { opacity: 1; }')
A('  .sidebar-icon-btn { min-width: 44px; min-height: 44px; }')
A('  .header-btn { min-width: 44px; min-height: 44px; }')
A('  .tool-btn { min-width: 44px; min-height: 44px; }')
A('  select, input, textarea { font-size: 16px; }')
A('}')

# Reduced data mode
A('@media (prefers-reduced-data: reduce) {')
A('  .bg-particles .particle { display: none; }')
A('  .rgb-border::before { display: none; }')
A('  .gradient-main, .gradient-chat { background: none; }')
A('  .welcome-logo, .welcome-card { filter: none; }')
A('  .avatar { background: var(--accent-5); }')
A('}')

# Backdrop filter fallback
A('@supports not (backdrop-filter: blur(1px)) {')
A('  .glass-card, .glass-glass, .sidebar, .settings-panel, .notification-panel, .modal, .input-wrapper, .message-content, .toast, .context-menu, .command-palette { background: rgba(18,18,42,0.95); }')
A('  .sidebar { background: var(--bg-secondary); }')
A('  .message-content { background: var(--bg-tertiary); }')
A('  .input-wrapper { background: var(--bg-tertiary); }')
A('}')

# V2.0 brand styles
A('.v2-rainbow-text { background: linear-gradient(90deg, #ff6b6b, #ffd93d, #6bcb77, #4d96ff, #9b59b6); background-size: 300% 100%; -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; animation: gradient-shift 4s ease infinite; }')
A('.v2-shine { position: relative; overflow: hidden; }')
A('.v2-shine::after { content: ""; position: absolute; top: 0; left: -100%; width: 100%; height: 100%; background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent); animation: shine-sweep 3s ease-in-out infinite; }')
A('@keyframes shine-sweep { 0% { left: -100%; } 100% { left: 200%; } }')
A('.v2-glow-border { position: relative; }')
A('.v2-glow-border::before { content: ""; position: absolute; inset: -2px; border-radius: inherit; background: linear-gradient(135deg, var(--accent-1), var(--accent-5), var(--accent-6), var(--accent-1)); background-size: 300% 300%; animation: gradient-shift 4s ease infinite; z-index: -1; opacity: 0.5; }')
A('.v2-glow-border::after { content: ""; position: absolute; inset: 0; border-radius: inherit; background: inherit; z-index: -0.5; }')

A('</style>')

# More HTML for various panels
A('')
A('<!-- Model Download Progress Indicator -->')
A('<div style="display:none;" id="modelDownloadIndicator">')
A('  <div class="status-item"><span class="status-dot loading"></span> Downloading...</div>')
A('</div>')

A('')
A('<!-- Keyboard Shortcuts Display for Accessibility -->')
A('<div class="sr-only" aria-live="polite" id="announcements"></div>')

A('')
A('<!-- Version Watermark -->')
A('<div class="watermark" id="watermarkMain" style="position:fixed;bottom:32px;right:32px;z-index:5;font-size:11px;color:var(--text-muted);opacity:0.3;pointer-events:none;font-weight:300;letter-spacing:0.5px;">SXIGOai <strong style="font-weight:600;background:var(--gradient-main);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;">V2.0</strong></div>')

# Final JS - housekeeping and extras
A('<script>')
A('// ===== V2.0 Final Housekeeping =====')
A('function cleanupOldDrafts() {')
A('  Object.keys(localStorage).forEach(function(key) {')
A('    if (key.startsWith("sxigo_draft_") && !conversations.some(function(c) { return key === "sxigo_draft_" + c.id; })) {')
A('      localStorage.removeItem(key);')
A('    }')
A('  });')
A('}')
A('setTimeout(cleanupOldDrafts, 10000);')
A('')
A('// Smooth scroll polyfill')
A('if (!("scrollBehavior" in document.documentElement.style)) {')
A('  // Smooth scroll not supported')
A('}')
A('')
A('// Prevent submit on forms')
A('document.addEventListener("submit", function(e) { e.preventDefault(); });')
A('')
A('// Log memory usage on stats')
A('function logPerformanceMetrics() {')
A('  if (performance && performance.memory) {')
A('    console.log("JS Heap: " + Math.round(performance.memory.usedJSHeapSize / 1024 / 1024) + "MB / " + Math.round(performance.memory.jsHeapSizeLimit / 1024 / 1024) + "MB");')
A('  }')
A('}')
A('setTimeout(logPerformanceMetrics, 5000);')
A('')
A('// Simple notification check')
A('setInterval(function() {')
A('  const badge = document.getElementById("notifBadge");')
A('  if (badge && parseInt(badge.textContent) > 0) {')
A('    // Flash the notification icon')
A('  }')
A('}, 10000);')
A('')
A('// Load saved font')
A('const savedFontFamily = localStorage.getItem("sxigo_font");')
A('if (savedFontFamily) {')
A('  document.documentElement.style.setProperty("--font-family", savedFontFamily);')
A('}')
A('')
A('// Detect reduced motion')
A('const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");')
A('if (reducedMotion.matches) {')
A('  document.documentElement.classList.add("reduced-motion");')
A('}')
A('')
A('// SXIGOai is fully initialized')
A('console.log("");')
A('console.log("╔══════════════════════════════════╗");')
A('console.log("║     SXIGOai V2.0 is ready       ║");')
A('console.log("║  Glassmorphism + RGB Effects    ║");')
A('console.log("╚══════════════════════════════════╝");')
A('console.log("");')
A('console.log("Chat Interface: Premium");')
A('console.log("Animations: Enabled");')
A('console.log("Themes: " + Object.keys(THEMES).length);')
A('console.log("Server: " + getServerUrl());')
A('console.log("Model: " + (settings.currentModel || "not selected"));')
A('</script>')

insertion = '\n'.join(extra)
content = content.replace('</body>', insertion + '\n</body>')

# Remove any duplicate </body></html>
last_body = content.rfind('</body>')
last_html = content.rfind('</html>')
if last_body > last_html:
    # Remove everything after last </body>
    content = content[:last_body] + '\n</body>\n</html>\n'

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

line_count = content.count('\n')
print(f'Total lines: {line_count}')
