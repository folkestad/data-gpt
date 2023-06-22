import guidance

# noinspection PyCallingNonCallable
generate_sql = guidance(
    """
{{~#system~}}
{{llm.default_system_prompt}}
{{~/system}}

{{#user~}}
Table information about tables in BigQuery containing table name and column information:

{{most_relevant_table}}

Based on the table information generate a BigQuery SQL query to answer the question "{{question}}". 

Samples of successful responses are listed directly below:
- SELECT * FROM rm-data-market-dev.raw_sales.retail_sales LIMIT 10;
- SELECT name FROM project-id.dataset_id.table_id LIMIT 1;

Samples of unsuccessful responses are listed directly below:
- Could not find a table with the data you are looking for.
- Could not find a column with the data you are looking for. 

Answer with nothing more than the SQL query if the answer is successful.
Otherwise answer with nothing more than an explanation of why you cannot find an answer.
{{~/user}}

{{#assistant~}}
{{gen 'sql' temperature=0}}
{{~/assistant~}}
"""
)

# noinspection PyCallingNonCallable
format_answer = guidance(
    """
{{~#system~}}
{{llm.default_system_prompt}}
{{~/system}}

{{#user~}}
question: "{{question}}"

sql: "{{sql}}"

answer: "{{answer}}"

Formulate a formatted concise response to the user in the 
format directly below where you fill in information in the <>:
- QUESTION:

    <question>

- SQL:

    <sql>

- ANSWER:

    <answer>
    
Try to make the answer as concise as possible.
{{~/user}}

{{#assistant~}}
{{gen 'answer' temperature=0}}
{{~/assistant~}}
"""
)
