from ..piece import Piece


class Pawn(Piece):
    def __init__(self, position):
        super().__init__(position)
        self.set_name('P')
