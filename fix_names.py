import os
import glob

html_files = glob.glob('/home/aza/Music/Shuni-Python/templates/main/*.html')

for filepath in html_files:
    with open(filepath, 'r') as f:
        content = f.read()
        
    original = content
    # Replace uppercase
    content = content.replace("O'ZENERGOTAMINLASH", "O'ZENERGOTA'MINLASH")
    # Replace capitalized
    content = content.replace("O'zenergotaminlash", "O'zenergota'minlash")
    
    if content != original:
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"Updated {os.path.basename(filepath)}")

