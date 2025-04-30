import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

solving_steps = []

def load_board(filename):
    board = []
    with open(filename, "r") as f:
        for line in f:
            board.append([int(x) for x in line.strip().split()])
    return board

def is_valid(board, row, col, num):
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False
    box_row, box_col = (row // 3) * 3, (col // 3) * 3
    for i in range(3):
        for j in range(3):
            if board[box_row + i][box_col + j] == num:
                return False
    return True

def solve(board, step_counter):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                for num in range(1, 10):
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        solving_steps.append((row, col, num))
                        step_counter[0] += 1
                        if solve(board, step_counter):
                            return True
                        board[row][col] = 0
                        solving_steps.append((row, col, 0))
                return False
    return True

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

def animate_solving(steps, original_puzzle):
    board = np.array(original_puzzle)
    fig, ax = plt.subplots()
    plt.title("Sudoku Solving (Backtracking Animation)")

    initial_text = [[str(val) if val != 0 else '' for val in row] for row in board]
    table = ax.table(cellText=initial_text, loc='center', cellLoc='center')
    table.scale(1, 2)
    ax.axis('off')

    for i in range(9):
        for j in range(9):
            if board[i][j] != 0:
                table[(i, j)].set_facecolor('#d3d3d3') 

    counter_text = ax.text(0.95, 0.02, "Step: 0", transform=ax.transAxes,
                           ha='right', va='bottom', fontsize=12, color='black')

    def update(frame):
        row, col, val = steps[frame]
        if original_puzzle[row][col] == 0:
            board[row][col] = val
            cell = table.get_celld()[(row, col)]
            cell.get_text().set_text(str(val) if val != 0 else '')
            cell.set_facecolor('#b3ffb3' if val != 0 else '#ffffff')
        counter_text.set_text(f"Step: {frame + 1}")
        return table,

    num_steps = len(steps)
    if num_steps < 200:
        interval = 100
    elif num_steps < 500:
        interval = 50
    else:
        interval = 10

    ani = FuncAnimation(fig, update, frames=num_steps, interval=interval, repeat=False)
    plt.show()


def main():
    filename = input("Enter the name of the Sudoku file to solve (e.g., puzzle1.txt): ").strip()
    solution_file = filename.replace(".txt", "_solution.txt")

    try:
        puzzle = load_board(filename)
        expected_solution = load_board(solution_file)
    except FileNotFoundError:
        print("File not found.")
        return

    step_counter = [0]
    puzzle_copy = [row[:] for row in puzzle]

    if solve(puzzle_copy, step_counter):
        print("\nTotal solving steps (placements + backtracks):", len(solving_steps))
        print("\nSolved Board:\n")
        print_board(puzzle_copy)
        animate_solving(solving_steps, puzzle)
        print("\n")
    else:
        print("No solution found.")

if __name__ == "__main__":
    main()
