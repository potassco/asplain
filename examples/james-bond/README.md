# James Bond

> [!Note] Read the full documentation for this example
> [here](https://potassco.org/asplain/examples/jamesbond/).

<!-- --8<-- [start:description] -->

The James Bond example encoding is a simple ASP encoding without any variables.
It is a causal encoding that models a scenario where James Bond is on vacation
and is offered a poisoned martini. If he is carful, he will notice the poison
and avoid drinking it. Or since he is a seasoned spy, he might have taken a
profilactic antidote that prevents him from being poisoned even if he drinks
the martini.

<!-- --8<-- [end:description] -->

![James Bond Example](../../docs/assets/images/jamesbond.svg)

## Usage

<!-- --8<-- [start:usage] -->

### Explanation

```bash
asplain examples/james-bond/encoding.lp --nexplanations 0 --query "p" 0
```

Explanation with __fixed model__:

```bash
asplain examples/james-bond/encoding.lp --nexplanations 0 --query "p" 0 --model examples/james-bond/model.lp
```

NL query explanation

```bash
asplain examples/james-bond/encoding.lp --nexplanations 0 --nl-query "Why is Bond not poisoned?" 0

```

### Using a cost function for selecting __preferred explanations__:

- Penalizing program changes

  ```bash
  asplain examples/james-bond/encoding.lp --nexplanations 0 --query "p"  0 --model examples/james-bond/model.lp --cost-encoding src/asplain/encodings/costs/program-difference.lp
  ```

- Penalizing also model difference

  ```bash
  asplain examples/james-bond/encoding.lp --nexplanations 0 --query "p"  0 --model examples/james-bond/model.lp --cost-encoding src/asplain/encodings/costs/program-difference.lp --cost-encoding src/asplain/encodings/costs/model-difference.lp
  ```

### Getting a __natural language__ explanation:

```bash
asplain examples/james-bond/encoding.lp --nexplanations 0 --query "p"  0 --model examples/james-bond/model.lp --cost-encoding src/asplain/encodings/costs/program-difference.lp --cost-encoding src/asplain/encodings/costs/model-difference.lp  --llm GPT_4O
```

### Using the __interactive__ explanation interface:

````bash
clinguin client-server --domain-files examples/james-bond/encoding.lp --ui-files src/asplain/encodings/ui.lp --custom-classes src/asplain/ui --backend ASPlainBackend  --cost-encoding src/asplain/encodings/costs/program-difference.lp```
````

<!-- --8<-- [end:usage] -->
