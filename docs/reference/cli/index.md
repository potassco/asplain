---
icon: octicons/command-palette-16
---

# CLI

You can access all of asplain's features over the commad-line interface (CLI).
This page details all available features and how to use them.

## CLI Specification

```bash
asplain --help
```

## Specifying the number of explanations

```
asplain [...] --nexplanations="<N>"
```

The number of explanations per model can be set by replacing `<N>`.
Choosing `0` will enumerate all possible explanations.

## Providing a Query

```
asplain [...] --query="<YOUR-QUERY-ATOM>"
```

Through this feature the user can express their expectations for the foil model.
If `<YOUR-QUERY-ATOM>` is replaced by concrete atoms, all foils that are found have to satisfy this query.
False queries are prefaced by a `-` and query atoms are separated by spaces.

## Providing a Model

```
asplain [...] --model <YOUR-MODEL-FILE>
```

This option allows to fix a specific model for the explanation.
Normally asplain finds a model for the provided program itself but with this option enabled it always uses the provided one.

## Providing Assumptions

```
asplain [...] --assumptions="<YOUR-ASSUMPTION-STRING>"
```

Assumptions can be used to enforce certain atoms in the solving process.
They can be provided over the `<YOUR-ASSUMPTION-STRING>` which can contain multiple assumptions separated by spaces.
False assumptions are preceded by a `-`.

## Pruning

```
asplain [...] --prune=<PRUNING-METHOD>
```

Pruning can be used as a post-processing feature to reduce the size of the contrastive explanation graph.
For complex problems the size of the explanation graph can grow to a level where interpretation can be difficult.
For cases like this pruning can be useful to remove parts of the explanation that are unrelated or not necessary.
The applicability and usfulness of the different pruning approaches vary for different programs.

- Options for `<PRUNING-METHOD>` :
    - `ORPHAN` :
        - Removes all orphan subgraphs that are not connected to the main subgraph containing __query__ and __changed__ nodes.
    - `PATHS` :
        - Finds paths over the contrastive graph edges connecting __query__ and __changed__ nodes. Only these paths are included.
    - `CHANGES`
        - Only keeps the nodes that changed between the reference and the foil.

## Natural Language Explanation (LLM)

!!! note

    asplain only supports prompting LLM's over an API. The two API's that are available for now are `google` and `openai`. To access them you need to provide an API key. This can be done two different ways:

    #### :one: Using a `.env` file

    ```dotenv
    OPENAI_API_KEY=<YOUR-OPENAI-API-KEY>
    GEMINI_API_KEY=<YOUR-GOOGLE-API-KEY>
    ```

    #### :two: Directly in command-line

    ```
    OPENAI_API_KEY=<YOUR-OPENAI-API-KEY> asplain [...] --llm=<LLM-TAG-OPENAI>
    ```

    ```
    GEMINI_API_KEY=<YOUR-GOOGLE-API-KEY> asplain [...] --llm=<LLM-TAG-GOOGLE>
    ```

```
asplain [...] --llm=<LLM-TAG>
```

With this option enabled a natural language explanation is generated on the basis of the contrastive explanation graph.
The LLM used for this generation can be specified by replacing `<LLM-TAG>`.

- Options for `<LLM-TAG>` :
    - `GPT_5`
    - `GPT_5_MINI`
    - `GPT_5_NANO`
    - `GPT_4O`
    - `GPT_4O_MINI`
    - `GEMINI_3_PRO`
    - `GEMINI_3_FLASH`
    - `GEMINI_2_5_FLASH`
    - `GEMINI_2_FLASH`
