---
icon: material/heart
---

# Explanation Preferences

Domain-specific preferences can be added to an explanation over cost functions.
They are used to assign higher costs to certain rules and/or atoms, e.g., to prioritize changes over the input, or the removal of integrity constraints over facts.

Asplain comes out of the box with a range of predefined cost functions for common preferences. You can use these functions as-is, or write your own to fit your needs.


## Model Difference

::: src/asplain/encodings/costs/model-difference.lp
    handler: asp
    options:
        encodings:
            git_link: true
            source: true
        start_level: 1

## Program Difference

::: src/asplain/encodings/costs/program-difference.lp
    handler: asp
    options:
        encodings:
            git_link: true
            source: true
        start_level: 1


## Penalize Added

::: src/asplain/encodings/costs/penalize-added.lp
    handler: asp
    options:
        encodings:
            git_link: true
            source: true
        start_level: 1

## Penalize Removed

::: src/asplain/encodings/costs/penalize-removed.lp
    handler: asp
    options:
        encodings:
            git_link: true
            source: true
        start_level: 1

## Penalize Removing Non-Assumptions

::: src/asplain/encodings/costs/penalize-non-assumptions-removed.lp
    handler: asp
    options:
        encodings:
            git_link: true
            source: true
        start_level: 1

## Penalize Removing Non-Constraints

::: src/asplain/encodings/costs/penalize-non-constraint-removed.lp
    handler: asp
    options:
        encodings:
            git_link: true
            source: true
        start_level: 1

## Penalize Removing Non-Facts

::: src/asplain/encodings/costs/penalize-non-facts-removed.lp
    handler: asp
    options:
        encodings:
            git_link: true
            source: true
        start_level: 1
