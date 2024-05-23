from .player import Player
MAX_PIECE_NAME_LENGTH = 5


class Game:
    def __init__(self, board_id=None):
        self.board = []
        self.player2 = None
        self.player1 = None
        self.turn = 1
        if board_id:
            # TODO: Eventually connect to database to retrieve stored game
            pass
        else:
            self.start_new_game()

    def start_new_game(self):
        self.player1, self.player2 = Player(is_first=True, name='Player1'), Player(is_first=False, name='Player2')
        self.player1.generate_pieces()
        self.player2.generate_pieces()
        self.board = self.generate_board()
        keep_playing = True
        while keep_playing:
            active_player = self.player1 if self.turn % 2 == 1 else self.player2
            keep_playing = self.perform_turn(active_player)

    def perform_turn(self, active_player: Player) -> bool:
        is_valid = False
        while not is_valid:
            self.display_board()
            move = input('Please enter desired move ' + active_player.get_name() + ': ')

        return False

    def display_board(self):
        if not self.board:
            board = self.generate_board()
        row_num = 8
        for index, row in enumerate(reversed(board)):
            row_string = str(row_num) + '|'
            row_num -= 1
            for value in row:
                row_string += str.center(value, MAX_PIECE_NAME_LENGTH+2) + '|'
            print(row_string)
        print(self.generate_vertical_coordinates())

    def generate_board(self):
        board = [['' for k in range(8)] for i in range(8)]
        for piece in self.player1.pieces:
            board[piece.position['row']-1][piece.position['col_num']-1] = '(W)' + piece.get_name()
        for piece in self.player2.pieces:
            board[piece.position['row']-1][piece.position['col_num']-1] = '(B)' + piece.get_name()
        return board

    @staticmethod
    def generate_vertical_coordinates() -> str:
        row_string = '  '
        for i in range(8):
            row_string += str.center(chr(i+97), MAX_PIECE_NAME_LENGTH+3)
        return row_string
