---
hide:
  - navigation
---

# Don't Drive Drunk

<div class="grid" markdown>

The don't drive drunk example encoding is a simple ASP encoding with variables.
It models a scenario where there are two people, Gabriel and Clare.
If any of the two people are drunk and also drives they get sentenced and have to go to prison.

![Sudoku Example](../assets/images/dontdrivedrunk.svg){ width="400", align=right }

</div>

## Usage

Explanation:

```bash
asplain examples/dont_drive_drunk/encoding.lp 1 --log info --query "sentence(gabriel,innocent)"
```

## Encodings

Base Encoding:

```clingo
--8<-- "examples/dont_drive_drunk/encoding.lp"
```
