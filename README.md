# data-gpt

Ask questions of your data in natural language.

This application uses an LLM model to
answer questions about your data based on schema definitions.

Or search data for terms using a vector database.

*Currently it supports:*
 - LLM: 
   - OpenAI models
 - Data sources:
   - BigQuery 

## How to use

### Prerequisites

1. `poetry install`
2. `cp .env.example .env` and fill in the values. 
See comments in `.env.example` for more details.
3. The first time you run the application, you need to index your data
which is present in BigQuery defined by `GCP_PROJECT_ID` and `GCP_DATASET_ID`.
    - `poetry run python cli.py -- --index`

### CLI

#### Help and usage

- `poetry run python cli.py -- --help`

#### Examples

##### Ask a question

- `poetry run python cli.py -- --question "what is the largest country by population and what is its total vaccinations?" --index` 
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

##### Search for terms in data

- `poetry run python cli.py -- -s "vaccinations" --index`

NB: `--index` is optional and will index the data if it has not been indexed already
or a different embedding model is used and re-index is needed.

### Slack bots

1. In https://api.slack.com/apps:
   1. Create a new app and install it to your workspace (see https://api.slack.com/start/building/bolt-python for more details)
   2. Under OAuth & Permissions give it the scopes `chat:write` and `app_mentions:read`
   3. Under OAuth & Permissions find the Bot User OAuth Token and add it to your `.env` file as `SLACK_BOT_TOKEN`
   4. Under Basic Information create an App-Level Token and add it to your `.env` file as `SLACK_APP_TOKEN`
   5. Under Event Subscription enable Events and subscribe to the `app_mention` event
   6. Under Socket Mode enable Socket Mode
2. In your Slack organization, invite the bot to a channel by `@`'ing it. E.g. `@<your-slack-app-name>`
3. Configure `.env`
4. Run the bot with `poetry run python slack_bot_*.py`
5. Ask it a question, e.g. `@data-gpt what is the largest country by population and what is its total vaccinations?`