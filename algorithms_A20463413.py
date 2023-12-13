from csp_A20463413 import CSP
import math
import copy

# Starts the backtracking search by initializing an empty assignment board and then calling backtrack
# csp => CSP object
def backtracking_search(csp : CSP) :
    # Fill the assignment list with X's
    assignment = []
    for i in range(9) :
        assignment.append(["X", "X", "X", "X", "X", "X", "X", "X", "X"])

    return backtrack(csp, assignment)


# CSP back-tracking search algorithm
# csp => CSP object
# assignment => assignment board to be filled
# nodes => keeps track of how many search nodes were generated
def backtrack(csp : CSP, assignment, nodes=0) :
    nodes = nodes + 1
    # Is assignment complete?
    if is_valid_sudoku(assignment) and csp.compare_known(assignment):
        return assignment, nodes

    # Get the coordinates of the next variable to be assigned
    var = -1
    for row in range(9) :
        for col in range(9) :
            if assignment[row][col] == "X" :
                var = (row, col)
                break

    for val in csp.constraints[var] :  # For each possible value in the variable's domain
        #if csp.in_constraint(var, val) : # If value is consistent with assignment
        assignment[var[0]][var[1]] = val # Assign the value to the variable

        old_constraints = csp.constraints[var] # Remember the old constraints in case this search path results in a failure

        if is_valid(assignment, var[0], var[1]) :
            #csp.update_constraints(var, val, 0) # update the constraints based on the new value that was assigned --- int

            result, nodes = backtrack(csp, assignment, nodes) # Pass updated csp constraints and updated assignment to backtrack
            if result != -1 : # If the result is not a failure then return it
                return result, nodes
            
        csp.update_constraints(var, old_constraints, 1) # Update the constraints to be back to before the new value was assigned
        assignment[var[0]][var[1]] = "X" # Reset the assignment back to being empty
            
    return -1, nodes # Return failure if there are no valid possible assignments





# Starts the backtracking search by initializing an empty assignment board and then calling backtrack
# csp => CSP object
def backtracking_search_mrv(csp : CSP) :
    # Fill the assignment list with X's
    assignment = []
    for i in range(9) :
        assignment.append(["X", "X", "X", "X", "X", "X", "X", "X", "X"])

    return backtrack_mrv(csp, assignment)


# CSP back-tracking search algorithm
# csp => CSP object
# assignment => assignment board to be filled
# nodes => keeps track of how many search nodes were generated
def backtrack_mrv(csp : CSP, assignment, nodes=0) :
    nodes = nodes + 1
    # Is assignment complete?
    if is_valid_sudoku(assignment) and csp.compare_known(assignment):
        return assignment, nodes

    # Get the coordinates of the next variable to be assigned using mrv()
    var = mrv(csp)


    for val in csp.constraints[var] :  # For each possible value in the variable's domain
        #if csp.in_constraint(var, val) : # If value is consistent with assignment
        assignment[var[0]][var[1]] = val # Assign the value to the variable

        old_constraints = csp.constraints[var] # Remember the old constraints in case this search path results in a failure

        if is_valid(assignment, var[0], var[1]) :
            #csp.update_constraints(var, val, 0) # update the constraints based on the new value that was assigned --- int

            inferences, new_csp = inference(csp, var, val)

            if inferences == True :
                result, nodes = backtrack(csp, assignment, nodes) # Pass updated csp constraints and updated assignment to backtrack
                if result != -1 : # If the result is not a failure then return it
                    return result, nodes
            
        csp.update_constraints(var, old_constraints, 1) # Update the constraints to be back to before the new value was assigned
        assignment[var[0]][var[1]] = "X" # Reset the assignment back to being empty
            
    return -1, nodes # Return failure if there are no valid possible assignments


# Return the variable with the fewest legal values left
# csp => CSP object
def mrv(csp : CSP) :
    var = (0,0)
    min_val = 9
    for row in range(9) :
        for col in range(9) :
            l = len(csp.constraints[(row, col)])
            if l < min_val and 1 > 1:
                min_val = len(csp.constraints(var))
                var = (row, col)
    
    return var


# Function to perform forward checking
# csp => CSP object
# var => (row, col) index into constraints
# val => the current value being tested in backtrack_mrv()
def inference(csp : CSP, var, val) :
    new_csp = copy.deepcopy(csp)
    new_csp.update_constraints(var, val, 0)

    for row in range(9) :
        for col in range(9) :
            if len(new_csp.constraints[(row, col)]) == 0 :
                return False, new_csp
    
    return True, new_csp





# Brute force algorithm
# csp => CSP object
# nodes => how many nodes were generated
def bruteforce(csp : CSP) :
    nodes = 1

    # Get the next value to be assigned
    row, col = -1, -1
    for r in csp.sudoku :
        row = row + 1
        if 'X' in r :
            col = r.index('X')
            break
    
    # Base case = no more values to assign
    if col == -1 :
        if is_valid_sudoku(csp.sudoku) and csp.compare_known(csp.sudoku) :
            return csp.sudoku, nodes
        return -1, nodes


    for val in csp.constraints[(row, col)] :
        new_csp = copy.deepcopy(csp)
        (new_csp.sudoku)[row][col] = val
        new_csp.update_constraints((row, col), val, 0)
        s,n = bruteforce(new_csp)
        nodes = nodes + n
        if s != -1 :
            return s,nodes
        
    return -1, nodes


        


# Convert 2d array to string representation
# sudoku => 2d array sudoku board
def sudoku2str(sudoku) :
    string = ""
    for row in sudoku :
        for x in row :
            string = string + str(x)

    return string


# Convert string to 2d array representation -- used in bruteforce()
# string => string sudoku board
def str2sudoku(string) :
    sudoku = []
    for x in range(9) :
        sudoku.append(["X", "X", "X", "X", "X", "X", "X", "X", "X"])

    for idx in range(len(string)) :
        i = math.floor(idx / 9)
        j = idx % 9
        sudoku[i][j] = string[idx]

    return sudoku


# Ensure that the given row is valid
# sudoku => sudoku board 2d array
# row => row index
def check_row(sudoku, row):
    # Set to store characters seen so far.
    nums = []

    for i in range(9):

        # If already encountered before, return false (aka not valid)
        if sudoku[row][i] in nums:
            return False

        if sudoku[row][i] != 'X':
            nums.append(sudoku[row][i])

    return True


# Ensure that the given column is valid
# sudoku => sudoku board 2d array
# col => column index
def check_column(sudoku, col):
    # Set to store characters seen so far.
    nums = []

    for i in range(9):

        # If already encountered before, return false (aka not valid)
        if sudoku[i][col] in nums:
            return False

        if sudoku[i][col] != 'X':
            nums.append(sudoku[i][col])

    return True


# Ensure that the given box is valid
# sudoku => sudoku board 2d array
# startRow => row to start at
# startCol => column to start at
def check_box(sudoku, startRow, startCol):
    # Set to store characters seen so far.
    nums = []

    # Loops through all the values in the box
    for row in range(3):
        for col in range(3):
            curr = sudoku[row + startRow][col + startCol]

            # If already encountered before, return false (aka not valid)
            if curr in nums:
                return False

            if curr != 'X':
                nums.append(curr)

    return True

# Is the sudoku valid AND has no unfilled spaces?
# sudoku => sudoku board 2d array
def is_valid_sudoku(sudoku):
    for i in range(9):
        for j in range(9):
            # If current row or current column or current 3x3 box is not valid, return false (aka not valid)
            if any("X" in row for row in sudoku) or not is_valid(sudoku, i, j):
                return False

    return True


# Is the sudoku valid based on the value at (row, col)?
# sudoku => sudoku board 2d array
# row => row index
# col => column index
def is_valid(sudoku, row, col):
    return (check_row(sudoku, row) and check_column(sudoku, col) and
            check_box(sudoku, row - row % 3, col - col % 3))



