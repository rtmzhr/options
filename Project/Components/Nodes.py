class Node:

    def __init__(self, index, data=None):
        self.id = index
        self.data = data
        self.next = None
        self.parent = None


class NodeList:
    def __init__(self, root=None):
        self.root = Node(0, root)
        self.count = 1

    def set_child(self, parent_node, child_node_data):
        if parent_node is not None:
            parent = parent_node
            if parent_node is not Node:
                parent = self.get_node(parent_node)
            parent.next = Node(self.count, child_node_data)
            parent.next.parent = parent
            self.count += 1
            return child_node_data
        else:
            return None

    def get_node(self, node_data):
        itr = self.root
        while itr.data is not node_data:
            itr = itr.next
        return itr
