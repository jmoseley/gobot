import sys
def calcH(p0, p1, p2, p3, p4, p5, p6):
  return p0 << 12 ^ p1 << 10 ^ p2 << 8 ^ p3 << 6 ^ p4 << 4 ^ p5 << 2 ^ p6

MAX_INT = sys.maxint

LOOKUP = [0]*10930
for player in range(2):
  color = player + 1
  for p1 in range(2):
    for p2 in range(2):
      for p3 in range(2):
        for p4 in range(2):
          for p5 in range(2):
            exponent = (p1 + p2 + p3 + p4 + p5)
            if exponent >= 3:
              val = 10 ** exponent
              if exponent == 5:
                val = MAX_INT
              h = calcH(0, p1 * color, p2 * color, p3 * color, p4 * color, p5 * color, 0)
              LOOKUP[h] = val
              for borderPlayer in range(2):
                borderColor = borderPlayer + 1
                if (color == 1 and borderColor != 1) or color == 2:
                  h = calcH(1 * borderColor, p1 * color, p2 * color, p3 * color, p4 * color, p5 * color, 0)
                  LOOKUP[h] = val
                  h = calcH(0, p1 * color, p2 * color, p3 * color, p4 * color, p5 * color, 1 * borderColor)
                  LOOKUP[h] = val
                  h = calcH(1 * borderColor, p1 * color, p2 * color, p3 * color, p4 * color, p5 * color, 1 * borderColor)
                  LOOKUP[h] = val

print LOOKUP