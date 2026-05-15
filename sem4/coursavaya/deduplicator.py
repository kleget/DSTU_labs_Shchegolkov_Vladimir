import re
from collections import Counter, defaultdict


WORD_RE = re.compile(r"[A-Za-zА-Яа-яЁё]+")


def norm(word):
    return word.lower().replace("ё", "е")


def levenshtein(a, b):
    if len(a) < len(b):
        a, b = b, a
    row = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        new_row = [i]
        for j, cb in enumerate(b, 1):
            new_row.append(min(
                row[j] + 1,
                new_row[j - 1] + 1,
                row[j - 1] + (ca != cb),
            ))
        row = new_row
    return row[-1]


class DSU:
    def __init__(self, n):
        self.parent = list(range(n))

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, a, b):
        a = self.find(a)
        b = self.find(b)
        if a != b:
            self.parent[b] = a


def read_words(text):
    """Понимает обычный текст и строки вида: word 5 / word,5 / word;5."""
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    counts = Counter()
    dict_mode = bool(lines)

    for line in lines:
        parts = re.split(r"[\s,;]+", line)
        if len(parts) == 1 and WORD_RE.fullmatch(parts[0]):
            counts[norm(parts[0])] += 1
        elif len(parts) == 2 and WORD_RE.fullmatch(parts[0]) and parts[1].isdigit():
            counts[norm(parts[0])] += int(parts[1])
        else:
            dict_mode = False
            break

    if dict_mode:
        return counts
    return Counter(norm(word) for word in WORD_RE.findall(text))


def deduplicate(text, max_dist=2, min_len=5, prefix_len=2):
    counts = read_words(text)
    words = sorted(counts.items(), key=lambda x: (-x[1], x[0]))
    dsu = DSU(len(words))
    buckets = defaultdict(list)

    for i, (word, _) in enumerate(words):
        if len(word) >= min_len:
            buckets[(len(word), word[:prefix_len])].append(i)

    for i, (word, _) in enumerate(words):
        if len(word) < min_len:
            continue
        for length in (len(word) - 1, len(word), len(word) + 1):
            for j in buckets.get((length, word[:prefix_len]), []):
                if i < j and levenshtein(word, words[j][0]) <= max_dist:
                    dsu.union(i, j)

    groups = defaultdict(list)
    for i in range(len(words)):
        groups[dsu.find(i)].append(i)

    result = []
    merged = []
    for group in groups.values():
        group.sort(key=lambda i: (-words[i][1], words[i][0]))
        main = group[0]
        main_word, total = words[main]

        for i in group[1:]:
            dist = levenshtein(main_word, words[i][0])
            if dist <= max_dist:
                total += words[i][1]
                merged.append((words[i][0], words[i][1], main_word, dist))
            else:
                result.append(words[i])

        result.append((main_word, total))

    result.sort(key=lambda x: (-x[1], x[0]))
    return result, merged, len(words)
