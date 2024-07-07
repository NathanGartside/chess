from ..piece import Piece


class Pawn(Piece):
    def __init__(self, position):
        super().__init__(position)
        self.set_name('P')
        self.first_move = True

    def can_move(self, new_pos: dict, **kwargs):
        if not super().can_move(new_pos, **kwargs):
            return False
        # Pawns can only move forward, not backwards or in the same row
        if (new_pos['row'] >= self.position['row'] and not kwargs['is_first'])\
                or (new_pos['row'] <= self.position['row'] and kwargs['is_first']):
            return False

        # Pawns have a speed limit
        row_diff = abs(new_pos['row'] - self.position['row'])
        col_diff = abs(new_pos['col_num'] - self.position['col_num'])
        if row_diff > 2 or (row_diff == 2 and not self.first_move) or col_diff > 1:
            return False

        # Cannot move diagonally UNLESS it is a capture
        if col_diff == 1 and not kwargs['is_capture']:
            return False

        # A pawn cannot capture by moving forward
        if col_diff == 0 and row_diff > 0 and kwargs['is_capture']:
            return False

        # first_move is set to false due to passing all move checks
        if self.first_move:
            self.first_move = False
        return True

    # Might need to be in Player class
    def promote(self, new_piece: str):
        pass
