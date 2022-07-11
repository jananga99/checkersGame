import pygame
import math
import random

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
TRANS = (1, 2, 3)

# CONSTANTS:
WIDTH = 700
HEIGHT = 700
MARK_SIZE = 50


class Game:

    def __init__(self):
        self.status = "ongoing"
        self.turn = 0
        self.players = ["O", "X"]
        self.selected_piece = False
        pygame.display.set_caption("%s's turn" % self.players[self.turn % 2])
        self.game_board = [['X', '-', 'X', '-', 'X', '-', 'X', '-'],
                           ['-', 'X', '-', 'X', '-', 'X', '-', 'X'],
                           ['X', '-', 'X', '-', 'X', '-', 'X', '-'],
                           ['-', '-', '-', '-', '-', '-', '-', '-'],
                           ['-', '-', '-', '-', '-', '-', '-', '-'],
                           ['-', 'O', '-', 'O', '-', 'O', '-', 'O'],
                           ['O', '-', 'O', '-', 'O', '-', 'O', '-'],
                           ['-', 'O', '-', 'O', '-', 'O', '-', 'O']]

    # rows are numbered from top to bottom and left to right.
    # 0,0 is leftmost topmost cell.
    # Numbering starts from 0.
    def evaluate_click(self, mouse_pos):
        if self.status == "ongoing":
            clicked_row = int(mouse_pos[1] // (HEIGHT / 8))
            clicked_column = int(mouse_pos[0] // (WIDTH / 8))
            if self.selected_piece:
                if self.selected_piece[0] == clicked_row and self.selected_piece[1] == clicked_column:
                    self.selected_piece = False
                else:
                    valid, jump_cell = self.is_possible_move([clicked_row, clicked_column])
                    if valid:
                        self.play(clicked_row, clicked_column, jump_cell)
            else:
                if self.game_board[clicked_row][clicked_column] == self.players[self.turn % 2]:
                    self.selected_piece = [clicked_row, clicked_column]

    # Returns is_possible_move, is_jump
    def is_possible_move(self, to_cell):
        if self.game_board[to_cell[0]][to_cell[1]] != "-":
            return False, False
        jump_cell = self.is_jump(to_cell)
        if jump_cell:
            return True, jump_cell
        elif abs(to_cell[1] - self.selected_piece[1]) == 1 and (
                self.turn == 0 and to_cell[0] - self.selected_piece[0] == -1 or self.turn == 1 and to_cell[0] -
                self.selected_piece[0] == 1):
            return True, False
        else:
            return False, False

    def is_jump(self, to_cell):
        jump_cell = [(self.selected_piece[0] + to_cell[0]) // 2, (self.selected_piece[1] + to_cell[1]) // 2]
        if abs(to_cell[1] - self.selected_piece[1]) == 2 and abs(to_cell[0] - self.selected_piece[0]) == 2 and \
                self.game_board[jump_cell[0]][jump_cell[1]] == self.players[(self.turn + 1) % 2]:
            return jump_cell
        return False

    def next_turn(self):
        self.turn = (self.turn + 1) % 2
        pygame.display.set_caption("%s's turn" % self.players[self.turn % 2])

    def play(self, clicked_row, clicked_column, jump_cell):
        self.game_board[self.selected_piece[0]][self.selected_piece[1]] = "-"
        self.selected_piece = False
        self.game_board[clicked_row][clicked_column] = self.players[self.turn]
        if jump_cell:
            self.game_board[jump_cell[0]][jump_cell[1]] = "-"
        self.next_turn()
        self.check_finish()

    def check_finish(self):
        piece_count = [0, 0]
        moves_exists = False
        for r in range(8):
            for c in range(8):
                if self.game_board[r][c] == self.players[0]:
                    piece_count[0] += 1
                elif self.game_board[r][c] == self.players[1]:
                    piece_count[1] += 1
                if not moves_exists and self.game_board[r][c] == self.players[self.turn]:
                    if self.turn == 1:
                        if r < 7:
                            if c < 7:
                                if self.game_board[r + 1][c + 1] == "-":
                                    moves_exists = True
                            if c > 0:
                                if self.game_board[r + 1][c - 1] == "-":
                                    moves_exists = True
                    elif self.turn == 0:
                        if r > 0:
                            if c < 7:
                                if self.game_board[r - 1][c + 1] == "-":
                                    moves_exists = True
                            if c > 0:
                                if self.game_board[r - 1][c - 1] == "-":
                                    moves_exists = True

                    if r < 6:
                        if 1 < c < 6:
                            if self.game_board[r + 2][c + 2] == "-" and self.game_board[r + 1][c + 1] == \
                                    self.players[(self.turn + 1) % 2] or self.game_board[r + 2][c - 2] == "-" and \
                                    self.game_board[r + 1][c - 1] == \
                                    self.players[(self.turn + 1) % 2]:
                                moves_exists = True
                        elif c <= 1:
                            if self.game_board[r + 2][c + 2] == "-" and self.game_board[r + 1][c + 1] == \
                                    self.players[(self.turn + 1) % 2]:
                                moves_exists = True
                        elif c >= 6:
                            if self.game_board[r + 2][c - 2] == "-" and self.game_board[r + 1][c - 1] == \
                                    self.players[(self.turn + 1) % 2]:
                                moves_exists = True
                    if r > 1:
                        if 1 < c < 6:
                            if self.game_board[r - 2][c + 2] == "-" and self.game_board[r - 1][c + 1] == \
                                    self.players[(self.turn + 1) % 2] or self.game_board[r - 2][c - 2] == "-" and \
                                    self.game_board[r - 1][c - 1] == \
                                    self.players[(self.turn + 1) % 2]:
                                moves_exists = True
                        elif c <= 1:
                            if self.game_board[r - 2][c + 2] == "-" and self.game_board[r - 1][c + 1] == \
                                    self.players[(self.turn + 1) % 2]:
                                moves_exists = True
                        elif c >= 6:
                            if self.game_board[r - 2][c - 2] == "-" and self.game_board[r - 1][c - 1] == \
                                    self.players[(self.turn + 1) % 2]:
                                moves_exists = True
        if piece_count[0] == 0:
            pygame.display.set_caption("%s wins!!!!" % self.players[1])
            self.finish()
        elif piece_count[1] == 0:
            pygame.display.set_caption("%s wins!!!!" % self.players[0])
            self.finish()
        elif not moves_exists:
            pygame.display.set_caption("Draw!!!!")
            self.finish()

    def finish(self):
        self.status = "finished"
        print("Game is finished")

    def draw(self):
        """
        Draw the game board and the X's and O's.
        """
        for i in range(9):
            pygame.draw.line(screen, WHITE, [i * WIDTH / 8, 0], [i * WIDTH / 8, HEIGHT], 5)
            pygame.draw.line(screen, WHITE, [0, i * HEIGHT / 8], [WIDTH, i * HEIGHT / 8], 5)
        font = pygame.font.SysFont('Calibri', MARK_SIZE, False, False)
        for r in range(len(self.game_board)):
            for c in range(len(self.game_board[r])):
                mark = self.game_board[r][c]
                if self.players[self.turn % 2] == mark.lower():
                    color = YELLOW
                else:
                    color = WHITE
                if self.selected_piece:
                    if self.selected_piece[0] == r and self.selected_piece[1] == c:
                        color = RED
                if mark != '-':
                    mark_text = font.render(self.game_board[r][c], True, color)
                    x = WIDTH / 8 * c + WIDTH / 16
                    y = HEIGHT / 8 * r + HEIGHT / 16
                    screen.blit(mark_text, [x - mark_text.get_width() / 2, y - mark_text.get_height() / 2])


pygame.init()
size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(size)

game = Game()

done = False
# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# game loop:
while not done:
    # --- Main event loop
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop
        if event.type == pygame.KEYDOWN:
            entry = str(event.key)
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            game.evaluate_click(pygame.mouse.get_pos())

    screen.fill(BLACK)
    game.draw()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
