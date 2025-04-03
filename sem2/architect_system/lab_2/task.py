import re

with open('bad_words.txt') as f:
    bad_words = [line.strip() for line in f]

with open('conversation.txt') as f:
    text = f.read()

pattern = re.compile(r'\b(' + '|'.join(re.escape(word) for word in bad_words) + r')\b', re.I)
result = pattern.sub(lambda x: '*' * len(x.group()), text)

with open('conversation.txt', 'w') as f:
    f.write(result)