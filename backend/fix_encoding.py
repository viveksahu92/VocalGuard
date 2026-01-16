import os
import codecs

# Fix all Python files in current directory
for filename in os.listdir('.'):
    if filename.endswith('.py'):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Decode unicode escape sequences
            content = content.encode('utf-8').decode('unicode_escape')
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"Fixed: {filename}")
        except Exception as e:
            print(f"Error with {filename}: {e}")

print("Done fixing all files!")
