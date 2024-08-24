import pygame
from settings import *


class UI:
    def __init__(self, screen, timer):
        self.screen = screen
        self.timer = timer
        self.number_font = pygame.font.Font(NUMBER_FONT_PATH, NUMBER_FONT_SIZE)
        self.text_font = pygame.font.Font(TEXT_FONT_PATH, TEXT_FONT_SIZE)
        self.timer_font = pygame.font.Font(TEXT_FONT_PATH, TIMER_FONT_SIZE)

    def _draw_cell(self, x, y, color, border_color, border_width, number, editable):
        pygame.draw.rect(self.screen, color, (x, y, CELL_SIZE - MARGIN, CELL_SIZE - MARGIN),
                         border_radius=BORDER_RADIUS)
        pygame.draw.rect(self.screen, border_color, (x, y, CELL_SIZE - MARGIN, CELL_SIZE - MARGIN), border_width,
                         border_radius=BORDER_RADIUS)

        if number != 0:
            text = self.number_font.render(str(number), True, NUMBER_COLOR if editable else PREDEFINED_NUMBER_COLOR)
            text_rect = text.get_rect(center=(x + (CELL_SIZE - MARGIN) // 2, y + (CELL_SIZE - MARGIN - 10) // 2))
            self.screen.blit(text, text_rect)

    def draw_screen(self, board, clicked_cell=None, valid_cell=None, invalid_cell=None, text=None):
        self.screen.fill(BG_COLOR)
        for row in range(ROWS):
            for col in range(COLS):
                x = col * CELL_SIZE + MARGIN // 2
                y = row * CELL_SIZE + MARGIN // 2

                color = LIGHTER_CELL_COLOR if (row // 3 + col // 3) % 2 == 0 else DARKER_CELL_COLOR

                border_color, border_width = BORDER_COLOR, BORDER_WIDTH
                if invalid_cell == [row, col]:
                    border_color, border_width = INVALID_BORDER_COLOR, CLICKED_BORDER_WIDTH
                elif valid_cell == [row, col]:
                    border_color, border_width = VALID_BORDER_COLOR, CLICKED_BORDER_WIDTH
                elif clicked_cell == [row, col]:
                    border_color, border_width = CLICKED_BORDER_COLOR, CLICKED_BORDER_WIDTH

                self._draw_cell(x, y, color, border_color, border_width, board.grid[row][col], board.editable[row][col])
        self._draw_time(self.timer.formatted_time)
        if text:
            self._draw_text(text, 150, HEIGHT + CELL_SIZE / 4, TEXT_COLOR, self.text_font)
        pygame.display.update()

    def _draw_time(self, elapsed_time):
        self._draw_text(elapsed_time, 10, HEIGHT + CELL_SIZE / 4, TIMER_COLOR, self.timer_font)

    def _draw_text(self, text, x, y, color, font):
        text_surface = font.render(str(text), True, color)
        text_rect = text_surface.get_rect(topleft=(x, y))
        self.screen.blit(text_surface, text_rect)

    def get_cell_pos(self, mouse_pos):
        x, y = mouse_pos
        row = y // CELL_SIZE
        col = x // CELL_SIZE
        return [row, col] if (row < 9 and col < 9) else None

    def wait_for_key(self):
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    waiting = False

    def handle_key_press(self, board, event, clicked_cell):
        valid_cell = invalid_cell = None
        if event.key == pygame.K_SPACE:
            self.timer.start_solving()
            can_be_solved = board.solve_with_visualization(self.draw_screen, self.timer)
            if not can_be_solved and not board.is_cleared:  # Clear the user numbers and try again!
                board.clear(only_editable=True)
                can_be_solved = board.solve_with_visualization(self.draw_screen, self.timer)
            if not can_be_solved:
                self.draw_screen(board, text='This sudoku is unsolvable! Press any key to continue')
                self.timer.stop()
                self.wait_for_key()
        if event.key == pygame.K_b:
            board.clear()
        if clicked_cell:
            row, col = clicked_cell
            if board.editable[row][col]:
                if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6,
                                 pygame.K_7, pygame.K_8, pygame.K_9]:
                    num = int(event.unicode)
                    if board.is_valid(row, col, num):
                        board.grid[row][col] = num
                        valid_cell = [row, col]
                    else:
                        invalid_cell = [row, col]

                elif event.key in [pygame.K_BACKSPACE, pygame.K_DELETE]:
                    board.grid[row][col] = 0
            if event.key == pygame.K_RIGHT and clicked_cell[1] < 8:
                clicked_cell[1] += 1
            elif event.key == pygame.K_LEFT and clicked_cell[1] > 0:
                clicked_cell[1] -= 1
            elif event.key == pygame.K_DOWN and clicked_cell[0] < 8:
                clicked_cell[0] += 1
            elif event.key == pygame.K_UP and clicked_cell[0] > 0:
                clicked_cell[0] -= 1
        return valid_cell, invalid_cell
