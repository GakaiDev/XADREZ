import random #"IA" que executa um movimento aleatório dentros dos movimentos válidos.

def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves)-1)]



def findBestMove(): #aprimorar a IA em futuras atualizações
    return