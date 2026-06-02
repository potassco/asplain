---
icon: "material/rocket-launch"
---

# Quick Start Guide

## Annotating the logic program

In asplain logic programs need to be annotated for explanations to be generated.
These annotations are done via tags.
Asplain comes with a range of predefined tags that can be used for annotating:

- `% @label("<YOUR-LABEL>")`
    - Assigns the rule after this tag the label `<YOUR-LABEL>`
    - Variables from the rule can be used in the label
    - _Example_:
    ```clingo
    % @label("{} is innocent since they were not punished",(P,))
    sentence(P, prison) :- punish(P).
    ```
    - This tag can also be used independent of a rule for labeling atoms
    - _Example_:
    ```clingo
    % @label("Person {} likes the pet {}",(P,A,)) :: person(P,A)
    ```
- `% @addable`
    - Adds a the rule below as a change candidate to add
    - In the foil finding process the rule might be added to the program to find a foil satisfying the query
- `% @removable`
    - Adds a the rule below as a change candidate to remove
    - In the foil finding process the rule might be removed from the program to find a foil satisfying the query
- `% @hide`
    - Hides the rule below in the contrastive explanation


## Command line interface

After properly annotating your logic program you can proceed to call asplain over the CLI.

```bash
asplain <YOUR-PROGRAM> 1 --open
```

If you want to also generate a __natural languge__ explanation:

```bash
asplain <YOUR-PROGRAM> 1 --open --llm=<LLM-TAG>
```

If you want to open the __interactive__ explanation web interface using [clinguin](https://potassco.org/clinguin/):

```bash
clinguin client-server --domain-files <YOUR-PROGRAM> --ui-files src/asplain/encodings/ui.lp --custom-classes src/asplain/ui --backend ASPlainBackend
```

More details about the command line usage can be found in the [CLI Refernce](../../reference/cli)
