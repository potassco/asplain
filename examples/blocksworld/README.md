

### Query: "Why not solvable in 2 steps" (FAIL)

```
--query="last(2) h(on(2),1,2) h(on(1),4,2) h(on(3),table,2) h(on(4),table,2)"
```

For encoding this natural language question as a query just `last(2)` will be neccesary, as that already enforces the rest of the atoms to be true.
However, by putting them in the query we force them to be in the graph.

```
asplain dom01.lp encoding.lp effect4.lp --explanation-preference explanation-preference.lp --log info --query="last(2) h(on(2),1,2) h(on(1),4,2) h(on(3),table,2) h(on(4),table,2)" --predicates predicates.txt 2>info.txt --llm --prune
```

By reading the graph we can conclude that we need to change the initial arrangement of the blocks for fulfilling the query.
Only by reading the abduced atoms for the initial setting, should be enough for giving a valid answer.
However, the llm focus too much in the connections learned from the encoding, which btw create a too large graph.

#### Model Feeding + Custom reachables (possible solution)


