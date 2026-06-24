
# Program Difference

Will penalize the differences in the reference and foil programs, prioritizing foils that are more similar to the reference program. This is useful when you want to find a foil that is as close as possible to the reference program, but still different enough to explain the difference in behavior.

::: src/asplain/encodings/costs/program-difference.lp
    handler: asp
    options:
        encodings:
            git_link: true
            source: true
            include_title: false
        start_level: 3
