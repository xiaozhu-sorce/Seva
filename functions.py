def update_grasses(grasses):
    for grass in grasses:
        grass.draw_grass()


def update_board(board):
    """更新木板的左右移动的状态"""
    if board.check_edges():
        board.direction *= -1
    board.move_left_right()
