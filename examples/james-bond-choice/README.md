# James Bond

If James Bond drinks drug d, he will have paralysis p unless has been
administered an antidote a. The MI5 daily administers Bond antidote a, unless
he is on holiday h. Suppose now that, that day, Bond was actually on a holiday
with Vesper.

## Command line

### Causal explanation

Reference and foil models are the same

We ask why Bond is poisoned.

```console
asplain examples/james-bond-choice/encoding.lp --log debug  --dynamic-tags examples/james-bond-choice/dynamic-tags.lp 0  --nexplanations 0 --query "p" --cost-encoding src/asplain/encodings/costs/program-difference.lp --model examples/james-bond-choice/model.lp --open
```

### Alternative explanation

Reference and foil models change but the graphs are the same.

We ask for an explanation where Bond is not poisoned (-p).

```console
asplain examples/james-bond-choice/encoding.lp --log debug  --dynamic-tags examples/james-bond-choice/dynamic-tags.lp 0  --nexplanations 0 --query "-p" --cost-encoding src/asplain/encodings/costs/program-difference.lp --model examples/james-bond-choice/model.lp --open
```

### Contrastive explanation

Reference and foil graphs change, since the cost defined in

We ask for an explanation where Bond is not poisoned (-p). In this case we add
an assumption in file `examples/james-bond-choice/assume-h.lp` that Bond is on
holiday.

```console
asplain examples/james-bond-choice/encoding.lp examples/james-bond-choice/assume-h.lp --log debug  --dynamic-tags examples/james-bond-choice/dynamic-tags.lp 0  --nexplanations 0 --query "-p" --cost-encoding src/asplain/encodings/costs/program-difference.lp --model examples/james-bond-choice/model.lp --open
```

This gives us two explanations: One where the rule `d.` is removed and one
where the rule `:- not h.` is removed (i.e., Bond is on holiday).

The following commend adds an addition cost to prefer explanations that remove
assumptions. Thus, the explanation where Bond was forced on holiday is
preferred and only that explanation is given.

```console
asplain examples/james-bond-choice/encoding.lp examples/james-bond-choice/assume-h.lp --log debug  --dynamic-tags examples/james-bond-choice/dynamic-tags.lp 0  --nexplanations 0 --query "-p" --cost-encoding src/asplain/encodings/costs/program-difference.lp --cost-encoding src/asplain/encodings/costs/prefer-assumptions.lp --model examples/james-bond-choice/model.lp --open
```

## UI

The clinguin UI can be ran using the following command:

```
clinguin client-server --domain-files examples/james-bond-choice/encoding.lp --ui-files src/asplain/encodings/ui.lp --custom-classes src/asplain/ui --backend ASPlainBackend --dynamic-tags examples/james-bond-choice/dynamic-tags.lp --cost-encoding src/asplain/encodings/costs/program-difference.lp src/asplain/encodings/costs/prefer-assumptions.lp
```
