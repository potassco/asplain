# Catdog

This example was used in the paper for clinguin in
[ICLP 2024](https://www.iclp24.utdallas.edu/). The aim is to place people in
tables so that no cat-people are sitting with dog-people.

```console
asplain examples/catdog/encoding.lp  --explanation-preference examples/catdog/explanation_preference.lp 0 --model examples/catdog/model.lp --query 'assign("Susana",(1,2))'
```

```console
asplain examples/catdog/encoding.lp  --explanation-preference examples/catdog/explanation_preference.lp --explanation-preference examples/catdog/input.lp 0 --query 'assign("Susana",(1,2))'
```

## Issues

Constraints are not yet handled, so we dont know how to link things.
