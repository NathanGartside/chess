class Piece:
    def __init__(self, position: dict):
        self.name = None
        self.position = position

    def set_name(self, name: str):
        self.name = name

    def get_name(self) -> str:
        return self.name

    def set_position(self, position: list):
        self.position = position
