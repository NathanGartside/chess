from ..piece import Piece


class Knight(Piece):
    def __init__(self, position):
        super().__init__(position)
        self.set_name('Kn')
