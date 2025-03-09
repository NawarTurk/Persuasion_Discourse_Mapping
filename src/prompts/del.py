import os
count = ''
for file in sorted(os.listdir()):
    if file.endswith('.txt'):
        with open(file, 'r', encoding='utf-8') as textfile:
            content = textfile.read()
            count += f'Filename: {file}  char count: {len(content)}\n'

with open('char_count.txt', 'w') as f:
    f.write(count)

