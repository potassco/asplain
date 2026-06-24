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

<!-- --8<-- [end:usage] -->
