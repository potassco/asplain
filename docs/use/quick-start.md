---
icon: "material/rocket-launch"
---

# Quick Start Guide

!!! example "James bond example"

    We suggest to start with the [James Bond example](../../examples/jamesbond) to get a better understanding of how to annotate your logic program and use the CLI.

## Annotating the logic program

Asplain comes with a range of predefined tags that can be used for annotating.
These tags are necessary to customize the explanation.

You can start with the basic tags by adding `@removable` and `@addable` tags to your logic program.

```clingo
% @removable
atom_removable.
% @addable
atom_addable.
```

!!! tip "Tags"

    The complete list of tags and their usage can be found in the [Tagging](../../reference/tagging) section.

## Command line interface

After properly annotating your logic program you can proceed to call asplain over the CLI.

```bash
asplain <YOUR-PROGRAM> 1 --open
```

If you want to also generate a __natural languge__ explanation:

```bash
asplain <YOUR-PROGRAM> 1 --open --llm=<LLM-TAG>
```

### User interface

If you want to open the __interactive__ explanation web interface using [clinguin](https://potassco.org/clinguin/) run:

```bash
clinguin client-server --domain-files <YOUR-PROGRAM> --ui-files src/asplain/encodings/ui.lp --custom-classes src/asplain/ui --backend ASPlainBackend
```

!!! tip "Command line"

    More details about the command line usage can be found in the [CLI](../../reference/cli)
