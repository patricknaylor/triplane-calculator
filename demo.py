# this is just a testing file; modify freely

import trisections as tri

braid = tri.Braid(4, [1,-2])
tangle = tri.Tangle(braid, "wickets")
flat = tri.Tangle(tri.Braid(4,[]),"wickets")
#print(tangle.draw())

triplane = tri.Triplane(tri.Tangle(tri.Braid(4, [1,3,-2,1]), "wickets"), tangle.mirror(), flat)
print(triplane.draw())


gp = tri.GroupPres(4,[[1,2]])
print(gp)
gp.add_gens(2)
gp.add_rels([[1,2]])
print(gp)