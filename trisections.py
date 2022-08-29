# main "trisection" class files

# To add:

# -triplanes:
# compute fundamental group of triplane diagram; input: triplane class -> output grouppres class
# compute peripheral subgroup

# -knots, etc
# compute pd code from knot
# unlink detection -- use PD code to compute invariants using snappy
# then certify unlink using LinkInfo database
# make sure tangles are legitimate, i.e, can be built with no crossings


def wirtrep(rel):
    wstr = ""
    if(len(rel) == 0):
        wstr = "1 "
        return wstr
    i = 0
    while i < len(rel):
        c = list[i]
        exp = 1
        j = i+1
        while j < len(rel):
            if(rel[j] == c):
                exp += 1
                j += 1
            else:
                break
        i = j
        if(c>0 and exp==1):
            wstr += ("x"+str(c)+" ")
        elif(c>0):
            wstr += ("x"+str(c)+"^"+str(exp)+" ")
        else:
            wstr += ("x"+str(-1*c)+"^"+str(-1*exp)+" ")
    return wstr

def wirtrep_magma(rel):
    wstr = ""
    if(len(rel) == 0):
        wstr = "1"
        return wstr
    i = 0
    while i < len(rel):
        c = list[i]
        exp = 1
        j = i+1
        while j < len(rel):
            if(rel[j] == c):
                exp += 1
                j += 1
            else:
                break
        i = j
        if(c>0 and exp==1):
            wstr += ("x"+str(c)+"*")
        elif(c>0):
            wstr += ("(x"+str(c)+")^"+str(exp)+"*")
        else:
            wstr += ("(x"+str(-1*c)+")^"+str(-1*exp)+"*")
    wstr = wstr[:-1]
    return wstr


class Braid:

    # constructor; initializes number of strands and presentation in Artin generators
    def __init__(self, strands, braid):

        self.strands = strands
        self.braid = braid

        # error checking
        if type(strands) != int or type(braid) != list:
            raise "Something went wrong with your braid input."
        if len(self.braid) != 0 and max(self.braid) > self.strands - 1:
            raise "The braid you tried to build doesn't have enough strands."

    # representation
    def __repr__(self):
        return "Braid on {} strands given by {} in Artin generators.".format(self.strands, self.braid)

    # adding method
    def __add__(self, other):
        if type(other) != Braid:
            raise "You tried to add a braid to something that isn't a braid."
        if self.strands != other.strands:
            raise "You can't add these braids together!"

        return Braid(self.strands, self.braid + other.braid)

    # drawing method
    def draw(self):

        drawing = ""

        # something to print in the empty case
        if len(self.braid) == 0:
            drawing = "| " * (self.strands - 1) + "|\n"
            return drawing
        else:
            # print the braid
            for element in self.braid[::-1]:
                line = ""
                if element > 0:
                    for i in range(element - 1):
                        line += "| "
                    line += "`/,"
                    for i in range(int((2 * self.strands - 1 - 3 - 2 * (element - 1)) / 2)):
                        line += " |"
                    line += "\n"
                    drawing += line

                if element < 0:
                    for i in range(-element - 1):
                        line += "| "
                    line += ",\`"
                    for i in range(int((2 * self.strands - 1 - 3 - 2 * (-element - 1)) / 2)):
                        line += " |"
                    line += "\n"
                    drawing += line

            return drawing

    # this method returns the mirror of the braid
    def mirror(self):
        return Braid(self.strands, [-i for i in self.braid])


# for us, a tangle will be a braid with a (crossing-less) identification of the endpoints.
# if you want wickets, you can just call it with the word "wickets"
class Tangle:

    # constructor
    def __init__(self, braid, endpoints):
        self.strands = braid.strands
        if endpoints == 'wickets':
            wickets = {}
            for i in range(1, self.strands + 1):
                if i % 2 == 0:
                    wickets[i] = i - 1
                if i % 2 == 1:
                    wickets[i] = i + 1
            self.endpoints = wickets
        else:
            self.endpoints = endpoints

        self.braid = braid

        # check that every endpoint is paired correctly
        for key in self.endpoints:
            if key not in self.endpoints.values() or self.endpoints[key] == key:
                raise "Tangle wasn't set up correctly!"

        # check that this tangle can be built without crossings

    # representation
    def __repr__(self):
        return "Tangle on {} strands, braid given by {} with endpoints identified as {}.".format(self.strands,
                                                                                                 self.braid,
                                                                                                 self.endpoints)

    # draw the tangle!
    def draw(self):

        # need to figure out the set of distances between hoops
        distances = set()
        for strand in self.endpoints:
            distances.add(abs(strand - self.endpoints[strand]))

        # initialize an empty line list, so we can point to characters like a matrix
        print_width = 2 * self.strands - 1  # set up the print width
        drawing_list = [[" " for i in range(print_width)] for j in range(len(distances) + 1)]
        
        # draw the vertical lines
        for strand in self.endpoints:

            # figure out how high we need to go
            high = sorted(distances).index(abs(strand - self.endpoints[strand])) + 1
            for h in range(high):
                drawing_list[h][2 * strand - 2] = "|"

        # now, draw the horizontal lines
        for strand in self.endpoints:
            # figure out height
            high = sorted(distances).index(abs(strand - self.endpoints[strand])) + 1
            for i in range(2 * strand - 1, 2 * self.endpoints[strand] - 2):
                drawing_list[high][i] = "_"

        # now convert back to a multi-line string
        drawing = ""
        for height in range(len(distances) + 1)[::-1]:
            for character in range(print_width):
                drawing += drawing_list[height][character]
            drawing += "\n"

        # now add this to the braid and return
        if (self.braid).braid == []:
            return drawing
        else:
            return drawing + self.braid.draw()

    # mirror of a tangle
    def mirror(self):
        return Tangle(self.braid.mirror(), self.endpoints)


# our basic "knot in bridge position" class; given as the union of two tangles.
# needs fixing
class Knot:

    # constructor
    def __init__(self, top, bottom):
        self.top = top
        self.bottom = bottom
        self.strands = top.strands

        bottom_word = [i for i in ((self.bottom).braid).braid[::-1]]
        self.braid = Braid(self.strands, bottom_word) + top.braid

        if type(top) != Tangle or type(bottom) != Tangle:
            raise "Knot wasn't set up correctly; you need to declare two tangles"
        if self.top.strands != self.strands or self.bottom.strands != self.strands:
            raise "Knot wasn't set up correctly; mismatched strands"

    # representation
    def __repr__(self):
        return "Knot in {}-bridge position.".format(int(self.strands / 2))

    # drawing! Use the tangle drawing methods
    def draw(self, bridges=False):

        # the top drawing is easy
        top_drawing = self.top.draw()

        # the bottom drawing takes a bit more work
        bottom_first_try = [line for line in (self.bottom.draw()).splitlines()[::-1]]

        bottom_drawing = ""
        for line in bottom_first_try:
            bottom_drawing += line + "\n"

        bottom_drawing = bottom_drawing.replace("_", "-")

        # optional bridges
        if bridges:
            return top_drawing + "=" * (2 * self.strands - 1) + "\n" + bottom_drawing
        else:
            return top_drawing + bottom_drawing


    # compute the pd code of the knot: this will be important for unlink detection
    def pdcode(self):
        pass

    # this will be the tricky one
    def is_unknot(self):
        pass


class Triplane:

    def __init__(self, t1, t2, t3):
        self.tangle_1 = t1
        self.tangle_2 = t2
        self.tangle_3 = t3

        self.strands = t1.strands

        if t1.strands != t2.strands or t2.strands != t3.strands or t3.strands != t1.strands:
            raise "Can't construct this triplane diagram; number of strands doesn't match!"

        # also need to compute whether it's valid here. 

    def __repr__(self):
        return "({},?)-triplane diagram.".format(int(self.strands/2))

    # drawing all three tangles side by side
    def draw(self):

        drawing = ""
        # first, get each drawing
        t1_lines = ((self.tangle_1).draw()).splitlines()
        t2_lines = ((self.tangle_2).draw()).splitlines()
        t3_lines = ((self.tangle_3).draw()).splitlines()

        height = max(len(t1_lines), len(t2_lines), len(t3_lines))

        for i in range(height - len(t1_lines)):
            t1_lines.insert(0, (2*(self.tangle_1).strands - 1)*" ")
        for i in range(height - len(t2_lines)):
            t2_lines.insert(0, (2*(self.tangle_2).strands - 1)*" ")
        for i in range(height - len(t3_lines)):
            t3_lines.insert(0, (2*(self.tangle_3).strands - 1)*" ")

        for h in range(height):
            drawing += t1_lines[h] + " "*5 + t2_lines[h] + " "*5 + t3_lines[h] + "\n"
        drawing += (3*(2*self.strands-1) + 10) * "*"
        return drawing

    # check if this really is a valid triplane diagram -- gets called in constructor
    def is_valid(self):
        pass
    
    def fundamental_group_arbitrary(self):

        def generators_initialize_arbitrary(n):
            generators = [None]*n
            for i in range(n):
                if(i%2 == 0):
                    generators[i] = [i+1]
                else:
                    generators[i] = [-1*(i+1)]
            return generators

        def generators_percolate(generatorsp,braid1):
            generators = generatorsp.copy()
            braid = braid1.braid
            for i in range(len(braid)):
                e = braid[i]
                if(e>0):
                    temp = generators[e].copy() #the undercrossing element
                    generators[e] = generators[e-1].copy() #transfers the overcrossing element
                    generators[e-1] += temp.copy() #[e-1] now holds the overcrossing followed by the undercrossing element
                    temp = generators[e].copy() #temp now holds the overcrossing element
                    for j in range(len(temp)): #temp will now hold the inverse of the overcrossing element
                        temp[j] = -temp[j]
                    generators[e-1] += temp.copy() #[e-1] now holds the undercrossing element conjugated by the overcrossing element
                else:
                    e = -e
                    temp = generators[e-1].copy() #the undercrossing element
                    generators[e-1] = generators[e].copy() #transfers the overcrossing element
                    for j in range(len(generators[e])): #[e] will now hold the inverse of the overcrossing element
                        generators[e][j] = -generators[e][j]
                    generators[e] += temp.copy() #now holding the inverse overcrossing element followed by the undercrossing
                    generators[e] += generators[e-1].copy() #[e] now holds the undercrossing element conjugated by the overcrossing
            return generators

        def generators_simplify(generatorsp):
            generators = generatorsp.copy()
            for i in range(len(generators)):
                c = 0
                while(c == 0):
                    c = 1
                    for j in range(len(generators[i])-1):
                        if(generators[i][j] == -1*generators[i][j+1]):
                            generators[i].pop(j)
                            generators[i].pop(j)
                            c = 0
                            break
            return generators

        def generators_to_relations_alternating(generators):
            n = int(len(generators)/2)
            relations = [None]*(n)
            for i in range(n):
                relations[i] = generators[2*i].copy()
                relations[i] += generators[2*i+1].copy()
            return relations
        
        generators = generators_initialize_arbitrary(self.strands)


        generators1 = generators.copy()
        generators1 = generators_percolate(generators1,self.tangle_1.braid)
        generators1 = generators_simplify(generators1)
        print(generators1)

        generators2 = generators.copy()
        generators2 = generators_percolate(generators2,self.tangle_2.braid)
        generators2 = generators_simplify(generators2)
        print(generators2)

        generators3 = generators.copy()
        generators3 = generators_percolate(generators3,self.tangle_3.braid)
        generators3 = generators_simplify(generators3)
        print(generators3)


        relations = generators_to_relations_alternating(generators1)
        relations += generators_to_relations_alternating(generators2)
        relations += generators_to_relations_alternating(generators3)

        group = GroupPres(self.strands,relations)

        return group

    def fundamental_group_A_trivial(self):

        def generators_initialize_A_trivial(n):
            generators = [None]*n
            for i in range(n):
                if(i%2 == 0):
                    generators[i] = [i+1]
                else:
                    generators[i] = [-1*(i)]
            return generators

        def generators_percolate(generatorsp,braid1):
            generators = generatorsp.copy()
            braid = braid1.braid
            for i in range(len(braid)):
                e = braid[i]
                if(e>0):
                    temp = generators[e].copy() #the undercrossing element
                    generators[e] = generators[e-1].copy() #transfers the overcrossing element
                    generators[e-1] += temp.copy() #[e-1] now holds the overcrossing followed by the undercrossing element
                    temp = generators[e].copy() #temp now holds the overcrossing element
                    for j in range(len(temp)): #temp will now hold the inverse of the overcrossing element
                        temp[j] = -temp[j]
                    generators[e-1] += temp.copy() #[e-1] now holds the undercrossing element conjugated by the overcrossing element
                else:
                    e = -e
                    temp = generators[e-1].copy() #the undercrossing element
                    generators[e-1] = generators[e].copy() #transfers the overcrossing element
                    for j in range(len(generators[e])): #[e] will now hold the inverse of the overcrossing element
                        generators[e][j] = -generators[e][j]
                    generators[e] += temp.copy() #now holding the inverse overcrossing element followed by the undercrossing
                    generators[e] += generators[e-1].copy() #[e] now holds the undercrossing element conjugated by the overcrossing
            return generators

        def generators_simplify(generatorsp):
            generators = generatorsp.copy()
            for i in range(len(generators)):
                c = 0
                while(c == 0):
                    c = 1
                    for j in range(len(generators[i])-1):
                        if(generators[i][j] == -1*generators[i][j+1]):
                            generators[i].pop(j)
                            generators[i].pop(j)
                            c = 0
                            break
            return generators

        def generators_to_relations_alternating(generators):
            n = int(len(generators)/2)
            relations = [None]*(n)
            for i in range(n):
                relations[i] = generators[2*i].copy()
                relations[i] += generators[2*i+1].copy()
            return relations
        
        generators = generators_initialize_A_trivial(self.strands)


        generators2 = generators.copy()
        generators2 = generators_percolate(generators2,self.tangle_2.braid)
        generators2 = generators_simplify(generators2)
        print(generators2)

        generators3 = generators.copy()
        generators3 = generators_percolate(generators3,self.tangle_3.braid)
        generators3 = generators_simplify(generators3)
        print(generators3)


        relations = generators_to_relations_alternating(generators2)
        relations += generators_to_relations_alternating(generators3)

        group = GroupPres(self.strands,relations)

        return group


class GroupPres:

    # constructor
    def __init__(self, gens, rels):
        self.gens = gens
        self.rels = rels

        if type(gens) != int or gens <= 0:
            raise "Group presentation not set up correctly: generators must a positive integer."

        if type(rels) != list:
            raise "Group presentation not set up correctly: relations must be a list of integers."

        for relation in self.rels:
            for i in relation:
                if abs(i) > gens:
                    raise "Group presentation not set up correctly: more generators than specified."

    # representation
    def __repr__(self):
        return "Group presentation on {} generators with {} relations.".format(self.gens, len(self.rels))

    # add generators
    def add_gens(self, number):
        if number <= 0:
            raise "You can't delete generators."
        self.gens += number

    # add relations
    def add_rels(self, new_rels):
        if type(new_rels) != list:
            raise "Something went wrong: you can't add this as a relation."
        (self.rels).append(new_rels)

    def wirt(self):
        wirt = "("
        for i in range(gens):
            wirt += "x" + str(i+1)
            if(i != n-1):
                wirt += ", "
        if(len(rels) == 0):
            wirt += ")"
            return wirt
        wirt += " | "
        for i in range(len(rels)):
            if(i != 0):
                wirt += ", "
            wirt += wirtrep(rels[i])
            wirt += "= 1"
        wirt += ")"
        return wirt

    def wirt_magma(self):
        generators = ""
        for i in range(gens):
            generators += "x" + str(i+1)
            if(i != n-1):
                generators += ","
        wirt = "G<"
        wirt += generators
        wirt += "> := FPGroup< "
        wirt += generators
        if(len(rels) == 0):
            wirt += ">"
            return wirt
        wirt += " | "
        for i in range(len(rels)):
            if(i != 0):
                wirt += ","
            wirt += wirtrep_magma(rels[i])
        wirt += " >"
        return wirt

    # G<x,y> := FPGroup< x,y |  y^-1*x*y*x^-1*y*x*y^-1*x^-1*y*x^-1,y^2 >;
    # magma format
