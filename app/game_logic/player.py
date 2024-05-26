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

    def move(self, coords: list) -> bool:
        for i, piece in enumerate(self.pieces):
            # TODO: CHECK IF MOVE IS VALID, SHOULD BE PIECE CLASS FUNCTION
            # TODO: NEED TO CHECK IF SPACE IS OCCUPIED BY ANOTHER PIECE AND
            #  CAPTURE IF ENEMY PIECE
            if piece.position['col_num'] == coords[0]['col_num'] \
                    and piece.position['row'] == coords[0]['row']\
                    and piece.can_move(coords[1], self.is_first):
                self.pieces[i].set_position(coords[1])
                return True
        print('Invalid move input, please try again')
        return False

    def get_name(self) -> str:
        return self.name
