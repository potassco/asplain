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

### LLMs

To use OpenAI's ChatGPT you have to provide an OpenAI API Key. To do this you
just have to set the environment variable `OPENAI_API_KEY` either directly or
in a `.env` file.

`.env` :

```
OPENAI_API_KEY=<ENTER-YOUR-KEY-HERE>
```

To get LLM Explanations use the `--llm` argument.

To specify the LLM Model you use use the `--model-tag` argument. You can choose
between:

- DEFAULT: LLAMA3.2:1B over Ollama
- `openai`: Over online API
- `deepsek`: Locally over Ollam

### Documentation

To generate the documentation, run

```bash
nox -s doc
```

Instructions to install and use `nox` can be found in
[DEVELOPMENT.md](./DEVELOPMENT.md)
