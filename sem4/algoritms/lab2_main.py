from __future__ import annotations

import sys

from lab2_trees import BSTMulti, BSTUnique, BinaryTree, SimpleMap, SimpleMultiSet, SimpleSet, is_bst_unique_tree


def setup_console_encoding() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")


def task_1() -> None:
    t = BinaryTree()
    for x in [10, 5, 15, 3, 7, 12]:
        t.insert_as_leaf(x)
    print("ЗАДАНИЕ 1")
    print(t.pretty())
    print("empty:", t.is_empty(), "contains 7:", t.contains(7), "height:", t.tree_height(), "count:", t.count_nodes())
    print("dfs rec:", t.preorder_recursive(), t.inorder_recursive(), t.postorder_recursive())
    print("dfs iter:", t.preorder_iterative(), t.inorder_iterative(), t.postorder_iterative())
    print("bfs:", t.breadth_first())
    print("delete 15:", t.delete(15))
    print(t.pretty(), "\n")


def task_2() -> None:
    t = BSTUnique()
    for x in [8, 3, 10, 1, 6, 14, 4, 7, 13]:
        t.insert(x)
    print("ЗАДАНИЕ 2")
    print("inorder:", t.inorder_iterative())
    print("insert duplicate 6:", t.insert(6), "delete 3:", t.delete(3))
    print("after:", t.inorder_iterative(), "\n")


def task_3() -> None:
    t = BSTMulti()
    for x in [8, 3, 10, 3, 6, 6, 14, 6, 10]:
        t.insert(x)
    print("ЗАДАНИЕ 3")
    print("before:", t.inorder_iterative())
    print("delete one 6:", t.delete(6))
    print("after:", t.inorder_iterative(), "\n")


def task_4() -> None:
    a, b = SimpleSet([1, 2, 3, 7, 8]), SimpleSet([3, 4, 5, 8])
    print("ЗАДАНИЕ 4")
    print("A:", a.values(), "B:", b.values())
    print("A∩B:", a.intersection(b).values(), "A∪B:", a.union(b).values(), "A\\B:", a.difference(b).values(), "\n")


def task_5() -> None:
    a, b = SimpleMultiSet([1, 1, 2, 3, 3, 3, 7]), SimpleMultiSet([1, 3, 3, 4, 7, 7])
    print("ЗАДАНИЕ 5")
    print("A:", a.values(), "B:", b.values())
    print("A∩B:", a.intersection(b).values(), "A∪B:", a.union(b).values(), "A\\B:", a.difference(b).values(), "\n")


def task_6() -> None:
    m = SimpleMap()
    m.put(10, "ten")
    m.put(5, "five")
    m.put(15, "fifteen")
    m.put(5, "FIVE")
    print("ЗАДАНИЕ 6")
    print("items:", m.items(), "get(10):", m.get(10), "contains 3:", m.contains_key(3), "remove 10:", m.remove(10))
    print("after:", m.items(), "\n")


def task_7() -> None:
    t = BSTUnique()
    for x in [8, 3, 10, 1, 6, 14, 4, 7, 13]:
        t.insert(x)
    l, r = t.split(7)
    merged = l.merge(r)
    print("ЗАДАНИЕ 7")
    print("src:", t.inorder_iterative())
    print("left:", l.inorder_iterative(), "right:", r.inorder_iterative(), "merge:", merged.inorder_iterative(), "\n")


def task_8() -> None:
    t = BSTUnique()
    for x in [10, 5, 15]:
        t.insert(x)
    print("ЗАДАНИЕ 8")
    print("before:\n" + t.pretty())
    print("add root 2:", t.add_as_root(2))
    print("add internal (10,right,12):", t.add_internal(10, 12, "right"))
    print("after:\n" + t.pretty(), "\n")


def task_9() -> None:
    t = BSTMulti()
    for x in [10, 10, 5, 5, 15, 12, 12]:
        t.insert(x)
    l, r = t.split(10)
    merged = l.merge(r)
    merged.add_as_root(1)
    merged.add_internal(10, 11, "right")
    print("ЗАДАНИЕ 9")
    print("src:", t.inorder_iterative())
    print("left:", l.inorder_iterative(), "right:", r.inorder_iterative(), "merge:", merged.inorder_iterative())
    print(merged.pretty(), "\n")


def task_10() -> None:
    bst = BSTUnique()
    for x in [8, 3, 10, 1, 6, 14]:
        bst.insert(x)
    ok = BinaryTree()
    ok.root = bst.root

    bad_bst = BSTUnique()
    for x in [8, 3, 10, 1, 6, 14]:
        bad_bst.insert(x)
    bad = BinaryTree()
    bad.root = bad_bst.root
    bad.root.left.key = 100  # type: ignore[union-attr]

    print("ЗАДАНИЕ 10")
    print("ok is BST:", is_bst_unique_tree(ok), "bad is BST:", is_bst_unique_tree(bad), "\n")


def run_all_tasks() -> None:
    for fn in [task_1, task_2, task_3, task_4, task_5, task_6, task_7, task_8, task_9, task_10]:
        fn()


if __name__ == "__main__":
    setup_console_encoding()
    run_all_tasks()
