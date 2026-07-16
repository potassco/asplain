---
icon: "material/head-question"
---

# Foil finding

The process of finding foils is done with a meta-program that interprets the fact representation obtained by the [setup construction](./setup.md) and searches for a modified version of the reference program that satisfies the query.


This is done with the following programs.

## Construct foil candidates

- Constructs a foil candidate
- Performs minimization using [cost functions](../preferences/index.md) to find the preferred foil candidate
- Computes the fired constraints for the [contrastive explanation graph](./explanation-graph.md)


::: src/asplain/encodings/construct-foil.lp
    handler: asp
    options:
        encodings:
            git_link: true
            source: false
            include_title: false
        start_level: 3


## Check foil model

This encoding is used in this step with the constant `graph=foil` to construct the foil model of the candidate foil program.

!!! info

    This same encoding is used to construct the reference model of the reference program with the constant `graph=ref`.

::: src/asplain/encodings/model-subgraph.lp
    handler: asp
    options:
        encodings:
            git_link: true
            source: false
            include_title: false
        start_level: 3
