import re

with open('/home/aza/Music/Shuni-Python/templates/main/_navbar.html', 'r') as f:
    content = f.read()

# Replace any newlines before endif or inside simple tags.
# Specifically fixing the broken endif tags
content = re.sub(r'\{%\s*\n\s*endif\s*%\}', '{% endif %}', content)

with open('/home/aza/Music/Shuni-Python/templates/main/_navbar.html', 'w') as f:
    f.write(content)
print("Syntax fixed")
