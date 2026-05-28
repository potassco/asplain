---
hide:
  - navigation
---

# Cat & Dog Seating

<div class="grid" markdown>

The cat & dog seating example encoding is an assignment ASP encoding with variables.
It models a scenario where there is an event where people are seated on tables depending on their preferences in pets.
Dog people are only allowed to sit with other dog people, and cat people are only allowed to sit with other cat people.
The goal is to seat all people while adhering to their pet preferences, while optionally optimizing for using the fewest number of tables possible.

![Sudoku Example](../assets/images/catdog.svg){ width="300", align=right }

</div>

## Usage

Explanation:

```bash
asplain examples/cat-dog/encoding.lp examples/cat-dog/instance.lp 1 --open --query='assign("Susana",(1,2))'
```

Explanation with optimization:

```bash
MISSING COMMAND
```

## Encodings

Base Encoding:

```clingo
--8<-- "examples/cat-dog/encoding.lp"
```

Instance:

```clingo
--8<-- "examples/cat-dog/instance.lp"
```
