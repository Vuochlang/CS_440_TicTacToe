# CS_440_TicTacToe

01/28/2021

Given the tictactoe folder with needed files:

_ in tictactoe.py, implement the 5 methods that are unimplemented:
  
    _ method 1: def move(self, where), update the board and players' turn if the given move is valid
    
    _ method 2: def show(self, stream=sys.stdout), print out a board-look for tictactoe game which can grow by given sizes
    
    _ method 3: def is_win(self), determines if the current board configuration is an end game, if any player has won or StaleMate
    
    _ method 4: def play(self, movefn=int_input, outstream=None, showwin=True), play the game of tictactoe
    
    _ method 5: def mc(state, n, debug=False), monte-carlo experiment - run the game for given n trails using random moves and get the 
                statistic of each players and StaleMate
