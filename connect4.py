import random
from typing import List, Tuple

SYMBOLS = [' ', 'X', 'O']
DIFFICULTY = 5
INFINITY = 512


class Connect4:
    def __init__(self, rows: int = 6, cols: int = 7) -> None:
        self.rows = rows
        self.cols = cols
        self.board: List[List[int]] = [
            [0 for i in range(cols)] for i in range(rows)
        ]

    def _is_horizontal(self, board, i, j) -> bool:
        return board[i][j] == board[i][j+1] \
            == board[i][j+2] == board[i][j+3] != 0

    def _is_vertical(self, board, i, j) -> bool:
        return board[i][j] == board[i+1][j] \
            == board[i+2][j] == board[i+3][j] != 0

    def _is_diagonal(self, board, i, j, d) -> bool:
        return board[i][j] == board[i+d][j+1] \
            == board[i+2*d][j+2] == board[i+3*d][j+3] != 0

    def draw_board(self) -> None:
        for row in range(self.rows):
            print("\n"+"+---" * (self.cols) + "+\n|", end="")
            for col in range(self.cols):
                print(" "+SYMBOLS[self.board[row][col]], end=' |')
        print("\n"+"+---" * (self.cols) + "+", end='\n  ')
        print("   ".join([str(i) for i in range(self.cols)]))

    def place(self, pos: int, player: int) -> bool:
        i = self.rows - 1
        while i >= 0:
            if self.board[i][pos] == 0:
                self.board[i][pos] = player
                return True
            i -= 1
        return False

    def remove(self, pos: int) -> bool:
        for i in range(self.rows):
            if self.board[i][pos] != 0:
                self.board[i][pos] = 0
                return True
        return False

    def check_win(self, board=None) -> int:
        '''
        Check if currently any player is winning based on
        current board configuration.
        0  -> no one is winning
        1  -> player is winning
        -1 -> computer is winning '''
        board = board or self.board

        # Horizontal Checker
        for i in range(self.rows):
            for j in range(self.cols-3):
                if self._is_horizontal(board, i, j):
                    return board[i][j]

        # Vertical Checker
        for i in range(self.rows-3):
            for j in range(self.cols):
                if self._is_vertical(board, i, j):
                    return board[i][j]

        # Diagonal Checker
        for i in range(self.rows-3):
            for j in range(self.cols-3):
                if self._is_diagonal(board, i, j, 1):
                    return board[i][j]
        for i in range(3, self.rows):
            for j in range(self.cols-3):
                if self._is_diagonal(board, i, j, -1):
                    return board[i][j]
        return 0

    def get_freespaces(self, pos) -> int:
        '''Returns the amount of freespace above a given position'''
        i = 0
        while i < self.rows and self.board[i][pos] == 0:
            i += 1
        return i

    def get_legal_moves(self) -> list:
        '''Returns a list of possible legal moves'''
        return [i for i in range(self.cols) if self.board[0][i] == 0]

    def minimax(self, depth, pos, is_max,
                alpha=-INFINITY, beta=INFINITY) -> int:
        '''minimax implementation with alpha beta pruning'''
        if is_max:
            player = -1
        else:
            player = 1

        self.place(pos, player)
        is_winning = self.check_win()
        legal_moves = self.get_legal_moves()

        # Terminal nodes
        if is_winning or depth == 0:
            self.remove(pos)
            return is_winning * depth * 32

        # Maximizer turn
        if is_max:
            best_val = -INFINITY
            for move in legal_moves:
                val = self.minimax(depth-1, move, False, alpha, beta)
                best_val = max(best_val, val)
                alpha = max(alpha, best_val)
                if beta <= alpha:
                    break
            self.remove(pos)
            return best_val
        # Minimizer turn
        else:
            best_val = INFINITY
            for move in legal_moves:
                val = self.minimax(depth-1, move, True, alpha, beta)
                best_val = min(best_val, val)
                beta = min(beta, best_val)
                if beta <= alpha:
                    break
            self.remove(pos)
            return best_val

    def play_ai(self, diff: int = 0) -> None:
        '''Make the AI make it's move'''
        if diff == 0:
            pos = random.choice(self.get_legal_moves())
            self.place(pos, -1)
        elif diff >= 1:
            legal_moves = self.get_legal_moves()
            best_val = INFINITY
            best_pos = legal_moves[0]
            for move in legal_moves:
                val = self.minimax(diff+1, move, True)
                val += abs(self.cols//2-move) - (self.get_freespaces(move)//2)
                if val < best_val:
                    best_val = val
                    best_pos = move
            print("Computer plays at position:", best_pos)
            self.place(best_pos, -1)

    def mainloop(self) -> int:
        while True:
            self.draw_board()
            if len(self.get_legal_moves()) == 0:
                return 0
            pos = int(input("Enter the position: "))
            try:
                if not game.place(pos, 1):
                    print("Invalid move. Try:", self.get_legal_moves())
                    continue
            except IndexError:
                print("Invalid move. Try:", self.get_legal_moves())
                continue
            if self.check_win():
                return self.check_win()
            self.play_ai(DIFFICULTY)
            if self.check_win():
                return self.check_win()


if __name__ == '__main__':
    game = Connect4()
    print("\nConnect 4\n---------")

    win = game.mainloop()
    game.draw_board()

    if win == 1:
        print("YOU WIN!")
    elif win == -1:
        print("COMPUTER WINS!")
    else:
        print("GAME IS A DRAW!")
