import re
path = r'C:\Users\gamju\AppData\Local\Temp\opencode\add_more_content.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()
# Find lines with ' + word + ' where word is not defined Python var
# We look for the pattern inside Python strings
lines = content.split('\n')
for i, line in enumerate(lines, 1):
    # Skip comments
    if line.strip().startswith('#'):
        continue
    # Find ' + varname + ' patterns
    matches = re.findall(r"' \+ (\w+) \+ '", line)
    for m in matches:
        # Check if this is a Python variable or JS variable
        # Python keywords and common vars
        py_vars = {'i', 'idx', 'm', 'f', 'item', 'div', 'btn', 'c', 'e', 'r', 't', 'val', 'name', 'id', 'type', 'tag', 'el'}
        # If it looks like a Python string building a JS string, the pattern should be ' + ' + varname + ' + '
        # If it's just ' + varname + ', it might be a problem
        if m in py_vars:
            print(f'Line {i}: possible issue with "{m}" -> {line.rstrip()[:120]}')
