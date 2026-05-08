# Penalize Removing Non-Facts

Penalize removing rules that are not facts.
This is useful when you want to remove first facts, in cases where the instance is the one that can be blamed.

::: src/asplain/encodings/costs/penalize-non-facts-removed.lp
    handler: asp
    options:
        encodings:
            git_link: true
            source: true
            include_title: false
        start_level: 3
