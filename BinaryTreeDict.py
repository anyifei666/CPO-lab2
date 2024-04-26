class TreeNode(object):
    def __init__(self, key, value, left=None, right=None):
        self.key = key
        self.value = value
        self.left = left
        self.right = right

    def __str__(self):
        return str(to_dict(self))

    def __eq__(self, other):
        if other is None:
            return False
        return str(self) == str(other)


def cons(key, value, node):
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


def remove(node, key):
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


def find_min(node):
    current = node
    while current.left:
        current = current.left
    return current


def size(node):
    if node is None:
        return 0
    return 1 + size(node.left) + size(node.right)


def member(key, node):
    # assert key is not None, 'key cannot be None'
    if node is None:
        return False
    if str(key) == str(node.key):
        return node.value
    elif str(key) < str(node.key):
        return member(key, node.left)
    else:
        return member(key, node.right)


def to_dict(node):
    if node is None:
        return {}
    return {**to_dict(node.left),
            node.key: node.value,
            **to_dict(node.right)}


def to_list(node):
    if node is None:
        return []
    return to_list(node.left) + [(node.key, node.value)] + to_list(node.right)


def from_dict(pydict):
    mydict = None
    for key, value in pydict.items():
        mydict = cons(key, value, mydict)
    return mydict


def mfilter(node, f):
    filtered_dict = {}
    if node is None:
        return filtered_dict
    filtered_dict.update(mfilter(node.left, f))
    if f(node.key, node.value):
        filtered_dict[node.key] = node.value
    filtered_dict.update(mfilter(node.right, f))
    return filtered_dict


def mmap(node, f):
    mapped_dict = {}
    if node is None:
        return mapped_dict
    mapped_dict.update(mmap(node.left, f))
    mapped_key, mapped_value = f(node.key, node.value)
    mapped_dict[mapped_key] = mapped_value
    mapped_dict.update(mmap(node.right, f))
    return mapped_dict


def reduce(n, f, initial_state):
    def _reduce(node, state):
        if node is None:
            return state
        state = _reduce(node.left, state)
        state = f(node.key, node.value, state)
        return _reduce(node.right, state)

    return _reduce(n, initial_state)


def iterator(node):
    stack = []
    current = node
    while current or stack:
        while current:
            stack.append(current)
            current = current.left
        current = stack.pop()
        yield current.key, current.value
        current = current.right


def concat(tree1_root, tree2_root):
    if tree1_root is None:
        return tree2_root
    if tree2_root is None:
        return tree1_root

    # 将第二棵树的节点逐个插入到第一棵树中
    def insert_node(root, node):
        if node is None:
            return root
        return cons(node.key, node.value, root)

    # 递归地将第二棵树中的节点插入到第一棵树中
    def merge_trees(tree1, tree2):
        if tree2 is None:
            return tree1
        tree1 = insert_node(tree1, tree2)
        tree1 = merge_trees(tree1, tree2.left)
        tree1 = merge_trees(tree1, tree2.right)
        return tree1

    # 将第二棵树合并到第一棵树中
    return merge_trees(tree1_root, tree2_root)


def mempty():
    return None
