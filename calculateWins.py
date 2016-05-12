import sys
def calcH(p1, p2, p3, p4, p5):
  print '%s %s %s %s %s' % (p1, p2, p3, p4, p5)
  return p1 << 8 ^ p2 << 6 ^ p3 << 4 ^ p4 << 2 ^ p5

MAX_INT = sys.maxint

LOOKUP = [0]*690
for player in range(2):
  color = player + 1
  for p1 in range(2):
    for p2 in range(2):
      for p3 in range(2):
        for p4 in range(2):
          for p5 in range(2):
            h = calcH(p1 * color, p2 * color, p3 * color, p4 * color, p5 * color)
            val = 10 ** (p1 + p2 + p3 + p4 + p5)
            if p1 == p2 and p2 == p3 and p3 == p4 and p4 == p5 and p1 != 0:
              val = MAX_INT
            LOOKUP[h] = val

print LOOKUP
print LOOKUP[calcH(1, 2, 0, 1, 1)]