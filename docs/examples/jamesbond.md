---
hide:
  - navigation
---

# James Bond

<div class="grid" markdown>

The James Bond example encoding is a simple ASP encoding without any variables.
It is a causal encoding that models a scenario where James Bond is on vacation and is offered a poisoned martini.
If he is carful, he will notice the poison and avoid drinking it.
Or since he is a seasoned spy, he might have taken a profilactic antidote that prevents him from being poisoned even if he drinks the martini.

![Sudoku Example](../assets/images/jamesbond.svg){ width="350", align=right }

</div>

## Usage

Explanation:

```bash
asplain examples/james-bond/encoding.lp --nexplanations 0 --query "p" 0
```

Explanation with fixed Model:

```bash
asplain examples/james-bond/encoding.lp --nexplanations 0 --query "p" 0 --model examples/james-bond/model.lp
```

## Encodings

Base Encoding:

```clingo
--8<-- "examples/james-bond/encoding.lp"
```

Model:

```clingo
--8<-- "examples/james-bond/model.lp"
```
