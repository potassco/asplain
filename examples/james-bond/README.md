# James Bond

James Bond might drink $d$ a martini, he cannot be poisoned $p$ if he is
careful $c$. There are two possible causes of poisoning:

- by contact with a toxin $t$,
- or by drinking without taking an antidote $a$.

Bond is careful and he takes the antidote.

## Command line

There are two models, but in none of them Bond is poisoned.

Asplain can be used to explain why Bond is not poisoned by checking the changes
needed for him to be poisoned.

```console
asplain examples/james-bond/encoding.lp --nexplanations 0 --query "p"  0
```

### Fixing the model

A single model can be provided using the `--model` option.

```console
asplain examples/james-bond/encoding.lp --nexplanations 0 --query "p"  0 --model examples/james-bond/model.lp
```

### Cost function

A cost function is used to select the best explanation via optimization.

- Penalizing program changes

```console
asplain examples/james-bond/encoding.lp --nexplanations 0 --query "p"  0 --model examples/james-bond/model.lp --cost-encoding src/asplain/encodings/costs/program-difference.lp
```

- Penalizing also model difference

```console
asplain examples/james-bond/encoding.lp --nexplanations 0 --query "p"  0 --model examples/james-bond/model.lp --cost-encoding src/asplain/encodings/costs/program-difference.lp --cost-encoding src/asplain/encodings/costs/model-difference.lp
```

### LLM

To get the explanation in natural language, use the `--llm` option. Make sure
to set up the LLM integration as described in the
[README.md](../../README.md#llm-intergration).

```console
asplain examples/james-bond/encoding.lp --nexplanations 0 --query "p"  0 --model examples/james-bond/model.lp --cost-encoding src/asplain/encodings/costs/program-difference.lp --cost-encoding src/asplain/encodings/costs/model-difference.lp  --llm GPT_4O
```

### Visualization

The graph can be visualized using the `--open` option which opens the browser
with the corresponding image. Hover on the nodes to see their labels.

```console
asplain examples/james-bond/encoding.lp --nexplanations 0 --query "p"  0 --model examples/james-bond/model.lp --cost-encoding src/asplain/encodings/costs/program-difference.lp --cost-encoding src/asplain/encodings/costs/model-difference.lp --open
```

### User interface

To open the user interface, use the `clinguin` command as follows:

````console
clinguin client-server --domain-files examples/james-bond/encoding.lp --ui-files src/asplain/encodings/ui.lp --custom-classes src/asplain/ui --backend ASPlainBackend  --cost-encoding src/asplain/encodings/costs/program-difference.lp```
````
