# Definitions

A contrastive explanation compares a reference model to a contrasted model.

$$
    G_c=...
$$

## Query

Identifies what atoms should/shouldn't be part of the model.

??? question "What can be part of the query?"

    - If we ground the program with all possible abducibles, this would give us anything that can be in a hypothetical model.
    - Anything that is not part of the program it should not be relevant


## Reference model

The provided model that is considered the current truth



## Contrasted model

The model found which fulfils the query.


!!! info "Cases"


    === "Same reference model"

        When the query is true in the current model, then the contrasted and reference model are the same.
        The output is something like the current output of xclingo or the work with Mario.

    === "Alternative model"

        When the query is not true in the current model but it it true without having to change the input (no abducible needed).
        This is the case where another model of the same program (with the same input) satisfies the query.

        The explanation would compare both models without need of abduction.

    === "Hypothetical model"

        When the query can't be satisfied with the current input
        Parts of the input can be abducted (changed) to achieve the query


??? question "Selecting the contrasting model"

    - We want to do some minimization. Perhaps something similar to the MUS.
        - Subset minimal vs cardinality minimal
        - Doing the minimization just in ASP is not possible directly
    - We can add preferences in something like asprin
        - We can say which predicates can be abduced etc
        - Perhaps the preferences also talk about some things that come from the interaction
        this way we could say to first abduce the things selected by the user before the input
    - This could be defined via an ASP program


## Contrastive graph


The contrastive graph includes all nodes and edges from the graphs of the reference and contrastive models. Additionally it includes inhibitor edges which link nodes that are not present in both graphs.


## Explanation preferences

### Distance

Defines how close the contrastive model is to the reference model.
It can be customizable.

??? question "Options for distance"
    - The things removed or the things added
    - The differences between what is true and false in both models
    - MUS as distance
    - Some time of distance that might be numerical difference

### Abducibles

Things that are not part of the reference model. They can be either added or removed in the contrasted model.

??? question "How to select what to abduce"

    - Could it be that some things are abducible to add but not to remove? or viceversa?
    - Can we limit the options of abducibles to things occurring on the rules.
        - Propositional: Then it could be limited to the atoms already in the program
        - First order: Not so easy because the program depends on the original input.
    - There is some similarity with `#defined`
    - Can we abduce any rule or just facts?


??? question "Incremental information"

    Additional information provided that makes differentiates what has been user selected.


    - This could also be interesting input for the LLM to explain differently
    - Add this information as additional facts `user(a).` and use a distance function that takes this into account.

## :material-book-multiple-outline: References

- [*Model Explanation via Support Graphs*][pedro-brais]
- [*Inhibitors*][inhibitors]

[pedro-brais]: https://www.cambridge.org/core/services/aop-cambridge-core/content/view/542C1AA568113B703F179D15E3CBB3EE/S1471068424000048a.pdf/model_explanation_via_support_graphs.pdf
[inhibitors]: https://arxiv.org/abs/1602.06897
