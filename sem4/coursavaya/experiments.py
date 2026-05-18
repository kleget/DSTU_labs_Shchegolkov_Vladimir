"""
Исследовательская часть курсовой работы.
 
Цель: экспериментально показать, ЗАЧЕМ нужен алгоритм де-дупликации словаря
на основе DSU + расстояния Левенштейна и что он РЕАЛЬНО помогает:
 
  Эксперимент 1. Эффективность сжатия словаря на текстах с опечатками.
  Эксперимент 2. Ускорение за счёт бакетов (группировка по длине и префиксу)
                 против наивного перебора всех пар O(n^2).
  Эксперимент 3. Масштабируемость: время работы от разме-ра словаря.
  Эксперимент 4. Влияние порога расстояния Левенштейна на качество склейки.
 
Все числовые результаты сохраняются в results.json, гра-фики — в *.png.
"""
 
import json
import random
import time
from collections import Counter, defaultdict
 
from deduplicator import levenshtein, DSU, read_words, deduplicate
 
random.seed(42)
 
# --------------------------------------------------------------------------
# Генератор реалистичных данных: базовый словарь + слу-чайные опечатки
# --------------------------------------------------------------------------
 
BASE_WORDS = [
    "algorithm", "deduplication", "structure", "func-tion", "variable",
    "dictionary", "programming", "computer", "interface", "database",
    "processor", "memory", "network", "protocol", "com-piler",
    "iteration", "recursion", "complexity", "perfor-mance", "optimization",
    "container", "reference", "parameter", "argument", "exception",
    "inheritance", "polymorphism", "encapsulation", "ab-straction", "framework",
    "library", "module", "package", "repository", "docu-mentation",
    "implementation", "specification", "architecture", "component", "infrastructure",
]
 
 
def make_typo(word):
    """Вносит одну случайную опечатку: замена, вставка, удаление, перестановка."""
    if len(word) < 3:
        return word
    op = random.choice(["sub", "ins", "del", "swap"])
    i = random.randint(0, len(word) - 1)
    if op == "sub":
        c = random.choice("abcdefghijklmnopqrstuvwxyz")
        return word[:i] + c + word[i + 1:]
    if op == "ins":
        c = random.choice("abcdefghijklmnopqrstuvwxyz")
        return word[:i] + c + word[i:]
    if op == "del":
        return word[:i] + word[i + 1:]
    if op == "swap" and i < len(word) - 1:
        return word[:i] + word[i + 1] + word[i] + word[i + 2:]
    return word
 
 
def generate_corpus(n_unique, typo_rate=0.35, copies_per_word=8):
    """
    Строит «грязный» словарь: каждое базовое слово встре-чается несколько раз,
    часть вхождений — с опечатками. Возвращает текст в формате 'слово частота'.
    """
    base = []
    while len(base) < n_unique:
        base.extend(BASE_WORDS)
    base = base[:n_unique]
    # делаем базовые слова уникальными суффиксом, чтобы их было ровно n_unique
    base = [w + ("" if k < len(BASE_WORDS) else str(k // len(BASE_WORDS)))
            for k, w in enumerate(base)]
 
    counter = Counter()
    for word in base:
        for _ in range(copies_per_word):
            if random.random() < typo_rate:
                counter[make_typo(word)] += 1
            else:
                counter[word] += 1
    lines = [f"{w} {c}" for w, c in counter.items()]
    random.shuffle(lines)
    return "\n".join(lines), len(base)
 
 
# --------------------------------------------------------------------------
# Наивная дедупликация: перебор ВСЕХ пар O(n^2), без ба-кетов.
# Нужна как точка отсчёта, чтобы показать выигрыш оптими-зированной версии.
# --------------------------------------------------------------------------
 
def deduplicate_naive(text, max_dist=2, min_len=5):
    counts = read_words(text)
    words = sorted(counts.items(), key=lambda x: (-x[1], x[0]))
    dsu = DSU(len(words))
    comparisons = 0
    for i in range(len(words)):
        if len(words[i][0]) < min_len:
            continue
        for j in range(i + 1, len(words)):
            if len(words[j][0]) < min_len:
                continue
            comparisons += 1
            if levenshtein(words[i][0], words[j][0]) <= max_dist:
                dsu.union(i, j)
    groups = defaultdict(list)
    for i in range(len(words)):
        groups[dsu.find(i)].append(i)
    return len(groups), comparisons
 
 
def deduplicate_counting(text, max_dist=2, min_len=5, prefix_len=2):
    """Копия оптимизированного алгоритма со счётчиком вы-зовов Левенштейна."""
    counts = read_words(text)
    words = sorted(counts.items(), key=lambda x: (-x[1], x[0]))
    dsu = DSU(len(words))
    buckets = defaultdict(list)
    comparisons = 0
    for i, (word, _) in enumerate(words):
        if len(word) >= min_len:
            buckets[(len(word), word[:prefix_len])].append(i)
    for i, (word, _) in enumerate(words):
        if len(word) < min_len:
            continue
        for length in (len(word) - 1, len(word), len(word) + 1):
            for j in buckets.get((length, word[:prefix_len]), []):
                if i < j:
                    comparisons += 1
                    if levenshtein(word, words[j][0]) <= max_dist:
                        dsu.union(i, j)
    groups = defaultdict(list)
    for i in range(len(words)):
        groups[dsu.find(i)].append(i)
    return len(groups), comparisons
 
 
# --------------------------------------------------------------------------
# Эксперимент 1. Эффективность сжатия словаря
# --------------------------------------------------------------------------
 
def experiment_compression():
    rates = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6]
    rows = []
    for r in rates:
        text, n_base = generate_corpus(40, typo_rate=r, copies_per_word=12)
        result, merged, before = deduplicate(text, max_dist=2)
        after = len(result)
        rows.append({
            "typo_rate": r,
            "before": before,
            "after": after,
            "merged": len(merged),
            "reduction_pct": round(100 * (before - after) / before, 1),
        })
    return rows
 
 
# --------------------------------------------------------------------------
# Эксперимент 2 и 3. Производительность и масштабируе-мость
# --------------------------------------------------------------------------
 
def experiment_performance():
    sizes = [20, 40, 80, 160, 320, 640]
    rows = []
    for n in sizes:
        text, _ = generate_corpus(n, typo_rate=0.35, copies_per_word=10)
 
        t0 = time.perf_counter()
        g_opt, cmp_opt = deduplicate_counting(text, max_dist=2)
        t_opt = time.perf_counter() - t0
 
        t0 = time.perf_counter()
        g_naive, cmp_naive = deduplicate_naive(text, max_dist=2)
        t_naive = time.perf_counter() - t0
 
        # размер реального (грязного) словаря
        dict_size = len(read_words(text))
        rows.append({
            "dict_size": dict_size,
            "time_naive_ms": round(t_naive * 1000, 2),
            "time_opt_ms": round(t_opt * 1000, 2),
            "cmp_naive": cmp_naive,
            "cmp_opt": cmp_opt,
            "speedup": round(t_naive / t_opt, 2) if t_opt > 0 else None,
            "cmp_ratio": round(cmp_naive / cmp_opt, 2) if cmp_opt > 0 else None,
        })
    return rows
 
 
# --------------------------------------------------------------------------
# Эксперимент 4. Влияние порога расстояния Левенштейна
# --------------------------------------------------------------------------
 
def experiment_threshold():
    text, n_base = generate_corpus(40, typo_rate=0.4, copies_per_word=12)
    rows = []
    for d in (0, 1, 2, 3, 4):
        result, merged, before = deduplicate(text, max_dist=d)
        rows.append({
            "max_dist": d,
            "before": before,
            "after": len(result),
            "merged": len(merged),
        })
    return rows
 
 
if __name__ == "__main__":
    data = {
        "compression": experiment_compression(),
        "performance": experiment_performance(),
        "threshold": experiment_threshold(),
    }
    with open("results.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
 
    print("=== Эксперимент 1: сжатие словаря ===")
    for r in data["compression"]:
        print(r)
    print("\n=== Эксперимент 2-3: производительность ===")
    for r in data["performance"]:
        print(r)
    print("\n=== Эксперимент 4: порог расстояния ===")
    for r in data["threshold"]:
        print(r)
