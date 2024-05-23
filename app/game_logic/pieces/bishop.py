from ..piece import Piece


class Bishop(Piece):
    def __init__(self, position):
        super().__init__(position)
        self.set_name('B')
