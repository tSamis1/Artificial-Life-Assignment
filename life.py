class Life:

    def __init__(self, inputFile):
        self.possibilities = [(-1,-1), (-1,0), (0,-1), (-1,1), (1,-1), (1,0), (0,1), (1,1)]
        self.num_gens = 0
        self.rows = 0
        self.cols = 0
        self.grid = []
        self.live = {}
        self.remove = []
        self.dead_neighbours = {}
        self.readFile(inputFile)

    def readFile(self, inputFile):
        f = open(inputFile, 'r')
        self.num_gens = int(f.readline().strip())
        for line in f:
            cells = [int(cell) for cell in line.strip()]
            self.grid.append(cells)
        self.rows = len(self.grid)
        self.cols = len(self.grid[0])
        self.findLive()

    def findLive(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.grid[i][j] == 1:
                    self.live[(i,j)] = 0
        self.play()

    def play(self):
        output = open("outLife.txt", 'w')
        output.write("Generation 0\n")
        for line in self.grid:
            output.write(str(line).replace("[", "").replace("]", "") + "\n")
        for i in range(self.num_gens):
            self.findNeighbours()
            output.write("Generation " + str(i + 1) +"\n")
            for line in self.grid:
                output.write(str(line).replace("[", "").replace("]", "") + "\n")

    def findNeighbours(self):
        for cell in self.live.keys():
            #print(cell)
            neighbours = []
            for move in self.possibilities:
                x, y = cell
                x2, y2 = move
                new_x = x + x2
                new_y = y + y2
                if (new_x < 0) or (new_y < 0) or (new_x > (self.rows-1)) or (new_y > (self.cols-1)):
                    continue
                else:
                    neighbours.append((new_x, new_y))
            self.updateNeighbours(cell, neighbours)
        self.updateGrid()

    def updateNeighbours(self, cell, neighbours):
        live_neighbours = 0
        for neighbour in neighbours:
            x, y = neighbour
            if self.grid[x][y] == 1:
                live_neighbours += 1
            else:
                if (x, y) in self.dead_neighbours:
                    self.dead_neighbours[(x, y)] += 1
                else:
                    self.dead_neighbours[(x, y)] = 1
        self.live[cell] = live_neighbours

    def updateGrid(self):
        new_live = {}
        for key in self.live.keys():
            if (self.live[key] < 2) or (self.live[key] > 3):
                x ,y = key
                self.grid[x][y] = 0
            else:
                new_live[key] = 0
        self.live = new_live

        new_dead_neighbours = {}
        for key in self.dead_neighbours.keys():
            if self.dead_neighbours[key] == 3:
                x, y = key
                self.grid[x][y] = 1
                self.live[key] = 0
            else:
                new_dead_neighbours[key] = 0
        self.dead_neighbours = new_dead_neighbours

def main():
    test = Life("inLife.txt")

main()
