from board import Board, TakenPositionError


def handle_move(board,player):
    while True:
        move = input('Enter position in format #,#\n>>> ').split(',')
        move = [int(p) for p in move]
        try:
            if board.is_available(move):
                board.field[move[0], move[1]] = player
                break
        except IndexError:
            continue
        except TakenPositionError:
            continue


if __name__ == '__main__':
    player1 = ' x'
    player2 = ' o'
    board = Board()
    print(board)
    while True:
        handle_move(board, player1)
        print(board)
        board.check()
        handle_move(board, player2)
        print(board)
        board.check()