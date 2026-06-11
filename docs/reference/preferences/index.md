---
icon: material/heart
---

# Explanation Preferences

Domain-specific preferences can be added to an explanation over cost functions.
They are used to assign higher costs to certain rules and/or atoms, e.g., to prioritize changes over the input, or the removal of integrity constraints over facts.

Asplain comes out of the box with a range of predefined cost functions for common preferences. You can use these functions as-is, or write your own to fit your needs.

__Usage__

```bash
asplain [...] --costs-encoding=<YOUR-COST-ENCODING>
```

## Predefined Cost Functions

### Model Difference

Prioritize a different model in the foil.

::: src/asplain/encodings/costs/model-difference.lp
    handler: asp
    options:
        encodings:
            git_link: true
            source: true
        start_level: 3

### Program Difference

Prioritize a different program as the foil.

::: src/asplain/encodings/costs/program-difference.lp
    handler: asp
    options:
        encodings:
            git_link: true
            source: true
        start_level: 3


### Penalize Added

Penalize adding new rules.

::: src/asplain/encodings/costs/penalize-added.lp
    handler: asp
    options:
        encodings:
            git_link: true
            source: true
        start_level: 3

### Penalize Removed

Penalize removing existing rules.

::: src/asplain/encodings/costs/penalize-removed.lp
    handler: asp
    options:
        encodings:
            git_link: true
            source: true
        start_level: 3

### Penalize Removing Non-Assumptions

Prioritize removing assumptions over other rules.

::: src/asplain/encodings/costs/penalize-non-assumptions-removed.lp
    handler: asp
    options:
        encodings:
            git_link: true
            source: true
        start_level: 3

### Penalize Removing Non-Constraints

Prioritize removing constraints over other rules.

::: src/asplain/encodings/costs/penalize-non-constraint-removed.lp
    handler: asp
    options:
        encodings:
            git_link: true
            source: true
        start_level: 3

### Penalize Removing Non-Facts

Prioritize removing facts over other rules.

::: src/asplain/encodings/costs/penalize-non-facts-removed.lp
    handler: asp
    options:
        encodings:
            git_link: true
            source: true
        start_level: 3
