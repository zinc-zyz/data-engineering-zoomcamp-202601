import pandas as pd
from sqlalchemy import create_engine
import click
import pyarrow.parquet as pq

@click.command()
@click.option('--green_taxi_parquet_file', default='green_tripdata_2025-11.parquet', help='Input Parquet file')
@click.option('--taxi_zone_csv', default='taxi_zone_lookup.csv', help='Input CSV file')
@click.option('--user', default='postgres', help='PostgreSQL user')
@click.option('--password', default='postgres', help='PostgreSQL password')
@click.option('--host', default='localhost', help='PostgreSQL host')
@click.option('--port', default=5433, type=int, help='PostgreSQL port')
@click.option('--db', default='ny_taxi', help='PostgreSQL database name')
def ingest_data(green_taxi_parquet_file, taxi_zone_csv, user, password, host, port, db):
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    # -------------------------
    # Ingest Green Taxi Data in chunks (PyArrow)
    # -------------------------
    green_table = "green_taxi_data_202511"
    chunk_size = 100000

    parquet_file = pq.ParquetFile(green_taxi_parquet_file)
    first_chunk = True

    for batch in parquet_file.iter_batches(batch_size=chunk_size):
        df_chunk = batch.to_pandas()
        df_chunk.to_sql(
            name=green_table,
            con=engine,
            if_exists="replace" if first_chunk else "append",
            index=False
        )
        first_chunk = False
        print(f"Inserted {len(df_chunk)} rows into {green_table}")

    print(f"Done inserting Green Taxi data into {green_table}!")

    # -------------------------
    # Ingest Taxi Zone Data in chunks (CSV)
    # -------------------------
    zone_table = "taxi_zone_data"
    first_chunk = True
    for df_chunk in pd.read_csv(taxi_zone_csv, chunksize=chunk_size):
        df_chunk.to_sql(
            name=zone_table,
            con=engine,
            if_exists="replace" if first_chunk else "append",
            index=False
        )
        first_chunk = False
        print(f"Inserted {len(df_chunk)} rows into {zone_table}")

    print(f"Done inserting Taxi Zone data into {zone_table}!")

if __name__ == '__main__':
    ingest_data()
