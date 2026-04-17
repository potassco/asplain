
COMMAND="asplain encoding.lp --stats -q"

INSTANCES=(
    "instance9x9.lp"
    "instance4x4.lp"
)
COMMANDS=(
    "$COMMAND --query 'sudoku(2,2,2)' --prune CHANGES --prune ORPHANS"
    "$COMMAND --query 'sudoku(2,2,2)' --prune CHANGES --prune ORPHANS --cost-encoding ../../src/asplain/encodings/costs/model-difference.lp"
    "$COMMAND --query 'sudoku(2,2,2)'"
    "$COMMAND --query 'sudoku(2,2,2)' --cost-encoding ../../src/asplain/encodings/costs/model-difference.lp"
)

OUTFILE="results.txt"
rm -f "$OUTFILE"
for instance in "${INSTANCES[@]}"; do
    for comand in "${COMMANDS[@]}"; do
        echo "------ $comand $instance ------" >> "$OUTFILE"
        eval $comand $instance "| grep "Asplain" -A 19" >> "$OUTFILE"
    done
done
