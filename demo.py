import trisections as tri

braid = tri.Braid(4, [1,-2])
tangle = tri.Tangle(braid, "wickets")
print(tangle.draw())


gp = tri.GroupPres(4,[[1,2]])
print(gp)
gp.add_gens(2)
gp.add_rels([[1,2]])
print(gp)