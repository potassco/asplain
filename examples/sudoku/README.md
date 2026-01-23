# Sudoku

Classic encoding of the sudoku puzzle in a 4x4 format. The problem instance looks the following way:

|||||
|:-:|:-:|:-:|:-:|
|1||||
||||2|
||1|||
|||2||

For this configuration of the problem there are 4 possible model solutions, one being provided in the file `model.lp`.

## Command line

The command line is used for passing a model solution to the given problem problem. We also include the query `sudoku(3,2,1)` for which we want to know why it is in the solution.

````console
asplain examples/sudoku/encoding.lp --model examples/sudoku/model.lp --dynamic-tags examples/sudoku/dynamic-tags.lp 1 --log info --query "sudoku(3,2,1)"
````
