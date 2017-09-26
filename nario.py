import sys
import argparse
import math
import heapq


class Graph:
    def __init__(self):
        self.states = []
 # Turn the board matrix into an array that contains coordinates without obstacles
    def makeCoordinates(self):
        nario = Nario()
        board = nario.board
        rows, cols = len(board), len(board[0])
        for x in range(rows):
          for y in range(cols):
              string = board[x][y]
              if string and string != "=": # make sure the value is not an obstacle
                  self.states.append((x, y))
        # print "The self,states is: ", self.states, "\n"," Its length is: ", len(self.states)
        return self.states

    # The edges are going to be the four directions: right, up, left, down
    # For any node we need to know the other nodes connected to this one by an edge
    def getNeighbors(self, state):
        dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        neighbors = []
        if state != (0,0):  # check the state is not goal state
            if state[1] == 0:  # if it's left edge points, they can go left off board
                dirs = [(1, 0), (0, 1), (0, 9), (0, -1)]
            if state[1] == 9: # if it's right edge points, they can go right off board
                dirs = [(0, -9), (0, 1), (-1, 0), (0, -1)]
            for dir in dirs:
                x, y = state
                next_state = (x + dir[0], y + dir[1])
                if next_state in self.states:
                    neighbors.append(next_state)

        # print "The neighbors of ", state, "is: ", neighbors
        return neighbors

class Nario:
    "A problem agent using A* Search Algorithm"
    def __init__(self):
        self.board = []
        self.came_from = {}
        self.cost_so_far = {}
        self.path_seq = []

        # pass filenames on the command line
        inFile = sys.argv[1]
        # read data from the text file and initialize board
        # self.board is a list
        with open(inFile, 'r') as f:
          data = f.readlines()
        f.closed
        # Get rid of newline character from the data list
        for i in range(len(data)):
          self.board.append(data[i].strip('\n'))

    def manhattan(self, current_state, goal_state):
        # print "You are using manhattan heuristic"
        # print "Your state state is: ", current_state

        x, y = current_state
        x1, y1 = goal_state
        if y == 9: # if ccurrent_state is in the right edge
            if x-1<0 and self.board[x][y]!= "=":
                y = 0
                distance = 1 + abs(x1 - x) + abs(y1 - y)
        distance = abs(x1 - x) + abs(y1 - y)
        # print "The manhattan distance is: ", distance, "\n"
        return distance

    def euclidean(self, current_state, goal_state):
        # print "You are using euclidean heuristic \n"
        x, y = current_state
        x1, y1 = goal_state
        if y == 9: # if ccurrent_state is in the right edge
            if x-1<0 and self.board[x][y]!= "=":
                y = 0
                distance = 1 + math.sqrt((x1 - x) ** 2 + (y1 - y) ** 2)
        distance = math.sqrt((x1 - x) ** 2 + (y1 - y) ** 2)
        # print "The euclidean distance is: ", distance, "\n"
        return distance

    def my_own(self, current_state, goal_state):
        # print "You are using my_own heuristic \n"
        x, y = current_state
        x1, y1 = goal_state
        if y == 9: # if ccurrent_state is in the right edge
            if x-1<0 and self.board[x][y]!= "=":
                y = 0
                distance = 1 + 1 * max(abs(x1 - x),abs(y1 - y))
        distance = 1 * max(abs(x1 - x),abs(y1 - y))
        # print "my_own distance is: ", distance, "\n"
        return distance

    def aStarSearch(self, graph, heuristic, start, goal):
        """ use the A* algorithm to determine a sequence of moves to take Nario from the bottom row of the board to the # """
        frontier = PriorityQueue()
        frontier.push(start, 0)
        path = []
        self.came_from[start] = None
        self.cost_so_far[start] = 0

        while not frontier.empty():
            current = frontier.pop()
            # print "your current state is: ", current
            path.append(current)
            if current == goal:
                # return self.reconstruct_path(goal)
                path = self.reconstruct_path(goal)
                break
            for next_state in graph.getNeighbors(current):
                new_cost = self.cost_so_far[current] + 1
                # Check if next_state is explored or not, or the new cost is lesser
                if next_state not in self.cost_so_far or new_cost < self.cost_so_far[next_state]:
                    self.cost_so_far[next_state] = new_cost
                    if heuristic == "manhattan":
                        priority = new_cost + self.manhattan(next_state, goal)
                    if heuristic == "euclidean":
                        priority = new_cost + self.euclidean(next_state, goal)
                    if heuristic == "my_own":
                        priority = new_cost + self.my_own(next_state, goal)
                    frontier.push(next_state, priority)
                    self.came_from[next_state] = current
        self.path_seq = path


    def reconstruct_path(self, current_state):
        """ Reconstruct the path recursively by traversing back through the came_from list """
        try:
            p = self.reconstruct_path(self.came_from[current_state])
            path = []
            path.extend(p)
            path.append(current_state)
            path_len = len(path)
            if path_len > 2:
                new_mv = path[path_len-1]
                prev_mv = path[path_len - 2]
                # print "The new move is: ", new_mv
                if prev_mv[1] == 9:
                    print "Nario wraps around by going right off board"
                if prev_mv[1] == 0:
                    print "Nario wraps around by going left off board"
                self.edit_mv(prev_mv, new_mv)
            return path
        except KeyError, e:
            return [current_state]

# Draw the game board
    def draw(self, board):
        for row in board:
            print row
        print "\n"

# Draw the game board after new moves
    def edit_mv(self, prev_mv, new_mv):
        x1, y1 = prev_mv
        x2, y2 = new_mv
        board = self.board
        # new_mv utilities:
        row2 = board[x2]
        s2 = list(row2)
        s2[y2] = '@'
        board[x2]= "".join(s2)

        # prev_mv utilities:
        row1 = board[x1]
        s1 = list(row1)
        s1[y1] = '.'
        board[x1] = "".join(s1)
        self.draw(board)

# Draw the whole moving process
    def draw_process(self):
        board = self.board
        for state in self.path_seq[2:]:
            x, y = state
            row = board[x]
            s = list(row)
            s[y] = '@'
            board[x]= "".join(s)
        self.draw(board)


# PriorityQueue utilities
class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def push(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def pop(self):
        return heapq.heappop(self.elements)[1]


# Tester:
nario = Nario()
board = nario.board
# print "You are using ", sys.argv[2], "heuristic:"
# print "--------------------- The original game board --------------------- \n"
nario.draw(board)
graph = Graph()
graph.makeCoordinates()
# print "--------------------- Conducting A* search ---------------------"
nario.aStarSearch(graph, sys.argv[2], (8, 5), (0, 0))
print "--------------------- The total process ---------------------"
nario.draw_process()
# print "--------------------- The total path ---------------------"
# print nario.path_seq
