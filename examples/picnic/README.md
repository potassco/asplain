# Picnic

<!-- --8<-- [start:description] -->

The picnic example encoding is a simple ASP encoding without any variables.
It models a picnic on a sunny day. During the picnic, it may start raining,
and Jane may or may not have brought an umbrella. The picnic can take place
either because the weather remains sunny or because Jane has an umbrella that
allows it to continue despite the rain.

<!-- --8<-- [end:description] -->

## Usage

<!-- --8<-- [start:usage] -->

Explanation with __fixed model__:

```bash
asplain examples/picnic/encoding.lp --nexplanations 0 --query "-p" 0 --model examples/picnic/model.lp
```

```bash
asplain examples/picnic/encoding.lp --nexplanations 0 --nl-query "Why did the picnic take place?" 0 --model examples/picnic/model.lp
```

<!-- --8<-- [end:usage] -->
>