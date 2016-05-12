import sys
def calcH(p0, p1, p2, p3, p4, p5, p6):
  return p0 << 12 ^ p1 << 10 ^ p2 << 8 ^ p3 << 6 ^ p4 << 4 ^ p5 << 2 ^ p6

MAX_INT = sys.maxint

LOOKUP = [0]*10930
for player in range(2):
  color = player + 1
  for p0 in range(2):
    for p1 in range(2):
      for p2 in range(2):
        for p3 in range(2):
          for p4 in range(2):
            for p5 in range(2):
              for p6 in range(2):
                if (color == 1 and p0 == 0 and p6 == 0) or color == 2:
                  h = calcH(p0*color, p1 * color, p2 * color, p3 * color, p4 * color, p5 * color, p6*color)
                  exponent = (p0 + p1 + p2 + p3 + p4 + p5 + p6)
                  if exponent >= 2:
                    val = 10 ** exponent
                    if p1 == p2 and p2 == p3 and p3 == p4 and p4 == p5 and p1 != 0:
                      val = MAX_INT
                    LOOKUP[h] = val

print LOOKUP