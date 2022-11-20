from math import trunc

import pygame
from life import GameOfLife
from pygame.locals import *
from ui import UI


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 12, speed: int = 5) -> None:
        self.cell_size = cell_size
        self.speed = speed
        # Устанавливаем размер окна
        # Создание нового окна
        super().__init__(life)

        self.height = self.life.rows * self.cell_size
        self.width = self.life.cols * self.cell_size
        self.screen_size = self.width, self.height
        self.screen = pygame.display.set_mode(self.screen_size)

    def write_debug(self, message):
        with open("c:\\temp\\life-debug.log", "a") as f:
            print(message, file=f)

    def draw_lines(self) -> None:
        # Copy from previous assignment
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("blue"), (0, y), (self.width, y))
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("blue"), (x, 0), (x, self.height))

    def draw_grid(self) -> None:
        # Copy from previous assignment
        for i in range(self.life.rows):
            for j in range(self.life.cols):
                if self.life.curr_generation[i][j]:
                    pygame.draw.rect(
                        self.screen,
                        pygame.Color("purple"),
                        (
                            j * self.cell_size + 1,
                            i * self.cell_size + 1,
                            self.cell_size - 1,
                            self.cell_size - 1,
                        ),
                    )
                else:
                    pygame.draw.rect(
                        self.screen,
                        pygame.Color("white"),
                        (
                            j * self.cell_size + 1,
                            i * self.cell_size + 1,
                            self.cell_size - 1,
                            self.cell_size - 1,
                        ),
                    )

    def run(self) -> None:
        # Copy from previous assignment
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        running = True
        pause = False

        self.draw_lines()

        while running:
            if not pause:
                self.draw_grid()
                pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if not pause:
                            pause = True
                        else:
                            pause = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    (y, x) = pygame.mouse.get_pos()
                    if pause:
                        cur_x = int(trunc(x / self.cell_size))
                        cur_y = int(trunc(y / self.cell_size))
                        if event.button == 1:
                            self.life.curr_generation[cur_x][cur_y] ^= 1
                        self.draw_grid()
                        pygame.display.flip()

            if self.life.is_max_generations_exceeded:
                running = False

            if not pause:
                self.life.step()

            clock.tick(self.speed)
        pygame.quit()


GUI(GameOfLife((20, 20))).run()

