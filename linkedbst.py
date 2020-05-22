"""
File: linkedbst.py
Author: Ken Lambert
"""

from .abstractcollection import AbstractCollection
from .bstnode import BSTNode
from .linkedstack import LinkedStack
from .linkedqueue import LinkedQueue
from math import log, floor
import copy


class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            s = ""
            if node != None:
                s += recurse(node.right, level + 1)
                s += "| " * level
                s += str(node.data) + "\n"
                s += recurse(node.left, level + 1)
            return s

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right != None:
                    stack.push(node.right)
                if node.left != None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node != None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) != None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        def recurse(node):
            if node is None:
                return None
            elif item == node.data:
                return node
            elif item < node.data:
                return recurse(node.left)
            else:
                return recurse(node.right)

        return recurse(self._root)

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""

        # Helper function to search for item's position
        def recurse(node):
            # New item is less, go left until spot is found
            if item < node.data:
                if node.left == None:
                    node.left = BSTNode(item)
                else:
                    recurse(node.left)
            # New item is greater or equal,
            # go right until spot is found
            elif node.right == None:
                node.right = BSTNode(item)
            else:
                recurse(node.right)
                # End of recurse

        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
        # Otherwise, search for the item's spot
        else:
            recurse(self._root)
        self._size += 1

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def liftMaxInLeftSubtreeToTop(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            currentNode = top.left
            while not currentNode.right == None:
                parent = currentNode
                currentNode = currentNode.right
            top.data = currentNode.data
            if parent == top:
                top.left = currentNode.left
            else:
                parent.right = currentNode.left

        # Begin main part of the method
        if self.isEmpty(): return None

        # Attempt to locate the node containing the item
        itemRemoved = None
        preRoot = BSTNode(None)
        preRoot.left = self._root
        parent = preRoot
        direction = 'L'
        currentNode = self._root
        while not currentNode == None:
            if currentNode.data == item:
                itemRemoved = currentNode.data
                break
            parent = currentNode
            if currentNode.data > item:
                direction = 'L'
                currentNode = currentNode.left
            else:
                direction = 'R'
                currentNode = currentNode.right

        # Return None if the item is absent
        if itemRemoved == None: return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not currentNode.left == None \
                and not currentNode.right == None:
            liftMaxInLeftSubtreeToTop(currentNode)
        else:

            # Case 2: The node has no left child
            if currentNode.left == None:
                newChild = currentNode.right

                # Case 3: The node has no right child
            else:
                newChild = currentNode.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = newChild
            else:
                parent.right = newChild

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = preRoot.left
        return itemRemoved

    def replace(self, item, newItem):
        """
        If item is in self, replaces it with newItem and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe != None:
            if probe.data == item:
                oldData = probe.data
                probe.data = newItem
                return oldData
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self, p=None):
        '''
        Return the height of tree
        :return: int
        '''

        def height1(top):
            '''
            Helper function
            :param top:
            :return:
            '''
            if top is None:
                return -1
            else:
                return 1 + max(height1(top.left), height1(top.right))

        if p is None:
            p = self._root
        return height1(p)

    def size(self):
        """
        Return number of nodes.
        :return: int
        """
        num_nodes = 0
        for node in self:
            num_nodes += 1
        return num_nodes

    def isBalanced(self):
        '''
        Return True if tree is balanced
        :return: bool
        '''
        if self._root is None:
            return True
        num_nodes = self.size()
        if self.height() < 2 * floor(log(num_nodes+1, 2)) - 1:
            return True
        else:
            return False

    def rangeFind(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low: int
        :param high: int
        :return: list
        '''
        elements = []
        for i in range(low, high+1):
            el = self.find(i)
            if el is not None:
                elements.append(el)
        return elements

    def rebalance(self):
        '''
        Rebalances the tree.
        :return: None
        '''
        def rebuild(data, first, last):
            if first <= last:
                mid = (first + last)//2
                self.add(data[mid])
                rebuild(data, first, mid-1)
                rebuild(data, mid+1, last)

        if not self.isBalanced():
            data = list(self.inorder())
            self.clear()
            rebuild(data, 0, len(data)-1)

    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item: int
        :return: BSTNode / None
        """
        if not self.isBalanced():
            twin = copy.copy(self)
            twin.rebalance()
            target = twin.find(item)
        else:
            target = self.find(item)

        if target is not None:
            res = target.right
            if res is not None:
                while res.left is not None:
                    res = res.left
            return res
        else:
            return None

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item: int
        :return: BSTNode / None
        """
        if not self.isBalanced():
            twin = copy.copy(self)
            twin.rebalance()
            target = twin.find(item)
        else:
            target = self.find(item)

        if target is not None:
            if target.left is not None:
                res = target.left
                while res.right is not None:
                    res = res.right
                return res
            else:
                res = self._root
                while res.right is not None:
                    res = res.right
        else:
            return None


if __name__ == '__main__':
    bst = LinkedBST()
    bst.add(5)
    bst.add(3)
    bst.add(1)
    bst.add(6)
    bst.add(23)
    bst.add(45)
    bst.add(78)
    bst.add(13)
    bst.add(10)
    bst.add(100)
    bst.add(1000)
    bst.add(79)
    bst.add(5.5)
    bst.add(4)
    print(bst)
    print('height =', bst.height())
    print('is balanced:', bst.isBalanced())
    print('78 predecessor =', bst.predecessor(78))
    print('10 successor =', bst.successor(10))
    print(bst)
    bst.rebalance()
    print('balanced:\n', bst)
    print('range(10, 79) =', bst.rangeFind(10, 79))
