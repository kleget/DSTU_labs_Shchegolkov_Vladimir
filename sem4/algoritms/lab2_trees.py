from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Any


@dataclass
class Node:
    key: Any
    value: Any = None
    left: "Node | None" = None
    right: "Node | None" = None


class BinaryTree:
    def __init__(self) -> None:
        self.root: Node | None = None

    def is_empty(self) -> bool:
        return self.root is None

    def insert_as_leaf(self, key: Any) -> Node:
        node = Node(key)
        if not self.root:
            self.root = node
            return node

        q: deque[Node] = deque([self.root])
        while q:
            cur = q.popleft()
            if not cur.left:
                cur.left = node
                return node
            if not cur.right:
                cur.right = node
                return node
            q.extend([cur.left, cur.right])
        return node

    def find_node(self, key: Any) -> Node | None:
        if not self.root:
            return None
        q: deque[Node] = deque([self.root])
        while q:
            cur = q.popleft()
            if cur.key == key:
                return cur
            if cur.left:
                q.append(cur.left)
            if cur.right:
                q.append(cur.right)
        return None

    def contains(self, key: Any) -> bool:
        return self.find_node(key) is not None

    def delete(self, key: Any) -> bool:
        if not self.root:
            return False

        q: deque[tuple[Node, Node | None]] = deque([(self.root, None)])
        target: Node | None = None
        last: Node = self.root
        last_parent: Node | None = None

        while q:
            cur, parent = q.popleft()
            if cur.key == key and not target:
                target = cur
            last, last_parent = cur, parent
            if cur.left:
                q.append((cur.left, cur))
            if cur.right:
                q.append((cur.right, cur))

        if not target:
            return False

        target.key, target.value = last.key, last.value
        if last_parent is None:
            self.root = None
        elif last_parent.left is last:
            last_parent.left = None
        else:
            last_parent.right = None
        return True

    def _h(self, node: Node | None) -> int:
        return 0 if node is None else 1 + max(self._h(node.left), self._h(node.right))

    def node_height(self, key: Any) -> int:
        node = self.find_node(key)
        return -1 if node is None else self._h(node)

    def tree_height(self) -> int:
        return self._h(self.root)

    def count_nodes(self) -> int:
        return len(self.breadth_first())

    def _pre(self, node: Node | None, out: list[Any]) -> None:
        if not node:
            return
        out.append(node.key)
        self._pre(node.left, out)
        self._pre(node.right, out)

    def _ino(self, node: Node | None, out: list[Any]) -> None:
        if not node:
            return
        self._ino(node.left, out)
        out.append(node.key)
        self._ino(node.right, out)

    def _post(self, node: Node | None, out: list[Any]) -> None:
        if not node:
            return
        self._post(node.left, out)
        self._post(node.right, out)
        out.append(node.key)

    def preorder_recursive(self) -> list[Any]:
        out: list[Any] = []
        self._pre(self.root, out)
        return out

    def inorder_recursive(self) -> list[Any]:
        out: list[Any] = []
        self._ino(self.root, out)
        return out

    def postorder_recursive(self) -> list[Any]:
        out: list[Any] = []
        self._post(self.root, out)
        return out

    def preorder_iterative(self) -> list[Any]:
        if not self.root:
            return []
        out: list[Any] = []
        st = [self.root]
        while st:
            n = st.pop()
            out.append(n.key)
            if n.right:
                st.append(n.right)
            if n.left:
                st.append(n.left)
        return out

    def inorder_iterative(self) -> list[Any]:
        out: list[Any] = []
        st: list[Node] = []
        cur = self.root
        while cur or st:
            while cur:
                st.append(cur)
                cur = cur.left
            cur = st.pop()
            out.append(cur.key)
            cur = cur.right
        return out

    def postorder_iterative(self) -> list[Any]:
        if not self.root:
            return []
        st1 = [self.root]
        st2: list[Node] = []
        while st1:
            n = st1.pop()
            st2.append(n)
            if n.left:
                st1.append(n.left)
            if n.right:
                st1.append(n.right)
        return [n.key for n in reversed(st2)]

    def breadth_first(self) -> list[Any]:
        if not self.root:
            return []
        out: list[Any] = []
        q: deque[Node] = deque([self.root])
        while q:
            cur = q.popleft()
            out.append(cur.key)
            if cur.left:
                q.append(cur.left)
            if cur.right:
                q.append(cur.right)
        return out

    def pretty(self) -> str:
        if not self.root:
            return "(empty)"
        lines: list[str] = []

        def walk(node: Node | None, level: int) -> None:
            if not node:
                return
            walk(node.right, level + 1)
            lines.append("    " * level + str(node.key))
            walk(node.left, level + 1)

        walk(self.root, 0)
        return "\n".join(lines)


class BST(BinaryTree):
    def __init__(self, allow_duplicates: bool) -> None:
        super().__init__()
        self.allow_duplicates = allow_duplicates

    def _go_left(self, key: Any, cur_key: Any) -> bool:
        return key < cur_key

    def insert(self, key: Any, value: Any = None) -> bool:
        if not self.root:
            self.root = Node(key, value)
            return True

        cur = self.root
        while True:
            if key == cur.key and not self.allow_duplicates:
                cur.value = value if value is not None else cur.value
                return False

            if self._go_left(key, cur.key):
                if not cur.left:
                    cur.left = Node(key, value)
                    return True
                cur = cur.left
            else:
                if not cur.right:
                    cur.right = Node(key, value)
                    return True
                cur = cur.right

    def find_node(self, key: Any) -> Node | None:
        cur = self.root
        while cur:
            if key == cur.key:
                return cur
            cur = cur.left if self._go_left(key, cur.key) else cur.right
        return None

    def _delete_rec(self, node: Node | None, key: Any) -> tuple[Node | None, bool]:
        if not node:
            return None, False
        if key < node.key:
            node.left, ok = self._delete_rec(node.left, key)
            return node, ok
        if key > node.key:
            node.right, ok = self._delete_rec(node.right, key)
            return node, ok

        if not node.left:
            return node.right, True
        if not node.right:
            return node.left, True

        succ_parent = node
        succ = node.right
        while succ.left:
            succ_parent, succ = succ, succ.left

        node.key, node.value = succ.key, succ.value
        if succ_parent.left is succ:
            succ_parent.left = succ.right
        else:
            succ_parent.right = succ.right
        return node, True

    def delete(self, key: Any) -> bool:
        self.root, ok = self._delete_rec(self.root, key)
        return ok

    def min_key(self) -> Any:
        cur = self.root
        while cur and cur.left:
            cur = cur.left
        return None if cur is None else cur.key

    def max_key(self) -> Any:
        cur = self.root
        while cur and cur.right:
            cur = cur.right
        return None if cur is None else cur.key

    def inorder_items(self) -> list[tuple[Any, Any]]:
        out: list[tuple[Any, Any]] = []

        def walk(node: Node | None) -> None:
            if not node:
                return
            walk(node.left)
            out.append((node.key, node.value))
            walk(node.right)

        walk(self.root)
        return out

    def split(self, key: Any) -> tuple["BST", "BST"]:
        left = BST(self.allow_duplicates)
        right = BST(self.allow_duplicates)
        for k, v in self.inorder_items():
            (left if k <= key else right).insert(k, v)
        return left, right

    def merge(self, other: "BST") -> "BST":
        merged = BST(self.allow_duplicates)
        for k, v in self.inorder_items() + other.inorder_items():
            merged.insert(k, v)
        return merged

    def add_as_root(self, key: Any, value: Any = None) -> bool:
        if not self.root:
            self.root = Node(key, value)
            return True

        mn, mx = self.min_key(), self.max_key()
        if key < mn or (self.allow_duplicates and key <= mn):
            self.root = Node(key, value, right=self.root)
            return True
        if key > mx:
            self.root = Node(key, value, left=self.root)
            return True
        return False

    def _find_with_bounds(self, key: Any) -> tuple[Node | None, Any, Any]:
        cur = self.root
        low = high = None
        while cur:
            if key == cur.key:
                return cur, low, high
            if key < cur.key:
                high, cur = cur.key, cur.left
            else:
                low, cur = cur.key, cur.right
        return None, None, None

    def _collect(self, root: Node | None) -> list[tuple[Any, Any]]:
        out: list[tuple[Any, Any]] = []

        def walk(node: Node | None) -> None:
            if not node:
                return
            walk(node.left)
            out.append((node.key, node.value))
            walk(node.right)

        walk(root)
        return out

    def _build_from_items(self, items: list[tuple[Any, Any]]) -> Node | None:
        tmp = BST(self.allow_duplicates)
        for k, v in items:
            tmp.insert(k, v)
        return tmp.root

    def add_internal(self, parent_key: Any, key: Any, side: str, value: Any = None) -> bool:
        if side not in ("left", "right"):
            return False
        parent, low, high = self._find_with_bounds(parent_key)
        if not parent:
            return False
        if not self.allow_duplicates and self.find_node(key):
            return False

        if side == "left":
            if not (key < parent.key):
                return False
            if low is not None and not (key > low):
                return False
            old = self._collect(parent.left)
        else:
            if not (key > parent.key or (self.allow_duplicates and key >= parent.key)):
                return False
            if high is not None and not (key < high):
                return False
            old = self._collect(parent.right)

        left_items: list[tuple[Any, Any]] = []
        right_items: list[tuple[Any, Any]] = []
        for k, v in old:
            if k < key:
                left_items.append((k, v))
            elif k > key:
                right_items.append((k, v))
            elif self.allow_duplicates:
                right_items.append((k, v))

        node = Node(key, value, self._build_from_items(left_items), self._build_from_items(right_items))
        if side == "left":
            parent.left = node
        else:
            parent.right = node
        return True


class BSTUnique(BST):
    def __init__(self) -> None:
        super().__init__(allow_duplicates=False)


class BSTMulti(BST):
    def __init__(self) -> None:
        super().__init__(allow_duplicates=True)


class SimpleSet:
    def __init__(self, values: list[int] | None = None) -> None:
        self.tree = BSTUnique()
        for x in values or []:
            self.tree.insert(x)

    def is_empty(self) -> bool:
        return self.tree.is_empty()

    def add(self, x: int) -> bool:
        return self.tree.insert(x)

    def remove(self, x: int) -> bool:
        return self.tree.delete(x)

    def contains(self, x: int) -> bool:
        return self.tree.contains(x)

    def values(self) -> list[int]:
        return self.tree.inorder_iterative()

    def intersection(self, other: "SimpleSet") -> "SimpleSet":
        return SimpleSet([x for x in self.values() if other.contains(x)])

    def union(self, other: "SimpleSet") -> "SimpleSet":
        return SimpleSet(self.values() + other.values())

    def difference(self, other: "SimpleSet") -> "SimpleSet":
        return SimpleSet([x for x in self.values() if not other.contains(x)])


class SimpleMultiSet:
    def __init__(self, values: list[int] | None = None) -> None:
        self.tree = BSTMulti()
        for x in values or []:
            self.tree.insert(x)

    def is_empty(self) -> bool:
        return self.tree.is_empty()

    def add(self, x: int) -> bool:
        return self.tree.insert(x)

    def remove(self, x: int) -> bool:
        return self.tree.delete(x)

    def contains(self, x: int) -> bool:
        return self.tree.contains(x)

    def values(self) -> list[int]:
        return self.tree.inorder_iterative()

    def _count(self) -> dict[int, int]:
        c: dict[int, int] = {}
        for x in self.values():
            c[x] = c.get(x, 0) + 1
        return c

    def intersection(self, other: "SimpleMultiSet") -> "SimpleMultiSet":
        a, b = self._count(), other._count()
        out: list[int] = []
        for x in a:
            out.extend([x] * min(a[x], b.get(x, 0)))
        return SimpleMultiSet(out)

    def union(self, other: "SimpleMultiSet") -> "SimpleMultiSet":
        a, b = self._count(), other._count()
        out: list[int] = []
        for x in sorted(set(a) | set(b)):
            out.extend([x] * max(a.get(x, 0), b.get(x, 0)))
        return SimpleMultiSet(out)

    def difference(self, other: "SimpleMultiSet") -> "SimpleMultiSet":
        a, b = self._count(), other._count()
        out: list[int] = []
        for x in a:
            out.extend([x] * max(0, a[x] - b.get(x, 0)))
        return SimpleMultiSet(out)


class SimpleMap:
    def __init__(self) -> None:
        self.tree = BSTUnique()

    def is_empty(self) -> bool:
        return self.tree.is_empty()

    def put(self, key: Any, value: Any) -> None:
        node = self.tree.find_node(key)
        if node:
            node.value = value
        else:
            self.tree.insert(key, value)

    def get(self, key: Any) -> Any:
        node = self.tree.find_node(key)
        return None if node is None else node.value

    def contains_key(self, key: Any) -> bool:
        return self.tree.find_node(key) is not None

    def remove(self, key: Any) -> bool:
        return self.tree.delete(key)

    def items(self) -> list[tuple[Any, Any]]:
        return self.tree.inorder_items()


def is_bst_unique_tree(tree: BinaryTree) -> bool:
    def check(node: Node | None, low: Any, high: Any) -> bool:
        if not node:
            return True
        if low is not None and node.key <= low:
            return False
        if high is not None and node.key >= high:
            return False
        return check(node.left, low, node.key) and check(node.right, node.key, high)

    return check(tree.root, None, None)
