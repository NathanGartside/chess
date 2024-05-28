from ..piece import Piece


class Queen(Piece):
    def __init__(self, position):
        super().__init__(position)
        self.set_name('Q')

    def can_move(self, new_pos: dict, **kwargs):
        if not super().can_move(new_pos, **kwargs):
            return False
        row_diff = abs(new_pos['row'] - self.position['row'])
        col_diff = abs(new_pos['col_num'] - self.position['col_num'])
        if col_diff != 0 and row_diff != 0 and (col_diff != row_diff or row_diff == 0 or col_diff == 0):
            return False
        return True
