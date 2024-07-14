import copy
import sys
import time
LETTERS = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

def print_usage():
    """
    Prints the usage instructions for running the script.
    """
    print("Usage: python domino.py \"<matrix>\"")
    print("Enter the state matrix as a list of lists, separated by commas and semicolons.")
    print("Example: python domino.py \"0,0,0,1;0,1,0,1;0,1,0,0,0,0,0,0\"")

def validate_state(state):
    """
    Validates the given state matrix.

    Args:
        state (list): The state matrix to validate.

    Returns:
        bool: True if the state matrix is valid, False otherwise.
    """
    # Check if state is a list
    if not isinstance(state, list):
        return False
    
    if(len(state) == 0):
        return False

    # Check if state is a matrix
    if not all(isinstance(row, list) for row in state):
        return False

    # Check if all elements in the matrix are either 0 or 1
    if not all(all(element == 0 or element == 1 for element in row) for row in state):
        return False

    # Check if all rows have the same length
    if len(set(len(row) for row in state)) > 1:
        return False

    return True

def domino_assignments(state):
    """
    Finds all possible domino assignments in the given state matrix.

    Args:
        state (list): The state matrix.

    Returns:
        list: A list of tuples representing the domino assignments.
    """
    rows = len(state)
    cols = len(state[0])
    assignments = []

    for i in range(rows):
        for j in range(cols):
            if state[i][j] == 0:
                # Check if the cell above is empty
                if i > 0 and state[i - 1][j] == 0:
                    assignments.append(((i - 1, j), (i, j)))
                # Check if the cell to the left is empty
                if j > 0 and state[i][j - 1] == 0:
                    assignments.append(((i, j - 1), (i, j)))

    return assignments

def is_solved(state):
    """
    Checks if the given state matrix is solved.

    Args:
        state (list): The state matrix.

    Returns:
        bool: True if the state matrix is solved, False otherwise.
    """
    if any(0 in row for row in state):
        return False
    return True


def is_solvable(state):
    """
    Checks if the given state matrix is solvable by checking whether there is a 0 with no neighbouring 0s.

    Args:
        state (list): The state matrix.

    Returns:
        bool: False if the state matrix contains a 0 with no neighbouring 0, True otherwise.
    """
    rows = len(state)
    cols = len(state[0])
    for i in range(rows):
        for j in range(cols):
            if state[i][j] == 0:
                # Check if the cell above is empty
                if i > 0 and state[i - 1][j] == 0:
                    continue
                # Check if the cell below is empty
                if i < rows - 1 and state[i + 1][j] == 0:
                    continue
                # Check if the cell to the left is empty
                if j > 0 and state[i][j - 1] == 0:
                    continue
                # Check if the cell to the right is empty
                if j < cols - 1 and state[i][j + 1] == 0:
                    continue
                return False
    return True

def is_equal(solution_1, solution_2):
    """
    Checks if two solutions are equal.

    Args:
        solution_1 (list): The first solution.
        solution_2 (list): The second solution.

    Returns:
        bool: True if the solutions are equal, False otherwise.
    """
    if len(solution_1) != len(solution_2):
        return False

    for i in range(len(solution_1)):
        if solution_1[i] not in solution_2:
            return False

    return True

def solve_domino(state, selected_assignments = []):
    """
    Solves the domino puzzle for the given state matrix.

    Args:
        state (list): The state matrix.
        avoid (list): A list of solutions to avoid.
        selected_assignments (list): The selected assignments for the current solution (default=[]).

    Returns:
        list: A list of solutions, which are lists of assignments.
    """
    solutions = []
    assignments = domino_assignments(state)
    if(len(assignments) == 0):
        return solutions
    
    for assignment in assignments:
        #create new assignment
        new_assignments = copy.deepcopy(selected_assignments)
        new_assignments.append(assignment)
        #create new state
        new_state = copy.deepcopy(state)
        new_state[assignment[0][0]][assignment[0][1]] = 1
        new_state[assignment[1][0]][assignment[1][1]] = 1
        #check whether a goal state is reached
        if is_solved(new_state):
            #check whether the solution is a new one
            solutions.append(new_assignments)
            continue
        #check whether the new state is solvable
        if(not is_solvable(new_state)):
            continue
        
        new_solutions = solve_domino(new_state, new_assignments)
        for new_solution in new_solutions:
            if(not any(is_equal(new_solution, solution) for solution in solutions)):
                solutions.append(new_solution)
    
    return solutions

def main():
    start_time = time.time()
    # get the matrix from the command line arguments
    if len(sys.argv) < 2:
        print("No matrix provided")
        print_usage()
        exit()

    matrix = sys.argv[1]
    try:
        input = [[int(num) for num in row.split(',')] for row in matrix.split(';')]
    except:
        print("Invalid matrix")
        print_usage()
        exit()
    
    if not validate_state(input):
        print("Invalid matrix")
        print_usage()
        exit()

    #solve the domino puzzle
    solutions = solve_domino(input)
    if(len(solutions) == 0):
        print("No solution found")

    #print the solutions
    count = 1
    for solution in solutions:
        grid = [['0'] * len(input[0]) for _ in range(len(input))]
        for i in range(len(solution)):
            assignment = solution[i]
            letter = LETTERS[i % len(LETTERS)]
            grid[assignment[0][0]][assignment[0][1]] = letter
            grid[assignment[1][0]][assignment[1][1]] = letter
        print("Solution " + str(count) + ":")
        count += 1
        for row in grid:
            print(','.join(map(str, row)))
        print()

    end_time = time.time()
    execution_time = end_time - start_time
    print()
    print("Execution time: {:.2f} seconds".format(execution_time))

if __name__ == "__main__":
    main()