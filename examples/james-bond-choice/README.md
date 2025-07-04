# James Bond

If James Bond drinks drug d, he will have paralysis p unless has been
administered an antidote a. The MI5 daily administers Bond antidote a, unless
he is on holiday h. Suppose now that, that day, Bond was actually on a holiday
with Vesper.

## Command line

The command line is used my passing the model where James was poisoned since he
was drudged and was on vacation. We also include the query `-p` which means
that we want `p` to be false (James not to be poisoned)

```console
asplain examples/james-bond-choice/encoding.lp  --explanation-preference examples/james-bond-choice/explanation_preference.lp 0 --query "p"
```

The computed graphs of the real model (provided) the hypothetical model, as
well as the graph contrasting both models.

=== "Explanation 1" ![James Bond](./out/james-bond-1.png) Shows that `h` had to
be removed (crossed out) for the antidote to have been provided so that James
is not poisoned.

=== "Explanation 2" ![James Bond](./out/james-bond-2.png) Shows that `d` had to
be removed (crossed out) for James not to be poisoned
