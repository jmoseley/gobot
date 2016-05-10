import copy
import Queue

winningPlayer = 2
losingPlayer = 1

ONE_HUNDRED_PRIMES = [2, 5, 11, 17, 23, 31, 41, 47, 59, 67, 73, 83, 97, 103, 109, 127, 137, 149, 157, 167, 179, 191, 197, 211, 227, 233, 241, 257, 269, 277, 283, 307, 313, 331, 347, 353, 367, 379, 389, 401, 419, 431, 439, 449, 461, 467, 487, 499, 509, 523, 541, 521, 503, 491, 479, 463, 457, 443, 433, 421, 409, 397, 383, 373, 359, 349, 337, 317, 311, 293, 281, 271, 263, 251, 239, 229, 223, 199, 193, 181, 173, 163, 151, 139, 131, 113, 107, 101, 89, 79, 71, 61, 53, 43, 37, 29, 19, 13, 7, 3]

def getPossibleMoves(board, player):
  moves = {}
  for row, r in enumerate(board):
    for column, c in enumerate(r):
      if board[row][column] == 0:
        newBoard = copy.deepcopy(board)
        newBoard[row][column] = player
        moves[(column, row)] = newBoard
  return moves

def getHash(board, player):
  h = 0
  for row, r in enumerate(board):
    for column, c in enumerate(r):
      piece = board[row][column]
      if piece == 0:
        multiplier = 0
      elif piece == player:
        multiplier = 1
      else:
        multiplier = -1
      h += ONE_HUNDRED_PRIMES[row + column]*multiplier
  return h

def printBoard(board):
  for row in board:
    print ' '.join([ '%s' % r for r in row ])

def isWin(board, player, move):
  row = move[0]
  col = move[1]
  # Horizontal
  # P * * * *
  if col <= 5:
    if board[row][col + 1] == player and board[row][col + 2] == player and board[row][col + 3] == player and board[row][col + 4] == player:
      # Ensure exactly 5 for player 1.
      if player == 1:
        if col + 5 < 10:
          if board[row][col + 5] != player:
            if col - 1 >= 0:
              if board[row][col - 1] != player:
                return True
            else:
              return True
        else:
          if col - 1 >= 0:
            if board[row][col - 1] != player:
              return True
          else:
            return True
      else:
        return True

  # * P * * *
  if col <= 6 and col >= 1:
    if board[row][col - 1] == player and board[row][col + 1] == player and board[row][col + 2] == player and board[row][col + 3] == player:
      # Ensure exactly 5 for player 1.
      if player == 1:
        if col + 4 < 10:
          if board[row][col + 4] != player:
            if col - 2 >= 0:
              if board[row][col - 2] != player:
                return True
            else:
              return True
        else:
          if col - 2 >= 0:
            if board[row][col - 2] != player:
              return True
          else:
            return True
      else:
        return True

  # * * P * *
  if col <= 7 and col >= 2:
    if board[row][col - 2] == player and board[row][col - 1] == player and board[row][col + 1] == player and board[row][col + 2] == player:
      # Ensure exactly 5 for player 1.
      if player == 1:
        if col + 3 < 10:
          if board[row][col + 3] != player:
            if col - 3 >= 0:
              if board[row][col - 3] != player:
                return True
            else:
              return True
        else:
          if col - 3 >= 0:
            if board[row][col - 3] != player:
              return True
          else:
            return True
      else:
        return True

  # * * * P *
  if col <= 8 and col >= 3:
    if board[row][col - 3] == player and board[row][col - 2] == player and board[row][col - 1] == player and board[row][col + 1] == player:
      # Ensure exactly 5 for player 1.
      if player == 1:
        if col + 2 < 10:
          if board[row][col + 2] != player:
            if col - 4 >= 0:
              if board[row][col - 4] != player:
                return True
            else:
              return True
        else:
          if col - 4 >= 0:
            if board[row][col - 4] != player:
              return True
          else:
            return True
      else:
        return True

  # * * * * P
  if col >= 4:
    if board[row][col - 4] == player and board[row][col - 3] == player and board[row][col - 2] == player and board[row][col - 1] == player:
      # Ensure exactly 5 for player 1.
      if player == 1:
        if col + 1 < 10:
          if board[row][col + 1] != player:
            if col - 5 >= 0:
              if board[row][col - 5] != player:
                return True
            else:
              return True
        else:
          if col - 5 >= 0:
            if board[row][col - 5] != player:
              return True
          else:
            return True
      else:
        return True

  # Vertical
  # P
  # *
  # *
  # *
  # *
  if row <= 5:
    if board[row + 1][col] == player and board[row + 2][col] == player and board[row + 3][col] == player and board[row + 4][col] == player:
      # Ensure exactly 5 for player 1.
      if player == 1:
        if row + 5 < 10:
          if board[row + 5][col] != player:
            if row - 1 >= 0:
              if board[row - 1][col] != player:
                return True
            else:
              return True
        else:
          if row - 1 >= 0:
            if board[row - 1][col] != player:
              return True
          else:
            return True
      else:
        return True

  # *
  # P
  # *
  # *
  # *
  if row <= 6 and row >= 1:
    if board[row - 1][col] == player and board[row + 1][col] == player and board[row + 2][col] == player and board[row + 3][col] == player:
      # Ensure exactly 5 for player 1.
      if player == 1:
        if row + 4 < 10:
          if board[row + 4][col] != player:
            if row - 2 >= 0:
              if board[row - 2][col] != player:
                return True
            else:
              return True
        else:
          if row - 2 >= 0:
            if board[row - 2][col] != player:
              return True
          else:
            return True
      else:
        return True

  # *
  # *
  # P
  # *
  # *
  if row <= 7 and row >= 2:
    if board[row - 2][col] == player and board[row - 1][col] == player and board[row + 1][col] == player and board[row + 2][col] == player:
      # Ensure exactly 5 for player 1.
      if player == 1:
        if row + 3 < 10:
          if board[row + 3][col] != player:
            if row - 3 >= 0:
              if board[row - 3][col] != player:
                return True
            else:
              return True
        else:
          if row - 3 >= 0:
            if board[row - 3][col] != player:
              return True
          else:
            return True
      else:
        return True

  # *
  # *
  # *
  # P
  # *
  if row <= 8 and row >= 3:
    if board[row - 3][col] == player and board[row - 2][col] == player and board[row - 1][col] == player and board[row + 1][col] == player:
      # Ensure exactly 5 for player 1.
      if player == 1:
        if row + 2 < 10:
          if board[row + 2][col] != player:
            if row - 4 >= 0:
              if board[row - 4][col] != player:
                return True
            else:
              return True
        else:
          if row - 4 >= 0:
            if board[row - 4][col] != player:
              return True
          else:
            return True
      else:
        return True

  # *
  # *
  # *
  # *
  # P
  if row >= 4:
    if board[row - 4][col] == player and board[row - 3][col] == player and board[row - 2][col] == player and board[row - 1][col] == player:
      # Ensure exactly 5 for player 1.
      if player == 1:
        if row + 1 < 10:
          if board[row + 1][col] != player:
            if row - 5 >= 0:
              if board[row - 5][col] != player:
                return True
            else:
              return True
        else:
          if row - 5 >= 0:
            if board[row - 5][col] != player:
              return True
          else:
            return True
      else:
        return True

    # Diagonal (Right)
    # P
    #   *
    #     *
    #       *
    #         *
    if row <= 5 and col <= 5:
      if board[row + 1][col + 1] == player and board[row + 2][col + 2] == player and board[row + 3][col + 3] == player and board[row + 4][col + 4] == player:
        if player == 1:
          if row + 5 < 10 and col + 5 < 10:
            if board[row + 5][col + 5] != player:
              if row - 1 >= 0 and col - 1 >= 0:
                if board[row - 1][col - 1] != player:
                  return True
              else:
                return True
          else:
            if row - 1 >= 0 and col - 1 >= 0:
              if board[row - 1][col - 1] != player:
                return True
            else:
              return True
        else:
          return True

    # *
    #   P
    #     *
    #       *
    #         *
    if row <= 6 and col <= 6 and row >= 1 and col >= 1:
      if board[row - 1][col - 1] == player and board[row + 1][col + 1] == player and board[row + 2][col + 2] == player and board[row + 3][col + 3] == player:
        if player == 1:
          if row + 4 < 10 and col + 4 < 10:
            if board[row + 4][col + 4] != player:
              if row - 2 >= 0 and col - 2 >= 0:
                if board[row - 2][col - 2] != player:
                  return True
              else:
                return True
          else:
            if row - 2 >= 0 and col - 2 >= 0:
              if board[row - 2][col - 2] != player:
                return True
            else:
              return True
        else:
          return True

    # *
    #   *
    #     P
    #       *
    #         *
    if row <= 7 and col <= 7 and row >= 2 and col >= 2:
      if board[row - 1][col - 1] == player and board[row - 2][col - 2] == player and board[row + 1][col + 1] == player and board[row + 2][col + 2] == player:
        if player == 1:
          if row + 3 < 10 and col + 3 < 10:
            if board[row + 3][col + 3] != player:
              if row - 3 >= 0 and col - 3 >= 0:
                if board[row - 3][col - 3] != player:
                  return True
              else:
                return True
          else:
            if row - 3 >= 0 and col - 3 >= 0:
              if board[row - 3][col - 3] != player:
                return True
            else:
              return True
        else:
          return True

    # *
    #   *
    #     *
    #       P
    #         *
    if row <= 8 and col <= 8 and row >= 3 and col >= 3:
      if board[row - 3][col - 3] == player and board[row - 2][col - 2] == player and board[row - 1][col - 1] == player and board[row + 1][col + 1] == player:
        if player == 1:
          if row + 2 < 10 and col + 2 < 10:
            if board[row + 2][col + 2] != player:
              if row - 4 >= 0 and col - 4 >= 0:
                if board[row - 4][col - 4] != player:
                  return True
              else:
                return True
          else:
            if row - 4 >= 0 and col - 4 >= 0:
              if board[row - 4][col - 4] != player:
                return True
            else:
              return True
        else:
          return True

    # *
    #   *
    #     *
    #       *
    #         P
    if row >= 4 and col >= 4:
      if board[row - 4][col - 4] == player and board[row - 3][col - 3] == player and board[row - 2][col - 2] == player and board[row - 1][col - 1] == player:
        if player == 1:
          if row + 1 < 10 and col + 1 < 10:
            if board[row + 1][col + 1] != player:
              if row - 5 >= 0 and col - 5 >= 0:
                if board[row - 5][col - 5] != player:
                  return True
              else:
                return True
          else:
            if row - 5 >= 0 and col - 5 >= 0:
              if board[row - 5][col - 5] != player:
                return True
            else:
              return True
        else:
          return True

    # Diagonal (Left)
    #         P
    #       *
    #     *
    #   *
    # *
    if row <= 5 and col >= 4:
      if board[row + 1][col - 1] == player and board[row + 2][col - 2] == player and board[row + 3][col - 3] == player and board[row + 4][col - 4] == player:
        if player == 1:
          if row + 5 < 10 and col - 5 >= 0:
            if board[row + 5][col - 5] != player:
              if row - 1 >= 0 and col + 1 < 10:
                if board[row - 1][col + 1] != player:
                  return True
              else:
                return True
          else:
            if row - 1 >= 0 and col + 1 < 10:
              if board[row - 1][col + 1] != player:
                return True
            else:
              return True
        else:
          return True

    #          *
    #        P
    #     *
    #   *
    # *
    if row <= 6 and col >= 3 and row >= 1 and col <= 8:
      if board[row - 1][col + 1] == player and board[row + 1][col - 1] == player and board[row + 2][col - 2] == player and board[row + 3][col - 3] == player:
        if player == 1:
          if row + 4 < 10 and col - 4 >= 0:
            if board[row + 4][col - 4] != player:
              if row - 2 >= 0 and col + 2 < 10:
                if board[row - 2][col + 2] != player:
                  return True
              else:
                return True
          else:
            if row - 2 >= 0 and col + 2 < 10:
              if board[row - 2][col + 2] != player:
                return True
            else:
              return True
        else:
          return True

    #          *
    #        *
    #     P
    #   *
    # *
    if row <= 7 and col >= 2 and row >= 2 and col <= 7:
      if board[row - 2][col + 2] == player and board[row - 1][col + 1] == player and board[row + 1][col - 1] == player and board[row + 2][col - 2] == player:
        if player == 1:
          if row + 3 < 10 and col - 3 >= 0:
            if board[row + 3][col - 3] != player:
              if row - 3 >= 0 and col + 3 < 10:
                if board[row - 3][col + 3] != player:
                  return True
              else:
                return True
          else:
            if row - 3 >= 0 and col + 3 < 10:
              if board[row - 3][col + 3] != player:
                return True
            else:
              return True
        else:
          return True

    #          *
    #        *
    #     *
    #   P
    # *
    if row <= 8 and col >= 1 and row >= 3 and col <= 6:
      if board[row - 3][col + 3] == player and board[row - 2][col + 2] == player and board[row - 1][col + 1] == player and board[row + 1][col - 1] == player:
        if player == 1:
          if row + 2 < 10 and col - 2 >= 0:
            if board[row + 2][col - 2] != player:
              if row - 4 >= 0 and col + 4 < 10:
                if board[row - 4][col + 4] != player:
                  return True
              else:
                return True
          else:
            if row - 4 >= 0 and col + 4 < 10:
              if board[row - 4][col + 4] != player:
                return True
            else:
              return True
        else:
          return True

    #          *
    #        *
    #     *
    #   *
    # P
    if row >= 4 and col <= 5:
      if board[row - 4][col + 4] == player and board[row - 3][col + 3] == player and board[row - 2][col + 2] == player and board[row - 1][col + 1] == player:
        if player == 1:
          if row + 1 < 10 and col - 1 >= 0:
            if board[row + 1][col - 1] != player:
              if row - 5 >= 0 and col + 5 < 10:
                if board[row - 5][col + 5] != player:
                  return True
              else:
                return True
          else:
            if row - 5 >= 0 and col + 5 < 10:
              if board[row - 5][col + 5] != player:
                return True
            else:
              return True
        else:
          return True

  return False

wins = set()
allMoves = set()
def getWins(board, lastPlayer):
  global wins, allMoves
  nextPlayer = 1 if lastPlayer == 2 else 2
  moves = getPossibleMoves(board, nextPlayer)
  for move, newBoard in moves.iteritems():
    h = getHash(newBoard, winningPlayer)
    if h not in allMoves:
      boardWins = isWin(newBoard, winningPlayer, move)
      allMoves.add(h)
      if boardWins:
        wins.add(h)
      else:
        getWins(newBoard, nextPlayer)

board = []
for r in range(10):
  columns = [0]*10
  board.append(columns)
getWins(board, losingPlayer)

print wins
