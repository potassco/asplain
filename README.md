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

### Examples

- Generally update examples to use assumptions so that we get less models

- Sudoku example

- Elevator example

### Explanation preference

- Parts of the graph that should always be mentioned.(Add them to the
  reachable)

- Explanation preference, include this atoms always

  - What to always include and what to not mention % \_mention(contraint(C)):-
    \\abduced(rm, constraint(C)).

### Pruning

- Add the abduced to the reachable
- Add the mentioned to the reachable

### Prompt changes/ideas

- Instructions to construct the prompt: "Start from the abduced and find a path
  to the query..."

- Maybe we want to talk about chosing something.

- Make the LLM be more explicit for alternative models

- Improve the understading of light blue nodes

- An example with a constraint not connected

- Example with multiple reasons in the contrastive graph

  - LLM can use just one of them

- Example with multiple abduced.

- Be explicit that we don't need the light blue nodes

  - We might not even need to mention these nodes unless they are on the path
    to the query, or abduced. Or maybe because it is an alternative model?

### Extra ideas if prompt fails

- ASP encoding for preprocessing information. info(graph_type, hypothetical).
  info(graph_type, alternative).

- Order with comments:

  ```
  %-----  This was the query
  attr(node,p,query,exclude).

  %----- This is in the real model where the query might or might not be
  node(d).
  node(h).
  node(p).
  edge(d,p,0).
  attr(node,d,origin,real).
  attr(node,h,origin,real).
  attr(node,p,origin,real).
  attr(edge,0,origin,real).
  attr(edge,0,rule_vars,()).
  attr(edge,0,rule_str,"p :- d; not a.").
  attr(edge,0,rule_id,1).
  attr(edge,0,type,cause).

  %----- (Direct changes) This changes must be made to satisfy query
  %----- You must mention them!
  attr(node,d,abduced,rm).

  %----- This is in the new model
  info(model, alternative/hypo/found).
  attr(node,h,origin,hypothetical).

  %-----  Real - Hypothetical
  %----- Indirect changes (Effects)
  %----- Things that
  info(p, node, real_not_hypo).
  info(d, node, real_not_hypo).
  info(0, edge, real_not_hypo).

  %----- Extra info for LLM

  attr(node,d,real_not_hypo).
  attr(node,d,hypo_not_real).
  attr(node,d,hypo_and_real).
  ```
