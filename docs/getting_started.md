# Getting started

## Installation

=== "Pip"

    ```console
    pip install asplain
    ```

=== "Development mode"

    ```console
    git clone https://github.com/potassco/asplain.git/
    cd asplain
    pip install -e .[all]
    ```

    !!! warning

        Use only for development purposes

## Usage

### Command line interface

Details about the command line usage can be found with:

```console
asplain -h
```

!!! example "Example: James Bond"

    ```console
    asplain examples/james-bond/encoding.lp --explanation-preference examples/james-bond/explanation-preference.lp 0
    ```
