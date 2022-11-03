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
        max_generations: tp.Optional[float] = float("inf"),
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
        matrix: Grid
        matrix = [[0] * self.cols for i in range(self.rows)]
        if randomize:
            for i in range(self.rows):
                for j in range(self.cols):
                    matrix[i][j] = random.randint(0, 1)
        return matrix

    def get_neighbours(self, cell: Cell) -> Cells:
        (x, y) = cell
        neighbours: Cells
        neighbours = []
        steps = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        for (step_x, step_y) in steps:
            cur_x = x + step_x
            cur_y = y + step_y
            if 0 <= cur_x < self.rows and 0 <= cur_y < self.cols:
                neighbours += [self.curr_generation[cur_x][cur_y]]
        return neighbours

    def get_next_generation(self) -> Grid:
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

    def step(self) -> None:
        if not self.is_max_generations_exceeded:
            self.get_next_generation()
            self.generations += 1


    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        if self.prev_generation == self.curr_generation:
            return False
        else:
            return True


    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        file = open(filename)
        whole = file.readlines()
        grid = []
        for i in range(len(whole)):
            if whole[i] != "\n":
                whole[i] = whole[i][:-1]
                row = [int(n) for n in list(whole[i])]
                grid.append(row)
        game = GameOfLife((len(grid), len(grid[0])))
        game.curr_generation = grid
        file.close()
        return game


    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        file = open(filename, "w")
        for i in range(len(self.curr_generation)):
            for j in range(len(self.curr_generation[0])):
                file.write(str(self.curr_generation[i][j]))
            file.write("\n")
        file.close()
