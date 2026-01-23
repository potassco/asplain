# asplain

> Remove this block after following the instructions below to use the template.
>
> This project template is configured to ease collaboration. Linters,
> formatters, and actions are already configured and ready to use.
>
> To use the project template, run the `init.py` script to give the project a
> name and some metadata. The script can then be removed and the
> `pyproject.toml` file be adjusted as needed.

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

### LLM Intergration

To setup the llm integration, run `asplain` with the `--llm` flag.

```bash
asplain --llm=<model-tag>
```

For using the OpenAI API, an API-Key has to be provided in the `OPENAI_API_KEY` environment variable.
This can be done using a `.env`file or directly in the command line.

#### Using the `.env` file

Create a `.env` file in the root directory of the project and add the following line

```.env
OPENAI_API_KEY=<your-api-key>
```

#### Using the command line

```bash
OPENAI_API_KEY=<your-api-key> asplain --llm=<model-tag>
```

### Documentation

To generate and open the documentation, run

```bash
mkdocs serve -o
```

Make sure to install the optional documentation dependencies via

```bash
pip install .[doc]
```

Instructions to install and use `nox` can be found in
[DEVELOPMENT.md](./DEVELOPMENT.md)
