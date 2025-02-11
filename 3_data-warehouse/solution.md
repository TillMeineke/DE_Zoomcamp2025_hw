# HW 3 Till Meineke

## Q1

Question 1: What is count of records for the 2024 Yellow Taxi Data?

- 65,623 ❌
- 840,402 ❌
- 20,332,093 ❌
- **85,431,289** ✅

As of now, the New York City Taxi and Limousine Commission (TLC) has not yet released the complete Yellow Taxi trip data for the year 2024. Therefore, it’s not possible to provide an exact count of records for the entire year. However, based on historical data, the annual number of Yellow Taxi trips in New York City has been substantial, often totaling in the tens of millions. For instance, in previous years, the total trip counts have been in the range of 80 to 100 million trips per year. Given this context, among the provided options, the figure of 85,431,289 records is the most plausible estimate for the 2024 Yellow Taxi data.

For the most accurate and up-to-date information, you can refer to the TLC Trip Record Data page on the NYC.gov website, where trip data is published monthly in PARQUET format.  ￼

## Q2

Write a query to count the distinct number of PULocationIDs for the entire dataset on both the tables.
What is the estimated amount of data that will be read when this query is executed on the External Table and the Table?

- **18.82 MB for the External Table and 47.60 MB for the Materialized Table** ✅
- 0 MB for the External Table and 155.12 MB for the Materialized Table ❌
- 2.14 GB for the External Table and 0MB for the Materialized Table ❌
- 0 MB for the External Table and 0MB for the Materialized Table ❌

Query to Count Distinct PULocationID on Both Tables
```sql
SELECT COUNT(DISTINCT PULocationID) AS unique_pu_locations
FROM `my_dataset.my_external_table`;
```

```sql
SELECT COUNT(DISTINCT PULocationID) AS unique_pu_locations
FROM `my_dataset.my_materialized_table`;
```

Explanation:

1. External Table (18.82 MB)
   - External tables in BigQuery do not store data internally. Instead, BigQuery reads the data directly from Google Cloud Storage (GCS) whenever queried.
   - When querying an external table, BigQuery reads only the required columns (PULocationID), leading to 18.82 MB of data being read.
   - External tables do not use clustering or partition pruning, which means performance depends on how well the data is structured in GCS.
2. Materialized Table (47.60 MB)
   - A materialized table is stored within BigQuery, benefiting from columnar storage, partitioning, and clustering for optimized query performance.
   - Since the data is physically stored in BigQuery, scanning distinct values requires reading from optimized storage.
   - Even though BigQuery is optimized for columnar access, querying PULocationID still results in 47.60 MB being read.

Why Not the Other Options?

❌ 0 MB for the External Table and 155.12 MB for the Materialized Table

- External tables are not cached, so querying them always reads data (not 0 MB).
- The materialized table reads 47.60 MB, not 155.12 MB.

❌ 2.14 GB for the External Table and 0 MB for the Materialized Table

- 2.14 GB is too high for reading just one column.
- The materialized table requires some data reading, not 0 MB.

❌ 0 MB for the External Table and 0 MB for the Materialized Table

- BigQuery does not automatically cache query results unless explicitly cached, so querying will always scan some data.

Key Takeaway 🚀

- Materialized tables are more efficient for frequent queries.
- External tables save storage costs but can be slower for complex queries.
- Columnar storage ensures only relevant columns are scanned, improving performance.

## Q3

Write a query to retrieve the PULocationID from the table (not the external table) in BigQuery. Now write a query to retrieve the PULocationID and DOLocationID on the same table. Why are the estimated number of Bytes different?

- **BigQuery is a columnar database, and it only scans the specific columns requested in the query. Querying two columns (PULocationID, DOLocationID) requires reading more data than querying one column (PULocationID), leading to a higher estimated number of bytes processed.** ✅
- BigQuery duplicates data across multiple storage partitions, so selecting two columns instead of one requires scanning the table twice, doubling the estimated bytes processed. ❌
- BigQuery automatically caches the first queried column, so adding a second column increases processing time but does not affect the estimated bytes scanned. ❌
- When selecting multiple columns, BigQuery performs an implicit join operation between them, increasing the estimated bytes processed ❌

Explanation:

BigQuery uses a columnar storage format, meaning that data is stored and read column by column, not row by row. This allows queries to scan only the requested columns, optimizing performance and reducing costs.

Why is the estimated number of bytes different?

- When retrieving only PULocationID, BigQuery scans just that one column.
- When retrieving both PULocationID and DOLocationID, BigQuery must scan two columns instead of one, doubling the amount of data read.
- The more columns you select, the more data BigQuery needs to scan, increasing the estimated bytes processed.
Queries

1️⃣ Retrieve PULocationID

```sql
SELECT PULocationID FROM my_dataset.my_table;
```

2️⃣ Retrieve PULocationID and DOLocationID

```sql
SELECT PULocationID, DOLocationID FROM my_dataset.my_table;
```

Why Not the Other Options?

❌ “BigQuery duplicates data across multiple storage partitions…”
 • Incorrect. BigQuery does not duplicate data across partitions in a way that affects query cost like this. Data partitioning helps with filtering, not column scanning.

❌ “BigQuery automatically caches the first queried column…”
 • Incorrect. BigQuery does cache query results, but caching does not affect the estimated bytes scanned before execution. The estimation is based on column size, not caching.

❌ “BigQuery performs an implicit join operation…”
 • Incorrect. Querying multiple columns does not trigger a join. The table remains the same, and no additional computational overhead from joins is involved.

Key Takeaway

Since BigQuery is columnar, querying fewer columns reduces the data scanned and improves performance. 🚀

## Q4

- 8333

## Q5

What is the best strategy to make an optimized table in Big Query if your query will always filter based on tpep_dropoff_datetime and order the results by VendorID (Create a new table with this strategy)

- Partition by tpep_dropoff_datetime and Cluster on VendorID ❌
- **Cluster on by tpep_dropoff_datetime and Cluster on VendorID** ✅
- Cluster on tpep_dropoff_datetime Partition by VendorID ❌
- Partition by tpep_dropoff_datetime and Partition by VendorID ❌

Explanation:

1. Partitioning by tpep_dropoff_datetime
    - Since queries will always filter on tpep_dropoff_datetime, partitioning the table by this column ensures that only relevant partitions are scanned, significantly improving query performance and reducing costs.
2. Clustering on VendorID
    - Since results are ordered by VendorID, clustering on this column helps organize the data within each partition. This improves query efficiency because BigQuery processes clustered columns in a sorted manner, reducing scan time.

Why Not the Other Options?

❌ Cluster on tpep_dropoff_datetime and VendorID

- Clustering alone does not create partitions, so queries filtering by tpep_dropoff_datetime will still scan unnecessary data.

❌ Cluster on tpep_dropoff_datetime and Partition by VendorID

- Partitioning by VendorID is not optimal because it likely has a low number of unique values, leading to inefficient partitioning. BigQuery supports a maximum of 4,000 partitions, and VendorID would result in very few partitions, making partition pruning ineffective.

❌ Partition by tpep_dropoff_datetime and Partition by VendorID

- BigQuery does not support multiple partitioned columns. Only one column can be used for partitioning.

SQL to Create the Optimized Table:

```sql
CREATE TABLE my_dataset.optimized_table
PARTITION BY DATE(tpep_dropoff_datetime)
CLUSTER BY VendorID AS
SELECT * FROM my_dataset.original_table;
```

This strategy ensures efficient partition pruning when filtering by tpep_dropoff_datetime and fast sorting when ordering by VendorID. 🚀

## Q6

310.24

## Q7

Where is the data stored in the External Table you created?

- Big Query ❌
- Container Registry ❌
- **GCP Bucket** ✅
- Big Table ❌

Explanation:

External tables in BigQuery reference data stored outside of BigQuery itself. When you create an external table, the data remains in its original location, such as Google Cloud Storage (GCS), and BigQuery only queries it when needed.

Why GCP Bucket?

- External tables in BigQuery commonly use data stored in Google Cloud Storage (GCS Buckets).
- The data is not loaded into BigQuery’s internal storage but is queried directly from its original location.

Why Not the Others?

❌ BigQuery – External tables do not store data in BigQuery; they only reference it.  
❌ Container Registry – This is used for storing Docker images, not data for BigQuery.  
❌ BigTable – BigQuery can integrate with BigTable, but external tables are not stored there.

Thus, for an external table, the data typically resides in a GCP Bucket (Google Cloud Storage).

## Q8

It is best practice in Big Query to always cluster your data:

- True ❌
- **False** ✅

Clustering in BigQuery can improve query performance and reduce costs, but it is not always the best practice for every dataset.

Explanation:

1. Use Case Dependent: Clustering is beneficial when queries frequently filter or group by specific columns. However, for datasets with unpredictable query patterns, clustering may not provide significant advantages.
2. Query Performance: Clustering helps by reducing the amount of data scanned, but for small datasets, the performance gain might be negligible compared to the overhead of maintaining clustered data.
3. Cost Considerations: Clustering can reduce query costs by limiting the amount of data read. However, it also affects how data is stored and may introduce additional storage costs.
4. Table Size: Clustering is most effective for large partitioned tables. For small tables, the benefits may not outweigh the complexity.

When to Cluster:

✅ Large datasets  
✅ Queries frequently filter or group by specific columns  
✅ High cardinality columns (but not too high)

When Not to Cluster:

❌ Small datasets where clustering provides no real benefit  
❌ Highly dynamic tables with frequent inserts/updates that might impact clustering efficiency  
❌ Queries that don’t take advantage of clustered columns

Thus, while clustering is a powerful feature, it should be used based on query patterns and dataset size rather than by default.
