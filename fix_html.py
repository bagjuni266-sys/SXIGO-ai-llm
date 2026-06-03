import re, sys

path = r'C:\Users\gamju\AppData\Local\Temp\opencode\SXIGOai.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')
filtered = []
for line in lines:
    stripped = line.strip()
    if stripped.startswith("'") and (stripped.endswith("',") or stripped.endswith("'")):
        if len(stripped) > 2:
            inner = stripped[1:-2] if stripped.endswith("',") else stripped[1:-1]
            filtered.append(inner)
        else:
            filtered.append("")
    else:
        filtered.append(line)

# Also clean up empty lines at the end
while filtered and filtered[-1].strip() == '':
    filtered.pop()

with open(path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(filtered))

with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()
print(f'Total lines: {len(lines)}')
for i, line in enumerate(lines[-15:], max(0, len(lines)-14)):
    print(f'{i+1}: {line.rstrip()[:120]}')
