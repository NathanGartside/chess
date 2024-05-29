from .pieces.king import King
from .pieces.queen import Queen
from .pieces.bishop import Bishop
from .pieces.knight import Knight
from .pieces.rook import Rook
from .pieces.pawn import Pawn


class Player:
    def __init__(self, is_first: bool, name: str = 'Player'):
        self.is_first = is_first
        self.pieces = []
        self.name = name

    def generate_pieces(self):
        # Generate pawn row
        for i in range(1, 9):
            pawn_row = 2 if self.is_first else 7
            self.pieces.append(Pawn({'row': pawn_row, 'col_num': i}))
        # Generate back row
        back_row = 1 if self.is_first else 8
        counter = 0
        for piece_object in [Rook, Knight, Bishop]:
            for i in range(2):
                col_num = i + counter if i == 1 else 8 - counter
                self.pieces.append(piece_object({'row': back_row, 'col_num': col_num}))
            counter += 1

        king_col, queen_col = 5, 4
        self.pieces.append(King({'row': back_row, 'col_num': king_col}))
        self.pieces.append(Queen({'row': back_row, 'col_num': queen_col}))

    def move(self, coords: list, other_player: "Player") -> bool:
        index = self.check_space_occupancy(coords[0], self.pieces)
        if index == -1:
            print('Invalid move input: Designated space not occupied by player\'s piece.')
            return False

        piece = self.pieces[index]
        # enemy piece index is calculated here due to pawns allowing movement if it is capturing
        enemy_piece_index = self.check_space_occupancy(coords[1], other_player.pieces)
        if not piece.can_move(coords[1], is_first=self.is_first, is_capture=enemy_piece_index != -1):
            print('Invalid move input: Piece cannot move to requested position.')
            return False

        # If the same team piece is occupying the new space, then invalid move
        if self.check_space_occupancy(coords[1], self.pieces) != -1:
            print('Invalid move input: New space is already occupied.')
            return False

        if self.check_middle_space_occupancy(coords[0], coords[1], self.pieces, other_player.pieces):
            print('Invalid move input: Designated piece cannot jump over other pieces')
            return False

        if enemy_piece_index != -1:
            other_player.remove_piece(enemy_piece_index)

        self.pieces[index].set_position(coords[1])
        return True

    def check_middle_space_occupancy(self, old_pos: dict, new_pos: dict,
                                     player1_pieces: list, player2_pieces: list) -> bool:
        row_diff = new_pos['row'] - old_pos['row']
        col_diff = new_pos['col_num'] - old_pos['col_num']
        # no need to continue if piece only moved one space OR is a knight
        if (abs(row_diff) < 2 and abs(col_diff) < 2) \
                or (abs(row_diff) == 1 and abs(col_diff) == 2) \
                or (abs(row_diff) == 2 and abs(col_diff) == 1):
            print('Distance is one space or a knight')
            return False

        # Middle spaces occupancy check
        pos = old_pos
        while pos['row'] != new_pos['row'] or pos['col_num'] != new_pos['col_num']:
            pos['row'] += row_diff / abs(row_diff) if row_diff != 0 else 0
            pos['col_num'] += col_diff / abs(col_diff) if col_diff != 0 else 0
            print('checking pos')
            print(pos)
            if self.check_space_occupancy(pos, player1_pieces) != -1 \
                    or self.check_space_occupancy(pos, player2_pieces) != -1:
                print('Found piece occupying middle space')
                return True
        print('No middle piece found')
        return False

    def remove_piece(self, piece_index: int) -> None:
        del self.pieces[piece_index]

    @staticmethod
    def check_space_occupancy(space: dict, pieces: list) -> int:
        for i, piece in enumerate(pieces):
            if piece.position['col_num'] == space['col_num'] \
                    and piece.position['row'] == space['row']:
                return i
        return -1

    def get_name(self) -> str:
        return self.name
