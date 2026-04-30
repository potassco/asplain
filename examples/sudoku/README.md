# Sudoku

Classic encoding of the sudoku puzzle in a 4x4 format. The problem instance
looks the following way:

|     |     |     |     |
| :-: | :-: | :-: | :-: |
|  1  |     |     |     |
|     |     |     |  2  |
|     |  1  |     |     |
|     |     |  2  |     |

For this configuration of the problem there are 4 possible model solutions, one
being provided in the file `model.lp`.

## Command line

The command line is used for passing a model solution to the given problem
problem. We also include the query `sudoku(3,2,1)` for which we want to know
why it is in the solution.

```console
asplain examples/sudoku/encoding.lp examples/sudoku/instance4x4.lp --log debug --query "sudoku(3,2,1)"  --prune PATHS
```

To get a contrastive explanation, we can ask for a query that is not in the
solution, for example `sudoku(2,2,2)`.

```console
asplain examples/sudoku/encoding.lp examples/sudoku/instance4x4.lp --log debug --query "sudoku(2,2,2)"  --prune PATHS
```

### Further pruning and optimization methods

Obtain an explanation for the same query, but with further pruning methods and
cost encoding for model difference.

```console
asplain encoding.lp --query 'sudoku(2,2,2)' --prune CHANGES --prune ORPHANS --cost-encoding ../../src/asplain/encodings/costs/model-difference.lp instance4x4.lp
```

```console
asplain encoding.lp --query 'sudoku(2,2,2)' --prune CHANGES --prune ORPHANS --cost-encoding ../../src/asplain/encodings/costs/model-difference.lp instance9x9.lp
```
