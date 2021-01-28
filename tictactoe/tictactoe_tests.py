import re
import unittest
import tictactoe as ttt
import subprocess


class TicTacToeTests(unittest.TestCase):

    def testTicTacToeBuildAndReset(self):
        t = ttt.TicTacToe(3)
        self.assertEquals(t.board, [0, 0, 0, 0, 0, 0, 0, 0, 0], "Board state is unexpected.")
        self.assertEquals(t.turn, 1, "Turn has unexpected state at start of game.")
        state = [0, 0, 0, 1, 0, 0, -1, 0, 0]
        t.reset(state)
        self.assertEquals(t.board, state, "Board state is unexpected after reset.")
        self.assertEquals(t.turn, 1, "Turn has unexpected state after reset to midgame.")
        state = [0, 0, 1, 1, 0, 0, -1, 0, 0]
        t.reset(state)
        self.assertEquals(t.board, state, "Board state is unexpected after reset.")
        self.assertEquals(t.turn, -1, "Turn has unexpected state after reset to midgame.")

    def testMove(self):
        t = ttt.TicTacToe(3)
        self.assertEquals(t.board, [0, 0, 0, 0, 0, 0, 0, 0, 0], "Board state is unexpected.")
        t.move(0)
        self.assertEquals(t.board, [1, 0, 0, 0, 0, 0, 0, 0, 0], "Board state is unexpected.")
        t.move(1)
        self.assertEquals(t.board, [1, -1, 0, 0, 0, 0, 0, 0, 0], "Board state is unexpected.")
        state = [0, 0, 0, 1, 0, 0, -1, 0, 0]
        t.reset(state)
        t.move(0)
        self.assertEquals(t.board, [1, 0, 0, 1, 0, 0, -1, 0, 0], "Board state is unexpected.")

    def testEndGame(self):
        t = ttt.TicTacToe(3)
        self.assertFalse(t.is_win())
        state = [1, 1, 1, 0, -1, -1, 0, 0, 0]
        state = [1, 1, 1, 0, -1, -1, 0, 0, 0]
        t.reset(state)
        self.assertEquals(t.is_win(), (ttt.TicTacToe.Row, 0, 1), "Row win is not detected.")
        state = [-1, 1, 0, 1, 1, 1, 0, -1, -1]
        t.reset(state)
        self.assertEquals(t.is_win(), (ttt.TicTacToe.Row, 1, 1), "Row win is not detected.")
        state = [-1, 0, 0, -1, 1, 1, -1, 0, 1]
        t.reset(state)
        self.assertEquals(t.is_win(), (ttt.TicTacToe.Column, 0, -1), "Column win is not detected.")
        state = [-1, 0, 0, 1, -1, 1, 0, 1, -1]
        t.reset(state)
        self.assertEquals(t.is_win(), (ttt.TicTacToe.Diagonal, 0, -1), "Diagonal win is not detected.")
        state = [-1, 0, 1, 1, 1, -1, 1, 0, -1]
        t.reset(state)
        self.assertEquals(t.is_win(), (ttt.TicTacToe.Diagonal, 1, 1), "Diagonal win not detected")
        state = [-1, 1, 1, 1, 1, -1, -1, -1, 1]
        t.reset(state)
        self.assertEquals(t.is_win(), (ttt.TicTacToe.StaleMate, 0, 0), "Stalemate is not detected.")

    def testEndGameLargeBoard(self):
        t = ttt.TicTacToe(4)
        t.reset([1, 1, 1, 0, -1, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.assertFalse(t.is_win())
        t.reset([1, 1, 1, 1, 1, 0, 0, -1, -1, 0, 0, -1, -1, 0, 0, 0])
        self.assertEquals(t.is_win(), (ttt.TicTacToe.Row, 0, 1))

    def testCommandLine1(self):
        cmd = 'python3 tictactoe.py --state 102022110 --mc 10000'
        out = subprocess.check_output(cmd, shell=True)
        # get the last line...
        lastout = out.decode('ascii').splitlines()[-1]
        pattern = '(\d+) trials: 1 wins ([\d\.]+), -1 wins ([\d\.]+), stalemates ([\d\.]+)'
        expected_re = re.compile(pattern)
        self.assertIsNotNone(expected_re.match(lastout),
                             "Last line doesn't match expected pattern")

        grps = expected_re.match(lastout).groups()
        self.assertEquals(int(grps[0]), 10000)
        wins = [float(g) for g in grps[1:]]
        tolerance = .08
        expected = [.67, .33, 0.0]

        for w, e in zip(wins, expected):
            in_tolerance = (w <= (e + tolerance) and w >= (e - tolerance))
            self.assertTrue(in_tolerance,
                            "Monte-Carlo results are outside of tolerance")
