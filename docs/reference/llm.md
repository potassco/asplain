---
icon: material/message-processing
---

The integration of Large Language Models (LLM) into *asplain* allows users to generate natural language explanations for contrastive explanations. This feature enhances the interpretability of the results by providing human-readable insights. It also enables users to pose queries in natural language, which are then translated into corresponding query atoms for analysis.



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

!!! warning "Labels"

    For the LLM to generate a better natural language explanations, the rules and atoms must have labels. This can be done by providing `@label` annotations in the ASP program. See the [Tagging](../tagging/) section for more details.


## Usage

The natural language interaction can be done using the options `--llm` and `--nl-query` in the command line.

It is also integrated in the interactive explanation interface. After generating the contrastive explanation graph, the user can click on the "Generate Natural Language Explanation" button to generate a natural language explanation of the contrastive explanation.

!!! example "Natural Language Explanation in James Bond Example"

    For details on the example see the [James Bond](../../examples/james-bond/) example.

    The following command generates a natural language explanation for the contrastive explanation of why Bond is not poisoned:

    ```bash
    > asplain examples/james-bond/encoding.lp --nexplanations 0   -n 0 --model examples/james-bond/model.lp --cost-encoding src/asplain/encodings/costs/program-difference.lp --cost-encoding src/asplain/encodings/costs/model-difference.lp  --llm GPT_4O --nl-query "Why is Bond not poisoned?"

    Answer: 1
    c a
    Query (expected atoms): p
    Foil model (satisfying query): p a t
                Removed: c.
                Added: t.
    LLM Explanation:
    To ensure Bond becomes poisoned, he needed to have contact with the toxin, which was added to the situation. Previously, his carefulness prevented him from being poisoned, as the constraints did not fire. By introducing the toxin, he gets poisoned regardless of taking the antidote or being careful.
    SATISFIABLE

    Models       : 1
    Calls        : 1
    Time         : 4.350s (Solving: 4.05s 1st Model: 0.00s Unsat: 4.05s)
    CPU Time     : 0.459s
    ```


## Prompt Templates

### NL Query to Query Atoms

```txt
--8<-- "src/asplain/llm/templates/prompt_templates/translate_instructions.txt"
```

### Explanation graph to NL Explanation

```txt
--8<-- "src/asplain/llm/templates/prompt_templates/explain_instructions.txt"
```
