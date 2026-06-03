path = r'C:\Users\gamju\AppData\Local\Temp\opencode\SXIGOai.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

blocks = []
def B(s):
    blocks.append(s)

# Generate ~1500 lines of additional content
B('<style>')
B('/* === V2.0 Complete Utility Suite === */')

# Pixel-scale utilities (0-100)
for i in range(0, 101, 2):
    B(f'.w-{i} {{ width: {i}px; }}')
    B(f'.h-{i} {{ height: {i}px; }}')
    B(f'.max-w-{i} {{ max-width: {i}px; }}')
    B(f'.min-w-{i} {{ min-width: {i}px; }}')
    if i <= 32:
        B(f'.rounded-{i} {{ border-radius: {i}px; }}')
        B(f'.gap-{i} {{ gap: {i}px; }}')
        B(f'.p-{i} {{ padding: {i}px; }}')

# Opacity scale
for i in range(0, 11):
    B(f'.opacity-{i*10} {{ opacity: {i/10}; }}')

# Border width
for i in range(1, 6):
    B(f'.border-{i} {{ border-width: {i}px; }}')

# Blur
for i in [1, 2, 4, 8, 12, 16, 20, 24, 32, 48, 64]:
    B(f'.blur-{i} {{ backdrop-filter: blur({i}px); -webkit-backdrop-filter: blur({i}px); }}')

# Scale transforms
for i in range(5, 20):
    s = i / 10
    B(f'.scale-{i*10} {{ transform: scale({s}); }}')

# Rotate
for i in range(0, 360, 45):
    B(f'.rotate-{i} {{ transform: rotate({i}deg); }}')
    B(f'.rotate-neg-{i} {{ transform: rotate(-{i}deg); }}')

# Translate
for i in [5, 10, 15, 20, 25, 30, 40, 50]:
    B(f'.translate-x-{i} {{ transform: translateX({i}px); }}')
    B(f'.translate-y-{i} {{ transform: translateY({i}px); }}')
    B(f'.translate-x-neg-{i} {{ transform: translateX(-{i}px); }}')
    B(f'.translate-y-neg-{i} {{ transform: translateY(-{i}px); }}')

# Overflow combinations
B('.overflow-visible { overflow: visible; }')
B('.overflow-scroll { overflow: scroll; }')
B('.overflow-x-hidden { overflow-x: hidden; }')
B('.overflow-y-hidden { overflow-y: hidden; }')
B('.overflow-x-scroll { overflow-x: scroll; }')
B('.overflow-y-scroll { overflow-y: scroll; }')

# Box-sizing
B('.border-box { box-sizing: border-box; }')
B('.content-box { box-sizing: content-box; }')

# List styles
B('.list-none { list-style: none; }')
B('.list-disc { list-style: disc; }')
B('.list-decimal { list-style: decimal; }')
B('.list-inside { list-style-position: inside; }')

# Table styles
B('.table-auto { table-layout: auto; }')
B('.table-fixed { table-layout: fixed; }')
B('.border-collapse { border-collapse: collapse; }')

# Text decoration
B('.underline { text-decoration: underline; }')
B('.line-through { text-decoration: line-through; }')
B('.no-underline { text-decoration: none; }')
B('.italic { font-style: italic; }')
B('.not-italic { font-style: normal; }')
B('.uppercase { text-transform: uppercase; }')
B('.lowercase { text-transform: lowercase; }')
B('.capitalize { text-transform: capitalize; }')
B('.normal-case { text-transform: none; }')

# Text align
B('.text-left { text-align: left; }')
B('.text-right { text-align: right; }')
B('.text-center { text-align: center; }')
B('.text-justify { text-align: justify; }')

# Whitespace
B('.whitespace-normal { white-space: normal; }')
B('.whitespace-pre { white-space: pre; }')
B('.whitespace-pre-line { white-space: pre-line; }')
B('.whitespace-pre-wrap { white-space: pre-wrap; }')

# Word break
B('.break-normal { word-break: normal; }')
B('.break-words { word-break: break-word; }')
B('.break-all { word-break: break-all; }')
B('.keep-all { word-break: keep-all; }')

# Vertical align
B('.align-baseline { vertical-align: baseline; }')
B('.align-top { vertical-align: top; }')
B('.align-middle { vertical-align: middle; }')
B('.align-bottom { vertical-align: bottom; }')

# Flex basis
for i in range(0, 101, 10):
    B(f'.flex-basis-{i} {{ flex-basis: {i}%; }}')
    B(f'.basis-{i} {{ flex-basis: {i}%; }}')

# Flex grow/shrink
B('.flex-grow { flex-grow: 1; }')
B('.flex-grow-0 { flex-grow: 0; }')
B('.flex-shrink { flex-shrink: 1; }')
B('.flex-shrink-0 { flex-shrink: 0; }')
B('.order-first { order: -9999; }')
B('.order-last { order: 9999; }')
for i in range(0, 13):
    B(f'.order-{i} {{ order: {i}; }}')

# Grid
B('.grid-cols-1 { grid-template-columns: repeat(1, 1fr); }')
B('.grid-cols-2 { grid-template-columns: repeat(2, 1fr); }')
B('.grid-cols-3 { grid-template-columns: repeat(3, 1fr); }')
B('.grid-cols-4 { grid-template-columns: repeat(4, 1fr); }')
B('.grid-cols-5 { grid-template-columns: repeat(5, 1fr); }')
B('.grid-cols-6 { grid-template-columns: repeat(6, 1fr); }')
B('.grid-cols-12 { grid-template-columns: repeat(12, 1fr); }')
B('.col-span-1 { grid-column: span 1; }')
B('.col-span-2 { grid-column: span 2; }')
B('.col-span-3 { grid-column: span 3; }')
B('.col-span-4 { grid-column: span 4; }')
B('.col-span-6 { grid-column: span 6; }')
B('.col-span-12 { grid-column: span 12; }')
B('.col-span-full { grid-column: 1 / -1; }')
B('.row-span-1 { grid-row: span 1; }')
B('.row-span-2 { grid-row: span 2; }')
B('.row-span-3 { grid-row: span 3; }')

# Place content/items/self
B('.place-center { place-items: center; }')
B('.place-start { place-items: start; }')
B('.place-end { place-items: end; }')
B('.place-stretch { place-items: stretch; }')
B('.content-center { align-content: center; }')
B('.content-start { align-content: start; }')
B('.content-end { align-content: end; }')
B('.content-between { align-content: space-between; }')
B('.content-around { align-content: space-around; }')
B('.content-evenly { align-content: space-evenly; }')
B('.items-stretch { align-items: stretch; }')
B('.justify-items-start { justify-items: start; }')
B('.justify-items-end { justify-items: end; }')
B('.justify-items-center { justify-items: center; }')
B('.justify-items-stretch { justify-items: stretch; }')

# Float
B('.float-right { float: right; }')
B('.float-left { float: left; }')
B('.float-none { float: none; }')
B('.clearfix::after { content: ""; display: table; clear: both; }')

# Visibility
B('.visible { visibility: visible; }')
B('.invisible { visibility: hidden; }')
B('.collapse { visibility: collapse; }')

B('</style>')

insertion = '\n'.join(blocks)
content = content.replace('</body>', insertion + '\n</body>')

# Fix any duplicate endings
last_body = content.rfind('</body>')
last_html = content.rfind('</html>')
if last_body > last_html:
    content = content[:last_body + 7] + '\n</html>\n'

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

line_count = content.count('\n')
print(f'Total lines: {line_count}')
