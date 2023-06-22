# bq-gpt

Ask general questions on your data.

This application uses an LLM model to
answer questions about your data based on its schema definitions.

*Currently it supports:*
 - LLM's: 
   - OpenAI's GPT-3.5 model.
 - Data sources:
   - BigQuery 

## How to use

### Prerequisites

1. `poetry install`
2. `cp .env.example .env` and fill in the values

### Run the CLI

1. `poetry run python cli.py -- --question "How many users are there?"`
for the simplest usage
2. `poetry run python cli.py -- --help` for help and more options 