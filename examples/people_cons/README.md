# People constraints

An example using variables and constraints about people sitting and standing
depending on their age.

```
asplain examples/people_cons/encoding.lp  --explanation-preference examples/people_cons/explanation-preference.lp 0  --query "stand(anna)" --log info
```

Ana can't be standing because she is over age, she would have to not be 70 to
be standing instead of sitting.
