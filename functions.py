def update_grasses(grasses):
    for grass in grasses:
        grass.update_grass()


def update_board(board):
    if board.check_edges():
        board.direction *= -1
    board.move_left_right()
