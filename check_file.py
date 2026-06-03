path = r'C:\Users\gamju\AppData\Local\Temp\opencode\SXIGOai.html'
with open(path, 'r', encoding='utf-8-sig') as f:
    lines = f.readlines()
print(f'Total lines: {len(lines)}')
print('First 10 lines:')
for i, line in enumerate(lines[:10]):
    print(f'{i+1}: {line.rstrip()[:120]}')
has_html = any('<html' in l for l in lines)
has_body = any('<body' in l for l in lines)
has_end_html = any('</html>' in l for l in lines)
has_end_body = any('</body>' in l for l in lines)
has_style = any('<style>' in l for l in lines)
has_doctype = any('DOCTYPE' in l for l in lines)
print(f'Has DOCTYPE: {has_doctype}')
print(f'Has html tag: {has_html}')
print(f'Has body tag: {has_body}')
print(f'Has /html tag: {has_end_html}')
print(f'Has /body tag: {has_end_body}')
print(f'Has style tag: {has_style}')
