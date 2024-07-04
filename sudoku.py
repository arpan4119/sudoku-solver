import os
import platform

# Determine the clear screen command based on the operating system
CLEAR_COMMAND = 'cls' if platform.system() == 'Windows' else 'clear'

# Function to clear the console screen
def clear_screen():
    os.system(CLEAR_COMMAND)

# Function to load puzzle data from a text file
def load_puzzle_data(grid_size, percentage):
    filename = 'pattern.txt'
    target_label = f'{grid_size}x{grid_size} {percentage}% puzzles'

    with open(filename, 'r') as file:
        content = file.read()
        puzzles = content.split('\n\n')  # Each puzzle is separated by two newline characters

    for puzzle_section in puzzles:
        if target_label in puzzle_section:
            puzzle_lines = puzzle_section.split('\n')
            puzzle = ''.join(puzzle_lines[1])
            return puzzle

    print(f"No puzzle found for size {grid_size} and percentage {percentage}.")
    return ""

# Function to get user input for grid size or percentage
def get_user_input(prompt, valid_inputs):
    while True:
        try:
            user_input = int(input(prompt))
            if user_input in valid_inputs:
                return user_input
            else:
                print(f"Invalid input. Please enter one of: {', '.join(map(str, valid_inputs))}")
        except ValueError:
            print("Invalid input. Please enter a number.")

# Function to solve the Sudoku puzzle using backtracking
def solve_sudoku(board, grid_size):
    def is_valid(board, num, pos):
        # Check row and column constraints
        for i in range(grid_size):
            if board[pos[0]][i] == num and pos[1] != i:
                return False
            if board[i][pos[1]] == num and pos[0] != i:
                return False

        # Check subgrid constraints
        subgrid_size = int(grid_size ** 0.5)
        subgrid_x = pos[1] // subgrid_size
        subgrid_y = pos[0] // subgrid_size

        for i in range(subgrid_y * subgrid_size, subgrid_y * subgrid_size + subgrid_size):
            for j in range(subgrid_x * subgrid_size, subgrid_x * subgrid_size + subgrid_size):
                if board[i][j] == num and (i, j) != pos:
                    return False

        return True

    # Find an empty cell in the Sudoku grid
    def find_empty_cell(board):
        for i in range(grid_size):
            for j in range(grid_size):
                if board[i][j] == 0:
                    return (i, j)
        return None

    # Backtracking algorithm to solve Sudoku
    def backtrack(board):
        empty_cell = find_empty_cell(board)
        if not empty_cell:
            return True
        else:
            row, col = empty_cell

        for num in range(1, grid_size + 1):
            if is_valid(board, num, (row, col)):
                board[row][col] = num

                if backtrack(board):
                    return True

                board[row][col] = 0

        return False

    return backtrack(board)

# Function to check if the solved Sudoku board is valid
def is_solution_valid(board, grid_size):
    def is_valid(board, num, pos):
        # Check row and column constraints
        for i in range(grid_size):
            if board[pos[0]][i] == num and pos[1] != i:
                return False
            if board[i][pos[1]] == num and pos[0] != i:
                return False

        # Check subgrid constraints
        subgrid_size = int(grid_size ** 0.5)
        subgrid_x = pos[1] // subgrid_size
        subgrid_y = pos[0] // subgrid_size

        for i in range(subgrid_y * subgrid_size, subgrid_y * subgrid_size + subgrid_size):
            for j in range(subgrid_x * subgrid_size, subgrid_x * subgrid_size + subgrid_size):
                if board[i][j] == num and (i, j) != pos:
                    return False

        return True

    # Check each cell in the board
    for i in range(grid_size):
        for j in range(grid_size):
            if board[i][j] == 0 or not is_valid(board, board[i][j], (i, j)):
                return False

    return True

# Function to print the Sudoku grid
def print_sudoku(board, grid_size):
    for i in range(grid_size):
        if i > 0 and i % int(grid_size ** 0.5) == 0:
            print("-" * (grid_size * 2 + int(grid_size ** 0.5) - 1))

        for j in range(grid_size):
            if j > 0 and j % int(grid_size ** 0.5) == 0:
                print("| ", end="")

            if j == grid_size - 1:
                if board[i][j] == 0:
                    print(" ")
                else:
                    print(board[i][j])
            else:
                if board[i][j] == 0:
                    print(" " + " ", end="")
                else:
                    print(str(board[i][j]) + " ", end="")

# Main execution
def main():
    clear_screen()
    print("Welcome to Sudoku Solver!\n")

    # Get user inputs for grid size and percentage of input
    grid_size = get_user_input("Enter the size of the Sudoku grid (4 or 9): ", [4, 9])
    percentage = get_user_input("Enter the percentage of input you want (30 or 70): ", [30, 70])

    # Load puzzle based on user input
    puzzle = load_puzzle_data(grid_size, percentage)

    # Initialize the Sudoku grid
    sudoku = []
    row = []

    # Convert puzzle string to a 2D list
    for i in range(len(puzzle)):
        row.append(int(puzzle[i]))
        if (i + 1) % grid_size == 0:
            sudoku.append(row)
            row = []

    # Display the initial problem
    clear_screen()
    print("\nProblem: \n")
    print_sudoku(sudoku, grid_size)

    # Wait for user input before displaying the solution
    input("\nPress Enter to See the Solution...")

    # Solve the Sudoku puzzle
    if solve_sudoku(sudoku, grid_size):
        clear_screen()
        print("\nSolution: \n")
        print_sudoku(sudoku, grid_size)

        # Verify the solution
        if is_solution_valid(sudoku, grid_size):
            print("\nThe solution is verified.")
        else:
            print("\nYour solution is incorrect. Please try again.")
    else:
        print("\nNo solution found for this Sudoku puzzle.")

if __name__ == "__main__":
    main()
