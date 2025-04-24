from ..piece import Piece

CASTLE_MOVES = [
    [{'row': 1, 'col_num': 5}, {'row': 1, 'col_num': 3}],
    [{'row': 1, 'col_num': 5}, {'row': 1, 'col_num': 7}],
    [{'row': 8, 'col_num': 5}, {'row': 8, 'col_num': 3}],
    [{'row': 8, 'col_num': 5}, {'row': 8, 'col_num': 7}],
]


class King(Piece):
    def __init__(self, position):
        super().__init__(position)
        self.set_name('K')

    def can_move(self, new_pos: dict, **kwargs):
        if not super().can_move(new_pos, **kwargs):
            return False
        row_diff = abs(new_pos['row'] - self.position['row'])
        col_diff = abs(new_pos['col_num'] - self.position['col_num'])
        if self.is_castle_attempt(self.position, new_pos):
            return True
        if col_diff > 1 or row_diff > 1 or (col_diff == 0 and row_diff == 0):
            return False
        return True

    # Passes initial check for a castle attempt, the player class continues to check if castling is possible
    def is_castle_attempt(self, old_pos: dict, new_pos: dict):
        if self.first_move and old_pos == self.position and [self.position, new_pos] in CASTLE_MOVES:
            return True
