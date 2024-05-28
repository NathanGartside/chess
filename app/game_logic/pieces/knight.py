from ..piece import Piece


class Knight(Piece):
    def __init__(self, position):
        super().__init__(position)
        self.set_name('Kn')

    def can_move(self, new_pos: dict, **kwargs):
        if not super().can_move(new_pos, **kwargs):
            return False
        row_diff = abs(new_pos['row'] - self.position['row'])
        col_diff = abs(new_pos['col_num'] - self.position['col_num'])
        if (row_diff == 1 and col_diff == 2) or (row_diff == 2 and col_diff == 1):
            return True
        return False
