"""TicTacToe. A module for playing a simple game.

Name: Vuochlang Chang, 01/28/2021

Answer the following questions using your implementation:

1. Is it significantly better to play as 'X', or 'O', or neither?

->  Assuming 'X' always goes first, it is better to play as 'X'.


2. Describe an approach that will allow you to test if all first moves
   are equally good for 'X'. The method should be valid (yields
   correct results) and efficient (use minimal calculation).

->  We could use the monte-carlo experiment to test the outcome for each games and study the
    probability between 'X', 'O' and StaleMate.


3. Using the method described in (2), are all first moves for 'X'
   equally good?  If so, what are the odds that 'X' will win?  If not
   which is the best move for 'X' and how much does it improve the
   odds 'X' will win over the second best move?

->  Not all first moves for 'X' will guarantee the chance for 'X' to win:
    _ when using monte-carlo experiment:
        python3 tictactoe.py --mc 1000
            1000 trials: 1 wins 0.36, -1 wins 0.19, stalemates 0.45
            1000 trials: 1 wins 0.34, -1 wins 0.18, stalemates 0.48
            1000 trials: 1 wins 0.36, -1 wins 0.20, stalemates 0.43
    _ if the first move of 'X' is chosen randomly, as shown above, even 'X' will be likely to win 'O',
        but the chance of StaleMate is higher.

->  On the other hand, if the first move for 'X' is in the center of the board, then
    'X' will have a higher to win the game. Since the first move is in the center, 'X' will have more options
    whether to focus on winning the game with the current row, current column, upper_left diagonal
    or the upper_right diagonal.
    _ when using monte-carlo experiment:
        python3 tictactoe.py --state 000010000 --mc 1000
            State is: (0, 0, 0, 0, 1, 0, 0, 0, 0)
                1000 trials: 1 wins 0.51, -1 wins 0.15, stalemates 0.34
                1000 trials: 1 wins 0.49, -1 wins 0.15, stalemates 0.36
                1000 trials: 1 wins 0.53, -1 wins 0.15, stalemates 0.32
    _ as shown, when starting with the center spot, 'X' will have about 50% to win the game.



4. If 'X' moves into the bottom middle square, what is O's best
   response? (i.e.  the response that is *least likely* to yield a win
   for X)?

->  O's best response would be taking the center square of the table. After that, the game will have almost
    equal chance that 'O' will likely to win the game or StaleMate.
    _When using monte-carlo experiment:
        python3 tictactoe.py --state 000020010 --mc 1000
            State is: (0, 0, 0, 0, -1, 0, 0, 1, 0)
                1000 trials: 1 wins 0.29, -1 wins 0.35, stalemates 0.36
                1000 trials: 1 wins 0.27, -1 wins 0.37, stalemates 0.36


5. As the board gets bigger, is X's first move more, or less,
   strategically important?

-> As the board gets bigger, it expands the possibility of to win in different columns and rows, therefore,
    'X' first move does not consider as much important as a board of 3*3. Also by using the monte-carlo
    experiment for 'X' goes first with difference board sizes, the probability that 'X' will win is less and less.
        _python3 tictactoe.py --mc 1000 -n 3
            1000 trials: 1 wins 0.60, -1 wins 0.28, stalemates 0.12
        _python3 tictactoe.py --mc 1000 -n 4
            1000 trials: 1 wins 0.30, -1 wins 0.28, stalemates 0.43
        _python3 tictactoe.py --mc 1000 -n 5
            1000 trials: 1 wins 0.23, -1 wins 0.16, stalemates 0.62
        _python3 tictactoe.py --mc 1000 -n 6
            1000 trials: 1 wins 0.11, -1 wins 0.12, stalemates 0.78

"""
import math
import sys


def int_input(state, mover):
    print("%s's turn...(0..%d)" % (TicTacToe.Chrs[mover], len(state) - 1))
    return int(input())


class TicTacToe():
    """A Class representing the game of TicTacToe."""
    Column = 0
    Row = 1
    Diagonal = 2
    StaleMate = 3
    Chrs = {0: ' ', 1: 'X', -1: 'O'}

    def __init__(self, n=3):
        """Create a n-by-n tic-tac-toe game. n=3 by default"""

        self.n = n
        self.n2 = n ** 2
        self.reset()

    def reset(self, state=None):
        """Reset the game to the specified state, or to an empty board.
        A state is encoded as a list (or tuple) of elements in {-1, 0, 1}.
        -1 represents an 'O' (player 2), 0 represents an empty space and
        1 represents an 'X' (player 1).  The state is assumed to have an
        appropriate number of 'X's relative to the number of 'O's."""

        if state:
            ones = sum([i for i in state if i == 1])
            negs = sum([1 for i in state if i == -1])
            # ones (x's) go first

            assert ones == negs or ones == negs + 1, "X's (1's) go first."
            assert len(state) == self.n2, "the specified state is not the correct length"
            # The game state is kept here as a list of values.
            # 0  indicates the space is unoccupied;
            # 1  indicates the space is occupied by Player 1 (X)
            # -1 indicates the space is occupied by Player 2 (O)
            self.board = list(state)
            s = sum(state)
            if s == 0:
                self.turn = 1
            else:
                self.turn = -1

        else:
            self.board = [0] * (self.n2)
            self.turn = 1

    def move(self, where):
        """_ Part 1: Implement This Method _

        Make the current player's move at the specified location/index and
        change turns to the next player; where is an index into the board in
        the range 0..(n**2-1)

        If the specified index is a valid move, modify the board,
        change turns and return True.

        Return False if the specified index is unopen, or does not exist"""

        # if the specified index <move> is not in the range of the board or is already taken
        if where < 0 or where >= self.n2 or self.board[where] != 0:
            return False

        # otherwise update the board and update players' turn
        self.board[where] = self.turn
        self.turn *= -1
        return True

    def show(self, stream=sys.stdout):
        """_ Part 2: Implement This Method _

        Displays the board on the specified stream."""

        start_index = 0
        for row in range(self.n):  # loop through each <row>
            print("|", end=" ", file=stream)  # starting pipe in each <row>
            limit = start_index + self.n  # limit to print from self.board for each <row>
            for i in range(start_index, limit):  # loop to print self.board info up until limit
                if self.board[i] == 1:
                    num = "X"
                elif self.board[i] == -1:
                    num = "O"
                else:  # empty box
                    num = " "
                print(num, end=" | ", file=stream)
            start_index = limit  # update the starting index for the next <row>
            if row < (self.n - 1):  # if the next <row> is the last row, then skip printing the horizontal dashes
                sum = (self.n * 3) + self.n  # calculate how many dashes to print with the size of the board
                for x in range(sum):
                    if x == 0:
                        print("\n-", end="", file=stream)
                    print("-", end="", file=stream)
            print(end="\n", file=stream)
        return

    def is_win(self):
        """_ Part 3: Implement This Method _

        Determines if the current board configuration is an end game.
        For a board of size n, a win requires one player to have n tokens
        in a line (vertical, horizontal or diagonal).

        Returns:
         (TicTacToe.Column, c, player): if player wins in column c
         (TicTacToe.Row, r, player): if player wins in row r
         (TicTacToe.Diagonal, 0, player): if player wins via
           a diagonal in the upper-left corner
         (TicTacToe.Diagonal, 1, player): if player wins via a
           diagonal in the upper-right corner
         (TicTacToe.StaleMate, 0, 0): if the game is a stalemate
         False: if the end state is not yet determined
        """

        # check row = horizontal, to see if a player won in any particular row
        start_index = 0
        for row in range(self.n):  # loop through each <row>
            win = True
            limit = start_index + self.n
            player_id = self.board[start_index]
            for i in range(start_index, limit):  # loop through each column of that <row>
                if player_id == 0:  # if the column is still empty
                    win = False
                    break
                if player_id != self.board[i]:  # if the column is taken by the other player
                    win = False
                    break
            start_index = limit  # update the starting index to check for the next row
            if win:
                return TicTacToe.Row, row, player_id

        # check column = vertical, to see if a player won in any particular column
        for column in range(self.n):  # loop through each <column> of the table
            win = True
            last = column
            player_id = self.board[last]
            if player_id != 0:  # if the <column> is taken
                while last < self.n2:  # loop through each square box in that <column>
                    if player_id == 0:  # if box is empty
                        win = False
                        break
                    if player_id != self.board[last]:  # if box is taken by other player
                        win = False
                        break
                    last += self.n  # update the index to check next square box in that <column>
            else:  # if that first box in the <column> is empty, move to the next column
                win = False
                last += self.n
            if win:
                return TicTacToe.Column, column, player_id

        # diagonal in the upper-left corner
        win = True
        player_id = self.board[0]  # most upper left
        for i in range(self.n):  # loop through each box in each row in a diagonally direction from the left
            if player_id == 0:
                win = False
                break
            start = (self.n * i) + i  # update the box-index for the next box in the next row
            if player_id != self.board[start]:
                win = False
                break
        if win:
            return TicTacToe.Diagonal, 0, player_id

        # diagonal in the upper-right corner
        win = True
        player_id = self.board[self.n - 1]  # most upper right
        for i in range(1, self.n + 1):  # loop through each box in each row in a diagonally direction from the right
            if player_id == 0:
                win = False
                break
            start = (self.n * i) - i  # update the box-index for the next box in the next row
            if player_id != self.board[start]:
                win = False
                break
        if win:
            return TicTacToe.Diagonal, 1, player_id

        # if it didn't return in any above check-point, then it's either the game is not over or is StaleMate
        # first, check if the board is full - StaleMater, otherwise, the continue the game
        full = True
        for i in range(self.n2):
            if self.board[i] == 0:
                full = False
                break
        if full:  # stale mate
            return TicTacToe.StaleMate, 0, 0

        return False  # game is not ended yet

    def describe_win(self, win):
        """Provides a text representation of an end-game state."""
        reason = {TicTacToe.Row: "Row", TicTacToe.Column: "Column",
                  TicTacToe.Diagonal: "Diagonal"}

        if win[0] == TicTacToe.StaleMate:
            return "StaleMate!"
        if win[0] == TicTacToe.Diagonal:
            if win[1] == 0:
                where = "Upper Left"
            else:
                where = "Upper Right"
        else:
            where = "%d" % win[1]
        return "%s (%d) wins @ %s %s" % (TicTacToe.Chrs[win[2]], win[2],
                                         reason[win[0]], where)

    def play(self, movefn=int_input, outstream=None, showwin=True):
        """_ Part 4: Implement This Method _

        Play the game of tictactoe!

        Arguments:
        movefn - a function that will provide possibly valid moves.
        outstream - a stream on which to show the game (if provided)
        showwin - if True, explicitly indicate the game is over
                  and describe the win

        Play should work (roughly) as follows:
         - verify the game is not in an end state
         - if outstream is provided, display the game state (using show())
         - acquire the next move from the movefn (see note below).
         - repeat steps above

         when an end state is reached:
         - print the state (if outstream is defined) and
         - print 'Game Over!' along with a description of the win
           if showwin is True.

        the movefn should take two arguments:
          (1) the game state; and (2) the current player
        """

        while not self.is_win():  # when the game is still playing
            if outstream:
                self.show(stream=outstream)  # show the board
            valid_move = self.move(movefn(self.board, self.turn))
            while not valid_move:  # loop until getting a valid move for the board
                print("Try again...")
                valid_move = self.move(movefn(self.board, self.turn))

        # game is ended up til this point
        if outstream:
            self.show(stream=outstream)  # show the board
            print("state is ", self.get_state(), file=outstream)
            if showwin:  # print message for who won the game
                print("Game Over!", self.describe_win(self.is_win()), file=outstream)

    def get_state(self):
        """Get the state of the board as an immutable tuple"""
        return tuple(self.board)

def mc(state, n, debug=False):
    """_ Part 5: Implement This Method _

    Run a monte-carlo experiment in which we play the game using random
    moves.  Start each game at the specified state and run n
    simulations. Record the distribution of outcomes. Monte-carlo
    experiments such as this are used to evaluate states in complex
    games such as chess and go.

    Return a 4-tuple of:
    (games played, % won by player-1, % won by player-2, % stalemates)

    """

    if state:  # get board size from state if other than 3*3
        size = int(math.sqrt(len(state)))
        tictactoe = TicTacToe(size)
    else:  # default value of 3*3
        tictactoe = TicTacToe()

    # count the number of winning for each players and if StaleMater
    x_count = 0
    o_count = 0
    stalemate = 0

    for trial in range(n):  # running each trial
        tictactoe.reset(state)  # reset the board is state is given
        who_move = tictactoe.turn

        while not tictactoe.is_win():  # while the game is still in the process
            move = random.randint(0, tictactoe.n2 - 1)

            while tictactoe.board[move] != 0:  # loop until <move> is a valid square box in the current board
                move = random.randint(0, tictactoe.n2 - 1)

            tictactoe.board[move] = who_move  # update the board
            who_move *= -1  # update whose turn
        win = (tictactoe.is_win())[2]  # get the variable that indicate who won the game or StaleMate
        if win == 1:
            x_count += 1
        elif win == -1:
            o_count += 1
        else:
            stalemate += 1
    return n, x_count/n, o_count/n, stalemate/n  # return probability over the total trials


if __name__ == "__main__":
    import argparse
    import random

    parser = argparse.ArgumentParser()
    parser.add_argument("--play", action='store_true')
    parser.add_argument("--state",
                        help="initial state comprised of values in {0,1,2}")
    parser.add_argument("--mc", type=int, default=1000,
                        help="monte carlo trials; default=%(default)s")
    parser.add_argument("-n", type=int, default=3,
                        help="board length,width; default=%(default)s")
    args = parser.parse_args()

    if args.state:
        # At the command line state will come in as a string drawn
        # from {0,1,2}.  -1 is not used here since it's awkwardly
        # two characters.
        assert len(args.state) == args.n ** 2, \
            "Expected string with %d elements" % (args.n ** 2)

        # state is input from set {0,1,2} but needs to be translated into
        # {0,1,-1} by changing '2' entries to -1.
        state = [int(z) for z in args.state]
        stateset = set(state)
        assert stateset.issubset(set([0, 1, 2])), \
            "Expected string with elements 0,1,2"
        state = [-1 if s == 2 else s for s in state]
        state = tuple(state)
        print("State is:", state)
    else:
        state = tuple([0] * (args.n ** 2))

    t = TicTacToe(args.n)
    if args.play:
        t.reset(state)
        t.play(outstream=sys.stdout)

    elif args.mc:
        (games, one, two, stale) = mc(state, args.mc)
        print("%d trials: 1 wins %.2f, "
              "-1 wins %.2f, stalemates %.2f" % (games, one, two, stale))
