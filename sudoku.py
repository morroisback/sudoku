from itertools import product

from utils import DancingLinksList


class Sudoku:
    def __init__(self, quad_dim: int = 3, field: list[list[int]] = None) -> None:
        if not isinstance(quad_dim, int):
            raise TypeError("Square dimension must be int.")

        self.__dim = quad_dim**2
        self.__quad_dim = quad_dim
        self.__field = None
        self.__xfield = None

        self.set_field(field)

    def __repr__(self) -> str:
        return f"Sudoku(sq_dim={self.__quad_dim})"

    def __str__(self) -> str:
        str_field = [[f"{value:>3}" for value in row] for row in self.__field]
        return "\n".join(["".join(row) for row in str_field]) + "\n"

    # def __getitem__(self, coords: tuple) -> int:
    #     if isinstance(coords, tuple) and len(coords) == 2:
    #         row, col = coords

    #         return self.get_node(row_idx, col_idx)
    #     else:
    #         raise TypeError("Invalid type for indexes")

    def clear_xfield(self) -> None:
        self.__xfield = DancingLinksList(len(str((self.__dim, self.__dim, self.__dim))) + 1)
        for row, col, value in product(range(1, self.__dim + 1), repeat=3):
            self.__xfield.set_row((row, col, value))

        for k, i, j in product(range(4), range(1, self.__dim + 1), range(1, self.__dim + 1)):
            self.__xfield.set_col((k, i, j))

        for row, col in product(range(1, self.__dim + 1), repeat=2):
            quad = (row - 1) // self.__quad_dim * self.__quad_dim + (col - 1) // self.__quad_dim + 1
            for value in range(1, self.__dim + 1):
                self.__xfield.set_node((row, col, value), (0, row, col))
                self.__xfield.set_node((row, col, value), (1, row, value))
                self.__xfield.set_node((row, col, value), (2, col, value))
                self.__xfield.set_node((row, col, value), (3, quad, value))

    def set_field(self, field: list[list[int]] | None) -> None:
        if field is None:
            self.__field = [[0 for _ in range(self.__dim)] for _ in range(self.__dim)]

            self.clear_xfield()
            self.field_to_xfield()
            return

        if len(field) != self.__dim:
            raise ValueError(f"Field must have {self.__dim} rows.")

        for i in range(self.__dim):
            if len(field[i]) != self.__dim:
                raise ValueError(f"Row {i} of field must have {self.__dim} columns.")

        if not all(0 <= value <= self.__dim for row in field for value in row):
            raise ValueError(f"Field values must be between 0 and {self.__dim}.")

        self.__field = field

        self.clear_xfield()
        self.field_to_xfield()

    def field_to_xfield(self) -> None:
        for row, col in product(range(self.__dim), repeat=2):
            if self.__field[row][col] > 0:
                subset = self.__xfield.get_row((row + 1, col + 1, self.__field[row][col]))
                self.__xfield.push_stack(subset)
                self.__xfield.cover(subset)

    def xfield_to_field(self) -> None:
        field = [[0 for _ in range(self.__dim)] for _ in range(self.__dim)]
        for cover_set in self.__xfield.get_stack():
            field[cover_set.idx[0] - 1][cover_set.idx[1] - 1] = cover_set.idx[2]

        self.__field = field

    def get_field(self) -> list[list[int]]:
        return self.__field

    def check_ceil(self, row: int, col: int, value: int) -> bool:
        if not all(isinstance(arg, int) for arg in (row, col, value)):
            raise TypeError("Row, col and value must be int.")

        if not all(1 <= arg <= self.__dim for arg in (row, col)):
            raise ValueError(f"Row and col must be between 1 and {self.__dim}")

        if not 0 <= value <= self.__dim:
            raise ValueError(f"Value must be between 0 and {self.__dim}")

        row -= 1
        col -= 1

        row_quad_cord = row // self.__quad_dim * self.__quad_dim
        col_quad_cord = col // self.__quad_dim * self.__quad_dim

        if value == 0:
            return True

        if value in self.__field[row]:
            return False

        if value in list(zip(*self.__field))[col]:
            return False

        for row in self.__field[row_quad_cord : row_quad_cord + self.__quad_dim]:
            if value in row[col_quad_cord : col_quad_cord + self.__quad_dim]:
                return False

        return True

    def set_ceil(self, row: int, col: int, value: int) -> bool:
        if self.check_ceil(row, col, value):
            self.__field[row - 1][col - 1] = value
            return True
        else:
            return False

    def get_ceil(self, row: int, col: int) -> int:
        if not all(isinstance(arg, int) for arg in (row, col)):
            raise TypeError("Row and col must be int.")

        if not all(1 <= arg <= self.__dim for arg in (row, col)):
            raise ValueError(f"Row and col must be between 1 and {self.__dim}")

        return self.__field[row - 1][col - 1]

    def solve(self, row: int = 1, col: int = 1) -> bool:
        if not all(isinstance(arg, int) for arg in (row, col)):
            raise TypeError("Row and col must be int.")

        if not all(1 <= arg <= self.__dim for arg in (row, col)):
            raise ValueError(f"Row and col must be between 1 and {self.__dim}")

        next_col = col + 1
        next_row = row
        if next_col == self.__dim + 1:
            next_col = 1
            next_row = row + 1

        if self.__field[row - 1][col - 1] != 0:
            if next_row == self.__dim + 1:
                return True
            return self.solve(next_row, next_col)

        for value in range(1, self.__dim + 1):
            if self.set_ceil(row, col, value):
                if next_row == self.__dim + 1:
                    return True

                if not self.solve(next_row, next_col):
                    self.set_ceil(row, col, 0)
                else:
                    return True

        return False

    def xsolve(self) -> bool:
        if self.__xfield.algorithm_x():
            return True

        return False
