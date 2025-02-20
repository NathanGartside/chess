class Piece:
    def __init__(self, position: dict):
        self.name = None
        self.position = position
        self.first_move = True

    def can_move(self, new_pos: dict, **kwargs) -> bool:
        if new_pos['row'] < 1 or new_pos['row'] > 8\
                or new_pos['col_num'] < 1 or new_pos['col_num'] > 8:
            return False
        return True

    def set_name(self, name: str):
        self.name = name

    def get_name(self) -> str:
        return self.name

    def set_position(self, position: dict):
        self.position = position

    def set_is_first_to_false(self):
        self.first_move = False

    def get_first_move(self):
        return self.first_move
