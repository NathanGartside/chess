from ..piece import Piece


class King(Piece):
    def __init__(self, position):
        super().__init__(position)
        self.set_name('K')
