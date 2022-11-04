import pathlib
import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: int = 10**9,
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        # Copy from previous assignment
        matrix: Grid
        matrix = [[0] * self.cols for i in range(self.rows)]
        if randomize:
            for i in range(self.rows):
                for j in range(self.cols):
                    matrix[i][j] = random.randint(0, 1)
        return matrix

    def get_neighbours(self, cell: Cell) -> Cells:
        # Copy from previous assignment
        out: Grid = []
        for i in range(0, self.rows):
            out.append([])
            for j in range(0, self.cols):
                out[i].append(0)
        for i in range(len(self.curr_generation)):
            for j in range(len(self.curr_generation[0])):
                cell: Cell = (i, j)
                sum = self.get_neighbours(cell).count(1)
                if self.curr_generation[i][j] and sum == 2 or sum == 3:
                    out[i][j] = 1
        return out

    def get_next_generation(self) -> Grid:
        # Copy from previous assignment
        matrix: Grid
        matrix = self.create_grid()
        self.prev_generation = self.curr_generation
        for i in range(self.rows):
            for j in range(self.cols):
                neighbours = self.get_neighbours((i, j))
                if self.curr_generation[i][j] == 1 and 2 <= neighbours.count(1) <= 3:
                    matrix[i][j] = 1
                elif self.curr_generation[i][j] == 0 and neighbours.count(1) == 3:
                    matrix[i][j] = 1

        self.curr_generation = matrix
        return matrix

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        if not self.is_max_generations_exceeded and self.is_changing:
            self.prev_generation = self.curr_generation
            self.curr_generation = self.get_next_generation()
            self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        if self.max_generations is None:
            self.max_generations = 1
        if self.generations >= self.max_generations:
            return True
        else:
            return Falsee

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        if self.prev_generation != self.curr_generation:
            return True
        else:
            return False

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        with open(filename) as f:
            grid = f.readlines()
            height = len(grid)
            width = len(grid[0].strip())

            grid1 = []
            for i in range(len(grid)):
                grid1.append(list(map(int, [*(grid[i].strip())])))

        life = GameOfLife((height, width))
        life.curr_generation = grid1
        return life

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        f = open(filename, "w")
        for i in range(self.rows):
            row = ""
            for j in range(self.cols):
                row += str(self.curr_generation[i][j])
            f.write(row + "\n")
