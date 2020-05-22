from arrays import Array2D
from btree import BTree
import random
import copy


class Board:
    CLEAN = ' _'
    def __init__(self):
        self.field = Array2D(3, 3)
        self.clear(self.CLEAN)
        self.last = ' x'
        #self.tree = LinkedBinaryTree(self.field)

    def clear(self, value=None):
        self.field.clear(value)

    def __str__(self):
        s = '   0 1 2\n'
        for i in range(3):
            s += f' {i}'
            for j in range(3):
                s += self.field[i, j]
            s += '\n'
        return s

    def check(self):
        def diagonal1_check():
            if self.field[0, 0] == self.field[1, 1] == self.field[2, 2]:
                return f'{self.field[0, 0]} wins!'
            else:
                return None

        def diagonal2_check():
            if self.field[0, 2] == self.field[1, 1] == self.field[2, 0]:
                return f'{self.field[0, 2]} wins!'
            else:
                return None

        def horizontal_check():
            for i in range(3):
                if self.field[i, 0] == self.field[i, 1] == self.field[i, 2]:
                    return f'{self.field[i, 0]} wins!'
                else:
                    continue
            else:
                return None

        def vertical_check():
            for j in range(3):
                if self.field[0, j] == self.field[1, j] == self.field[2, j]:
                    return f'{self.field[j, 0]} wins!'
                else:
                    continue
            else:
                return None

        def is_full():
            if len(self.availables()) == 0:
                return True
            else:
                return False

        if not is_full():
            res = diagonal1_check() or diagonal2_check() or \
                   horizontal_check() or vertical_check()
            if res is None:
                res = 'continue..'
            return res
        else:
            return 'draw!'

    def generate_position(self):
        av = self.availables()
        p = random.randint(0, len(av))
        return av[p]

    def build_tree(self, node):
        if len(self.availables()) != 1:
            self.laaast()
            tree = BTree(self)

            left_tree = copy.deepcopy(self)
            lp = left_tree.generate_position()
            left_tree.field[lp] = self.last
            right_tree = copy.deepcopy(self)
            rp = right_tree.generate_position()
            right_tree.field[rp] = self.last

            tree.insert_left(left_tree)
            tree.insert_right(right_tree)

            left_tree.build_tree()
            right_tree.build_tree()
        else:
            left_tree = copy.deepcopy(self)
            lp = left_tree.generate_position()
            left_tree.field[lp] = self.last

    def laaast(self):
        if self.last == ' o':
            self.last = ' x'
        else:
            self.last = ' o'

    def availables(self):
        av = []
        for i in range(3):
            for j in range(3):
                if self.is_available((i,j)):
                    av.append((i,j))
        return av

    def is_available(self, position):
        if 0 <= position[0] <= 2 and 0 <= position[1] <= 2:
            if self.field[position[0], position[1]] == self.CLEAN:
                return True
            else:
                return False
        else:
            raise IndexError('This position is out of game field!')


class TakenPositionError(Exception):
    def __init__(self, position):
        self.position = position
        self.message = 'This position has already been taken!'


if __name__ == '__main__':
    pass
