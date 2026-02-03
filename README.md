# asplain

Asplain is a tool for generating contrastive explanations for answer set
programs (ASP).

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

For a basic usage example, see the
[examples/james-bond/README.md](examples/james-bond/README.md) file.

### LLM Integration

For using the OpenAI API, an API-Key has to be provided in the `OPENAI_API_KEY`
environment variable. This can be done using a `.env`file or directly in the
command line.

#### Using the `.env` file

Create a `.env` file in the root directory of the project and add the following
line

```.env
OPENAI_API_KEY=<your-api-key>
```

#### Using the command line

```bash
OPENAI_API_KEY=<your-api-key> asplain --llm=<model-tag>
```
