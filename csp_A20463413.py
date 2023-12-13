# A class to represent the constraint satisfaction problem
# sudoku => 2d array which stores the sudoku board
# domain => [1..9] for each variable (initially)
# constraints => a dictionary that maps coordinate variables to integers --- { (row, col) : val }
# known => list of all coordinate variables initially known
class CSP :
    def __init__(self, sudoku):
        self.sudoku = sudoku
        self.domain = [1,2,3,4,5,6,7,8,9]
        self.constraints = init_constraints(self.sudoku, self.domain, {})
        self.known = init_known(self.sudoku, [])


    # Given a sudoku board, this function makes sure that all of the initial known values are still in place
    # This is most useful for the bruteforce() function
    def compare_known(self, sudoku) :
        for var in self.known :
            if not ( sudoku[var[0]][var[1]] == self.sudoku[var[0]][var[1]] ) :
                return False
            
        return True
    

    # Update constraints (to either remove or add constraints) in the row, column, and box that correlates to var
    # var => (row, col) index into the sudoku
    # val => the value that should go at the location stored in var
    # type => 0 = add constraints / 1 = remove constraints
    def update_constraints(self, var, val, type) :
        if type == 0 : # val should be an int here
            self.constraints[var] = [val]
            self.constraints = remove_from_row(self.constraints, var)
            self.constraints = remove_from_col(self.constraints, var)
            self.constraints = remove_from_box(self.constraints, var)
        elif type == 1 : # val should be a list here
            self.constraints[var] = val
            self.constraints = add2row(self.constraints, var)
            self.constraints = add2col(self.constraints, var)
            self.constraints = add2box(self.constraints, var)


    def reset_constraints(self) :
        c = {}
        for row in range(9):
            for col in range(9):
                if (self.sudoku)[row][col] == "X" :
                    c[(row, col)] = [1,2,3,4,5,6,7,8,9]
                else :
                    c[(row, col)] = [(self.sudoku)[row][col]]
        self.constraints = c


    #  X 6 X | 2 X 4 | X 5 X
    #  4 7 X | X 6 X | X 8 3
    #  X X 5 | X 7 X | 1 X X
    #  ------+-------+------
    #  9 X X | 1 X 3 | X X 2
    #  X 1 2 | X X X | 3 4 X
    #  6 X X | 7 X 9 | X X 8
    #  ------+-------+------
    #  X X 6 | X 8 X | 7 X X
    #  1 4 X | X 9 X | X 2 5
    #  X 8 X | 3 X 5 | X 9 X

    # Prints out the sudoku board in the format shown above
    def show_sudoku(self) :
        for row in range(9) :
            if row == 3 or row == 6 :
                print("------+-------+------")
            for col in range(9) :
                if col == 3 or col == 6 :
                    print("|", end = " ")
                print(str(self.sudoku[row][col]), end = " ")
            print("")
        print("\n")






# ---- The functions below are not part of the class ---- #

# Initializes self.known when a CSP object is created
def init_known(sudoku, known) :
    for row in range(9) :
        for col in range(9) :
            if sudoku[row][col] != "X" :
                known.append((row, col))

    return known
    

# Initializes self.constraint when a CSP object is created
def init_constraints(sudoku, domain, constraints):
        # Initialize the constraints dictionary with [1..9] for each (row, col) variable initially
        for row in range(9):
            for col in range(9):
                constraints[(row, col)] = domain.copy()

        # Update the constraint domain for each variable based on existing filled cells
        for row in range(9):
            for col in range(9):
                if sudoku[row][col] != "X":
                    constraints[(row, col)] = [sudoku[row][col]]
                    constraints = remove_from_row(constraints, (row,col))
                    constraints = remove_from_col(constraints, (row,col))
                    constraints = remove_from_box(constraints, (row,col))

        return constraints


# Remove the value located at var from the constraint lists in its row
# constraints => constraints dictionary
# var => (row, col) index
def remove_from_row(constraints, var):
    val = constraints[var] # Get the value located at var
    row = var[0] # Get the row index

    for i in range(9) :
        if len(constraints[(row, i)]) > 1  : # len(constraints[(row,i)]) = 1 means that value is filled and can't be removed
            for x in val :
                # Remove val from the constraint lists
                if x in constraints[(row, i)] :
                    c: list = constraints[(row, i)]
                    c.remove(x)
                    constraints[(row, i)] = c

    return constraints


# Remove the value located at var from the constraint lists in its column
# constraints => constraints dictionary
# var => (row, col) index
def remove_from_col(constraints, var):
    val = constraints[var] # Get the value located at var
    col = var[1] # Get the column index

    for i in range(9):
        if len(constraints[(i, col)]) > 1 : # len(constraints[(row,i)]) = 1 means that value is filled and can't be removed
            for x in val :
                # Remove val from the constraint lists
                if x in constraints[(i, col)] :
                    c: list = constraints[(i, col)]
                    c.remove(x)
                    constraints[(i, col)] = c

    return constraints


# Remove the value located at var from the constraint lists in its box
# constraints => constraints dictionary
# var => (row, col) index
def remove_from_box(constraints, var):
    val = constraints[var] # Get the value located at var

    # The coordinates of the bottom-right of each box
    boxes = [(2,2), (2,5), (2,8), (5,2), (5,5), (5,8), (8,2), (8,5), (8,8)]

    # Determines which box the given coordinates are located in
    i = -1
    for box in boxes :
        i = i + 1
        if var[0] <= box[0] and var[1] <= box[1] :
            break

    # Loops through the values in the box and fix the constraints
    for row in range(boxes[i][0] - 2, boxes[i][0] + 1) :
        for col in range(boxes[i][1] - 2, boxes[i][1] + 1) :
            if len(constraints[(row, col)]) > 1 : # len(constraints[(row,i)]) = 1 means that value is filled and can't be removed
                for x in val :
                    # Remove val from the constraint lists
                    if x in constraints[(row, col)] :
                        c: list = constraints[(row, col)]
                        c.remove(x)
                        constraints[(row, col)] = c

    return constraints


# Add the value(s) located at var to the constraint lists in its row
# constraints => constraints dictionary
# var => (row, col) index
def add2row(constraints, var) :
    val = constraints[var] # Get the value located at var
    row = var[0] # Get the row index

    for i in range(9) :
        if len(constraints[(row, i)]) > 1 : # TODO: CHECK TO MAKE SURE THE LOCATION ISN'T VAR INSTEAD
            for x in val :
                # Add the value(s) in val to the constraint lists
                if x not in constraints[(row, i)] :
                    constraints[(row, i)].append(x)     
            constraints[(row, i)].sort()

    return constraints


# Add the value(s) located at var to the constraint lists in its column
# constraints => constraints dictionary
# var => (row, col) index
def add2col(constraints, var) :
    val = constraints[var] # Get the value located at var
    col = var[1] # Get the column index

    for i in range(9) :
        if len(constraints[(i, col)]) > 1 : # TODO: CHECK TO MAKE SURE THE LOCATION ISN'T VAR INSTEAD
            for x in val :
                # Add the value(s) in val to the constraint lists
                if x not in constraints[(i, col)] :
                    constraints[(i, col)].append(x)     
            constraints[(i, col)].sort()

    return constraints


# Add the value(s) located at var to the constraint lists in its box
# constraints => constraints dictionary
# var => (row, col) index
def add2box(constraints, var) :
    val = constraints[var]

    # The coordinates of the bottom-right of each box
    boxes = [(2,2), (2,5), (2,8), (5,2), (5,5), (5,8), (8,2), (8,5), (8,8)]

    # Determines which box the given coordinates are located in
    i = -1
    for box in boxes :
        i = i + 1
        if var[0] <= box[0] and var[1] <= box[1] :
            break

    # Loop through the values in the box and fix the constraints
    for row in range(boxes[i][0] - 2, boxes[i][0] + 1) :
        for col in range(boxes[i][1] - 2, boxes[i][1] + 1) :
            if len(constraints[(row, col)]) > 1 : # TODO: CHECK TO MAKE SURE THE LOCATION ISN'T VAR INSTEAD
                for x in val :
                    # Add the value(s) in val to the constraint lists
                    if x not in constraints[(row, col)] :
                        constraints[(row, col)].append(x)     
                constraints[(row, col)].sort()

    return constraints