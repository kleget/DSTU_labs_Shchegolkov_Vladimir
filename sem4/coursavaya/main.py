import tkinter as tk
from tkinter import filedialog

from deduplicator import deduplicate


EXAMPLE = """algorithm 7
algoritm 2
algorithn 1
deduplication 5
dedublication 1
structure 4
strukture 2
banana 4
bananna 1
"""


def load_file():
    name = filedialog.askopenfilename(filetypes=[("Text", "*.txt *.csv"), ("All", "*.*")])
    if not name:
        return
    with open(name, encoding="utf-8") as file:
        source.delete("1.0", tk.END)
        source.insert(tk.END, file.read())


def run():
    result.delete("1.0", tk.END)
    text = source.get("1.0", tk.END)
    max_dist = int(distance_entry.get())
    cleaned, merged, old_count = deduplicate(text, max_dist=max_dist)

    result.insert(tk.END, f"Было уникальных слов: {old_count}\n")
    result.insert(tk.END, f"Стало уникальных слов: {len(cleaned)}\n\n")
    result.insert(tk.END, "ИТОГОВЫЙ СЛОВАРЬ:\n")
    for word, count in cleaned:
        result.insert(tk.END, f"{word}: {count}\n")

    result.insert(tk.END, "\nСКЛЕЙКИ:\n")
    for old_word, count, new_word, dist in merged:
        result.insert(tk.END, f"{old_word} ({count}) -> {new_word}, расстояние {dist}\n")


root = tk.Tk()
root.title("Дедупликация словаря")
root.geometry("900x600")

top = tk.Frame(root)
top.pack(fill=tk.X, padx=8, pady=8)

tk.Button(top, text="Открыть файл", command=load_file).pack(side=tk.LEFT)
tk.Button(top, text="Дедуплицировать", command=run).pack(side=tk.LEFT, padx=8)
tk.Label(top, text="Макс. расстояние:").pack(side=tk.LEFT)
distance_entry = tk.Entry(top, width=4)
distance_entry.insert(0, "2")
distance_entry.pack(side=tk.LEFT)

body = tk.Frame(root)
body.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

source = tk.Text(body, width=45)
source.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
source.insert(tk.END, EXAMPLE)

result = tk.Text(body, width=55)
result.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(8, 0))

root.mainloop()
