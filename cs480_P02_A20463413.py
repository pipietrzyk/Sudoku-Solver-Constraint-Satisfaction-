import sys
import csv
from algorithms_A20463413 import *
from csp_A20463413 import CSP
import timeit

if len(sys.argv) != 3 :
    sys.exit("ERROR: Not enough/too many/illegal input arguments.")

mode = int(sys.argv[1])
fname = sys.argv[2]

modeText = ""
if mode == 1 :
    modeText = "Brute Force Search"
elif mode == 2 :
    modeText = "CSP Back-Tracking Search"
elif mode == 3 :
    modeText = "CSP with Forward Checking and MRV Heuristics"
elif mode == 4 :
    modeText = "TEST"
else :
    sys.exit("ERROR: Not enough/too many/illegal input arguments.")

if not fname.endswith(".csv") :
    sys.exit("ERROR: Not enough/too many/illegal input arguments.")

def main() :
    print("Pietrzyk, Piotr, A20463413 solution:\nInput File: " + fname + "\nAlgorithm: " + modeText + "\n")
    
    sudoku = []
    # Read the csv file into a 2d array
    with open(fname, 'r', encoding='utf-8-sig') as csvFile :
        csvReader = csv.reader(csvFile)
        for row in csvReader :
            sudoku.append(row)

        csvFile.close()
    
    # Convert str() numbers into int()
    for row in range(9) :
        for col in range(9) :
            if sudoku[row][col] != "X" :
                sudoku[row][col] = int(sudoku[row][col])
    
    # Create a csp object and give it the sudoku board
    # From there it will build a constraint dictionary which maps coordinates in the board to possible values for that coordinate
    # It will also keep a list of which coordinate variables were known initially from reading the file
    csp = CSP(sudoku)


    print("Input Puzzle: ")
    csp.show_sudoku()

    if mode == 1 :
        csp.reset_constraints()

        timeStart = timeit.default_timer()

        csp.sudoku, nodes = bruteforce(csp)

        timeEnd = timeit.default_timer()
        elapsedTimeInSec = timeEnd - timeStart

        if csp.sudoku == -1 :
            exit("Sudoku has no solution")

        print("Number of search tree nodes generated: " + str(nodes))
        print("Search time: " + str(elapsedTimeInSec) + " seconds")
        print("Solved puzzle: ")

        csp.show_sudoku()
    elif mode == 2 :
        timeStart = timeit.default_timer()

        csp.sudoku, nodes = backtracking_search(csp)

        timeEnd = timeit.default_timer()
        elapsedTimeInSec = timeEnd - timeStart

        if csp.sudoku == -1 :
            exit("Sudoku has no solution")

        print("Number of search tree nodes generated: " + str(nodes))
        print("Search time: " + str(elapsedTimeInSec) + " seconds")
        print("Solved puzzle: ")

        csp.show_sudoku()
    elif mode == 3 :
        timeStart = timeit.default_timer()

        csp.sudoku, nodes = backtracking_search_mrv(csp)

        timeEnd = timeit.default_timer()
        elapsedTimeInSec = timeEnd - timeStart

        if csp.sudoku == -1 :
            exit("Sudoku has no solution")

        print("Number of search tree nodes generated: " + str(nodes))
        print("Search time: " + str(elapsedTimeInSec) + " seconds")
        print("Solved puzzle: ")
        
        csp.show_sudoku()
    elif mode == 4 :
        if is_valid_sudoku(csp.sudoku) :
            print("This is a valid, solved, Sudoku puzzle.")
        else :
            sys.exit("ERROR: This is NOT a solved Sudoku puzzle.")


if __name__ == "__main__" :
    main()