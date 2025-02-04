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

## LLMs

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

- DEFAULT: openai
- `openai`: Over online API
- `deepsek`: Locally over Ollam

### Example command lines:

All of the following example have NOT been used in the prompt in any way

```bash
asplain examples/dont_drive_drunk/encoding.lp --explanation-preference examples/dont_drive_drunk/explanation_preference.lp 0 --model examples/dont_drive_drunk/model.lp --query "sentence(clare,prison)"   --predicates examples/dont_drive_drunk/predicates.txt --log info --llm
```

The following only works well with the NOT pruned graph. We need to see why or
improve the pruning in general. src/asplain/encodings/reachable.lp should use
#const reachable=false.

```bash
asplain examples/config/encoding.lp examples/config/instance.lp --explanation-preference examples/config/explanation_preference.lp --log info --llm --query "value(\"frontWheel\",\"W14\")"
```

The following only works well with the pruned graph. We need to see why or
improve the pruning in general. src/asplain/encodings/reachable.lp should use
#const reachable=true.

```bash
asplain examples/dont_drive_drunk/encoding.lp --explanation-preference examples/dont_drive_drunk/explanation_preference.lp 0 --model examples/dont_drive_drunk/model.lp --query "-sentence(gabriel,prison)"   --predicates examples/dont_drive_drunk/predicates.txt --log info --llm
```

The following works better with the pruned graph. Also, only one of the
explanations in natural language is correct. But this changes. We need to
investigate

```bash
asplain examples/catdog/encoding_constraints.lp  --explanation-preference examples/catdog/explanation_preference.lp --model examples/catdog/model.lp --query 'assign("Susana",(1,2))'  --log info --llm --predicates examples/catdog/predicates.txt
```

### Documentation

To generate the documentation, run

```bash
nox -s doc
```

Instructions to install and use `nox` can be found in
[DEVELOPMENT.md](./DEVELOPMENT.md)

## TODOS/Questions

- For some cases the reachable graph is better (like catdog) But reachability
  might be wrong because the config example does not work.

- Maybe we want to talk about chosing something.

- Make the LLM be more explicit for alternative models and current model
  (causal explanation)
