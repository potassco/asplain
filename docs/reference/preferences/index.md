---
icon: material/heart
---

# Explanation Selection

Domain-specific preferences can be added to an explanation over cost functions.
They are used to assign higher costs to certain rules and/or atoms, e.g., to prioritize changes over the input, or the removal of integrity constraints over facts.

Asplain comes out of the box with a range of predefined cost functions for common preferences. You can use these functions as-is, or write your own to fit your needs.

## Usage

```bash
asplain [...] --costs-encoding=<YOUR-COST-ENCODING>
```

!!! tip "Multiple cost functions"

    You can provide multiple cost functions by repeating the `--costs-encoding` option multiple times.

Your cost encoding must obtain atoms using the `cost/3` predicate.

::: src/asplain/encodings/costs/docs.lp
    handler: asp
    options:
        glossary:
            include_title: false
            include_references: false
        start_level: 3


!!! example "Cost encodings"

    In this section we provide a few examples of cost encodings for common preferences.
    Browse the files in the left for more examples and the complete list of predefined cost encodings.

    Adjust the `Value` and `Level` to prioritize certain explanations over others.
