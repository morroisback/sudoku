import time

from sudoku import Sudoku

def get_3_sudoku() -> list:
    sudoku_field = [
        [6, 0, 0, 5, 0, 0, 2, 0, 8],
        [9, 0, 8, 0, 7, 2, 3, 0, 5],
        [2, 0, 0, 0, 3, 0, 4, 9, 0],
        [0, 8, 7, 0, 0, 5, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 8, 5, 1],
        [0, 0, 0, 0, 2, 0, 0, 0, 0],
        [8, 0, 3, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 2],
        [0, 6, 9, 0, 0, 4, 5, 3, 0],
    ]
    return sudoku_field


def get_4_sudoku(num: int) -> list:
    sudoku_field_1 = [
        [13, 16, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 6, 11],
        [8, 0, 0, 0, 9, 13, 0, 15, 10, 0, 3, 1, 0, 0, 0, 2],
        [1, 0, 10, 3, 0, 7, 0, 0, 0, 0, 2, 0, 12, 14, 0, 9],
        [0, 0, 14, 0, 16, 4, 0, 1, 9, 0, 11, 6, 0, 3, 0, 0],
        [0, 2, 0, 8, 0, 0, 0, 6, 16, 0, 0, 0, 13, 0, 1, 0],
        [0, 1, 16, 12, 0, 0, 7, 0, 0, 15, 0, 0, 14, 4, 9, 0],
        [0, 0, 0, 0, 0, 16, 4, 9, 12, 6, 1, 0, 0, 0, 0, 0],
        [0, 6, 0, 4, 1, 0, 13, 0, 0, 5, 0, 2, 16, 0, 3, 0],
        [0, 9, 0, 13, 5, 0, 11, 0, 0, 10, 0, 15, 4, 0, 2, 0],
        [0, 0, 0, 0, 0, 6, 16, 13, 3, 11, 5, 0, 0, 0, 0, 0],
        [0, 5, 6, 15, 0, 0, 9, 0, 0, 4, 0, 0, 11, 1, 14, 0],
        [0, 3, 0, 16, 0, 0, 0, 2, 8, 0, 0, 0, 9, 0, 5, 0],
        [0, 0, 1, 0, 7, 11, 0, 5, 4, 0, 8, 14, 0, 9, 0, 0],
        [6, 0, 12, 11, 0, 15, 0, 0, 0, 0, 9, 0, 3, 2, 0, 4],
        [3, 0, 0, 0, 13, 8, 0, 10, 11, 0, 16, 12, 0, 0, 0, 1],
        [16, 7, 13, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 12, 11, 14]
    ]

    sudoku_field_2 = [
        [9, 0, 0, 4, 0, 0, 14, 13, 7, 15, 0, 0, 12, 0, 0, 8],
        [0, 6, 15, 8, 0, 0, 12, 0, 0, 14, 0, 0, 9, 2, 1, 0],
        [0, 11, 0, 0, 3, 0, 4, 9, 13, 10, 0, 6, 0, 0, 7, 0],
        [16, 3, 0, 14, 2, 0, 15, 0, 0, 8, 0, 9, 6, 0, 5, 4],
        [0, 0, 6, 5, 0, 9, 0, 16, 11, 0, 10, 0, 14, 13, 0, 0],
        [0, 0, 0, 0, 10, 1, 0, 2, 14, 0, 9, 3, 0, 0, 0, 0],
        [10, 7, 2, 16, 0, 0, 0, 0, 0, 0, 0, 0, 11, 9, 15, 3],
        [11, 0, 4, 0, 6, 7, 0, 0, 0, 0, 13, 15, 0, 8, 0, 2],
        [13, 0, 7, 0, 5, 2, 0, 0, 0, 0, 8, 14, 0, 12, 0, 6],
        [2, 12, 14, 10, 0, 0, 0, 0, 0, 0, 0, 0, 5, 1, 3, 11],
        [0, 0, 0, 0, 12, 15, 0, 1, 5, 0, 2, 10, 0, 0, 0, 0],
        [0, 0, 11, 1, 0, 13, 0, 14, 9, 0, 12, 0, 2, 15, 0, 0],
        [5, 4, 0, 11, 14, 0, 2, 0, 0, 16, 0, 8, 10, 0, 13, 9],
        [0, 2, 0, 0, 11, 0, 7, 6, 15, 9, 0, 5, 0, 0, 4, 0],
        [0, 16, 9, 6, 0, 0, 1, 0, 0, 3, 0, 0, 7, 5, 14, 0],
        [14, 0, 0, 7, 0, 0, 16, 8, 10, 6, 0, 0, 3, 0, 0, 12]
    ]

    match num:
        case 1:
            return sudoku_field_1
        case 2:
            return sudoku_field_2
        case _:
            raise ValueError("Invalid sudoku number. Must be 1 or 2.")
        

def get_5_sudoku() -> list:
    letters = {
        "A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6, "G": 7, "H": 8, "I": 9, "J": 10,
        "K": 11, "L": 12, "M": 13, "N": 14, "O": 15, "P": 16, "Q": 17, "R": 18, "S": 19, "T": 20,
        "U": 21, "V": 22, "W": 23, "X": 24, "Y": 25, "Z": 0
    }
    sudoku_field = [
        [letters["Z"], letters["Z"], letters["L"], letters["Z"], letters["Z"],
         letters["Z"], letters["U"], letters["Z"], letters["Z"], letters["K"],
         letters["Z"], letters["Z"], letters["Z"], letters["Z"], letters["Z"],
         letters["Z"], letters["Z"], letters["Z"], letters["G"], letters["Z"],
         letters["Z"], letters["Z"], letters["I"], letters["Z"], letters["X"]],
        [letters["Z"], letters["Z"], letters["Z"], letters["Z"], letters["Q"],
         letters["H"], letters["Z"], letters["R"], letters["Z"], letters["Z"],
         letters["K"], letters["Z"], letters["Z"], letters["Z"], letters["Z"],
         letters["Z"], letters["V"], letters["Z"], letters["Z"], letters["Z"],
         letters["A"], letters["M"], letters["T"], letters["Z"], letters["Z"]],
        [letters["D"], letters["A"], letters["B"], letters["H"], letters["I"],
         letters["Z"], letters["Z"], letters["Z"], letters["C"], letters["Z"],
         letters["Z"], letters["Z"], letters["X"], letters["T"], letters["Z"],
         letters["Z"], letters["F"], letters["Z"], letters["Z"], letters["Z"],
         letters["Z"], letters["Z"], letters["Z"], letters["V"], letters["K"]],
        [letters["Z"], letters["V"], letters["X"], letters["W"], letters["Z"],
         letters["Z"], letters["D"], letters["J"], letters["E"], letters["Z"],
         letters["Z"], letters["Z"], letters["I"], letters["R"], letters["A"],
         letters["Z"], letters["Z"], letters["O"], letters["Z"], letters["Z"],
         letters["C"], letters["H"], letters["Z"], letters["Z"], letters["Z"]],
        [letters["Z"], letters["Z"], letters["Z"], letters["Z"], letters["Z"],
         letters["X"], letters["F"], letters["Z"], letters["B"], letters["W"],
         letters["Q"], letters["D"], letters["Z"], letters["Z"], letters["L"],
         letters["Z"], letters["Z"], letters["Z"], letters["Z"], letters["Z"],
         letters["Z"], letters["Z"], letters["O"], letters["Z"], letters["Z"]],

        [letters["Z"], letters["Z"], letters["Z"], letters["Z"], letters["Z"],
         letters["Q"], letters["I"], letters["U"], letters["Z"], letters["Z"],
         letters["Z"], letters["O"], letters["Z"], letters["S"], letters["Z"],
         letters["Z"], letters["Z"], letters["Z"], letters["R"], letters["Z"],
         letters["Z"], letters["Z"], letters["Z"], letters["Z"], letters["N"]],
        [letters["Z"], letters["Z"], letters["Z"], letters["E"], letters["Z"],
         letters["F"], letters["V"], letters["K"], letters["Z"], letters["J"],
         letters["Z"], letters["Z"], letters["Z"], letters["P"], letters["Q"],
         letters["Z"], letters["Z"], letters["L"], letters["Z"], letters["A"],
         letters["M"], letters["I"], letters["Y"], letters["Z"], letters["H"]],
        [letters["Z"], letters["Z"], letters["F"], letters["Z"], letters["C"],
         letters["Z"], letters["R"], letters["A"], letters["Z"], letters["Z"],
         letters["Z"], letters["Z"], letters["N"], letters["U"], letters["G"],
         letters["Z"], letters["Z"], letters["Z"], letters["I"], letters["W"],
         letters["S"], letters["Z"], letters["Z"], letters["B"], letters["Z"]],
        [letters["Z"], letters["I"], letters["Z"], letters["Q"], letters["H"],
         letters["Z"], letters["O"], letters["Y"], letters["Z"], letters["Z"],
         letters["L"], letters["Z"], letters["Z"], letters["D"], letters["Z"],
         letters["Z"], letters["B"], letters["Z"], letters["Z"], letters["K"],
         letters["T"], letters["Z"], letters["U"], letters["Z"], letters["Z"]],
        [letters["Z"], letters["M"], letters["G"], letters["Z"], letters["Z"],
         letters["W"], letters["C"], letters["Z"], letters["Z"], letters["Z"],
         letters["Z"], letters["Z"], letters["T"], letters["Z"], letters["Z"],
         letters["Z"], letters["Z"], letters["Z"], letters["Z"], letters["J"],
         letters["Z"], letters["R"], letters["Z"], letters["D"], letters["V"]],

        [letters["M"], letters["Z"], letters["R"], letters["Z"], letters["E"],
         letters["B"], letters["Z"], letters["Z"], letters["Z"], letters["Z"],
         letters["Z"], letters["Z"], letters["D"], letters["Z"], letters["Z"],
         letters["C"], letters["Z"], letters["Z"], letters["Z"], letters["H"],
         letters["Z"], letters["A"], letters["Z"], letters["G"], letters["W"]],
        [letters["Z"], letters["Z"], letters["Z"], letters["P"], letters["W"],
         letters["Z"], letters["Z"], letters["G"], letters["Z"], letters["Z"],
         letters["A"], letters["Y"], letters["Z"], letters["Z"], letters["E"],
         letters["Z"], letters["Z"], letters["Z"], letters["Z"], letters["Z"],
         letters["X"], letters["Z"], letters["N"], letters["Z"], letters["Z"]],
        [letters["Z"], letters["Z"], letters["Z"], letters["K"], letters["Y"],
         letters["Z"], letters["Z"], letters["L"], letters["Z"], letters["Z"],
         letters["Z"], letters["Z"], letters["Z"], letters["W"], letters["U"],
         letters["T"], letters["Z"], letters["N"], letters["D"], letters["Z"],
         letters["Z"], letters["Z"], letters["Z"], letters["Z"], letters["Z"]],
        [letters["H"], letters["L"], letters["T"], letters["S"], letters["Z"],
         letters["Z"], letters["Z"], letters["Z"], letters["W"], letters["Z"],
         letters["Z"], letters["Z"], letters["V"], letters["Z"], letters["K"],
         letters["X"], letters["Z"], letters["Z"], letters["Z"], letters["Z"],
         letters["Z"], letters["Z"], letters["Q"], letters["Z"], letters["Z"]],
        [letters["N"], letters["B"], letters["Z"], letters["Z"], letters["Z"],
         letters["Z"], letters["H"], letters["Z"], letters["S"], letters["Y"],
         letters["Z"], letters["P"], letters["Z"], letters["C"], letters["I"],
         letters["Z"], letters["Z"], letters["E"], letters["Z"], letters["L"],
         letters["Z"], letters["Z"], letters["Z"], letters["T"], letters["O"]],

        [letters["L"], letters["Q"], letters["Z"], letters["Z"], letters["Z"],
         letters["Z"], letters["Z"], letters["E"], letters["Z"], letters["U"],
         letters["R"], letters["Z"], letters["Z"], letters["Z"], letters["Z"],
         letters["B"], letters["I"], letters["Z"], letters["Z"], letters["Z"],
         letters["D"], letters["Z"], letters["Z"], letters["Z"], letters["T"]],
        [letters["B"], letters["Z"], letters["Z"], letters["A"], letters["Z"],
         letters["Z"], letters["Z"], letters["Z"], letters["Z"], letters["C"],
         letters["Z"], letters["Z"], letters["Z"], letters["Z"], letters["Y"],
         letters["S"], letters["Z"], letters["Z"], letters["U"], letters["V"],
         letters["P"], letters["Z"], letters["Z"], letters["Z"], letters["Z"]],
        [letters["T"], letters["Z"], letters["Z"], letters["X"], letters["P"],
         letters["Z"], letters["Z"], letters["Z"], letters["Z"], letters["Z"],
         letters["Z"], letters["Z"], letters["Q"], letters["A"], letters["Z"],
         letters["Z"], letters["Z"], letters["W"], letters["Z"], letters["Z"],
         letters["R"], letters["Y"], letters["Z"], letters["C"], letters["Z"]],
        [letters["Z"], letters["H"], letters["Z"], letters["Z"], letters["N"],
         letters["Y"], letters["Q"], letters["Z"], letters["Z"], letters["Z"],
         letters["X"], letters["I"], letters["S"], letters["Z"], letters["Z"],
         letters["F"], letters["Z"], letters["Z"], letters["Z"], letters["Z"],
         letters["Z"], letters["K"], letters["W"], letters["A"], letters["Z"]],
        [letters["Z"], letters["Z"], letters["K"], letters["Y"], letters["F"],
         letters["T"], letters["A"], letters["Z"], letters["Z"], letters["G"],
         letters["Z"], letters["Z"], letters["P"], letters["N"], letters["Z"],
         letters["Z"], letters["Z"], letters["Z"], letters["Z"], letters["Z"],
         letters["Q"], letters["L"], letters["Z"], letters["Z"], letters["U"]],

        [letters["V"], letters["W"], letters["Z"], letters["Z"], letters["Z"],
         letters["U"], letters["Z"], letters["P"], letters["Z"], letters["Z"],
         letters["Z"], letters["H"], letters["Z"], letters["Z"], letters["R"],
         letters["G"], letters["Z"], letters["X"], letters["Z"], letters["Z"],
         letters["Z"], letters["N"], letters["M"], letters["Z"], letters["Q"]],
        [letters["Z"], letters["G"], letters["Z"], letters["O"], letters["Z"],
         letters["Z"], letters["T"], letters["Z"], letters["Z"], letters["F"],
         letters["Z"], letters["X"], letters["Z"], letters["B"], letters["N"],
         letters["M"], letters["Z"], letters["Z"], letters["K"], letters["C"],
         letters["Z"], letters["Z"], letters["E"], letters["Z"], letters["Y"]],
        [letters["C"], letters["U"], letters["Z"], letters["Z"], letters["Z"],
         letters["G"], letters["Y"], letters["N"], letters["O"], letters["S"],
         letters["Z"], letters["Z"], letters["Z"], letters["I"], letters["Z"],
         letters["V"], letters["Z"], letters["F"], letters["Z"], letters["Z"],
         letters["B"], letters["Z"], letters["Z"], letters["Z"], letters["Z"]],
        [letters["I"], letters["Z"], letters["Z"], letters["Z"], letters["Z"],
         letters["R"], letters["E"], letters["Z"], letters["Z"], letters["Z"],
         letters["W"], letters["S"], letters["O"], letters["Z"], letters["J"],
         letters["Z"], letters["Z"], letters["A"], letters["Z"], letters["Z"],
         letters["Z"], letters["Z"], letters["K"], letters["Z"], letters["Z"]],
        [letters["Z"], letters["P"], letters["Z"], letters["Z"], letters["T"],
         letters["C"], letters["Z"], letters["X"], letters["M"], letters["D"],
         letters["Z"], letters["Z"], letters["Z"], letters["Q"], letters["Z"],
         letters["Z"], letters["Z"], letters["Z"], letters["Z"], letters["Y"],
         letters["Z"], letters["U"], letters["L"], letters["O"], letters["Z"]]
    ]

    return sudoku_field


def main() -> None:
    # sudoku_field = None
    sudoku_field = get_3_sudoku()
    # sudoku_field = get_4_sudoku(1)
    # sudoku_field = get_5_sudoku()

    sudoku = Sudoku(3)

    sudoku.set_field(sudoku_field)
    print(sudoku)

    start_time = time.time()
    is_solved = sudoku.xsolve()
    end_time = time.time()

    xsolve_elapsed_time = end_time - start_time
    sudoku.xfield_to_field()
    print(sudoku)

    print("Sudoku is solved" if is_solved else "Sudoku is not solved")
    print("Xsolve elapsed time:", xsolve_elapsed_time)

    print("=" * 40, end="\n\n")

    sudoku.set_field(sudoku_field)
    print(sudoku)

    start_time = time.time()
    is_solved = sudoku.solve()
    end_time = time.time()

    solve_elapsed_time = end_time - start_time
    print(sudoku)

    print("Sudoku is solved" if is_solved else "Sudoku is not solved")
    print("Solve elapsed time:", solve_elapsed_time)


if __name__ == '__main__':
    main()
