import numpy as np
from cell import Cell
import random


import numpy as np
from cell import Cell
import random


class Board:

    def __init__(self, size: tuple[int, int], init_type: str, cell_width: int, cell_height: int):
        self.size = size
        self.cell_width = cell_width
        self.cell_height = cell_height

        if init_type == 'random':
            self.cells: np.ndarray[Cell] = np.array(
                self.random_init()).flatten()
        elif init_type == 'empty':
            self.cells: np.ndarray[Cell] = np.array(
                self.zeros_init()).flatten()
            self.init_glider()

        for cell in self.cells:
            cell.assign_neighbours(self)

    def __str__(self) -> str:
        representation = ""
        for cell in self.cells:
            representation += str(cell.aliveNeighbours) + " "
            if cell.xpos%10 == 9:
                representation += "\n"
        return representation
    
    def __repr__(self) -> str:
        representation = ""
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                cell = self.cells[x + y * self.size[0]]
                representation += f"C({x} {y}) {cell.aliveNeighbours}\n"
        return representation
        

    def random_init(self):
        return [[Cell(random.getrandbits(1), i, j, self.cell_width, self.cell_height) for i in range(self.size[1])] for j in range(self.size[0])]

    def zeros_init(self):
        return [[Cell(False, i, j, self.cell_width, self.cell_height) for i in range(self.size[1])] for j in range(self.size[0])]

    def init_glider(self):
        glider = [
            [0, 0, 1],
            [1, 0, 1],
            [0, 1, 1]
        ]

        glider_row = random.randint(0, self.size[1] - len(glider))
        glider_col = random.randint(0, self.size[0] - len(glider[0]))

        for i in range(len(glider)):
            for j in range(len(glider[0])):
                self.cells[glider_row + i + (glider_col + j) * i].isAlive = glider[i][j]

    def draw_cells(self, canvas, color: str):
        if color == 'white':
            for cell in self.cells:
                cell.draw(canvas, (255,255,255))
        else:
            for cell in self.cells:
                cell.draw(canvas, (255-int(cell.xpos/self.size[1]*255),int(cell.xpos/self.size[1]*255),int(cell.ypos/self.size[0]*255)))

    def update_neighbour_sums(self):
        for cell in self.cells:
            cell.update_alive_neighbours()

    def update_cells(self):
        self.update_neighbour_sums()

        for cell in self.cells:
            alive_neighbours = cell.aliveNeighbours
            if cell.isAlive and (alive_neighbours == 2 or alive_neighbours == 3):
                pass
            elif not cell.isAlive and alive_neighbours == 3:
                cell.resurrect()
            else:
                cell.kill()