import copy
import sys
import time

currentPlayer = None

playedMoves = set()

MAX_TURN_LENGTH = 4.8
MAX_DEPTH = 10

MAX_INT = sys.maxint
MIN_INT = -sys.maxint - 1

HEURISTIC_VALUES =[100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 200, 200, 200, 200, 200, 200, 200, 200, 100, 100, 200, 300, 300, 300, 300, 300, 300, 200, 100, 100, 200, 300, 400, 400, 400, 400, 300, 200, 100, 100, 200, 300, 400, 500, 500, 400, 300, 200, 100, 100, 200, 300, 400, 500, 500, 400, 300, 200, 100, 100, 200, 300, 400, 400, 400, 400, 300, 200, 100, 100, 200, 300, 300, 300, 300, 300, 300, 200, 100, 100, 200, 200, 200, 200, 200, 200, 200, 200, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100]

TWO_HUNDRED_PRIMES = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97,101,103,107,109,113,127,131,137,139,149,151,157,163,167,173,179,181,191,193,197,199,211,223,227,229,233,239,241,251,257,263,269,271,277,281,283,293,307,311,313,317,331,337,347,349,353,359,367,373,379,383,389,397,401,409,419,421,431,433,439,443,449,457,461,463,467,479,487,491,499,503,509,521,523,541,547,557,563,569,571,577,587,593,599,601,607,613,617,619,631,641,643,647,653,659,661,673,677,683,691,701,709,719,727,733,739,743,751,757,761,769,773,787,797,809,811,821,823,827,829,839,853,857,859,863,877,881,883,887,907,911,919,929,937,941,947,953,967,971,977,983,991,997,1009,1013,1019,1021,1031,1033,1039,1049,1051,1061,1063,1069,1087,1091,1093,1097,1103,1109,1117,1123,1129,1151,1153,1163,1171,1181,1187,1193,1201,1213,1217,1223]

def printBoard(board):
  for row in board:
    print ' '.join([ '%s' % r for r in row ])

def getPossibleMoves(board):
  moves = []
  for row in range(10): #[5, 4, 6, 3, 7, 2, 8, 1, 9, 0]:
    for col in range(10): #[5, 4, 6, 3, 7, 2, 8, 1, 9, 0]:
      # Only include moves that are adjacent to already played pieces, or in the center of the board.
      if board[row][col] == 0 and (
          (row - 1 >= 0 and (
            board[row - 1][col] != 0 or
            (col + 1 < 10 and board[row - 1][col + 1] != 0) or
            (col - 1 >= 0 and board[row - 1][col - 1] != 0)
          )) or
          (row + 1 < 10 and (
            board[row + 1][col] != 0 or
            (col + 1 < 10 and board[row + 1][col + 1] != 0) or
            (col - 1 >= 0 and board[row + 1][col - 1] != 0)
          )) or
          (col + 1 < 10 and board[row][col + 1] != 0) or
          (col - 1 >= 0 and board[row][col - 1] != 0) or
          (row >= 4 and row <= 6 and col >= 4 and col <= 6)
        ):
        moves.append((row, col))
  return moves

def getHash(board):
  h = 0
  for row in range(10):
    for col in range(10):
      piece = board[row][col]
      if piece != 0:
        h += TWO_HUNDRED_PRIMES[(row*10 + col)*piece]
  return h

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

def getHeuristic(board, move, player):
  row = move[0]
  col = move[1]
  piece = board[row][col]

  potentialWins = 0

  if col + 1 < 10:
    potentialWins += board[row][col + 1] == player
    potentialWins += (row + 1 < 10 and board[row + 1][col + 1] == player)
    potentialWins += (row - 1 >= 0 and board[row - 1][col + 1] == player)
    if col + 2 < 10:
      potentialWins += board[row][col + 2] == player
      potentialWins += (row + 2 < 10  and board[row + 2][col + 2] == player)
      potentialWins += (row - 2 >= 0 and board[row - 2][col + 2] == player)
      if col + 3 < 10:
        potentialWins += board[row][col + 3] == player
        potentialWins += (row + 3 < 10 and board[row + 3][col + 3] == player)
        potentialWins += (row - 3 >= 0 and board[row - 3][col + 3] == player)
        if col + 4 < 10:
          potentialWins += board[row][col + 4] == player
          potentialWins += (row + 4 < 10 and board[row + 4][col + 4] == player)
          potentialWins += (row - 4 >= 0 and board[row - 4][col + 4] == player)

  if col - 1 < 10:
    potentialWins += board[row][col - 1] == player
    potentialWins += (row + 1 < 10 and board[row + 1][col - 1] == player)
    potentialWins += (row - 1 >= 0 and board[row - 1][col - 1] == player)
    if col - 2 < 10:
      potentialWins += board[row][col - 2] == player
      potentialWins += (row + 2 < 10  and board[row + 2][col - 2] == player)
      potentialWins += (row - 2 >= 0 and board[row - 2][col - 2] == player)
      if col - 3 < 10:
        potentialWins += board[row][col - 3] == player
        potentialWins += (row + 3 < 10 and board[row + 3][col - 3] == player)
        potentialWins += (row - 3 >= 0 and board[row - 3][col - 3] == player)
        if col - 4 < 10:
          potentialWins += board[row][col - 4] == player
          potentialWins += (row + 4 < 10 and board[row + 4][col - 4] == player)
          potentialWins += (row - 4 >= 0 and board[row - 4][col - 4] == player)

  # Vertical
  if row + 1 < 10:
    potentialWins += board[row + 1][col] == player
    if row + 2 < 10:
      potentialWins += board[row + 2][col] == player
      if row + 3 < 10:
        potentialWins += board[row + 3][col] == player
        potentialWins += (row + 4 < 10 and board[row + 4][col] == player)

  if row - 1 >= 0:
    potentialWins += board[row - 1][col] == player
    if row - 2 >= 0:
      potentialWins += board[row - 2][col] == player
      if row - 3 >= 0:
        potentialWins += board[row - 3][col] == player
        potentialWins += (row - 4 >= 0 and board[row - 4][col] == player)

  return potentialWins*1000 + HEURISTIC_VALUES[row*10 + col]*20

def max_play(board, player, depth, max_depth, startTime):
  nextPlayer = 2 if player == 1 else 1
  moves = getPossibleMoves(board)
  best_score = MIN_INT
  for move in moves:
    if time.time() - startTime > MAX_TURN_LENGTH:
      break
    # Set the move.
    board[move[0]][move[1]] = player
    h = getHash(board)
    if h not in playedMoves:
      playedMoves.add(h)
      score = MIN_INT
      if isWin(board, player, move):
        score = MAX_INT
      else:
        heuristic = getHeuristic(board, move, player)
        #print h
        if depth >= max_depth:
          score = heuristic*depth
        else:
          score = min_play(board, nextPlayer, depth + 1, max_depth, startTime)
      if score > best_score:
        best_score = score
    # Unset the move.
    board[move[0]][move[1]] = 0
  return best_score

def min_play(board, player, depth, max_depth, startTime):
  nextPlayer = 2 if player == 1 else 1
  moves = getPossibleMoves(board)
  best_score = MAX_INT
  for move in moves:
    if time.time() - startTime > MAX_TURN_LENGTH:
      break
    # Set the move.
    board[move[0]][move[1]] = player
    h = getHash(board)
    if h not in playedMoves:
      playedMoves.add(h)
      score = MAX_INT
      if isWin(board, player, move):
        score = MIN_INT
      else:
        heuristic = getHeuristic(board, move, player)
        #print h
        if depth >= max_depth:
          score = heuristic*depth
        else:
          score = max_play(board, nextPlayer, depth + 1, max_depth, startTime)
      if score < best_score:
        best_score = score
    # Unset the move.
    board[move[0]][move[1]] = 0
  return best_score

def minimax(board, player, currentDepth):
  best_score = MIN_INT
  nextPlayer = 2 if player == 1 else 1
  moves = getPossibleMoves(board)
  best_move = moves[-1]
  startTime = time.time()
  for move in moves:
    board[move[0]][move[1]] = player
    score = min_play(board, nextPlayer, 0, MAX_DEPTH, startTime)
    board[move[0]][move[1]] = 0
    if score > best_score:
      best_score = score
      best_move = move
  return best_move

startingBoard = []

# Parse the input. This assumes well formed input.
currentMoveCount = 0
for line in sys.stdin:
  columns = [ int(col.strip()) for col in line.split(' ') ]
  currentMoveCount += 10 - columns.count(0)
  startingBoard.append(columns)

# Remove the last row to figure out which player we are.
currentPlayer = startingBoard[-1][0]
del startingBoard[-1]

bestMove = minimax(startingBoard, currentPlayer, currentMoveCount)
print '%s %s' % bestMove
