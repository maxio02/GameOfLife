import pygame
from board import Board
import sys
ROWS = 144*5//4
COLS = 256*5//4
WINDOW_HEIGHT = 1440
WINDOW_WIDTH = 2560


pygame.init()
screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h
CELL_WIDTH = screen_width // COLS
CELL_HEIGHT = screen_height // ROWS

window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Game Of Life")
clock = pygame.time.Clock()
clock.tick(60)

board = Board((ROWS, COLS), 'random', CELL_WIDTH, CELL_HEIGHT)
fps_font = pygame.font.SysFont(None, 24)
def update_board():
    global board
    global current_fps
    global previous_time

    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

    window.fill((0, 0, 0))
    board.draw_cells(window, 'white')
    clock.tick(144)
    fps_label = fps_font.render(f"FPS: {clock.get_fps():.1f}", True, (255, 255, 255))
    window.blit(fps_label, (10, 10))

    board.update_cells()
    pygame.display.flip()
    

while True:
    update_board()
