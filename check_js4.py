import re
path = r'C:\Users\gamju\AppData\Local\Temp\opencode\append_js4.py'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i, line in enumerate(lines, 1):
    matches = re.findall(r"' \+ (\w+) \+ '", line)
    for m in matches:
        print(f'Line {i}: issue with JS var "{m}" -> {line.rstrip()[:120]}')
