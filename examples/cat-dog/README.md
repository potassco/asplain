# Cat & Dog Seating

> [!Note] Read the full documentation for this example
> [here](https://potassco.org/asplain/examples/catdog/).

<!-- --8<-- [start:description] -->

The cat & dog seating example encoding is an assignment ASP encoding with
variables. It models a scenario where there is an event where people are seated
on tables depending on their preferences in pets. Dog people are only allowed
to sit with other dog people, and cat people are only allowed to sit with other
cat people. The goal is to seat all people while adhering to their pet
preferences.

<!-- --8<-- [end:description] -->

![Cat & Dog Seating Example](../../docs/assets/images/catdog.svg)

## Usage

<!-- --8<-- [start:usage] -->

Explanation:

```bash
asplain examples/cat-dog/encoding.lp examples/cat-dog/instance.lp 1 --open --query='assign("Susana",(1,2))'
```

<!-- --8<-- [end:usage] -->
