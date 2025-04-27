import random
import copy

def is_valid(board, row, col, num):
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False
    box_row, box_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[box_row + i][box_col + j] == num:
                return False
    return True

def fill_board(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                nums = list(range(1, 10))
                random.shuffle(nums)
                for num in nums:
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if fill_board(board):
                            return True
                        board[row][col] = 0
                return False
    return True

def count_solutions(board, limit=2):
    def solve_count(b):
        for row in range(9):
            for col in range(9):
                if b[row][col] == 0:
                    for num in range(1, 10):
                        if is_valid(b, row, col, num):
                            b[row][col] = num
                            if solve_count(b):
                                return True
                            b[row][col] = 0
                    return False
        nonlocal solutions
        solutions += 1
        return solutions >= limit

    board_copy = [row[:] for row in board]
    solutions = 0
    solve_count(board_copy)
    return solutions

def remove_cells(board, difficulty):
    max_remove = {
        'easy': 35,
        'medium': 45,
        'hard': 55
    }.get(difficulty, 35)

    removed = 0
    attempts = 0
    while removed < max_remove and attempts < 1000:
        row, col = random.randint(0, 8), random.randint(0, 8)
        if board[row][col] != 0:
            temp = board[row][col]
            board[row][col] = 0
            if count_solutions(board) == 1:
                removed += 1
            else:
                board[row][col] = temp
        attempts += 1

def write_board_to_file(filename, board):
    with open(filename, "w") as f:
        for row in board:
            f.write(" ".join(str(num) for num in row) + "\n")

def print_board(board):
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("-" * 21)
        for j in range(9):
            if j % 3 == 0 and j != 0:
                print("|", end=" ")
            cell = board[i][j]
            print(cell if cell != 0 else ".", end=" ")
        print()

def generate_puzzle_with_solution(difficulty, filename):
    full_board = [[0 for _ in range(9)] for _ in range(9)]
    fill_board(full_board)

    puzzle = copy.deepcopy(full_board)
    remove_cells(puzzle, difficulty)

    write_board_to_file(f"{filename}.txt", puzzle)
    write_board_to_file(f"{filename}_solution.txt", full_board)

    print(f"\nPuzzle saved to {filename}.txt")
    print(f"Solution saved to {filename}_solution.txt")
    print("\nHere is the puzzle preview:\n")
    print_board(puzzle)
    print("\n")

def main():
    difficulty = input("What difficulty? (easy, medium, hard): ").lower().strip()
    if difficulty not in ['easy', 'medium', 'hard']:
        print("Invalid choice. Defaulting to easy.")
        difficulty = 'easy'

    filename = input("What would you like to name this puzzle (without extension)? ").strip()
    if not filename:
        filename = "sudoku_puzzle"

    generate_puzzle_with_solution(difficulty, filename)

if __name__ == "__main__":
    main()
