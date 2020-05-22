class BTree:
    def __init__(self, root):
        self.key = root
        self.left = None
        self.right = None

    def insert_left(self, new_node):
        if self.left is None:
            self.left = BTree(new_node)
        else:
            tmp = BTree(new_node)
            tmp.left = self.left
            self.left = tmp

    def insert_right(self, new_node):
        if self.right is None:
            self.right = BTree(new_node)
        else:
            tmp = BTree(new_node)
            tmp.right = self.right
            self.right = tmp

    def get_right(self):
        return self.right


    def get_left(self):
        return self.left


    def set_root(self, obj):
        self.key = obj


    def get_root(self):
        return self.key


    def preorder(self):
        print(self.key)
        if self.left:
            self.left.preorder()
        if self.right:
            self.right.preorder()


    def inorder(self):
        if self.left:
            self.left.inorder()
        print(self.key)
        if self.right:
            self.right.inorder()


    def postorder(self):
        if self.left:
            self.left.postorder()
        if self.right:
            self.right.postorder()
        print(self.key)




ll = BTree(12)
ll.insert_right(123)
ll.insert_left(567)
ll.insert_left(9876)

print(ll)
print(ll.key)
print(ll.left.key)