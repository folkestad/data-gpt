import io
import json

from google.cloud import bigquery


def client(project_id: str):
    return bigquery.Client(project=project_id)


def schemas(client: bigquery.Client, project_id: str, dataset_id: str):
    dataset = client.get_dataset(f"{project_id}.{dataset_id}")
    tables = list(client.list_tables(dataset))
    _schemas: list[str] = []
    for table in tables:
        table_ref = client.get_table(dataset.table(table.table_id))
        stream = io.StringIO("")
        client.schema_to_json(table_ref.schema, stream)
        _schemas.append(
            f"Table name: {project_id}.{dataset_id}.{table.table_id}\n"
            f"Column information: {json.loads(stream.getvalue())}"
        )
    return _schemas


def query(
    client: bigquery.Client,
    query_string: str,
    dry_run: bool,
    use_query_cache: bool = True,
):
    job_config = bigquery.QueryJobConfig(
        dry_run=dry_run, use_query_cache=use_query_cache
    )
    query_job = client.query(query_string, job_config=job_config)

    if dry_run:
        return f"{query_job.total_bytes_processed}"

    results = query_job.result()
    return results.to_dataframe().to_string()
