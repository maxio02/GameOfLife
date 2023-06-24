import pygame

class Cell:
    def __init__(self, isAlive: bool, xpos: int, ypos: int, width: int, height: int):
        self.isAlive = isAlive
        self.aliveNeighbours = 0
        self.neighbours = []
        self.prev_state = isAlive
        self.xpos = xpos
        self.ypos = ypos
        self.width = width
        self.height = height

    def __str__(self) -> str:
        return str(self.isAlive)

    def __repr__(self) -> str:
        return str(self.aliveNeighbours) + " "

    def kill(self):
        self.isAlive = False

    def resurrect(self):
        self.prev_state = self.isAlive
        self.isAlive = True

    def assign_neighbours(self, board):
        neighbours = []
        board_size = board.size
        for y_offset in [-1, 0, 1]:
            for x_offset in [-1, 0, 1]:
                if y_offset == 0 and x_offset == 0:
                    continue
                neighbour_y = (self.ypos + y_offset) % board_size[0]
                neighbour_x = (self.xpos + x_offset) % board_size[1]
                neighbours.append(board.cells[neighbour_x + (neighbour_y * board_size[1])])

        self.neighbours = neighbours

    def update_alive_neighbours(self):
        for neighbour in self.neighbours:
                neighbour.aliveNeighbours += 1

    def draw(self, surface, color: tuple[int, int, int]):
            x1 = self.xpos * self.width
            y1 = self.ypos * self.height
            pygame.draw.rect(surface, color, (x1, y1, self.width-1, self.height-1))
