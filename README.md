# data-gpt

Ask questions of your data in natural language.

This application uses an LLM model to
answer questions about your data based on schema definitions.

*Currently it supports:*
 - LLM: 
   - OpenAI models
 - Data sources:
   - BigQuery 

## How to use

### Prerequisites

1. `poetry install`
2. `cp .env.example .env` and fill in the values

### Run the CLI

1. `poetry run python cli.py -- --question "what is the largest country by population and what is its total vaccinations?"` 
   - Example output:
      ```
         - QUESTION:

          What is the largest country by population and what is its total vaccinations?

         - SQL:

           SELECT country, total_vaccinations
           FROM `test.test.country_vaccinations`
           JOIN `test.test.country_population`
           ON `test.test.country_vaccinations`.country = `test.test.country_population`.Country__or_dependency_
           ORDER BY `test.test.country_population`.Population__2020_ DESC
           LIMIT 1;

         - ANSWER:

           The largest country by population is China with a total of 845,299,000 vaccinations.

2. `poetry run python cli.py -- --help` for help and more options

### Run the Slack bot

1. `poetry run python slack_bot.py`
2. In Slack, invite the bot to a channel and ask it a question, e.g. `@data-gpt what is the largest country by population and what is its total vaccinations?`