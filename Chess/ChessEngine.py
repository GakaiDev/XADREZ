"""
essa classe é responsável por guardar toda a informação do jogo atual. 
Também vai determindar os movimnetos válidos e guardar uma lista dos movimentos.
"""

from base64 import encode
import pygame as p
import pyttsx3



class GameState():
    def __init__(self):
        #o campo é uma lista 8x8,e cada elemento da lista possui 2 caracteres.
        #o primeiro representa a cor, "b" ou "w".
        #o segundo representa o tipo da peça, "K", "Q", "R", "B", "N" ou "p"
        #"--" representa uma casa sem peça.
        self.board = [
            ["bR","bN","bB","bQ","bK","bB","bN","bR"],
            ["bp","bp","bp","bp","bp","bp","bp","bp"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["wp","wp","wp","wp","wp","wp","wp","wp"],
            ["wR","wN","wB","wQ","wK","wB","wN","wR"]]
        self.moveFunctions = {'p': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves, 'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves}
        
        
        
        self.WhiteToMove = True
        self.moveLog = []
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.checkMate = False
        self.staleMate = False
        


    """
    executa um movimento
    """

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.WhiteToMove = not self.WhiteToMove
        if move.pieceMoved == "wK":
           self.whiteKingLocation = (move.endRow, move.endCol)

        
        elif move.pieceMoved == "bK": 
            self.blackKingLocation = (move.endRow, move.endCol)
        


  
        



    """
    Refaz um movimento
    """

    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved 
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.WhiteToMove = not self.WhiteToMove
            if move.pieceMoved == "wK":
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == "bK": 
                self.blackKingLocation = (move.startRow, move.startCol)


    """
    Todos os movimentos válidos
    """
    def getValidMoves(self):
        moves = self.getAllPossibleMoves()

        for i in range(len(moves)-1, -1, -1):
            self.makeMove(moves[i])

            self.WhiteToMove = not self.WhiteToMove
            if self.inCheck():
                moves.remove(moves[i])
            self.WhiteToMove = not self.WhiteToMove
            self.undoMove()
        if len(moves) == 0:
            if self.inCheck():
                self.checkMate = True
            else:
                self.staleMate = True
        else:
            self.checkMate = False
            self.staleMate = False
        
        return moves



    
    def inCheck(self): #analisa se o rei está em cheque para limitar os proximos movimentos.
        if self.WhiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])


    
    def squareUnderAttack(self, r, c):
        self.WhiteToMove = not self.WhiteToMove
        oppMoves = self.getAllPossibleMoves()
        self.WhiteToMove = not self.WhiteToMove
        for move in oppMoves:
            if move.endRow == r and move.endCol == c:
                return True
        
        return False
    
    """
    apenas os movimentos possíveis
    """
    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == "w" and self.WhiteToMove) or (turn == "b" and not self.WhiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves)
                    
                    
        return moves 

    



    """
    movimentos dos peões
    """

    def getPawnMoves(self, r, c, moves):
        if self.WhiteToMove:
            if self.board[r-1][c] == "--": #salto unico do peão
                moves.append(Move((r, c), (r-1, c), self.board))
                if r == 6 and self.board[r-2][c] == "--": #salto duplo do peão
                     moves.append(Move((r, c), (r-2, c), self.board))
            if c-1 >= 0:
                if self.board[r-1][c-1][0] == 'b':
                    moves.append(Move((r, c), (r-1, c-1), self.board))
            if c+1 <= 7:
                if self.board[r-1][c+1][0] == 'b':
                    moves.append(Move((r, c), (r-1, c+1), self.board))
        else: #movimento dos peões pretos
            if self.board[r + 1][c] == "--":
                moves.append(Move((r, c), (r + 1, c), self.board))
                if r == 1 and self.board[r + 2][c] == "--":
                    moves.append(Move((r, c), (r + 2, c), self.board))
            if c - 1 >= 0:
                if self.board[r + 1][c - 1][0] == "w":
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))
            if c + 1 <= 7:
                if self.board[r + 1][c + 1][0] == "w":
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))
            #adicionar as promoções depois




    """
    movimento das torres
    """
    def getRookMoves(self, r, c, moves):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        enemyColor = "b" if self.WhiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board)) 
                        break
                    else:
                        break
                else:
                    break                   
                


    """
    movimento dos cavalos
    """

    def getKnightMoves(self, r, c, moves):
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        allyColor = "w" if self.WhiteToMove else "b"
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    moves.append(Move((r, c), (endRow, endCol), self.board))

    """
       movimento dos bispos
       """

    def getBishopMoves(self, r, c, moves):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        enemyColor = "b" if self.WhiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board)) 
                        break
                    else:
                        break
                else:
                    break    

    """
       movimento da rainha
       """

    def getQueenMoves(self, r, c, moves): #podemos apenas puxar as funções do bispo e da torre já que a rainha se move como uma junção dos dois.
        self.getBishopMoves(r, c , moves)
        self.getRookMoves(r, c, moves)

    """
       movimento do rei
       """

    def getKingMoves(self, r, c, moves):
        kingMoves = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        allyColor = "w" if self.WhiteToMove else "b"
        for i in range(8):
            endRow = r + kingMoves[i][0]
            endCol = c + kingMoves[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    moves.append(Move((r, c), (endRow, endCol), self.board))
    




class Move(): 
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}

    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filestoCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}

    colsToFiles= {v: k for k, v in filestoCols.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
        

    
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False
    
    def getChessNotation(self): #funções responsáveis por salvar os movimentos realizados
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]