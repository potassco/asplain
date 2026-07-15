# Don't Drive Drunk

> [!Note] Read the full documentation for this example
> [here](https://potassco.org/asplain/examples/dontdrivedrunk/).

<!-- --8<-- [start:description] -->

The don't drive drunk example encoding is a simple ASP encoding with variables.
It models a scenario where there are two people, Gabriel and Clare. If any of
the two people are drunk and also drives they get sentenced and have to go to
prison.

<!-- --8<-- [end:description] -->

![Don't Drive Drunk Example](../../docs/assets/images/dontdrivedrunk.svg)

## Usage

<!-- --8<-- [start:usage] -->

Explanation:

```bash
asplain examples/dont_drive_drunk/encoding.lp 1 --log info --query "sentence(gabriel,innocent)"
```

### Pruned graph

```bash
asplain examples/dont_drive_drunk/encoding.lp 1 --log info --query "sentence(gabriel,innocent)" --open --prune CHANGES
```

### Using the __interactive__ explanation interface:

```bash
clinguin client-server --domain-files examples/dont_drive_drunk/encoding.lp --ui-files src/asplain/encodings/ui.lp --custom-classes src/asplain/ui --backend ASPlainBackend  --cost-encoding src/asplain/encodings/costs/program-difference.lp
```

<!-- --8<-- [end:usage] -->
