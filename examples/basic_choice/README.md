# Basic choice

Example used in research with Mario for 1-PUS

```
asplain examples/basic_choice/encoding.lp --explanation-preference examples/basic_choice/abd_preference.lp --model examples/basic_choice/model.lp --query "p(a)"
```

## Issues

Constraints are not handled so the implication only shows the implication from
s(a,b) to p(a).
