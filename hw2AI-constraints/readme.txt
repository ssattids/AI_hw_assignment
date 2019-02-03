Run p2.py without any arguments to see the results for the sudoku puzzles listed in the same directory using different techniques. (a puzzle file must contain 'puz' and be a .txt file)

A puzzle looks like the following:
7 8 1 6 - 2 9 - 5
9 - 2 7 1 - - - -
- - 6 8 - - - 1 2
2 - - 3 - - 8 5 1
- 7 3 5 - - - - 4
- - 8 - - 9 3 6 -
1 9 - - - 7 - 8 -
8 6 7 - - 3 4 - 9
- - 5 - - - 1 - -


It solves each puzzle 3 times by using the following techniques:
1) plain backtracking
2) MRV and backstracking
3) waterfall (methods include hidden pairs, AC-3, intersection pairs)


For each of the above techniques above and for each puzzle it: 
1) prints out the file name of the puzzle it is solving
2) solves the puzzles and prints the solved puzzle
3) prints out the number of guesses it used for a puzzle