---
icon: material/code-greater-than
---

# CLI

You can access all of asplain's features over the commad-line interface (CLI).
This page details all available features and how to use them.

!!! note "Clingo arguments"

    **asplain** extends the standard clingo command line interface with a range of options for customizing the generated contrastive explanation graph and the natural language explanation.

!!! warning "Note"

    Additional clingo options provided in the command line, will be applied to finding the models, not the explanations.
    For example, if you provide `-n=2` as a clingo option, asplain will find 2 models for the provided program and generate explanations for those 2 models.

Get the up to date CLI specification by running the following command which will display the normal clingo options and the additional asplain options:

```console
> asplain --help
    ...
    Asplain Options:

    --log=<level>                  : Provide logging level.
                <level> ={DEBUG|INFO|ERROR|WARNING}
                (default: WARNING)
    --model=<model>                : File with a fixed model to explain. Input should be an ASP program using facts.
    If this parameter is not provided, the solving will follow normally in search for models.
    --query=<query>                : A query to explain. Input should be atoms separated by spaces.
                Negated atoms are preceded by '-'.
                If not given, queries will be provided interactively via the command line
    --assumptions=<assumptions>    : Assumptions to enforce. Input should be atoms separated by spaces.
                False assumptions are preceded by '-'.
                If not given, assumptions will be provided interactively via the command line
    --nexplanations=<nexplanations>: Number of explanations to compute. (default: 1)
    --llm=<llm-tag>                : Generate a natural language explanation using an LLM.
                <llm-tag> ={GPT_5|GPT_5_MINI|GPT_5_NANO|GPT_4O|GPT_4O_MINI|GEMINI_3_PRO|GEMINI_3_FLASH|GEMINI_2_5_FLASH|GEMINI_2_FLASH}

    --prune,-p <method>            : Apply pruning to the explanation graph to simplify it.
    Multiple pruning methods can be applied by providing this argument multiple self.statistics.
    They will be applied in the order they are given.
                <method> ={NONE|ORPHANS|PATHS|PATHS_UNDIRECTED|CHANGES}

    --dynamic-tags=<dynamic-tags>  : Preference file for automatic tagging.
    --cost-encoding=<cost-encoding>: Encoding defining the cost function to calculate the best foils via optimization.
    --[no-]open                    : If active the graphs for all contrastive explanations will be opened automatically.
    ...
```



## Specifying the number of explanations

```
asplain [...] --nexplanations="<N>"
```

The number of explanations per model can be set by replacing `<N>`.
Choosing `0` will enumerate all possible explanations.

## Providing a Query

Through this feature the user can express their expectations for the [foil model](../foils/).
The query can be seen as a set of literals.

```
asplain [...] --query="<YOUR-QUERY-ATOM>"
```

`<YOUR-QUERY-ATOM>` is replaced by concrete atoms, all foils that are found have to satisfy this query.
False queries are prefaced by a `-` and query atoms are separated by spaces.

!!! example "Query example"

    If the user expects `p` to be true and `q` to be false, the query would be:

    ```
    asplain [...] --query="p -q"
    ```

## Providing a Model

```
asplain [...] --model <YOUR-MODEL-FILE>
```

This option allows to fix a specific model for the explanation.
Normally *asplain* finds all models for the provided program itself,
but with this option enabled it always uses the provided one.

The model is provided as a file containing facts.

!!! example "Model example"

    If the user wants to fix a model where `p` and `q` are true, the model file would contain:

    `model.lp`
    ```clingo
    p.
    q.
    ```

    ```console
    asplain [...] --model model.lp
    ```

## Providing Assumptions

```
asplain [...] --assumptions="<YOUR-ASSUMPTION-STRING>"
```

Assumptions can be used to enforce certain atoms in the solving process.
They can be provided over the `<YOUR-ASSUMPTION-STRING>` which can contain multiple assumptions separated by spaces.
False assumptions are preceded by a `-`.

Assumptions are automatically tagged and can be used in the preferences to prioritize certain explanations, see the [Explanation Selection](../preferences/) for more details.

!!! example "Assumptions example"

    If the user wants to enforce `d` to be true in all computed models.

    ```
    asplain [...] --assumptions="d"
    ```

See the [Penalize Removing Non-Assumptions](../preferences/penalize-non-assumptions) for an example of how to use the special tag of assumptions in the preferences.


## Pruning

```
asplain [...] --prune=<PRUNING-METHOD>
```

Pruning can be used as a post-processing feature to reduce the size of the contrastive explanation graph.
A more detailed description of the different pruning methods can be found in the [Pruning](../pruning/) Section.

- Options for `<PRUNING-METHOD>` :
    - `ORPHAN` :
        - Removes all orphan subgraphs that are not connected to the main subgraph containing __query__ and __changed__ nodes.
    - `PATHS` :
        - Finds paths over the contrastive graph edges connecting __query__ and __changed__ nodes. Only these paths are included.
    - `CHANGES`
        - Only keeps the nodes that changed between the reference and the foil.

!!! tip "Multiple pruning methods"

    Multiple pruning methods can be applied by providing this argument multiple times.
    They will be applied in the order they are given.

!!! example "Pruning example"

    If the user wants to only keep the nodes that changed between the reference and the foil, and then remove all orphan subgraphs:

    ```
    asplain [...] --prune=CHANGES --prune=ORPHAN
    ```

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

!!! warning "Response time"

    Generating a natural language explanation takes additional time so be patient after running the command with the `--llm` option, especially if you are using a more powerful LLM.
