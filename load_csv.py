from google.cloud import bigquery, storage

client = bigquery.Client()
# client2 = storage.Client()
# bucket = client2.get_bucket('tp_land_data')
# breakpoint()

table_id = "landmanagementservice.land_deal_info.owners"

job_config = bigquery.LoadJobConfig(
    schema=[
        bigquery.SchemaField("full_name", "STRING"),
        bigquery.SchemaField("address", "STRING"),
        bigquery.SchemaField("county_state_zip", "STRING"),
        bigquery.SchemaField("phone_no", "STRING")
    ],
    skip_leading_rows=1,
    allow_quoted_newlines = True
    # The source format defaults to CSV, so the line below is optional.
    # source_format=bigquery.SourceFormat.CSV,
)
uri = "https://storage.cloud.google.com/tp_land_data/bq_owners.csv"

load_job = client.load_table_from_uri(
    uri, table_id, job_config=job_config
)  # Make an API request.

load_job.result()  # Waits for the job to complete.

destination_table = client.get_table(table_id)  # Make an API request.
print("Loaded {} rows.".format(destination_table.num_rows))
# [END bigquery_load_table_gcs_csv]