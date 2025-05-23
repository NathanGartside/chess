from .player import Player
import re
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
        # TODO: Include counters for stalemate! 50 moves without capture or 3 same moves from each player
        while keep_playing:
            active_player = self.player1 if self.turn % 2 == 1 else self.player2
            other_player = self.player2 if self.turn % 2 == 1 else self.player1
            keep_playing = self.perform_turn(active_player, other_player)
            self.turn += 1

    def perform_turn(self, active_player: Player, other_player: Player) -> bool:
        is_valid = False
        while not is_valid:
            self.display_board()
            move = input('Please enter desired move ' + active_player.get_name() + ' (i.e. A2:A4): ')
            split_moves = move.split(':')
            if not self.validate_coordinates(split_moves):
                print("Invalid coordinates put in, please try again.")
                continue
            for index, coord in enumerate(split_moves):
                split_moves[index] = self.get_input_coords(coord)
            is_valid = active_player.move(split_moves, other_player)
        self.display_board()
        if other_player.check_if_in_check(active_player):
            if other_player.check_for_check_mate(active_player):
                print(f'CHECKMATE! {other_player.get_name()} is checkmated!')
                return False
            else:
                print(f'WARNING! {other_player.get_name()} is in check!!!!')
        elif other_player.check_if_in_stalemate(active_player):
            print('STALEMATE! It\'s a tie!')
            return False
        return input('Do you want to keep playing (Y/N)? ').upper() == 'Y'

    def display_board(self):
        self.board = self.generate_board()
        row_num = 8
        for index, row in enumerate(reversed(self.board)):
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

    def get_input_coords(self, user_input: str) -> dict:
        row = int(user_input[1])
        col = self.convert_char_to_number(user_input[0])
        return {'row': row, 'col_num': col}

    @staticmethod
    def generate_vertical_coordinates() -> str:
        row_string = '  '
        for i in range(8):
            row_string += str.center(chr(i+97), MAX_PIECE_NAME_LENGTH+3)
        return row_string

    @staticmethod
    def convert_char_to_number(char: str) -> int:
        return ord(char.upper()) - 64

    @staticmethod
    def validate_coordinates(coordinates: list) -> bool:
        pattern = re.compile("[A-Za-z][0-9]")
        if len(coordinates) == 1:
            return False
        for coord in coordinates:
            if not pattern.match(coord):
                return False
        return True

