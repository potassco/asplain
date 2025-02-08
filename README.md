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

### Simple example

```bash
asplain examples/james-bond/encoding.lp --explanation-preference examples/james-bond/explanation_preference.lp
```

### A bit more evolved

```bash
asplain examples/dont_drive_drunk/encoding.lp --explanation-preference examples/dont_drive_drunk/explanation_preference.lp 0 --model examples/dont_drive_drunk/model.lp --query "sentence(clare,prison)"
```

### With constraints

```bash
asplain examples/catdog/encoding_constraints.lp  --explanation-preference examples/catdog/explanation_preference.lp 0 --model examples/catdog/model.lp --query 'assign("Susana",(1,2))'
```

To generate the documentation, run

```bash
nox -s doc
```

Instructions to install and use `nox` can be found in
[DEVELOPMENT.md](./DEVELOPMENT.md)
