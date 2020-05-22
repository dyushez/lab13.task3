from arrays import Array2D


class Board:
    def __init__(self):
        self.field = Array2D(3, 3)
        self.clear(' _')

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
                    return f'{self.field[j, 0]} wins!'
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
            for i in range(3):
                for j in range(3):
                    position = [i, j]
                    if self.is_available(position):
                       return False
            else:
                return True

        if not is_full():
            return diagonal1_check() or diagonal2_check() or \
                   horizontal_check() or vertical_check()
        else:
            return 'friendship wins!'

    def build_tree(self):
        pass

    def is_available(self, position):
        if 0 <= position[0] <= 2 and 0 <= position[1] <= 2:
            if self.field[position[0], position[1]] == ' _':
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
