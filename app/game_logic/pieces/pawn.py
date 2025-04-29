from ..piece import Piece


class Pawn(Piece):
    def __init__(self, position):
        super().__init__(position)
        self.set_name('P')
        self.en_passant = False

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

        # En Passant, passed kwarg "enemy"
        # Check if move was two spaces
        other_player = kwargs['enemy']
        enemy_move = other_player.previous_move_data['previous_move']
        if enemy_move:
            last_moved_enemy_piece = other_player.pieces[other_player.get_piece_index(enemy_move[1])]
            enemy_row_diff = abs(enemy_move[0]['row'] - enemy_move[1]['row'])
            if last_moved_enemy_piece.get_name() == 'P' and enemy_row_diff == 2 and enemy_move[1]['col_num'] == new_pos[
                'col_num'] and row_diff == 1 and col_diff == 1:
                self.set_is_en_passant(True)
                print('passed en passant')
                return True

        if row_diff > 2 or (row_diff == 2 and not self.first_move) or col_diff > 1:
            return False

        # Cannot move diagonally UNLESS it is a capture
        if col_diff == 1 and not kwargs['is_capture']:
            return False

        # A pawn cannot capture by moving forward
        if col_diff == 0 and row_diff > 0 and kwargs['is_capture']:
            return False
        return True

    def get_is_en_passant(self):
        return self.en_passant

    def set_is_en_passant(self, is_en_passant: bool):
        self.en_passant = is_en_passant

    # Might need to be in Player class
    def promote(self, new_piece: str):
        # TODO: Get to this eventually
        pass
