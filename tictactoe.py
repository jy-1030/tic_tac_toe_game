# -*- coding: utf-8 -*-

import random
import sys
import copy

class TicTacToe:
    # 初始化設定
    def __init__(self):
        self.board = [' '] * 10
        self.playerName = ''
        self.playerLetter = ''
        self.computerName = 'computer'
        self.computerLetter = ''
        self.corners = [1,3,7,9]
        self.sides = [2,4,6,8]
        self.middle = 5

        self.form = '''
            \t        |   |
            \t      %s | %s | %s
            \t        |   |
            \t    -------------
            \t        |   |
            \t      %s | %s | %s
            \t        |   |
            \t    -------------
            \t        |   |
            \t      %s | %s | %s
            \t        |   |
           '''

    # 開始遊戲
    def startGame(self):

        # 畫棋盤，調用 drawBoard()
        self.drawBoard(board = None)

        # 獲取代表棋子的字符，調用 inputPlayerLetter()
        self.playerLetter, self.computerLetter = self.inputPlayerLetter()
        print("您的選擇是 " + self.playerLetter)

        # 隨機選擇誰執先手，並開始遊戲。調用 startGameLoop()
        if random.randint(0,1) == 0:
            print(self.computerName + "爲執先手方!")
            self.startGameLoop(self.computerName)
        else:
            print(self.playerName + "爲執先手方!")
            self.startGameLoop(self.playerName)

    # 畫棋盤，如果遊戲新開始，沒有棋盤，就初始化棋盤，棋盤格都爲空。如果在遊戲中，就在網格中顯示字符。
    def drawBoard(self,board = None):
        if board is None:
            print(self.form % tuple(self.board[7:10] + self.board[4:7] + self.board[1:4]))
        else:
            print(self.form % tuple(board[7:10] + board[4:7] + board[1:4]))

    # 玩家輸入選擇的代表棋子的字符
    def inputPlayerLetter(self):
        letter = ''
        while not (letter == 'X' or letter == 'O'):
            print('選擇 X 還是 O ?')
            letter = input().upper()
      
        if letter == 'X':
            return ['X', 'O']
        else:
            return ['O', 'X']

    # 遊戲主循環
    def startGameLoop(self,turn):
        gameIsRunning = True
        player = turn
        while gameIsRunning:
            # 如果是玩家下棋
            if player == self.playerName:
                playerInput = self.getPlayerMove()
                self.makeMove(self.board, self.playerLetter, playerInput)
                if(self.isWin(self.board, self.playerLetter)):
                    self.drawBoard()
                    print("\n\t玩家獲勝!!! \t\n")
                    gameIsRunning = False
                else:
                    if self.isBoardFull():
                        self.drawBoard()
                        print("\n\t 平局!!! \n\t")
                        gameIsRunning = False
                    else:
                        self.drawBoard()
                        player = self.computerName
            # 轉爲計算機下棋
            else:
                computerMove =  self.getComputerMove()
                self.makeMove(self.board, self.computerLetter, computerMove)
                if (self.isWin(self.board, self.computerLetter)):
                    self.drawBoard()
                    print("\n\t電腦獲勝 \t\n" )
                    gameIsRunning = False
                    break
                else:
                    if self.isBoardFull():
                        self.drawBoard()
                        print("\n\t 平局!!! \n\t")
                        gameIsRunning = False
                    else:
                        self.drawBoard()
                        player = self.playerName

        # 當跳出遊戲循環，及獲勝、平局、失敗後結束遊戲。
        self.endGame()

    # 玩家下棋，返回輸入的位置數字
    def getPlayerMove(self):
        move = int(input("請選擇棋子位置: (1-9) "))
        while move not in range(1,10) or not self.isSpaceFree(self.board, move):
            move = int(input("無效操作，請重新選擇: (1-9) "))
        return move

    # 下棋，將字符配給相應的棋盤網格
    def makeMove(self,board, letter, move):
        board[move] = letter

    # 判斷獲勝的標準
    def isWin(self, board, letter):
        if ((board[1] == letter and board[2] == letter and board[3] == letter) or      # 下橫線
                (board[4] == letter and board[5] == letter and board[6] == letter) or  # 中橫線
                (board[7] == letter and board[8] == letter and board[9] == letter) or  # 上橫線
                (board[1] == letter and board[4] == letter and board[7] == letter) or  # 左豎線
                (board[2] == letter and board[5] == letter and board[8] == letter) or  # 中豎線
                (board[3] == letter and board[6] == letter and board[9] == letter) or  # 右豎線
                (board[1] == letter and board[5] == letter and board[9] == letter) or  # 一條對角線
                (board[3] == letter and board[5] == letter and board[7] == letter)):   # 又一條對角線
            return True
        else:
            return False

    # 檢測棋盤是否下滿
    def isBoardFull(self):
        for i in range(1,10):
            if self.isSpaceFree(self.board, i):
                return False
        return True

    # 檢測哪個位置爲空的，可以下棋
    def isSpaceFree(self, board, move):
        return board[move] == ' '

    # 計算機下棋，得到要下的位置
    # 依次做五個檢測： 1、自己下一步棋是否會贏； 2、玩家下一步棋是否會贏； 3、檢測四個角是否爲空； 4、檢測中心是否爲空； 5、檢測邊是否有空位。
    def getComputerMove(self):
        for i in range(1, 10):
            boardCopy = copy.deepcopy(self.board)
            if self.isSpaceFree(boardCopy, i):
                self.makeMove(boardCopy, self.computerLetter, i)
                if self.isWin(boardCopy, self.computerLetter):
                    return i

        for i in range(1, 10):
            boardCopy = copy.deepcopy(self.board)
            if self.isSpaceFree(boardCopy, i):
                self.makeMove(boardCopy, self.playerLetter, i)
                if self.isWin(boardCopy, self.playerLetter):
                    return i

        move = self.chooseRandomMove(self.corners)
        if move != None:
            return move

        if self.isSpaceFree(self.board, self.middle):
            return self.middle

        return self.chooseRandomMove(self.sides)

    # 隨機下棋
    def chooseRandomMove(self, moveList):
        possibleWinningMoves = []
        for move in moveList:
            if self.isSpaceFree(self.board, move):
                possibleWinningMoves.append(move)
                if len(possibleWinningMoves) != 0:
                    return random.choice(possibleWinningMoves)
                else:
                    return None

    # 遊戲結束
    def endGame(self):
        playAgain = input("再來一場? (y/n): ").lower()
        if playAgain == 'y':
            self.__init__()
            self.startGame()
        else:
            print("\n\t-- 遊戲結束!!!--\n\t")
            self.exitGame()

    # 退出遊戲
    def exitGame(self):
        sys.exit()

if __name__ == "__main__":
     TTT = TicTacToe()
     TTT.startGame()