# -*- coding: utf-8 -*-
from __future__ import print_function
import os

class Sudoku_Tile (object):
    def __init__ (self, domain, value):
        self.value = value
        self.domain = domain
        self.pos = (0,0)
        self.constraints = []

    def set_position(self, pos):
        self.pos = pos
        # Add row constraints
        for i in range(9):
            self.col = self.pos[1]
            self.const = (i, self.col)
            if self.const != self.pos:
                self.constraints.append(self.const)
        # Add column constraints
        for j in range(9):
            self.row = self.pos[0]
            self.const = (self.row, j)
            if self.const != self.pos:
                self.constraints.append(self.const)
        # Add block constraints
        self.row_block_start = (self.row // 3) * 3
        self.col_block_start = (self.col // 3) * 3
        for i in range(self.row_block_start, self.row_block_start+3):
            for j in range(self.col_block_start, self.col_block_start+3):
                self.const = (i, j)
                if self.const != self.pos and self.const not in self.constraints:
                    self.constraints.append(self.const)

    def __str__(self):
        lst = "["
        for val in self.domain:
            lst = lst + str(val) + ", "
        return lst[:-2] + "]"

#open the sudoku file and return it as a 2D np array object
#conver chars to number, convert dashes to 0
def open_sudoku(filename):
    fh = open(filename, "r")
    a = fh.readlines()    
    #print(a[0])
    
    all_rows = []
    for i in range(len(a)):
        row = []
        for j in range(0, len(a[i]), 2):
            if (a[i][j] == '-'):
                row.append(Sudoku_Tile([1,2,3,4,5,6,7,8,9], 0))
            else:
                row.append(Sudoku_Tile([int(a[i][j])], int(a[i][j])))
        all_rows.append(row)
    
    for i in range(len(all_rows)):
        for j in range(len(all_rows)):
            all_rows[i][j].set_position((i, j))

    # update_domain_all(all_rows)
    # AC3_algorithm(all_rows)
    
    return all_rows

#update the domain of all the variables based on each position of the board
def update_domain_all(puzzle):
    for i in range(len(puzzle)):
        for j in range(len(puzzle)):
            update_domain_atpos(puzzle, (i, j))

#update the domain of all variables based on one position
def update_domain_atpos(puzzle, pos):
    row = pos[0]
    col = pos[1]
    value = puzzle[row][col].value
    #update all domains in the entire row
    for i in range(len(puzzle)):
        #the same location as puzzle, we want to skip this
        if (puzzle[row][i] == puzzle[row][col]):
            pass
        elif (value in puzzle[row][i].domain):
            puzzle[row][i].domain.remove(value)
    #update all domain in the entire col
    for i in range(len(puzzle)):
        if (puzzle[i][col] == puzzle[row][col]):
            pass
        elif (value in puzzle[i][col].domain):
            puzzle[i][col].domain.remove(value)
    #update all domains in the entire block
    row_block_start = (row // 3) * 3
    col_block_start = (col // 3) * 3
    for i in range(row_block_start, row_block_start+3):
        for j in range(col_block_start, col_block_start+3):
            if (puzzle[i][j] == puzzle[row][col]):
                pass
            elif (value in puzzle[i][j].domain):
                puzzle[i][j].domain.remove(value)
                
def AC3_algorithm(puzzle):
    #build the entire queue
    queue = []
    for i in range(len(puzzle)):
        for j in range(len(puzzle[i])):
            partial_queue = puzzle[i][j].constraints
            for k in range(len(partial_queue)):
                double_tuple = ((i,j), partial_queue[k])
                queue.append(double_tuple)

    while (len(queue) != 0):
        Xi_Xj = queue.pop(0)
        Xi = Xi_Xj[0]
        Xj = Xi_Xj[1]
        if (revise(puzzle, Xi, Xj)):
            Xi_obj = puzzle[Xi[0]][Xi[1]]
            if (len(Xi_obj.domain) == 0):
                return False
            for constraint in Xi_obj.constraints:
                constraint_tuple = (Xi,constraint)
                if constraint_tuple not in queue:
                    queue.append(constraint_tuple)
    return True
            
def revise (puzzle, Xi, Xj):
    Xi_obj = puzzle[Xi[0]][Xi[1]]
    Xj_obj = puzzle[Xj[0]][Xj[1]]
    if (len(Xj_obj.domain) > 1):
        return False
    elif (len(Xj_obj.domain) == 1):
        if Xj_obj.value in Xi_obj.domain:
            Xi_obj.domain.remove(Xj_obj.value)
            return True
        return False
    else:
        raise ValueError("Domain can not be less than one")


#check if the assignnment is complete
def complete_assignment_check(puzzle):
    for i in range(len(puzzle)):
        for j in range(len(puzzle[i])):
            tile = puzzle[i][j]
            if (tile.value == 0): #there is no assignment for this yet
                return False
    return True

#check if the given assignment is legal
#note the assignment is not done in this function, just checked if valid
def check_legal_assignment (puzzle, value, pos):
    row = pos[0]
    col = pos[1]
    #check the entire row
    for i in range(len(puzzle)):
        if (value == puzzle[row][i].value):
            return False
    #check the entire column
    for i in range(len(puzzle)):
        if (value == puzzle[i][col].value):
            return False
    #check the entire block
    row_block_start = (row // 3) * 3
    col_block_start = (col // 3) * 3
    for i in range(row_block_start, row_block_start+3):
        for j in range(col_block_start, col_block_start+3):
            if (value == puzzle[i][j].value):
                return False
      
    return True
        
#print the actual puzzle
def print_puzzle(puzzle): 
    for i in range(len(puzzle)):
        for j in range(len(puzzle[i])):
            print(puzzle[i][j].value, end=',')
        print()


def select_unassigned_variable_mrv(puzzle):
    # Using MRV
    mcv = (-1, -1)
    mcv_size = float("inf")
    for row in range(len(puzzle)):
        for col in range(len(puzzle[row])):
            domain_size = len(puzzle[row][col].domain)
            if puzzle[row][col].value == 0 and domain_size < mcv_size:
                mcv = (row, col)
                mcv_size = domain_size
    return mcv

def select_unassigned_variable_static(puzzle):
    for row in range(len(puzzle)):
        for col in range(len(puzzle[row])):
            if puzzle[row][col].value == 0:
                return (row, col)
    return (-1, -1)

def select_variable_mrv_no_domain_update(puzzle):
    mcv = (-1, -1)
    mcv_size = float("inf")
    for row in range(len(puzzle)):
        for col in range(len(puzzle[row])):
            domain_size = check_available_values(puzzle, row, col)
            if puzzle[row][col].value == 0 and domain_size < mcv_size:
                mcv = (row, col)
                mcv_size = domain_size
    return mcv

def check_available_values(puzzle, row, col):
    all_values = [1,2,3,4,5,6,7,8,9]
    # Check rows
    for i in range(9):
        current_val = puzzle[i][col].value
        if current_val != 0 and current_val in all_values:
            all_values.remove(current_val)
    # Check cols
    for j in range(9):
        current_val = puzzle[row][j].value
        if current_val != 0 and current_val in all_values:
            all_values.remove(current_val)
    # Check block
    row_block_start = (row // 3) * 3
    col_block_start = (col // 3) * 3
    for i in range(row_block_start, row_block_start+3):
        for j in range(col_block_start, col_block_start+3):
            current_val = puzzle[i][j].value
            if current_val != 0 and current_val in all_values:
                all_values.remove(current_val)

    return len(all_values)

def order_domain_variable(puzzle, tile_pos):
    return puzzle[tile_pos[0]][tile_pos[1]].domain

def add_assignment(puzzle, position, val):
    row = position[0]
    col = position[1]
    puzzle[row][col].value = val

def remove_assignment(puzzle, position):
    add_assignment(puzzle, position, 0)

def naive_recursive_backtracking(puzzle, guesses, select_unassigned_variable):
    if complete_assignment_check(puzzle):
        return (True, guesses)
    tile_pos = select_unassigned_variable(puzzle)
    # Check if there was an error selecting next variable
    if tile_pos[0] == -1:
        raise ValueError("select_unassigned_variable returned (-1, -1)")
    domain = order_domain_variable(puzzle, tile_pos)
    new_guesses = guesses + len(domain) - 1
    for val in domain:
        if (check_legal_assignment(puzzle, val, tile_pos)):
            add_assignment(puzzle, tile_pos, val)
            complete, new_guesses = naive_recursive_backtracking(puzzle, new_guesses, select_unassigned_variable)
            if complete:
                return (True, new_guesses)
            remove_assignment(puzzle, tile_pos)
    return (False, new_guesses)

def recursive_backtracking(puzzle, guesses, select_unassigned_variable, inference):
    if complete_assignment_check(puzzle):
        return (True, guesses)
    tile_pos = select_unassigned_variable(puzzle)
    # Check if there was an error selecting next variable
    if tile_pos[0] == -1:
        raise ValueError("select_unassigned_variable returned (-1, -1)")
    domain = order_domain_variable(puzzle, tile_pos)
    new_guesses = guesses + len(domain) - 1
    for val in domain:
        if (check_legal_assignment(puzzle, val, tile_pos)):
            add_assignment(puzzle, tile_pos, val)
            all_domains = backup_domains(puzzle)
            puzzle[tile_pos[0]][tile_pos[1]].domain = [val]
            inferences = inference(puzzle)
            if inferences:
                complete, new_guesses = recursive_backtracking(puzzle, new_guesses, select_unassigned_variable, inference)
                if complete:
                    return (True, new_guesses)
            remove_assignment(puzzle, tile_pos)
            restore_domains(puzzle, all_domains)
    return (False, new_guesses)


def backup_domains(puzzle):
    all_domains = []
    for row in range(len(puzzle)):
        for col in range(len(puzzle)):
            temp = puzzle[row][col].domain[:]
            all_domains.append(temp)
    return all_domains

def restore_domains(puzzle, all_domains):
    for row in range(len(puzzle)):
        for col in range(len(puzzle)):
            puzzle[row][col].domain = all_domains[row * len(puzzle) + col]


def get_all_domains_size(puzzle):
    all_domains_size = 0
    for row in range(9):
        for col in range(9):
            all_domains_size += len(puzzle[row][col].domain)
    return all_domains_size

def waterfall(puzzle):
    current_size = float("inf")
    while get_all_domains_size(puzzle) < current_size:
        current_size = get_all_domains_size(puzzle)
        hidden_pairs(puzzle)
        if not intersection_removal(puzzle):
            return False
        if not AC3_algorithm(puzzle):
            return False
        
    return True

def intersection_removal(puzzle):
    return intersection_removal_rows(puzzle) and intersection_removal_cols(puzzle)

def intersection_removal_rows(puzzle):
    for col in range(0, 9, 3):
        for row in range(9):
            row_block_values = get_row_block_values(puzzle, row, col)
            other_row_block_values = get_other_row_block_values(puzzle, row, col)
            row_block_values = row_block_values - other_row_block_values
            # If intersection removal is possible
            if len(row_block_values) > 0:
                cols_to_check = set([0,1,2,3,4,5,6,7,8])
                cols_to_remove = set([col, col+1, col+2])
                cols_to_check = list(cols_to_check - cols_to_remove)
                for j in cols_to_check:
                    puzzle[row][j].domain = list(set(puzzle[row][j].domain[:]) - row_block_values)
                    if len(puzzle[row][j].domain) == 0:
                        return False
    return True

def intersection_removal_cols(puzzle):
    for row in range(0, 9, 3):
        for col in range(9):
            col_block_values = get_col_block_values(puzzle, row, col)
            other_col_block_values = get_other_col_block_values(puzzle, row, col)
            col_block_values = col_block_values - other_col_block_values
            # If intersection removal is possible
            if len(col_block_values) > 0:
                rows_to_check = set([0,1,2,3,4,5,6,7,8])
                rows_to_remove = set([row, row+1, row+2])
                rows_to_check = list(rows_to_check - rows_to_remove)
                for i in rows_to_check:
                    puzzle[i][col].domain = list(set(puzzle[i][col].domain[:]) - col_block_values)
                    if len(puzzle[i][col].domain) == 0:
                        return False
    return True

def get_row_block_values(puzzle, row, col):
    row_block_values = []
    for j in range(col, col + 3):
        if puzzle[row][j].value != 0:
            temp_domain = puzzle[row][j].domain[:]
            row_block_values = row_block_values + temp_domain
    return set(row_block_values)

def get_col_block_values(puzzle, row, col):
    col_block_values = []
    for i in range(row, row + 3):
        if puzzle[i][col].value != 0:
            temp_domain = puzzle[i][col].domain[:]
            col_block_values = col_block_values + temp_domain
    return set(col_block_values)

def get_other_row_block_values(puzzle, row, col):
    other_row_block_values = []
    rows = [0,1,2]
    increment = row // 3
    increment *= 3
    rows = [x+increment for x in rows]
    rows = list(set(rows) - set([row]))
    for i in rows:
        other_row_block_values = other_row_block_values + list(get_row_block_values(puzzle, i, col))
    return set(other_row_block_values)

def get_other_col_block_values(puzzle, row, col):
    other_col_block_values = []
    cols = [0,1,2]
    increment = col // 3
    increment *= 3
    cols = [x+increment for x in cols]
    cols = list(set(cols) - set([col]))
    for j in cols:
        other_col_block_values = other_col_block_values + list(get_col_block_values(puzzle, row, j))
    return set(other_col_block_values)

def hidden_pairs_update_domain(puzzle, all_numbers, positions):
    #count how many times the each number is in each domain
    counts = []
    for i in range(1,10):
        counts.append(all_numbers.count(i))
    #if the number of times a variable appears is twice and they are 2 variables
    #then we have a possible hidden pair
    if (counts.count(2) == 2):
        #indices of the numbers 
        indices = [i for i in range(len(counts)) if counts[i] == 2]
        #the numbers which have a count of 2
        num_occur_twice = [x+1 for x in indices]
        n1 = num_occur_twice[0]
        n2 = num_occur_twice[1]
        positions_1 = [positions[i] for i in range(len(all_numbers)) if all_numbers[i] == n1]
        positions_2 = [positions[i] for i in range(len(all_numbers)) if all_numbers[i] == n2]
        #they were both found in the same position
        if (set(positions_1) == set(positions_2)):
            pos_1 = positions_1[0]
            pos_2 = positions_1[1]
#            print("suzzess!!")
#            print(pos_1)
#            print(pos_2)
#            print(n1)
#            print(n2)
            puzzle[pos_1[0]][pos_1[1]].domain = [n1, n2]
            puzzle[pos_2[0]][pos_2[1]].domain = [n1, n2]
    


def hidden_pairs(puzzle):
    #indices to access each block
    rows = [0, 0, 0, 3, 3, 3, 6, 6, 6]
    cols = [0, 3, 6, 0, 3, 6, 0, 3, 6]
    #check all the blocks
    for a in range(len(rows)):
        all_numbers = []
        positions = []
        row_block_start = (rows[a] // 3) * 3
        col_block_start = (cols[a] // 3) * 3
        for i in range(row_block_start, row_block_start+3):
            for j in range(col_block_start, col_block_start+3):
                all_numbers = all_numbers + puzzle[i][j].domain
                positions = positions + [(i,j)]*len(puzzle[i][j].domain)
        
        hidden_pairs_update_domain(puzzle, all_numbers, positions)
    
#    #check all the cols
#    for i in range(len(puzzle)):
#        all_numbers = []
#        positions = []  
#        for j in range(len(puzzle)):
#            all_numbers = all_numbers + puzzle[i][j].domain
#            positions = positions + [(i,j)]*len(puzzle[i][j].domain)
#        hidden_pairs_update_domain(puzzle, all_numbers, positions)
#            
#    #check all the rows
#    for i in range(len(puzzle)):
#        all_numbers = []
#        positions = []  
#        for j in range(len(puzzle[i])):
#            all_numbers = all_numbers + puzzle[j][i].domain
#            positions = positions + [(j,i)]*len(puzzle[j][i].domain)
#        hidden_pairs_update_domain(puzzle, all_numbers, positions)
#            
    return True


#######################################################################################
#           This is for question 2.3
#######################################################################################
# file = "puz-082.txt"
# sudokupuzzle = open_sudoku(file)
# complete, guesses = naive_recursive_backtracking(sudokupuzzle, 0, select_unassigned_variable_static)
# print_puzzle(sudokupuzzle)
# print(guesses)
# sudokupuzzle = open_sudoku(file)
# complete, guesses = naive_recursive_backtracking(sudokupuzzle, 0, select_variable_mrv_no_domain_update)
# print_puzzle(sudokupuzzle)
# print(guesses)
#######################################################################################

#######################################################################################
#           This is AC3 alone working
#######################################################################################
# file = "puz-010.txt"
# sudokupuzzle = open_sudoku(file)
# complete, guesses = naive_recursive_backtracking(sudokupuzzle, 0, select_unassigned_variable_static)
# print_puzzle(sudokupuzzle)
# print(guesses)
# sudokupuzzle = open_sudoku(file)
# AC3_algorithm(sudokupuzzle)
# complete, guesses = recursive_backtracking(sudokupuzzle, 0, select_unassigned_variable_mrv, AC3_algorithm)
# print_puzzle(sudokupuzzle)
# print(guesses)
#######################################################################################


#######################################################################################
#           This is Waterfall alone working
#######################################################################################
#file = "puz-082.txt"
#sudokupuzzle = open_sudoku(file)
#AC3_algorithm(sudokupuzzle)
##hidden_pairs(sudokupuzzle)
#print_puzzle(sudokupuzzle)
#complete, guesses = recursive_backtracking(sudokupuzzle, 0, select_unassigned_variable_mrv, AC3_algorithm)
#print_puzzle(sudokupuzzle)
#print(guesses)
#sudokupuzzle = open_sudoku(file)
#AC3_algorithm(sudokupuzzle)
#complete, guesses = recursive_backtracking(sudokupuzzle, 0, select_unassigned_variable_mrv, waterfall)
#print_puzzle(sudokupuzzle)
#print(guesses)
########################################################################################


dir_path = os.getcwd()
file_names = []
for root, dirs, files in os.walk(dir_path):
    for f in files:
        if ('puz-' in f):
            file_names.append(f)
file_names.sort()
print(file_names)


print("---------------------------------------------------------------------")
print("+++++++++++++++++++++++++++++Q2.2 & Q2.3+++++++++++++++++++++++++++++")
print("---------------------------------------------------------------------")
print("Printing puzzle and guesses for only recursive backtracking algorithm")
guesses_stat_static = []
for file in file_names:
    print(file)
    sudokupuzzle = open_sudoku(file)
    complete, guesses = naive_recursive_backtracking(sudokupuzzle, 0, select_unassigned_variable_static)
    print_puzzle(sudokupuzzle)
    print(guesses)
    guesses_stat_static.append(guesses)
print("Number of guesses for each puzzle using only recursive backtracking algorithm")
print(guesses_stat_static)
print("---------------------------------------------------------------------")

print("Printing puzzle and guesses using recursive backtracking algorithm and MRV")
guesses_stat_static_mrv = []
for file in file_names:
    print(file)
    sudokupuzzle = open_sudoku(file)
    complete, guesses = naive_recursive_backtracking(sudokupuzzle, 0, select_variable_mrv_no_domain_update)
    print_puzzle(sudokupuzzle)
    print(guesses)
    guesses_stat_static_mrv.append(guesses)
print("Number of guesses for each puzzle using recursive backtracking algorithm and MRV")
print(guesses_stat_static_mrv)
print("---------------------------------------------------------------------")


print("---------------------------------------------------------------------")
print("+++++++++++++++++++++++++++++++++Q2.4++++++++++++++++++++++++++++++++")
print("---------------------------------------------------------------------")
print("Printing puzzle and guesses using waterfall methods")
guesses_stat_waterfall = []
for file in file_names:
    print(file)
    sudokupuzzle = open_sudoku(file)
    AC3_algorithm(sudokupuzzle)
    complete, guesses = recursive_backtracking(sudokupuzzle, 0, select_unassigned_variable_mrv, waterfall)
    print_puzzle(sudokupuzzle)
    print(guesses)
    guesses_stat_waterfall.append(guesses)
print("Number of guesses for each puzzle using waterfall methods")
print(guesses_stat_waterfall)
print("---------------------------------------------------------------------")
