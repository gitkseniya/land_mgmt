from google.cloud import bigquery, storage

client = bigquery.Client()

table_id = "landmanagementservice.land_deal_info.unit_owners"

job_config = bigquery.LoadJobConfig(
    schema=[
        bigquery.SchemaField("owner_id", "STRING"),
        bigquery.SchemaField("interest_type", "STRING"),
        bigquery.SchemaField("current_owner", "BOOLEAN"),
        bigquery.SchemaField("comments", "STRING"),
        bigquery.SchemaField("vesting_docs", "STRING"),
    ],
    write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
    source_format=bigquery.SourceFormat.CSV,
    skip_leading_rows=1,
    allow_quoted_newlines = True
    # The source format defaults to CSV, so the line below is optional.
    # source_format=bigquery.SourceFormat.CSV,
)
uri = "https://storage.cloud.google.com/tp_land_data/bq_units2.csv"

load_job = client.load_table_from_uri(
    uri, table_id, job_config=job_config
)  # Make an API request.

load_job.result()  # Waits for the job to complete.

destination_table = client.get_table(table_id)  # Make an API request.
print("Loaded {} rows.".format(destination_table.num_rows))
# [END bigquery_load_table_gcs_csv]