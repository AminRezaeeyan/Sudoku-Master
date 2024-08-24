import sys
import time

import pygame
from settings import WIDTH, HEIGHT, CELL_SIZE
from board import Board
from UI import UI
from timer import Timer

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT + CELL_SIZE))
pygame.display.set_caption("Sudoku Master")
pygame.font.init()


class Main:
    def __init__(self, screen):
        self.screen = screen
        self.timer = Timer()
        self.user_interface = UI(screen, self.timer)

    def main(self):
        board = Board.generate()

        self.timer.reset()
        self.timer.start()

        clicked_cell = board.find_empty()
        valid_cell = invalid_cell = None

        while self.timer.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.timer.stop()
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    clicked_cell = self.user_interface.get_cell_pos(pygame.mouse.get_pos())
                elif event.type == pygame.KEYDOWN:
                    valid_cell, invalid_cell = self.user_interface.handle_key_press(board, event, clicked_cell)

            self.user_interface.draw_screen(board, clicked_cell, valid_cell, invalid_cell)
            if valid_cell or invalid_cell:
                valid_cell = invalid_cell = None
                time.sleep(0.5)
                self.user_interface.draw_screen(board, clicked_cell)
            if not board.find_empty():
                self.timer.stop()
                self.user_interface.draw_screen(board, text='Game Over! Press any key to continue')
                self.user_interface.wait_for_key()


if __name__ == "__main__":
    game = Main(screen)

    while True:
        game.main()
