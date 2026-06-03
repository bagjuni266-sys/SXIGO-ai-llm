import re
path = r'C:\Users\gamju\AppData\Local\Temp\opencode\add_more_content.py'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines, 1):
    stripped = line.strip()
    if not stripped or stripped.startswith('#'):
        continue
    # Look for ' + word + ' where word is likely a JS variable in a Python string context
    # This pattern means: string end ' then + varname + then string start '
    # which Python interprets as variable reference
    matches = re.findall(r"' \+ (\w+) \+ '", stripped)
    for m in matches:
        print(f'Line {i}: bare JS var "{m}" -> {stripped[:120]}')
