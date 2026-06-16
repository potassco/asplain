# Penalize Removing Non-Constraints

Penalize removing rules that are not integrity constraints.
This is useful when you want to remove first constraints, in cases such as debugging.

::: src/asplain/encodings/costs/penalize-non-constraint-removed.lp
    handler: asp
    options:
        encodings:
            git_link: true
            source: true
            include_title: false
        start_level: 3
