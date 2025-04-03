import re

patern_phone = r'\+7\(\d{3}\)\d{3}-\d{2}-\d{2}'
patern_email = r'[\w\.-]+@[\w\.-]+\.\w+'
with open("laba3.txt", 'r') as file:
    text = file.read()
    print(re.findall(patern_phone, text))

with open("laba3_3.txt", 'r', encoding='utf-8') as file:
    text = file.read()

modified_text = re.sub(r'\d', '*', text)

with open("laba3_3moded.txt", 'w', encoding='utf-8') as file:
    file.write(modified_text)

with open("laba3_1.txt", 'r') as file1:
    email = file1.read()
    print(re.findall(patern_email, email))
