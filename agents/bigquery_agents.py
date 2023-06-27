import io
import json

from google.cloud import bigquery

from service.document import Document


def client(project_id: str):
    return bigquery.Client(project=project_id)


def schemas(
    bigquery_client: bigquery.Client, project_id: str, dataset_id: str
) -> list[Document]:
    dataset = bigquery_client.get_dataset(f"{project_id}.{dataset_id}")
    tables = list(bigquery_client.list_tables(dataset))
    bigquery_schemas: list[Document] = []
    for table in tables:
        table_ref = bigquery_client.get_table(dataset.table(table.table_id))
        stream = io.StringIO("")
        bigquery_client.schema_to_json(table_ref.schema, stream)
        bigquery_schemas.append(
            Document(f"{project_id}.{dataset_id}.{table.table_id}", str(json.loads(stream.getvalue())))
        )
    return bigquery_schemas


def query(
    bigquery_client: bigquery.Client,
    query_string: str,
    dry_run: bool,
):
    job_config = bigquery.QueryJobConfig(
        dry_run=dry_run
    )
    query_job = bigquery_client.query(query_string, job_config=job_config)

    if dry_run:
        return f"{query_job.total_bytes_processed}"

    results = query_job.result()
    return results.to_dataframe().to_string()
