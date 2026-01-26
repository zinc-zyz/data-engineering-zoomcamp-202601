# Data Engineering Zoomcamp Week 1 Homework 

This is my homework in learning Docker + Postgres, Data Analysis (SQL) and Terraform configuration. Let's dive into it!

## Question 1: Understanding Docker images

**Question:** What's the version of pip in the python:3.13 image?

```bash
docker pull python:3.13
docker run --rm python:3.13 pip --version
```

## Question 2: Understanding Docker networking and docker-compose

**Reference file:** `Given the docker-compose.yaml, what is the hostname and port that pgadmin should use to connect to the postgres database?`

**Question:** What's the version of pip in the python:3.13 image?

**docker-compose.yaml services:**
- Postgres service name: `pgdatabase`
- Postgres internal port: `5432`

**Explanation:**
- Service name: db → used as hostname  
- Internal port: 5432 → used for container-to-container connections  
- Host port 5433 is only for connections from the host machine, not for pgAdmin inside Compose  

## Prerequisites for SQL: Setting up Docker Container and PostgreSQL database for Data Preparation

```bash
docker run -it --rm \
  -e POSTGRES_USER="postgres" \
  -e POSTGRES_PASSWORD="postgres" \
  -e POSTGRES_DB="ny_taxi" \
  -v vol-pgdata:/var/lib/postgresql/data \
  -p 5433:5432 \
  postgres:17-alpine
```

Run this in new terminal:
```bash
uv run pgcli -h localhost -p 5433 -u postgres -d ny_taxi
```

**Data Ingestion**
**Reference file:** `data/ingest_data.py`

## Question 3: Counting short trips

**Question:** For the trips in November 2025 (lpep_pickup_datetime between '2025-11-01' and '2025-12-01', exclusive of the upper bound), how many trips had a trip_distance of less than or equal to 1 mile?

**SQL Query:**
```sql
SELECT COUNT(*) FROM green_taxi_data_202511 WHERE lpep_pickup_datetime >= '2025-11-01' AND lpep_pickup_datetime < '2025-12-01' AND trip_distance <= 1;
```


## Question 4: Longest trip for each day

**Question:** Which was the pick up day with the longest trip distance? Only consider trips with trip_distance less than 100 miles (to exclude data errors).

Use the pick up time for your calculations.

**SQL Query:**
```sql
SELECT lpep_pickup_datetime::date AS pickup_day,
       trip_distance
FROM green_taxi_data_202511
WHERE lpep_pickup_datetime >= '2025-11-01'
  AND lpep_pickup_datetime < '2025-12-01'
  AND trip_distance < 100
ORDER BY trip_distance DESC
LIMIT 1;
```


## Question 5: Biggest pickup zone

**Question:** Which was the pickup zone with the largest total_amount (sum of all trips) on November 18th, 2025?

**SQL Query:**
```sql
SELECT t."Zone" AS pickup_zone,
       SUM(g.total_amount) AS total_amount_sum
FROM green_taxi_data_202511 AS g
INNER JOIN taxi_zone_data AS t
  ON g."PULocationID" = t."LocationID"
WHERE g."lpep_pickup_datetime" >= '2025-11-18'
  AND g."lpep_pickup_datetime" < '2025-11-19'
GROUP BY t."Zone"
ORDER BY total_amount_sum DESC
LIMIT 1;
```



## Question 6: Largest Tip

**Question:** For the passengers picked up in the zone named "East Harlem North" in November 2025, which was the drop off zone that had the largest tip?

Note: it's tip , not trip. We need the name of the zone, not the ID.

**SQL Query:**
```sql
SELECT dz."Zone" AS dropoff_zone,
        MAX(g.tip_amount) AS total_tip
FROM green_taxi_data_202511 AS g
INNER JOIN taxi_zone_data AS pz
  ON g."PULocationID" = pz."LocationID"
INNER JOIN taxi_zone_data AS dz
  ON g."DOLocationID" = dz."LocationID"
WHERE pz."Zone" = 'East Harlem North'
  AND g."lpep_pickup_datetime" >= '2025-11-01'
  AND g."lpep_pickup_datetime" < '2025-12-01'
GROUP BY dz."Zone"
ORDER BY total_tip DESC
LIMIT 1;
```


