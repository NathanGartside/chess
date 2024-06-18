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
        self.in_check = False

    def generate_pieces(self):
        # Generate pawn row
        #for i in range(1, 9):
        #    pawn_row = 2 if self.is_first else 7
        #    self.pieces.append(Pawn({'row': pawn_row, 'col_num': i}))
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
        result = self.can_move(coords, other_player)
        if result.get('status_code') == -1:
            print('Invalid move input: Designated space not occupied by player\'s piece.')
            return False

        if result.get('status_code') == -2:
            print('Invalid move input: Piece cannot move to requested position.')
            return False

        # If the same team piece is occupying the new space, then invalid move
        if result.get('status_code') == -3:
            print('Invalid move input: New space is already occupied.')
            return False

        if result.get('status_code') == -4:
            print('Invalid move input: Designated piece cannot jump over other pieces')
            return False

        data = result.get('data')

        if data.get('enemy_piece_index') != -1:
            other_player.remove_piece(data.get('enemy_piece_index'))

        self.pieces[data.get('piece_index')].set_position(coords[1])
        return True

    def can_move(self, coords: list, other_player: "Player") -> dict:
        piece_index = self.check_space_occupancy(coords[0], self.pieces)
        if piece_index == -1:
            return {'status_code': -1, 'data': None}

        piece = self.pieces[piece_index]
        # enemy piece index is calculated here due to pawns allowing movement if it is capturing
        enemy_piece_index = self.check_space_occupancy(coords[1], other_player.pieces)
        if not piece.can_move(coords[1], is_first=self.is_first, is_capture=enemy_piece_index != -1):
            return {'status_code': -2, 'data': None}

        # If the same team piece is occupying the new space, then invalid move
        if self.check_space_occupancy(coords[1], self.pieces) != -1:
            return {'status_code': -3, 'data': None}

        if self.check_middle_space_occupancy(coords[0], coords[1], self.pieces, other_player.pieces):
            return {'status_code': -4, 'data': None}

        return {'status_code': 1, 'data': {'piece_index': piece_index, 'enemy_piece_index': enemy_piece_index}}

    def check_middle_space_occupancy(self, old_pos: dict, new_pos: dict,
                                     player1_pieces: list, player2_pieces: list) -> bool:
        row_diff = new_pos['row'] - old_pos['row']
        col_diff = new_pos['col_num'] - old_pos['col_num']
        # no need to continue if piece only moved one space OR is a knight
        if (abs(row_diff) < 2 and abs(col_diff) < 2) \
                or (abs(row_diff) == 1 and abs(col_diff) == 2) \
                or (abs(row_diff) == 2 and abs(col_diff) == 1):
            return False

        # Middle spaces occupancy check
        pos = old_pos.copy()
        pos['row'] += row_diff / abs(row_diff) if row_diff != 0 else 0
        pos['col_num'] += col_diff / abs(col_diff) if col_diff != 0 else 0
        while pos['row'] != new_pos['row'] or pos['col_num'] != new_pos['col_num']:
            print(f'### CHECKING POS {pos} ###')
            if self.check_space_occupancy(pos, player1_pieces) != -1 \
                    or self.check_space_occupancy(pos, player2_pieces) != -1:
                print('FOUND MIDDLE PIECE')
                return True
            pos['row'] += int(row_diff / abs(row_diff)) if row_diff != 0 else 0
            pos['col_num'] += int(col_diff / abs(col_diff)) if col_diff != 0 else 0
        return False

    def check_if_in_check(self, enemy_player: "Player") -> bool:
        self.in_check = self.position_results_in_check(enemy_player, self.get_king().position)
        return self.in_check

    def check_for_check_mate(self, enemy_player: "Player") -> bool:
        king = self.get_king()
        possible_king_moves = []
        for row in range(-1, 2):
            for col in range(-1, 2):
                position = {'row': king.position['row'] + row, 'col_num': king.position['col_num'] + col}
                if self.can_move([king.position, position], enemy_player)['status_code'] == 1:
                    possible_king_moves.append(position)
        index = 0
        # Check if the move results in the king being in check
        while index != len(possible_king_moves):
            if self.position_results_in_check(enemy_player, possible_king_moves[index]):
                del possible_king_moves[index]
            else:
                index += 1
        # the king is not in check or can move out of check
        if possible_king_moves or not self.in_check:
            # TODO: if possible moves is empty and not in check, then check for stalemate
            return False

        enemies_checking = []
        for piece in enemy_player.pieces:
            print(enemy_player.can_move([piece.position, king.position], self))
            if enemy_player.can_move([piece.position, king.position], self)['status_code'] == 1:
                enemies_checking.append(piece)

        # If king cannot get himself out of check and two pieces are checking him, no need to continue
        if len(enemies_checking) > 1:
            return True

        checking_piece = enemies_checking[0]
        # list of positions that would get the king out of check assuming a piece can move there
        saving_positions = [checking_piece.position]
        row_velocity = king.position['row'] - checking_piece.position['row']
        col_velocity = king.position['col_num'] - checking_piece.position['col_num']

        # checking piece is not a pawn or knight and checking piece is not next to the king
        if checking_piece.get_name() not in ['P', 'Kn'] and (abs(row_velocity) > 1 or abs(col_velocity) > 1):
            # Iterate through the spaces between the king and piece, these spaces determine if we can stop checkmate
            current_pos = checking_piece.position.copy()
            current_pos['row'] += row_velocity / abs(row_velocity) if row_velocity != 0 else 0
            current_pos['col_num'] += col_velocity / abs(col_velocity) if col_velocity != 0 else 0

            # current_pos = {
            #    'row': checking_piece.position['row'] + (row_velocity / abs(row_velocity) if row_velocity != 0 else 0),
            #    'col_num': checking_piece.position['col_num'] + (
            #        col_velocity / abs(col_velocity) if col_velocity != 0 else 0)
            # }
            while current_pos != king.position:
                print(f'\nAPPENDING {current_pos}')
                saving_positions.append(current_pos.copy())
                current_pos['row'] += row_velocity / abs(row_velocity) if row_velocity != 0 else 0
                current_pos['col_num'] += col_velocity / abs(col_velocity) if col_velocity != 0 else 0

        # TODO: Test if other pieces can stop check!
        #   1: if a piece can capture the threatening enemy piece
        #   2: if a piece can block the path to the king
        print(f'\n####### SAVING POSITIONS! {saving_positions}#######')
        for piece in self.pieces:
            if piece.get_name() == 'K':
                continue
            for saving_pos in saving_positions:
                print(f'\n###### CHECKING PIECE: {piece.get_name()} in position {piece.position} #######')
                if self.can_move([piece.position, saving_pos], enemy_player)['status_code'] == 1:
                    return False

        # TODO: Check if any of the other player pieces can stop the check
        #   - Do this by identifying space that would save the king
        #   - This is impossible if the enemy piece checking the king is a knight
        #       OR there are two pieces putting the king in check
        return True

    def position_results_in_check(self, enemy_player: "Player", coord: dict) -> bool:
        coords = [None, coord.copy()]
        for piece in enemy_player.pieces:
            coords[0] = {'row': piece.position['row'], 'col_num': piece.position['col_num']}
            if enemy_player.can_move(coords, self)['status_code'] == 1:
                return True
        return False

    def get_king(self) -> King:
        for piece in self.pieces:
            if isinstance(piece, King):
                return piece

    def remove_piece(self, piece_index: int) -> None:
        del self.pieces[piece_index]

    def get_name(self) -> str:
        return self.name

    @staticmethod
    def check_space_occupancy(space: dict, pieces: list) -> int:
        for i, piece in enumerate(pieces):
            if piece.position['col_num'] == space['col_num'] \
                    and piece.position['row'] == space['row']:
                return i
        return -1
