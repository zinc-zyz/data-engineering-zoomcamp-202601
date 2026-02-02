# Data Engineering Zoomcamp Week 2 Homework 

This is my homework in learning Kestra in workflow orchesstration. Let's dive into it!
## Prerequisites

Make sure to have `06_gcp_kv.yaml` set for the environment vairables (e.g. GCP Project ID, GCP Location, GCS Bucket Name, BigQuery Dataset Name). In this module, the variables declared as below for explanation later on. 

- GCP Project ID: `sample-project`
- GCP Location: `asia-southeast2`
- GCS Bucket Name: `sample-bucket` (it should be globally unique)
- BigQuery Dataset Name: `sample_dataset`

## Question 1

**Question:** Within the execution for `Yellow` Taxi data for the year `2020` and month `12`: what is the uncompressed file size (i.e. the output file `yellow_tripdata_2020-12.csv` of the `extract` task)?

Locate the GCS bucket and look for the output file size (under Size). 

## Question 2

**Question:** What is the rendered value of the variable `file` when the inputs `taxi` is set to `green`, `year` is set to `2020`, and `month` is set to `04` during execution?

The format of the file is as shown: `"{{inputs.taxi}}_tripdata_{{trigger.date | date('yyyy-MM')}}.csv"`

## Question 3

**Question:** How many rows are there for the `Yellow` Taxi data for all CSV files in the year 2020?

```sql
SELECT COUNT(*) AS total_rows
FROM `sample-project.sample_dataset.yellow_tripdata`
WHERE filename LIKE '%2020%'
```

## Question 4

**Question:** How many rows are there for the `Green` Taxi data for all CSV files in the year 2020?

```sql
SELECT COUNT(*) AS total_rows
FROM `sample-project.sample_dataset.green_tripdata`
WHERE filename LIKE '%2020%'
```

## Question 5

**Question:** How many rows are there for the `Yellow` Taxi data for the March 2021 CSV file?

Check out `sample_dataset.yellow_tripdata_2021_03` and look for **Details - Storage info - Number of Rows**

## Question 6

**Question:** How would you configure the timezone to New York in a Schedule trigger?

In Kestra, a Schedule trigger defines when a workflow should run. The `timezone` property determines the local time that the schedule should follow. Using `America/New_York` is the official IANA timezone identifier for New York.

- Using `EST` or `UTC-5` is not recommended because they are ambiguous and may not account for Daylight Saving Time.

- The `location` property does not exist in Kestra for timezones.

By specifying `timezone: America/New_York`, the workflow will automatically adjust for Eastern Standard Time (EST) and Eastern Daylight Time (EDT), ensuring that scheduled runs occur at the correct local time throughout the year.