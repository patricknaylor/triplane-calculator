# this is just a testing file; modify freely

import trisections as tri

braid = tri.Braid(4, [1,-2])
tangle = tri.Tangle(braid, "wickets")
tangle2 = tri.Tangle(tri.Braid(4, [3]), {1:4, 2:3, 3:2, 4:1})

print(tangle.draw())
print((tangle.mirror()).draw())
knot = tri.Knot(tangle2, tangle.mirror())
knot.pdcode()

print((knot.braid).draw())
print(knot.draw())