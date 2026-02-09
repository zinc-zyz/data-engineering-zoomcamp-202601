# Data Engineering Zoomcamp Week 3 Homework 

This is my homework in learning Data Warehouse. Let's dive into it!

## Prerequisites

Load all the parquet files within the `data` folder and manually upload to a GCS bucket. 

Create an external table using the Yellow Taxi Trip Records.

```sql
CREATE OR REPLACE EXTERNAL TABLE `my_project.my_dataset.external_trips`
(
  VendorID INT64,
  tpep_pickup_datetime TIMESTAMP,
  tpep_dropoff_datetime TIMESTAMP,
  passenger_count INT64,
  trip_distance FLOAT64,
  RatecodeID INT64,
  store_and_fwd_flag STRING,
  PULocationID INT64,
  DOLocationID INT64,
  payment_type INT64,
  fare_amount FLOAT64,
  extra FLOAT64,
  mta_tax FLOAT64,
  tip_amount FLOAT64,
  tolls_amount FLOAT64,
  improvement_surcharge FLOAT64,
  total_amount FLOAT64,
  congestion_surcharge FLOAT64
)
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://my-bucket/trips/*.parquet']
);
```

Create a (regular/materialized) table in BQ using the Yellow Taxi Trip Records (do not partition or cluster this table).

```sql
CREATE OR REPLACE TABLE `my_project.my_dataset.yellowtrips`
AS
SELECT
  CAST(VendorID AS STRING) AS VendorID,
  tpep_pickup_datetime,
  tpep_dropoff_datetime,
  passenger_count,
  CAST(trip_distance AS NUMERIC) AS trip_distance,
  CAST(RatecodeID AS STRING) AS RatecodeID,
  store_and_fwd_flag,
  CAST(PULocationID AS STRING) AS PULocationID,
  CAST(DOLocationID AS STRING) AS DOLocationID,
  payment_type,
  CAST(fare_amount AS NUMERIC) AS fare_amount,
  CAST(extra AS NUMERIC) AS extra,
  CAST(mta_tax AS NUMERIC) AS mta_tax,
  CAST(tip_amount AS NUMERIC) AS tip_amount,
  CAST(tolls_amount AS NUMERIC) AS tolls_amount,
  CAST(improvement_surcharge AS NUMERIC) AS improvement_surcharge,
  CAST(total_amount AS NUMERIC) AS total_amount,
  CAST(congestion_surcharge AS NUMERIC) AS congestion_surcharge
FROM `my_project.my_dataset.external_yellowtrips`;
```

## Question 1: Counting Records

**Question:** What is count of records for the 2024 Yellow Taxi Data?

Check from the `my_project.my_dataset.yellowtrips` table (Details - Storage info - Number of rows)

## Question 2: Data read estimation

**Question:** Write a query to count the distinct number of PULocationIDs for the entire dataset on both the tables.

What is the estimated amount of data that will be read when this query is executed on the External Table and the Table?

```sql
-- On external table
SELECT COUNT(DISTINCT PULocationID) AS distinct_pickup_zones
FROM `my_project.my_dataset.external_yellowtrips`;
```

```sql
-- On regular table
SELECT COUNT(DISTINCT PULocationID) AS distinct_pickup_zones
FROM `my_project.my_dataset.yellowtrips`;
```

## Question 3: Understanding columnar storage

**Question:** Write a query to retrieve the PULocationID from the table (not the external table) in BigQuery. Now write a query to retrieve the PULocationID and DOLocationID on the same table.

Why are the estimated number of Bytes different?

```sql
SELECT PULocationID
FROM `my_project.my_dataset.yellowtrips`;
```

```sql
SELECT PULocationID, DOLocationID
FROM `my_project.my_dataset.yellowtrips`;
```

## Question 4: Counting zero fare trips

**Question:** How many records have a fare_amount of 0?

```sql
SELECT COUNT(*) AS zero_fare_trips
FROM `my_project.my_dataset.yellowtrips` WHERE fare_amount = 0;
```

## Question 5: Partitioning and clustering

**Question:** What is the best strategy to make an optimized table in Big Query if your query will always filter based on tpep_dropoff_datetime and order the results by VendorID (Create a new table with this strategy)

```sql
CREATE OR REPLACE TABLE `my_project.my_dataset.yellow_tripdata_optimized`
PARTITION BY DATE(tpep_dropoff_datetime)
CLUSTER BY VendorID AS
SELECT *
FROM `my_project.my_dataset.yellow_tripdata`;
```

## Question 6: Partition benefits

**Question:** Write a query to retrieve the distinct VendorIDs between tpep_dropoff_datetime 2024-03-01 and 2024-03-15 (inclusive)

Use the materialized table you created earlier in your from clause and note the estimated bytes. Now change the table in the from clause to the partitioned table you created for question 5 and note the estimated bytes processed. What are these values?

```sql
SELECT DISTINCT VendorID
FROM `my_project.my_dataset.yellow_tripdata`
WHERE tpep_dropoff_datetime BETWEEN '2024-03-01' AND '2024-03-15';
```
```sql
SELECT DISTINCT VendorID
FROM `my_project.my_dataset.yellow_tripdata_optimized`
WHERE tpep_dropoff_datetime BETWEEN '2024-03-01' AND '2024-03-15';
```

## Question 7: Partition benefits

**Question:** Where is the data stored in the External Table you created?

## Question 8: Clustering best practices

**Question:** It is best practice in Big Query to always cluster your data: True or False

Clustering in BigQuery is useful when you frequently filter, group, or order by certain columns.
- For small tables, clustering adds no benefit.
- For tables without predictable query patterns, clustering may increase storage costs slightly without helping queries.
Best practice: cluster only when it aligns with query patterns.

## Question 9: Understanding table scans

**Question:** Write a `SELECT count(*)` query FROM the materialized table you created. How many bytes does it estimate will be read? Why?
```sql
SELECT COUNT(*) 
FROM `my_project.my_dataset.yellow_tripdata`;
```
For a materialized (regular) table, BigQuery stores table metadata including row counts.

When you run COUNT(*) without referencing any columns, BigQuery can return the result from metadata only.