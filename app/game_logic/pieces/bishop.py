from ..piece import Piece


class Bishop(Piece):
    def __init__(self, position):
        super().__init__(position)
        self.set_name('B')

    def can_move(self, new_pos: dict, is_first: bool):
        if not super().can_move(new_pos, is_first):
            return False
        row_diff = abs(new_pos['row'] - self.position['row'])
        col_diff = abs(new_pos['col_num'] - self.position['col_num'])
        if col_diff != row_diff or row_diff == 0 or col_diff == 0:
            return False
        return True
