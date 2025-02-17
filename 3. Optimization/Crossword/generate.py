import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for var in self.domains:
            var_length = var.length
            valid_val = set()
            for x in self.domains[var]:
                if len(x) == var_length:
                    valid_val.add(x)
            self.domains[var] = valid_val

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revised = False

        overlap = self.crossword.overlaps[x, y]

        if overlap is None:
            return False
        
        i, j = overlap 

        to_remove = set()
        for x_word in self.domains[x]:
            have_satisfy = False
            for y_word in self.domains[y]:
                if y_word[j] == x_word[i]:
                    have_satisfy = True
                    break
            if not have_satisfy:
                to_remove.add(x_word)
                

        self.domains[x] -= to_remove
        revised = True

        return revised


    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        if arcs is None:
            arcs = []
            for x in self.domains:
                for y in self.crossword.neighbors(x):
                    arcs.append((x, y))
        
        while len(arcs) != 0:
            x, y = arcs.pop()
            if self.revise(x, y):
                if len(self.domains[x]) == 0:
                    return False
                for z in self.crossword.neighbors(x):
                    if z != y:
                        arcs.append((z, x))
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        if len(assignment) == len(self.domains):
            return True
        else:
            return False

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # to check if all values are distinct
        values = set()
        #print(assignment)
        for var in assignment:
            values.add(assignment[var])
        if len(values) != len(assignment):
            return False
        
        # check every value is correct length
        all_correct_length = True
        for var in assignment:
            if var.length != len(assignment[var]):
                all_correct_length = False
        if not all_correct_length:
            return False
        
        # no conflicts between neighboring variables
        for var in assignment:
            overlapping_var = self.crossword.neighbors(var)
            for _ in overlapping_var:
                res = self.crossword.overlaps[var, _]
                if res is None:
                    return False
                i, j = res
                if assignment[var][i] != assignment[_][j]:
                    return False

        return True
        

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        order = []
        var_neighbours = self.crossword.neighbors(var)

        # remove variables present in assignment
        for _ in assignment:
            if _ in var_neighbours:
                var_neighbours.remove(_)
        
        # count num of eliminations and add to order
        for val in self.domains[var]:
            count = 0
            for neighbour in var_neighbours:
                if val in self.domains[neighbour]:
                    count += 1
            order.append((val, count))
        
        # sort order by count, ascending
        sorted(order, key=lambda v: v[1])

        res = []
        for i in order:
            res.append(i[0])
        
        return res


    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        res = []

        for var in self.domains:
            if var not in assignment:
                count = len(self.domains[var])
                res.append((var, count))
        
        # sort by minimum remaining value heuristic
        #print(res)
        res = sorted(res, key=lambda v: v[1])
        #print(res)
        # check if there is tie
        min_val = res[0][1]
        # no tie
        if res[1][1] != min_val:
            return res[0][0]
        
        # tie
        tied_vars = []
        for i in res:
            if i[1] == min_val:
                tied_vars.append(i[0])

        # check for degree
        new_res = []
        for var in tied_vars:
            tied_vars_neighbours = self.crossword.neighbors(var)
            num_neighbours = len(tied_vars_neighbours)
            new_res.append((var, num_neighbours))
        # sort by degree heuristic
        new_res = sorted(new_res, key=lambda v: v[1])

        # return last (largest degree)
        return new_res[-1][0]

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        #print(assignment)
        if self.assignment_complete(assignment):
            #print(assignment)
            return assignment
        var = self.select_unassigned_variable(assignment)
        for val in self.order_domain_values(var, assignment):
            assignment[var] = val
            if self.consistent(assignment):
                result = self.backtrack(assignment)
                if result:
                    return result
            del assignment[var]
        return None
        '''
        #failure:
        # get all assigned values
        assigned = []
        for var in assignment:
            assigned.append(assignment[var])

        # iterate through var's values
        failure = True
        for val in self.domains[var]:
            if val not in assigned:
                failure = False
        if failure:
            return None
        '''


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
