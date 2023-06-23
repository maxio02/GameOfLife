import pygame
from board import Board
ROWS = 200
COLS = 200
WINDOW_HEIGHT = 800
WINDOW_WIDTH = 800
CELL_WIDTH = WINDOW_WIDTH // COLS
CELL_HEIGHT = WINDOW_HEIGHT // ROWS

pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Game Of Life")
clock = pygame.time.Clock()
clock.tick(20)

board = Board((ROWS, COLS), 'random', CELL_WIDTH, CELL_HEIGHT)
fps_font = pygame.font.SysFont(None, 24)
def update_board():
    global board
    global current_fps
    global previous_time

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            return

    window.fill((0, 0, 0))
    board.draw_cells(window, 'white')
    clock.tick(20)
    fps_label = fps_font.render(f"FPS: {clock.get_fps():.1f}", True, (255, 255, 255))
    window.blit(fps_label, (10, 10))

    board.update_cells()
    pygame.display.flip()
    

while True:
    update_board()
