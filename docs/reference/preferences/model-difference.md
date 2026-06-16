# Model Difference

Will penalize the differences in the reference and foil models, prioritizing foils that are as similar as possible to the reference model. This is useful when you want to find a foil that is as close as possible to the reference model, for instance, one that takes the same choices when multiple options are available.

::: src/asplain/encodings/costs/model-difference.lp
    handler: asp
    options:
        encodings:
            git_link: true
            source: true
            include_title: false
        start_level: 3
