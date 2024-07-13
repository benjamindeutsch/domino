import copy

input = [[1,0,0,0],[0,0,1,0],[0,0,0,0]]

def validate_state(state):
    # Check if state is a list
    if not isinstance(state, list):
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
    if any(0 in row for row in state):
        return False
    return True

def is_equal(solution_1, solution_2):
    if len(solution_1) != len(solution_2):
        return False

    for i in range(len(solution_1)):
        if solution_1[i] not in solution_2:
            return False

    return True

def solve_domino(state, avoid, selected_assignments = [], ):
    if is_solved(state):
        if(any(is_equal(solution, selected_assignments) for solution in avoid)):
            return None
        return selected_assignments
    
    assignments = domino_assignments(state)
    if(len(assignments) == 0):
        return None
    
    for assignment in assignments:
        #create new assignment
        new_assignments = copy.deepcopy(selected_assignments)
        new_assignments.append(assignment)
        #create new state
        new_state = copy.deepcopy(state)
        new_state[assignment[0][0]][assignment[0][1]] = 1
        new_state[assignment[1][0]][assignment[1][1]] = 1
        #solve new state
        solution = solve_domino(new_state, avoid, new_assignments)
        if(solution is not None):
            return solution
    
    return None

if validate_state(input):
    solutions = []
    while True:
        solution = solve_domino(input, solutions)
        if solution is None:
            break
        solutions.append(solution)
    
    if(len(solutions) == 0):
        print("No solution found")

    letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

    for solution in solutions:
        grid = [['0'] * len(input[0]) for _ in range(len(input))]
        for i in range(len(solution)):
            assignment = solution[i]
            letter = letters[i % len(letters)]
            grid[assignment[0][0]][assignment[0][1]] = letter
            grid[assignment[1][0]][assignment[1][1]] = letter
        print("Solution:")
        for row in grid:
            print(row)
        print()