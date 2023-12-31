import numpy as np
from cell import Cell
import random


class Board:
    def __init__(self, size: tuple[int, int], init_type: str, cell_width: int, cell_height: int):
        self.size = size
        self.cell_width = cell_width
        self.cell_height = cell_height
        self.alive_cells = []

        if init_type == 'random':
            self.cells: np.ndarray[Cell] = np.array(
                self.random_init()).flatten()
        elif init_type == 'empty':
            self.cells: np.ndarray[Cell] = np.array(
                self.zeros_init()).flatten()
            self.init_glider()
        elif init_type == 'center':
            self.cells: np.ndarray[Cell] = np.array(
                self.zeros_init()).flatten()
            self.random_fill_area(size[1]//2, size[0]//2, 10, 10)

        for cell in self.cells:
            cell.assign_neighbours(self)
            if cell.isAlive:
                self.alive_cells.append(cell)


    def __str__(self) -> str:
        representation = ""
        for cell in self.cells:
            representation += str(cell.aliveNeighbours) + " "
            if cell.xpos % 10 == 9:
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


    def random_fill_area(self, start_x: int, start_y: int, width: int, height: int):
        for y in range(start_y, start_y + height):
            for x in range(start_x, start_x + width):
                cell = self.cells[x + y * self.size[1]]
                cell.isAlive = bool(random.getrandbits(1))


    def zeros_init(self):
        return [[Cell(False, i, j, self.cell_width, self.cell_height) for i in range(self.size[1])] for j in range(self.size[0])]

    def init_glider(self):
        glider = [
            [0, 0, 1],
            [1, 0, 1],
            [0, 1, 1]
        ]

        glider_row = random.randint(0, self.size[0] - len(glider))
        glider_col = random.randint(0, self.size[1] - len(glider[0]))

        for i in range(len(glider)):
            for j in range(len(glider[0])):
                cell = self.cells[glider_col + i + (glider_row + j) * self.size[1]]
                cell.isAlive = glider[i][j]


    def draw_cells(self, canvas, color: str):
        if color == 'white':
            for cell in self.alive_cells:
                cell.draw(canvas, (255, 255, 255))
        else:
            for cell in self.alive_cells:
                cell.draw(canvas, (255-int(cell.xpos/self.size[1]*255), int(cell.xpos/self.size[1]*255), int(cell.ypos/self.size[0]*255)))


    def update_neighbour_sums(self):
        for cell in self.cells:
            cell.aliveNeighbours = 0

        for cell in self.alive_cells:
            cell.update_alive_neighbours()

    def update_cells(self):
        self.update_neighbour_sums()

        new_alive_cells = []

        for cell in self.cells:
            alive_neighbours = cell.aliveNeighbours
            if cell.isAlive and (alive_neighbours == 2 or alive_neighbours == 3):
                new_alive_cells.append(cell)
            elif not cell.isAlive and alive_neighbours == 3:
                cell.resurrect()
                new_alive_cells.append(cell)
            elif cell.isAlive:
                cell.kill()

        self.alive_cells = new_alive_cells

    def update_cells_maze(self):
        self.update_neighbour_sums()

        new_alive_cells = []
        for cell in self.alive_cells:
            alive_neighbours = cell.aliveNeighbours
            if alive_neighbours >= 1 and alive_neighbours <= 5:
                new_alive_cells.append(cell)
            else:
                cell.kill()

        for cell in self.cells:
            if not cell.isAlive:
                if cell.aliveNeighbours == 3:
                    cell.resurrect()
                    new_alive_cells.append(cell)

        self.alive_cells = new_alive_cells
