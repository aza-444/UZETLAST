import os

files_to_fix = [
    '/home/aza/Music/Shuni-Python/media/partners/elektroizol.svg',
    '/home/aza/Music/Shuni-Python/media/partners/akhan.svg'
]

for file_path in files_to_fix:
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Replace white fills with dark gray
        content = content.replace('fill="white"', 'fill="#333333"')
        content = content.replace('fill="#ffffff"', 'fill="#333333"')
        content = content.replace('fill="#FFFFFF"', 'fill="#333333"')
        
        with open(file_path, 'w') as f:
            f.write(content)
        print(f"Fixed {file_path}")
    else:
        print(f"File not found: {file_path}")
