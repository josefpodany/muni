#!/usr/local/bin/python
__author__ = "Josef Podany, V4D PROG"
__email__ = "josef.podany.ml@gmail.com"
import time
# 1. check all valid moves
# 2. create all possible children (check all ancestors)
# 3. append children to list
# 4. save range of children where are in the list
# 5. check if children in range are solution
# 6. again

class Puzzle:
    def __init__(self, values, ancestors = [], moves = []):
        # takes in array of values
        self.values = values
        self.ancestors = ancestors      # array of indeces of all ancestors
        self.moves = moves
        self.possible_moves = {
            "shifts": [1, -1, 3, -3],
            "words": ["Right", "Left", "Down", "Up"]
        }

    def __str__(self):
        string =  "layer       : " + str(len(self.ancestors)) + "\n"
        string += "ancestors   : " + str(self.ancestors) + "\n"
        string += "moves       : "
        for move in self.moves:
            string += self.possible_moves["words"][self.possible_moves["shifts"].index(move)] + " "
        string += "\n"
        for value in self.values:
            string = string + str(value) + "\n" if self.values.index(value) % 3 == 2 else string + str(value) + " "
        return string
    
    def get_values(self):
        return self.values

    def get_moves(self):
        return self.moves

    def get_indeces_of_ancestors(self):
        return self.ancestors

    def get_valid_states(self):
        position_of_zero = self.values.index(0)
        shifts = [1, -1, 3, -3]                     # right, left, down, up
        valid_states = []
        for shift in shifts:
            new_index = shift + position_of_zero
            if 0 <= new_index < len(self.values):
                if not ((position_of_zero in [3, 6] and shift == -1) or (position_of_zero in [2, 5] and shift == 1)):
                    temp_values = self.values[:]        # deep copy to create copy and not link
                    temp_values[new_index], temp_values[position_of_zero] = temp_values[position_of_zero], temp_values[new_index]
                    valid_states.append({
                                        "array": temp_values,
                                        "direction": shift})
        return valid_states


class Solver:
    def __init__(self, root, goal, max_layers = 25, time_elapsed = 0):
        self.tree = [root]
        self.goal = goal
        self.max_layers = max_layers

    def get_ancestors(self, node_indeces_of_ancesters):
        return [self.tree[index] for index in node_indeces_of_ancesters]

    def create_children_of_node(self, node, parent_node_index):
        states = node.get_valid_states()
        indeces_of_ancestors = node.get_indeces_of_ancestors()
        if indeces_of_ancestors is not None:
            ancestors = self.get_ancestors(indeces_of_ancestors)
            ancestors_values = [ancestor.get_values() for ancestor in ancestors]
            for state in states:
                if state["array"] not in ancestors_values:
                    new_child = Puzzle(state["array"], indeces_of_ancestors + [parent_node_index], node.get_moves() + [state["direction"]])
                    self.tree.append(new_child)
    
    def show_solution(self, node):
        for index in node.ancestors:
            print(self.tree[index])
            print("\n")
        print(node)
        print("tree length : " + str(len(self.tree)))

    def solve(self):
        left = 0        # index to keep the children in the tree seperate
        start = time.time()
        while True:
            temp = len(self.tree)
            for index in range(left, len(self.tree)):    # checks the solution and adds a new layer of nodes
                node = self.tree[index]
                if node.get_indeces_of_ancestors() is not None:
                    if len(node.get_indeces_of_ancestors()) > self.max_layers:
                        print("Stopping at layer {}".format(self.max_layers))
                        print("self.tree: " + str(len(self.tree)))
                        self.time_elapsed = time.time() - start
                        return False
                if node.get_values() == self.goal.get_values():
                    # FOUND IT!
                    self.time_elapsed = time.time() - start
                    return node
                else:
                    self.create_children_of_node(node, index)
            left = temp

if __name__ == '__main__':
    root1 = Puzzle([0, 1, 3, 4, 2, 5, 7, 8, 6])
    root2 = Puzzle([1, 2, 3, 0, 5, 6, 4, 7, 8])
    root3 = Puzzle([0, 8, 3, 4, 6, 5, 7, 1, 2])
    goal = Puzzle([1, 2, 3, 4, 5, 6, 7, 8, 0])
    solver = Solver(root3, goal)
    if solver.solve():
        solver.show_solution(solver.solve())
        



