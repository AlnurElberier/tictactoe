#!/usr/bin/env python3
import sys

class Game:
    
    def __init__(self):
        self.score = {'X': 0, 'O': 0}
        self.first_player = 'X'
        self.reset()

    
    def reset(self):
        self.board = [
            [None, None, None],
            [None, None, None],
            [None, None, None]
        ]
        self.turn = self.first_player
        self.first_player = 'O' if self.first_player == 'X' else 'X'          
        self.winner = None
        self.message = ""
        


    def isDraw(self): 

        if self.winner is not None:
            return False

        for row in self.board:
            if None in row:
                return False
                
        return True
    
    def isOver(self):
        return self.winner is not None or self.isDraw()

    
    def isWon(self):

        for r in range(3):
            if self.board[r][0] and self.board[r][0] == self.board[r][1] == self.board[r][2]:
                return True

        for c in range(3):
            if self.board[0][c] and self.board[0][c] == self.board[1][c] == self.board[2][c]:
                return True

        if self.board[0][0] and self.board[0][0] == self.board[1][1] == self.board[2][2]:
            return True

        if self.board[0][2] and self.board[0][2] == self.board[1][1] == self.board[2][0]:
            return True

        return False

            

    def makeMove(self, row, col):

        # validate move
        if not (0 <= row < 3 and 0 <= col < 3):
            self.message = "Invalid Move"
            return False
        
        if self.isOver():
            self.message = "Game Over"
            return False

        if self.board[row][col] is not None:
            self.message = "Cell Taken"
            return False
        
        # place move
        self.board[row][col] = self.turn

        # update game state
        if self.isWon():
            self.winner = self.turn
            self.score[self.winner] += 1
        elif not self.isDraw():
            self.turn = 'O' if self.turn == 'X' else 'X'

        self.message = ""
        return True



CLEAR = "\033[H\033[J"

class Display:
    def render(self, game):
        b = game.board

        print(CLEAR, end="")
        for i in range(3):
            print(f" {b[0][i] or ' '} | {b[1][i] or ' '} | {b[2][i] or ' '} ")
            if i != 2:
                print("---+---+---")
        print()

        if game.winner:
            print(f"{game.winner} wins!")
        elif game.isDraw():
            print("It's a draw!")
        else:
            print(f"{game.turn}'s turn (1-9)")

        if game.message:
            print(game.message)

        print(f"X:{game.score['X']}  O:{game.score['O']}")



KEY_MAP = {
    1:(0, 2),
    2:(1, 2),
    3:(2, 2),
    4:(0, 1),
    5:(1, 1),
    6:(2, 1),
    7:(0, 0),
    8:(1, 0),
    9:(2, 0)
}

class TerminalInput:
    def getMove(self):
        while True:
            try:
                text = input("> ").strip()
            except (KeyboardInterrupt, EOFError):
                sys.exit()
            if len(text) == 1 and text in '123456789':
                return KEY_MAP[int(text)]

    def waitForNewGame(self):
        try:
            input("Game over: Enter = new game, Ctrl-C = quit ")
        except (KeyboardInterrupt, EOFError):
            sys.exit()

    

def main():
    g = Game()
    d = Display()
    t = TerminalInput()

    while True:
        d.render(g) # draw board

        while not g.isOver(): 
            g.makeMove(*t.getMove())    # take input to make move
            d.render(g)                 # draw update

        t.waitForNewGame()  # check if they want to play again              
        g.reset()           # reset board state

    


if __name__ == "__main__":
    main()