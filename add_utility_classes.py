path = r'C:\Users\gamju\AppData\Local\Temp\opencode\SXIGOai.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

extra = []
def A(s):
    extra.append(s)

# == MASSIVE ADDITION: CSS, HTML, JS ==
A('<style>')
# Theme transition effects
for i in range(30):
    A(f'.delay-{i}00 {{ animation-delay: {i*0.1}s; }}')
    A(f'.stagger-{i} {{ transition-delay: {i*0.05}s; }}')
    A(f'.fade-{i} {{ opacity: {1-i*0.1}; }}')

A('.fade-scale { transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); }')
A('.hover-lift { transition: transform 0.2s ease, box-shadow 0.2s ease; }')
A('.hover-lift:hover { transform: translateY(-4px); box-shadow: 0 8px 30px rgba(0,0,0,0.3); }')
A('.hover-glow { transition: box-shadow 0.2s ease; }')
A('.hover-glow:hover { box-shadow: 0 0 20px rgba(102,126,234,0.3); }')
A('.hover-scale { transition: transform 0.2s ease; }')
A('.hover-scale:hover { transform: scale(1.05); }')
A('.active-press:active { transform: scale(0.95); }')

# Micro-interactions
A('.btn-ripple { position: relative; overflow: hidden; }')
A('.btn-ripple::after { content: ""; position: absolute; border-radius: 50%; background: rgba(255,255,255,0.3); width: 100px; height: 100px; margin-top: -50px; margin-left: -50px; top: 50%; left: 50%; transform: scale(0); opacity: 0; }')
A('.btn-ripple:active::after { animation: ripple-effect 0.6s ease-out; }')
A('@keyframes ripple-effect { from { transform: scale(0); opacity: 0.5; } to { transform: scale(4); opacity: 0; } }')

# Glass variants
for i in range(1, 11):
    depth = i * 0.02
    A(f'.glass-{i} {{ background: rgba(255,255,255,{depth}); backdrop-filter: blur({i*2}px); border: 1px solid rgba(255,255,255,{0.03+i*0.005}); }}')
    A(f'.glass-border-{i} {{ border-color: rgba(255,255,255,{0.02+i*0.008}); }}')

# RGB color variants
colors = ['ff6b6b', 'ffd93d', '6bcb77', '4d96ff', '9b59b6', 'e67e22', '1abc9c', 'e74c3c', '3498db', '2ecc71']
for i, c in enumerate(colors):
    A(f'.rgb-{i} {{ color: #{c}; }}')
    A(f'.rgb-bg-{i} {{ background: #{c}; }}')
    A(f'.rgb-border-{i} {{ border-color: #{c}; }}')
    A(f'.rgb-glow-{i} {{ box-shadow: 0 0 15px #{c}44; }}')

# Gradient variants
A('.gradient-fire { background: linear-gradient(135deg, #f093fb, #f5576c, #fca311); }')
A('.gradient-ocean { background: linear-gradient(135deg, #667eea, #764ba2, #4facfe); }')
A('.gradient-forest { background: linear-gradient(135deg, #2ecc71, #27ae60, #1abc9c); }')
A('.gradient-sunset { background: linear-gradient(135deg, #ff6b6b, #ffa07a, #ffd93d); }')
A('.gradient-neon { background: linear-gradient(135deg, #00ff87, #60efff, #ff00ff); }')
A('.gradient-midnight { background: linear-gradient(135deg, #7c3aed, #a78bfa, #6366f1); }')
A('.gradient-aurora { background: linear-gradient(135deg, #00b4d8, #0077b6, #90e0ef); }')
A('.gradient-candy { background: linear-gradient(135deg, #ff6b6b, #ffa07a, #ffd93d); }')
A('.gradient-chrome { background: linear-gradient(135deg, #e0e0e0, #9e9e9e, #616161); }')
A('.gradient-rainbow { background: linear-gradient(90deg, #ff0000, #ff7700, #ffff00, #00ff00, #0000ff, #8b00ff); background-size: 300% 100%; animation: gradient-shift 4s ease infinite; }')
A('.gradient-silver { background: linear-gradient(135deg, #ececec, #bdc3c7, #95a5a6); }')
A('.gradient-gold { background: linear-gradient(135deg, #ffd700, #ffb300, #ff8f00); }')

# Shadow variants
A('.shadow-sm { box-shadow: 0 1px 3px rgba(0,0,0,0.12); }')
A('.shadow-md { box-shadow: 0 4px 6px rgba(0,0,0,0.15); }')
A('.shadow-lg { box-shadow: 0 10px 25px rgba(0,0,0,0.2); }')
A('.shadow-xl { box-shadow: 0 20px 50px rgba(0,0,0,0.3); }')
A('.shadow-2xl { box-shadow: 0 30px 80px rgba(0,0,0,0.4); }')
A('.shadow-glow { box-shadow: 0 0 20px rgba(102,126,234,0.3), 0 0 40px rgba(102,126,234,0.1); }')
A('.shadow-glow-lg { box-shadow: 0 0 40px rgba(102,126,234,0.4), 0 0 80px rgba(102,126,234,0.1); }')
A('.shadow-inner { box-shadow: inset 0 2px 4px rgba(0,0,0,0.1); }')

# Glass card presets
A('.glass-card-sm { padding: 12px; border-radius: var(--radius-sm); background: rgba(255,255,255,var(--glass-depth)); backdrop-filter: blur(8px); border: 1px solid var(--glass-border); }')
A('.glass-card-md { padding: 16px; border-radius: var(--radius-md); background: rgba(255,255,255,var(--glass-depth)); backdrop-filter: blur(12px); border: 1px solid var(--glass-border); }')
A('.glass-card-lg { padding: 24px; border-radius: var(--radius-lg); background: rgba(255,255,255,var(--glass-depth)); backdrop-filter: blur(20px); border: 1px solid var(--glass-border); }')
A('.glass-card-xl { padding: 32px; border-radius: calc(var(--radius-lg) * 1.5); background: rgba(255,255,255,var(--glass-depth)); backdrop-filter: blur(32px); border: 1px solid var(--glass-border); }')

# Responsive typography
A('.text-xs { font-size: 10px; }')
A('.text-sm { font-size: 12px; }')
A('.text-base { font-size: var(--font-size-base); }')
A('.text-lg { font-size: 16px; }')
A('.text-xl { font-size: 20px; }')
A('.text-2xl { font-size: 24px; }')
A('.text-3xl { font-size: 32px; }')
A('.text-4xl { font-size: 40px; }')
A('.font-light { font-weight: 300; }')
A('.font-normal { font-weight: 400; }')
A('.font-medium { font-weight: 500; }')
A('.font-semibold { font-weight: 600; }')
A('.font-bold { font-weight: 700; }')
A('.font-extrabold { font-weight: 900; }')

# Sizing
A('.w-full { width: 100%; }')
A('.h-full { height: 100%; }')
A('.max-w-sm { max-width: 480px; }')
A('.max-w-md { max-width: 640px; }')
A('.max-w-lg { max-width: 820px; }')
A('.max-w-xl { max-width: 1024px; }')
A('.min-w-0 { min-width: 0; }')

# Padding/Margin scale
for i in [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 24, 28, 32]:
    A(f'.p-{i} {{ padding: {i}px; }}')
    A(f'.px-{i} {{ padding-left: {i}px; padding-right: {i}px; }}')
    A(f'.py-{i} {{ padding-top: {i}px; padding-bottom: {i}px; }}')
    A(f'.m-{i} {{ margin: {i}px; }}')
    A(f'.mx-{i} {{ margin-left: {i}px; margin-right: {i}px; }}')
    A(f'.my-{i} {{ margin-top: {i}px; margin-bottom: {i}px; }}')

# Display utilities
A('.block { display: block; }')
A('.inline { display: inline; }')
A('.inline-block { display: inline-block; }')
A('.flex { display: flex; }')
A('.inline-flex { display: inline-flex; }')
A('.grid { display: grid; }')
A('.hidden { display: none; }')
A('.flex-row { flex-direction: row; }')
A('.flex-col { flex-direction: column; }')
A('.flex-wrap { flex-wrap: wrap; }')
A('.flex-1 { flex: 1; }')
A('.flex-shrink-0 { flex-shrink: 0; }')
A('.items-start { align-items: flex-start; }')
A('.items-center { align-items: center; }')
A('.items-end { align-items: flex-end; }')
A('.justify-start { justify-content: flex-start; }')
A('.justify-center { justify-content: center; }')
A('.justify-end { justify-content: flex-end; }')
A('.justify-between { justify-content: space-between; }')
A('.gap-0 { gap: 0; }')
A('.self-start { align-self: flex-start; }')
A('.self-end { align-self: flex-end; }')
A('.self-center { align-self: center; }')

# Border radius
A('.rounded-sm { border-radius: var(--radius-sm); }')
A('.rounded-md { border-radius: var(--radius-md); }')
A('.rounded-lg { border-radius: var(--radius-lg); }')
A('.rounded-xl { border-radius: calc(var(--radius-lg) * 1.5); }')
A('.rounded-full { border-radius: 9999px; }')
A('.border { border: 1px solid var(--glass-border); }')
A('.border-t { border-top: 1px solid var(--glass-border); }')
A('.border-b { border-bottom: 1px solid var(--glass-border); }')
A('.border-l { border-left: 1px solid var(--glass-border); }')
A('.border-r { border-right: 1px solid var(--glass-border); }')

# Overflow
A('.overflow-hidden { overflow: hidden; }')
A('.overflow-auto { overflow: auto; }')
A('.overflow-y-auto { overflow-y: auto; }')
A('.overflow-x-auto { overflow-x: auto; }')
A('.overflow-ellipsis { text-overflow: ellipsis; }')
A('.whitespace-nowrap { white-space: nowrap; }')
A('.whitespace-pre-wrap { white-space: pre-wrap; }')

# Cursor
A('.cursor-pointer { cursor: pointer; }')
A('.cursor-default { cursor: default; }')
A('.cursor-not-allowed { cursor: not-allowed; }')
A('.pointer-events-none { pointer-events: none; }')
A('.select-none { user-select: none; }')
A('.select-text { user-select: text; }')

# Z-index scale
for i in range(1, 1000, 100):
    A(f'.z-{i} {{ z-index: {i}; }}')
A('.z-max { z-index: 99999; }')

# Misc
A('.no-scrollbar::-webkit-scrollbar { display: none; }')
A('.no-scrollbar { -ms-overflow-style: none; scrollbar-width: none; }')
A('.sr-only { position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0,0,0,0); white-space: nowrap; }')
A('.truncate-single { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }')
A('.truncate-multi { display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden; }')
A('.aspect-square { aspect-ratio: 1; }')
A('.aspect-video { aspect-ratio: 16 / 9; }')
A('.object-cover { object-fit: cover; }')
A('.object-contain { object-fit: contain; }')

# Dark overlay variants
A('.overlay-10 { background: rgba(0,0,0,0.1); }')
A('.overlay-20 { background: rgba(0,0,0,0.2); }')
A('.overlay-30 { background: rgba(0,0,0,0.3); }')
A('.overlay-40 { background: rgba(0,0,0,0.4); }')
A('.overlay-50 { background: rgba(0,0,0,0.5); }')
A('.overlay-60 { background: rgba(0,0,0,0.6); }')
A('.overlay-70 { background: rgba(0,0,0,0.7); }')
A('.overlay-80 { background: rgba(0,0,0,0.8); }')
A('.overlay-90 { background: rgba(0,0,0,0.9); }')

# Position
A('.absolute { position: absolute; }')
A('.relative { position: relative; }')
A('.fixed { position: fixed; }')
A('.sticky { position: sticky; }')
A('.inset-0 { top: 0; right: 0; bottom: 0; left: 0; }')
A('.top-0 { top: 0; }')
A('.bottom-0 { bottom: 0; }')
A('.left-0 { left: 0; }')
A('.right-0 { right: 0; }')

# Container queries simulation
A('.container-sm { max-width: 640px; margin: 0 auto; }')
A('.container-md { max-width: 820px; margin: 0 auto; }')
A('.container-lg { max-width: 1024px; margin: 0 auto; }')
A('.container-xl { max-width: 1280px; margin: 0 auto; }')

# Focus ring
A('.focus-ring { outline: none; }')
A('.focus-ring:focus-visible { outline: 2px solid var(--accent-5); outline-offset: 2px; }')
A('.focus-ring-inset:focus-visible { outline: 2px solid var(--accent-5); outline-offset: -2px; }')

# Button preset
A('.btn-glass { padding: 8px 20px; border-radius: var(--radius-sm); background: rgba(255,255,255,0.04); backdrop-filter: blur(8px); border: 1px solid var(--glass-border); color: var(--text-primary); cursor: pointer; transition: var(--transition); font-size: 13px; display: inline-flex; align-items: center; gap: 6px; }')
A('.btn-glass:hover { background: rgba(255,255,255,0.08); border-color: rgba(255,255,255,0.15); }')
A('.btn-primary { padding: 8px 20px; border-radius: var(--radius-sm); background: linear-gradient(135deg, #667eea, #764ba2); border: none; color: #fff; cursor: pointer; transition: var(--transition); font-size: 13px; display: inline-flex; align-items: center; gap: 6px; }')
A('.btn-primary:hover { box-shadow: 0 4px 20px rgba(102,126,234,0.4); transform: translateY(-1px); }')
A('.btn-danger { padding: 8px 20px; border-radius: var(--radius-sm); background: linear-gradient(135deg, #ff6b6b, #ee5a24); border: none; color: #fff; cursor: pointer; transition: var(--transition); font-size: 13px; }')
A('.btn-danger:hover { box-shadow: 0 4px 20px rgba(255,107,107,0.4); }')
A('.btn-ghost { padding: 8px 20px; border-radius: var(--radius-sm); background: transparent; border: none; color: var(--text-secondary); cursor: pointer; transition: var(--transition); font-size: 13px; }')
A('.btn-ghost:hover { background: rgba(255,255,255,0.04); color: var(--text-primary); }')
A('.btn-sm { padding: 4px 12px; font-size: 11px; }')
A('.btn-lg { padding: 12px 28px; font-size: 15px; }')
A('.btn-icon { width: 36px; height: 36px; padding: 0; display: flex; align-items: center; justify-content: center; }')

A('</style>')

# Insert before </body>
insertion = '\n'.join(extra)
content = content.replace('</body>', insertion + '\n</body>')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

line_count = content.count('\n')
print(f'Total lines: {line_count}')
