import copy
import sys
import time

currentPlayer = None

playedMoves = set()

MAX_TURN_LENGTH = 4.8
MAX_DEPTH = 3

MAX_INT = sys.maxint
MIN_INT = -sys.maxint - 1

HEURISTIC_VALUES =[100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 200, 200, 200, 200, 200, 200, 200, 200, 100, 100, 200, 300, 300, 300, 300, 300, 300, 200, 100, 100, 200, 300, 400, 400, 400, 400, 300, 200, 100, 100, 200, 300, 400, 500, 500, 400, 300, 200, 100, 100, 200, 300, 400, 500, 500, 400, 300, 200, 100, 100, 200, 300, 400, 400, 400, 400, 300, 200, 100, 100, 200, 300, 300, 300, 300, 300, 300, 200, 100, 100, 200, 200, 200, 200, 200, 200, 200, 200, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100]

ZOBRIST = [[7290265662272011974, 7884192977348706402, 8276608735294253170, 6257272580128527177, 3826322599972342146, 8763581601468893181, 6623211701908720727, 2311043642590771844, 577138791170082020, 2151790476447217852, 8884812645859972208, 7891617826428733006, 308347041185362948, 3380819997952635361, 5408056050269713311, 3548387399104207712, 6878113415679622319, 5426163895622046575, 8227346488697563383, 5258070279882873042, 3297051373848447333, 6317017261038603701, 7425372210164420828, 8497396498345598773, 1644909507234680917, 1140730245951785357, 300123338418939639, 1602468880189200012, 2982699448865927713, 7364618189373832780, 4709534388439936588, 2975503629424874163, 8998044173611233261, 6590193987666937554, 8661892203589989716, 9132115223390870148, 7339523591090208603, 3511237179152245691, 1804203940455887617, 519186202297288754, 683687765591196346, 2953582720194739670, 8300321981513198409, 972801447586547964, 8301424351696489286, 3771363043529057370, 8042347444844442379, 914893860307763825, 4666147092386989247, 7490003691892603695, 5961155937320682751, 9146213095763115877, 2821136781364438670, 3471628947281402060, 4103738291052017780, 25329723041668855, 6774276217878035311, 3284575622143046437, 6232862891574728320, 185483119068229035, 1059584181765127005, 4160355973461878002, 9015035266721131286, 470325562851708821, 6954986301340979835, 4162436661961625084, 4384189587251086044, 5058556557785393340, 4220550258701761220, 4133633248962158451, 936054263570807707, 1378920764458066863, 5753759861723018534, 6227981192537824038, 5542739044605895973, 4381532213941648687, 6344360308512892478, 1769768646944970558, 5410481269696977461, 5519982486939045013, 3938025647349968504, 9221252597257392112, 7198298237383806949, 3548985249638864697, 6554027372043574584, 1468996564281267510, 2209055615455469286, 4769601675195838476, 6908853458788999810, 5896156783399673384, 8592737776064682928, 4395926629254573291, 118943718616630665, 2445325008130591126, 1017322887312792154, 6851038760195257473, 3349818810447980154, 9180845536076830859, 1415082600966829138, 8793258376049394618], [1515607145219025427, 2310514410154383833, 75602807467007795, 3736589759593807096, 8569974774231535839, 2381348120996325102, 6434775176476791857, 7228919215893118212, 4511028396846405658, 5804234688736858349, 6461713518683712814, 5700185475523449599, 4537947802518477848, 3164579690432780253, 2081253449731706938, 1095200519755841103, 1168933908768660552, 2914591247599665265, 5563992229965048862, 3778271935518133562, 1953168760001205531, 4425621528397426413, 9071234697792836172, 287447553706410381, 7988514133051625914, 3707738523204327381, 1284849472278667929, 6678927446390711759, 5680122694095354196, 5058503320047444575, 4004431658440535620, 2164139851352780654, 6864248087316101329, 4270944855413503204, 5034870302412543544, 1128384108661548343, 4869169700246872767, 3125950886892479546, 7278280434526279337, 4115936417309503514, 5480965827229017092, 2883719104762268969, 297746066717249775, 6383926084622783195, 2107287639079378164, 6586722825801836374, 9147376472942169981, 2015028097855682183, 4296834638343230412, 3302045871840643185, 4753953043907706334, 1883628674730888852, 2959997424212390486, 5829764440547530093, 6553105742553908741, 4432812284782624084, 1878542471364576815, 372590321695468966, 1008489488610308719, 3005263098813337308, 2350887885154000514, 3592103426236164244, 2386241631285044743, 4651575593477378063, 8926480462405169126, 5924009401913285492, 8180495578577435448, 1817756619037158036, 2261917786456814927, 6331049989600401476, 2766532502262244579, 699663681608765493, 5144966265565660756, 7075569156893435968, 6488737257293844106, 7659511168409991605, 4472283309033491284, 6435878214777819832, 7741239407944097986, 5369199411024138738, 8448938617768247479, 3771468002664835385, 3464124614207715894, 5267702263203034162, 2469603632357129869, 1310026544733860136, 255685458253700228, 3781290313545404092, 4988941002521439368, 1770110568609622304, 8869271410406055914, 5932189649155246671, 1912384363417201381, 3188949385633120425, 4224169290560438821, 700055381192465510, 1749168603623270232, 2764971252863589012, 5905655873501856231, 7719819448667559672]]

LOOKUP = [1, 10, 10, 0, 10, 100, 0, 0, 10, 0, 100, 0, 0, 0, 0, 0, 10, 100, 0, 0, 100, 1000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0, 100, 0, 0, 0, 0, 0, 100, 0, 1000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 100, 0, 0, 100, 1000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 100, 1000, 0, 0, 1000, 10000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0, 100, 0, 0, 0, 0, 0, 100, 0, 1000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 100, 0, 1000, 0, 0, 0, 0, 0, 1000, 0, 10000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 100, 0, 0, 100, 1000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 100, 1000, 0, 0, 1000, 10000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 100, 1000, 0, 0, 1000, 10000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1000, 10000, 0, 0, 10000, 9223372036854775807, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0, 100, 0, 0, 0, 0, 0, 100, 0, 1000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 100, 0, 1000, 0, 0, 0, 0, 0, 1000, 0, 10000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 100, 0, 1000, 0, 0, 0, 0, 0, 1000, 0, 10000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1000, 0, 10000, 0, 0, 0, 0, 0, 10000, 0, 9223372036854775807, 0, 0, 0, 0, 0, 0, 0]

def printBoard(board):
  for row in board:
    print ' '.join([ '%s' % r for r in row ])

def getPossibleMoves(board):
  moves = []
  for row in [5, 4, 6, 3, 7, 2, 8, 1, 9, 0]:
    for col in [5, 4, 6, 3, 7, 2, 8, 1, 9, 0]:
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
          (col - 1 >= 0 and board[row][col - 1] != 0)
        ):
        moves.append((row, col))
  if len(moves) == 0:
    moves = [(4, 4), (4, 5), (4, 6), (5, 4), (5, 5), (5, 6), (6, 4), (6, 5), (6, 6)]
  return moves

def getHash(board, move, previousHash):
  row = move[0]
  col = move[1]
  piece = board[row][col] - 1
  if piece >= 0:
    return previousHash ^ ZOBRIST[piece][row*10 + col]
  else:
    return previousHash

def getWinHash(p1, p2, p3, p4, p5):
  h = p1 << 8 ^ p2 << 6 ^ p3 << 4 ^ p4 << 2 ^ p5
  return LOOKUP[h]

def getHeuristic(board, move, player):
  row = move[0]
  col = move[1]
  heuristic = 0
  # Horizontal
  # P * * * *
  if col + 4 < 10:
    h = getWinHash(board[row][col], board[row][col + 1], board[row][col + 2], board[row][col + 3], board[row][col + 4])
    heuristic += h

  # * P * * *
  if col + 3 < 10 and col - 1 >= 0:
    h = getWinHash(board[row][col - 1], board[row][col], board[row][col + 1], board[row][col + 2], board[row][col + 3])
    heuristic += h

  # * * P * *
  if col + 2 < 10 and col - 2 >= 0:
    h = getWinHash(board[row][col - 2], board[row][col - 1], board[row][col], board[row][col + 1], board[row][col + 2])
    heuristic += h

  # * * * P *
  if col + 1 < 10 and col + 3 >= 0:
    h = getWinHash(board[row][col - 3], board[row][col - 2], board[row][col - 1], board[row][col], board[row][col + 1])
    heuristic += h

  # * * * * P
  if col - 4 >= 0:
    h = getWinHash(board[row][col - 4], board[row][col - 3], board[row][col - 2], board[row][col - 1], board[row][col])
    heuristic += h

  # Vertical
  # P
  # *
  # *
  # *
  # *
  if row + 4 < 10:
    h = getWinHash(board[row][col], board[row + 1][col], board[row + 2][col], board[row + 3][col], board[row + 4][col])
    heuristic += h

  # *
  # P
  # *
  # *
  # *
  if row + 3 < 10 and row - 1 >= 0:
    h = getWinHash(board[row - 1][col], board[row][col], board[row + 1][col], board[row + 2][col], board[row + 3][col])
    heuristic += h

  # *
  # *
  # P
  # *
  # *
  if row + 2 < 10 and row - 2 >= 0:
    h = getWinHash(board[row - 2][col], board[row - 1][col], board[row][col], board[row + 1][col], board[row + 2][col])
    heuristic += h

  # *
  # *
  # *
  # P
  # *
  if row + 1 < 10 and row - 3 >= 0:
    h = getWinHash(board[row - 3][col], board[row - 2][col], board[row - 1][col], board[row][col], board[row + 1][col])
    heuristic += h

  # *
  # *
  # *
  # *
  # P
  if row - 4 >= 0:
    h = getWinHash(board[row - 4][col], board[row - 3][col], board[row - 2][col], board[row - 1][col], board[row][col])
    heuristic += h

  # Diagonal (Right)
  # P
  #   *
  #     *
  #       *
  #         *
  if row + 4 < 10 and col + 4 < 10:
    h = getWinHash(board[row][col], board[row + 1][col + 1], board[row + 2][col + 2], board[row + 3][col + 3], board[row + 4][col + 4])
    heuristic += h

  # *
  #   P
  #     *
  #       *
  #         *
  if row + 3 < 10 and col + 3 < 10 and row - 1 >= 0 and col - 1 >= 0:
    h = getWinHash(board[row - 1][col - 1], board[row][col], board[row + 1][col + 1], board[row + 2][col + 2], board[row + 3][col + 3])
    heuristic += h

  # *
  #   *
  #     P
  #       *
  #         *
  if row + 2 < 10 and col + 2 < 10 and row - 2 >= 0 and col - 2 >= 0:
    h = getWinHash(board[row - 2][col - 2], board[row - 1][col - 1], board[row][col], board[row + 1][col + 1], board[row + 2][col + 2])
    heuristic += h

  # *
  #   *
  #     *
  #       P
  #         *
  if row + 1 < 10 and col + 1 < 10 and row - 3 >= 0 and col - 3 >= 0:
    h = getWinHash(board[row - 3][col - 3], board[row - 2][col - 2], board[row - 1][col - 1], board[row][col], board[row + 1][col + 1])
    heuristic += h

  # *
  #   *
  #     *
  #       *
  #         P
  if row - 4 >= 0 and col - 4 >= 0:
    h = getWinHash(board[row - 4][col - 4], board[row - 3][col - 3], board[row - 2][col - 2], board[row - 1][col - 1], board[row][col])
    heuristic += h

  # Diagonal (Left)
  #         P
  #       *
  #     *
  #   *
  # *
  if row + 4 < 10 and col - 4 >= 0:
    h = getWinHash(board[row][col], board[row + 1][col - 1], board[row + 2][col - 2], board[row + 3][col - 3], board[row + 4][col - 4])
    heuristic += h

  #          *
  #        P
  #     *
  #   *
  # *
  if row + 3 < 10 and col - 3 >= 0 and row - 1 >= 0 and col + 1 < 10:
    h = getWinHash(board[row - 1][col + 1], board[row][col], board[row + 1][col - 1], board[row + 2][col - 2], board[row + 3][col - 3])
    heuristic += h

  #          *
  #        *
  #     P
  #   *
  # *
  if row + 2 < 10 and col - 2 >= 0 and row - 2 >= 0 and col + 2 < 10:
    h = getWinHash(board[row - 2][col + 2], board[row - 1][col + 1], board[row][col], board[row + 1][col - 1], board[row + 2][col - 2])
    heuristic += h

  #          *
  #        *
  #     *
  #   P
  # *
  if row + 1 < 10 and col - 1 >= 0 and row - 3 >= 0 and col + 3 < 10:
    h = getWinHash(board[row - 3][col + 3], board[row - 2][col + 2], board[row - 1][col + 1], board[row][col], board[row + 1][col - 1])
    heuristic += h

  #          *
  #        *
  #     *
  #   *
  # P
  if row - 4 >= 0 and col + 4 < 10:
    h = getWinHash(board[row - 4][col + 4], board[row - 3][col + 3], board[row - 2][col + 2], board[row - 1][col + 1], board[row][col])
    heuristic += h

  return min(heuristic, MAX_INT)

def max_play(board, boardHash, player, depth, startTime, debug):
  nextPlayer = 2 if player == 1 else 1
  moves = getPossibleMoves(board)
  best_score = MIN_INT
  move_played = False
  for move in moves:
    if time.time() - startTime > MAX_TURN_LENGTH:
      break
    # Set the move.
    board[move[0]][move[1]] = player
    h = getHash(board, move, boardHash)
    if h not in playedMoves:
      move_played = True
      playedMoves.add(h)
      score = None
      heuristic = getHeuristic(board, move, player)
      if heuristic != MAX_INT and depth < MAX_DEPTH:
          score = min_play(board, h, nextPlayer, depth + 1, startTime, debug)
      if score is None:
        score = heuristic
      if score > best_score:
        best_score = score
    # Unset the move.
    board[move[0]][move[1]] = 0
  if not move_played:
    return None
  return best_score

def min_play(board, boardHash, player, depth, startTime, debug):
  nextPlayer = 2 if player == 1 else 1
  moves = getPossibleMoves(board)
  best_score = MAX_INT
  move_played = False
  for move in moves:
    if time.time() - startTime > MAX_TURN_LENGTH:
      break
    # Set the move.
    board[move[0]][move[1]] = player
    h = getHash(board, move, boardHash)
    if h not in playedMoves:
      move_played = True
      playedMoves.add(h)
      score = None
      heuristic = -getHeuristic(board, move, player)
      if heuristic != -MAX_INT and depth < MAX_DEPTH:
        score = max_play(board, h, nextPlayer, depth + 1, startTime, debug)
      if score is None:
        score = heuristic
      if score < best_score:
        best_score = score
    # Unset the move.
    board[move[0]][move[1]] = 0
  if not move_played:
    return None
  return best_score

def minimax(board, player, currentDepth):
  best_score = MIN_INT
  nextPlayer = 2 if player == 1 else 1
  moves = getPossibleMoves(board)
  best_move = moves[-1]
  startTime = time.time()
  for move in moves:
    board[move[0]][move[1]] = player
    h = getHash(board, move, 0)
    if h not in playedMoves:
      playedMoves.add(h)
      debug = False
      score = min_play(board, h, nextPlayer, 1, startTime, debug)
      if score is not None and score >= best_score:
        best_score = score
        best_move = move
    board[move[0]][move[1]] = 0
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
