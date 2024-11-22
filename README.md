# asplain

## Installation

To install the project, run

```bash
pip install .
```

## Usage

Run the following for basic usage information:

```bash
asplain -h
```

For example

```bash
asplain examples/james-bond/encoding.lp --explanation-config examples/james-bond/explanation-conf.lp --log info
```

To generate and open the documentation, run

```bash
nox -s doc -- open
```

Instructions to install and use `nox` can be found in
[DEVELOPMENT.md](./DEVELOPMENT.md)
