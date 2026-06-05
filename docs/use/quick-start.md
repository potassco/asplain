---
icon: "material/rocket-launch"
---

# Quick Start Guide

## Annotating the logic program

Asplain comes with a range of predefined tags that can be used for annotating.
These tags are necessary for the foil finding process to generate an explanation.
You can start by adding `@removable` and `@addable` tags to your logic program.

```clingo
% @removable
atom_removable.
% @addable
atom_addable.
```

More details about the annotation tags can be found in the [Tagging Reference](../../reference/tagging).

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
