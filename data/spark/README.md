# Spark

Isolated Spark experiments, one folder each.  
They share nothing and can be run in any order.

```text
.
├── graphx/       GraphFrames: distances per node + LoL item cost with Pregel (own README)
├── notebooks/    lab-liquid-clustering.ipynb: Delta CLUSTER BY, size and files before vs after (Databricks)
├── samples/      tiny mock CSVs used by the scripts (Springfield transactions, Duff Beer sales)
└── scripts/      high_order_functions.py and positional_file.py (PySpark 4.1.1, uv)
```

Python code shares one uv project (`pyproject.toml` in this folder), run it with `uv run` from here or from any folder below it.

<details>
<summary><b>high order functions</b></summary>

```bash
(cd data/spark && uv run spark-submit scripts/high_order_functions.py)
```

**Expected Output 👇**
```text
+-------------+--------------+--------+-------------------------------------------------+
|name_origin  |n_transactions|n_frauds|transactions                                     |
+-------------+--------------+--------+-------------------------------------------------+
|Homer Simpson|3             |1       |[{CASH_OUT, 50.0, false}, {PAYMENT, 10.0, false}]|
|Bart Simpson |2             |1       |[{DEBIT, 15.0, false}]                           |
+-------------+--------------+--------+-------------------------------------------------+
```

> [Databricks: Higher-order functions](https://docs.databricks.com/optimizations/higher-order-lambda-functions.html) / 
> [Databricks: Working with Nested Data Using Higher Order Functions in SQL](https://www.databricks.com/blog/2017/05/24/working-with-nested-data-using-higher-order-functions-in-sql-on-databricks.html)

</details>

<br/>

<details>
<summary><b>positional file</b></summary>

Writes a single fixed-width (positional) file from `samples/duff_sales.csv` (Duff Beer sales per bar). Spark writes a folder with one part file, so the command renames it to `data/DUFF_SALES.TXT`.

```bash
(cd data/spark \
  && uv run spark-submit scripts/positional_file.py \
  && mv data/duff_sales/*.txt data/DUFF_SALES.TXT \
  && rm -rf data/duff_sales)
```

**Expected Output 👇** (`data/DUFF_SALES.TXT`)
```text
201501040000000001000043502149     BARNEY'S BOWL-A-RAMA
201501040000000001790000137395             DUFF GARDENS
201501040000000001220004087328             MOE'S TAVERN
201501110000000001350000125000              KWIK-E-MART
201501110000000002100000009840              LENNY'S PUB
201501110000000000980000751250             MOE'S TAVERN
```

</details>

<br/>

<details>
<summary><b>liquid clustering</b></summary>

Delta Lake liquid clustering: compares table size and files before and after `CLUSTER BY` on airline data. Databricks notebook, not meant to run locally.

1. Import `notebooks/lab-liquid-clustering.ipynb` into a Databricks workspace and attach it to a cluster.
2. Change the schema in the SQL cells (`anthony_caliani`) to one you own. The notebook creates it and drops its `airlines_delta*` tables.
3. Run all cells. It reads `/databricks-datasets/asa/airlines/` (22 CSVs, 1987 to 2008).

> [Delta: Liquid Clustering](https://delta.io/blog/liquid-clustering/) /
> [Delta: Optimize](https://delta.io/blog/delta-lake-optimize/) /
> [Databricks: Delta Lake transaction log](https://www.databricks.com/blog/2019/08/21/diving-into-delta-lake-unpacking-the-transaction-log.html) /
> [Databricks: Datasets](https://docs.databricks.com/aws/en/discover/databricks-datasets)

</details>
