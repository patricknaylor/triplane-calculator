# here are some class files for the objects we'll need.
# includes "Braid" at the moment; maybe others

# To add:
# triplane diagrams
# compute pd code?
# unlink detection -- tentative plan: get PD code by gluing braid to crossing-less tangles;
# then compute everything in snappy
# make sure tangles can be built with no crossings

class Braid:

    # constructor; initializes number of strands and presentation in Artin generators
    def __init__(self, strands, word):

        self.strands = strands
        self.word = word

        # error checking
        if type(strands) != int or type(word) != list:
            raise "Something went wrong with your braid input."
        if len(self.word) != 0 and max(self.word) > self.strands - 1:
            raise "The braid you tried to build doesn't have enough strands."

    # representation
    def __repr__(self):
        return "Braid on {} strands given by {} in Artin generators.".format(self.strands, self.word)

    # adding method
    def __add__(self, other):
        if type(other) != Braid:
            raise "You tried to add a braid to something that isn't a braid."
        if self.strands != other.strands:
            raise "You can't add these braids together!"

        return Braid(self.strands, self.word + other.word)

    # drawing method
    def draw(self):

        drawing = ""

        # something to print in the empty case
        if len(self.word) == 0:
            drawing = "| " * (self.strands - 1) + "|\n"
            return drawing
        else:
            # print the braid
            for element in self.word:
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
        return Braid(self.strands, [-i for i in self.word])


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
        if (self.braid).word == []:
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

    # mirroring
    def mirror(self):
        pass

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

        # first, get each drawing
        t1_lines = ((self.tangle_1).draw()).splitlines()
        t2_lines = ((self.tangle_2).draw()).splitlines()
        t3_lines = ((self.tangle_3).draw()).splitlines()









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



