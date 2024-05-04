from typing import Optional, Tuple, Generator, Dict, Callable, List, Union

KeyType = Union[str, int, None]
ValueType = Union[str, int, None]


class TreeNode(object):
    def __init__(self, key: KeyType, value: ValueType,
                 left: Optional['TreeNode'] = None,
                 right: Optional['TreeNode'] = None) -> None:
        self.key: KeyType = key
        self.value: ValueType = value
        self.left: Optional['TreeNode'] = left
        self.right: Optional['TreeNode'] = right

    def __str__(self) -> str:
        return str(to_dict(self))

    def __eq__(self, other: object) -> bool:
        if other is None:
            return False
        return str(self) == str(other)


def cons(key: KeyType, value: ValueType, node: Optional[TreeNode]) -> TreeNode:
    if node is None:
        return TreeNode(key, value)
    if str(key) < str(node.key):
        return TreeNode(node.key, node.value,
                        left=cons(key, value, node.left), right=node.right)
    elif str(key) > str(node.key):
        return TreeNode(node.key, node.value,
                        left=node.left, right=cons(key, value, node.right))
    else:
        node.value = value
        return node


def remove(node: Optional[TreeNode], key: KeyType) -> Optional[TreeNode]:
    assert node is not None, "empty dictionary"
    if str(key) < str(node.key):
        return TreeNode(node.key, node.value,
                        left=remove(node.left, key), right=node.right)
    elif str(key) > str(node.key):
        return TreeNode(node.key, node.value,
                        left=node.left, right=remove(node.right, key))
    else:
        if node.left is None:
            return node.right
        elif node.right is None:
            return node.left
        else:
            successor = find_min(node.right)
            node.key = successor.key
            node.value = successor.value
            node.right = remove(node.right, successor.key)
            return node


def find_min(node: TreeNode) -> TreeNode:
    current = node
    while current.left:
        current = current.left
    return current


def size(node: Optional[TreeNode]) -> int:
    if node is None:
        return 0
    return 1 + size(node.left) + size(node.right)


def member(key: KeyType, node: Optional[TreeNode]) -> ValueType:
    # assert key is not None, 'key cannot be None'
    if node is None:
        return False
    if str(key) == str(node.key):
        return node.value
    elif str(key) < str(node.key):
        return member(key, node.left)
    else:
        return member(key, node.right)


def to_dict(node: Optional[TreeNode]) -> Dict[KeyType, ValueType]:
    if node is None:
        return {}
    return {**to_dict(node.left),
            node.key: node.value,
            **to_dict(node.right)}


def to_list(node: Optional[TreeNode]) -> List[Tuple[KeyType, ValueType]]:
    if node is None:
        return []
    return to_list(node.left) + [(node.key, node.value)] + to_list(node.right)


def from_dict(pydict: Dict[KeyType, ValueType]) -> Optional[TreeNode]:
    mydict: Optional[TreeNode] = None
    for key, value in pydict.items():
        mydict = cons(key, value, mydict)
    return mydict


def mfilter(node: Optional[TreeNode],
            f: Callable[[KeyType, ValueType], bool]) \
        -> Dict[KeyType, ValueType]:
    filtered_dict: Dict[KeyType, ValueType] = {}
    if node is None:
        return filtered_dict
    filtered_dict.update(mfilter(node.left, f))
    if f(node.key, node.value):
        filtered_dict[node.key] = node.value
    filtered_dict.update(mfilter(node.right, f))
    return filtered_dict


def mmap(node: Optional[TreeNode],
         f: Callable[[KeyType, ValueType],
         Tuple[KeyType, ValueType]]) -> Dict[KeyType, ValueType]:
    mapped_dict: Dict[KeyType, ValueType] = {}
    if node is None:
        return mapped_dict
    mapped_dict.update(mmap(node.left, f))
    mapped_key, mapped_value = f(node.key, node.value)
    mapped_dict[mapped_key] = mapped_value
    mapped_dict.update(mmap(node.right, f))
    return mapped_dict


def reduce(n: Optional[TreeNode],
           f: Callable[[KeyType, ValueType, int], int],
           initial_state: int) -> int:
    def _reduce(node: Optional[TreeNode], state: int) -> int:
        if node is None:
            return state
        state = _reduce(node.left, state)
        state = f(node.key, node.value, state)
        return _reduce(node.right, state)

    return _reduce(n, initial_state)


def iterator(node: Optional[TreeNode]) \
        -> Generator[Tuple[KeyType, ValueType], None, None]:
    stack: List[TreeNode] = []
    current: Optional[TreeNode] = node
    while current or stack:
        while current:
            stack.append(current)
            current = current.left
        current = stack.pop()
        assert current is not None
        yield current.key, current.value
        current = current.right


def concat(tree1_root: Optional[TreeNode],
           tree2_root: Optional[TreeNode]) -> Optional[TreeNode]:
    if tree1_root is None:
        return tree2_root
    if tree2_root is None:
        return tree1_root

    # Insert nodes from the second tree into the first tree
    def insert_node(root: Optional[TreeNode],
                    node: Optional[TreeNode]) -> Optional[TreeNode]:
        if node is None:
            return root
        return cons(node.key, node.value, root)

    # Recursively merge nodes from the second tree into the first tree
    def merge_trees(tree1: Optional[TreeNode],
                    tree2: Optional[TreeNode]) -> Optional[TreeNode]:
        if tree2 is None:
            return tree1
        tree1 = insert_node(tree1, tree2)
        tree1 = merge_trees(tree1, tree2.left)
        tree1 = merge_trees(tree1, tree2.right)
        return tree1

    # Merge the second tree into the first one
    return merge_trees(tree1_root, tree2_root)


def mempty() -> Optional[TreeNode]:
    return None
