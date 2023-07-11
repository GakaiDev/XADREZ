import pygame as p
import ChessEngine, IAnotSoSmart
import pyttsx3



WIDTH = HEIGHT = 512  #valores para criar a janela no pygame
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}


"""
iniciar um dicionario de imagens. que vai ser usado apenas uma vez no cidgo principal 
(para evitar sobrecarga e causar lag.)
"""

def loadimages():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wQ', 'wK', 'bp', 'bR', 'bN', 'bB', 'bQ', 'bK' ]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("Chess/images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))


"""
codigo principal
"""

def main():
    p.init()
    p.display.set_caption('Chess')
    Icon = p.image.load('Chess/logo.png')
    p.display.set_icon(Icon)
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False
    loadimages()
    robo = pyttsx3.init() #inicia o pyttsx3 para a leitura dos movimentos.
    running = True
    sqSelected =()
    playerClicks = []
    playerOne = True #escolher entre True e False para selecionar um player ou uma IA.
    playerTwo = False #o mesmo mas para jogar com as peças pretas.
    while running:
        humanTurn = (gs.WhiteToMove and playerOne) or (not gs.WhiteToMove and playerTwo)
        for e in p.event.get():
            if e.type == p.QUIT: 
                p.quit
                running = False
            elif e.type == p.MOUSEBUTTONDOWN: 
                if humanTurn:
                    location = p.mouse.get_pos()
                    col = location[0]//SQ_SIZE
                    row = location[1]//SQ_SIZE
                    if sqSelected == (row, col):
                        sqSelected = ()
                        playerClicks = [] #limpa os clicks
                    else:
                        sqSelected = (row ,col)
                        playerClicks.append(sqSelected)
                    if len(playerClicks) == 2:
                        move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                        print(move.getChessNotation())
                        if move in validMoves:
                            gs.makeMove(move)
                            robo.say(move.getChessNotation())
                            robo.runAndWait()
                            moveMade = True
                            sqSelected = ()
                            playerClicks = []
                        else:
                            playerClicks = [sqSelected]
        
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()
                    moveMade = True

        if not humanTurn: #turno da IA
            AIMove = IAnotSoSmart.findRandomMove(validMoves)
            gs.makeMove(AIMove)
            moveMade = True 
            print(AIMove.getChessNotation())
            robo.say(AIMove.getChessNotation())
            robo.runAndWait()

            


        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False
        
           
        drawGameState(screen, gs, validMoves, sqSelected)
        clock.tick(MAX_FPS)
        p.display.flip()
        
"""
responsavel pelas funçoes graficas
"""

def highlightSquares(screen, gs, validMoves, sqSelected): #função responsável por mostrar os movimentos possiveis ao selecionar a peça.
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.WhiteToMove else 'b'):
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)
            s.fill(p.Color('blue'))
            screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))
            s.fill(p.Color('yellow'))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (move.endCol*SQ_SIZE, move.endRow*SQ_SIZE))
                    








def drawGameState(screen, gs, validMoves, sqSelected):
    drawBoard(screen)
    highlightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board)


def drawBoard(screen):
    colors = [p.Color("white"), p.Color("pink")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c) % 2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

if __name__ == "__main__":
    main()