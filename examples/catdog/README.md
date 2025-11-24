# Catdog

This example was used in the paper for clinguin in
[ICLP 2024](https://www.iclp24.utdallas.edu/). The aim is to place people in
tables so that no cat-people are sitting with dog-people.

```console
asplain examples/catdog/encoding_no_bounds.lp  --explanation-preference examples/catdog/explanation_preference_assumption.lp 0 --model examples/catdog/model.lp --query 'assign("Susana",(1,2))' --assumptions 'assign("Torsten",(1,1))'
```

## Issues

Constraints are not yet handled, so we dont know how to link things.
