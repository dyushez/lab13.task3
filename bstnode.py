class BTNode(object):
    """Represents a node for a linked binary search tree."""

    def __init__(self, data, left = None, right = None):
        self.data = data
        self.left = left
        self.right = right

    def __repr__(self):
        return str(self.data)

    def __str__(self):
        return str(self.data)
