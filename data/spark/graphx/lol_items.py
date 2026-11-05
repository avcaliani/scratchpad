"""
GraphFrames + Pregel: total cost of each League of Legends item.

The items form a graph: an edge `src -> dst` means "dst is built with `amount` units of src".
Rule: total_cost = cost + sum(component total_cost * amount). A "Basic" item has no components,
so its total_cost is its own cost. The target is "Sunfire Aegis".

Diagram: .docs/lol-graph.png (editable source: .docs/graphs.excalidraw)

Notes:
- GraphFrames needs a column called "id", so the item name is the "id".
- Since GraphFrames 0.12, messages only see the edge columns declared with `required_edge_columns`.
- The GraphFrames jar comes from `spark.jars.packages`, so the first run needs internet access.

Run: uv run python lol_items.py
"""
import tempfile

from graphframes import GraphFrame
from graphframes.lib import Pregel
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as f

EXPECTED_TOTALS = {
    'Ruby Crystal': 400,
    'Cloth Armor': 300,
    "Bami's Cinder": 1000,
    'Chain Vest': 800,
    'Sunfire Aegis': 2700,
}


def spark_session() -> SparkSession:
    spark = SparkSession.builder \
        .master('local[*]') \
        .appName('graphx-lol-items') \
        .config('spark.jars.packages', 'io.graphframes:graphframes-spark4_2.13:0.12.3') \
        .getOrCreate()
    spark.sparkContext.setLogLevel('ERROR')
    spark.sparkContext.setCheckpointDir(tempfile.mkdtemp(prefix='graphx-checkpoints-'))
    return spark


def build_graph(spark: SparkSession) -> GraphFrame:
    items = spark.createDataFrame(
        data=[
            ('Ruby Crystal', 'Basic', 400),
            ("Bami's Cinder", 'Epic', 200),
            ('Cloth Armor', 'Basic', 300),
            ('Chain Vest', 'Epic', 500),
            ('Sunfire Aegis', 'Legendary', 900),
        ],
        schema=['id', 'rarity', 'cost'],
    )
    items_relation = spark.createDataFrame(
        data=[
            ('Ruby Crystal', "Bami's Cinder", 2),
            ('Cloth Armor', 'Chain Vest', 1),
            ("Bami's Cinder", 'Sunfire Aegis', 1),
            ('Chain Vest', 'Sunfire Aegis', 1),
        ],
        schema=['src', 'dst', 'amount'],
    )
    return GraphFrame(v=items, e=items_relation)


def calculate_total_cost(graph: GraphFrame) -> DataFrame:
    components_cost = Pregel.src('previous_items_cost') + Pregel.src('cost')
    return (
        graph.pregel
        .setMaxIter(3)
        .required_edge_columns('amount')
        .withVertexColumn(
            colName='previous_items_cost',
            initialExpr=f.lit(0),
            updateAfterAggMsgsExpr=Pregel.msg(),
        )
        .sendMsgToDst(
            f.when(Pregel.src('previous_items_cost').isNotNull(), components_cost)
            .otherwise(Pregel.src('cost')) * Pregel.edge('amount')
        )
        .aggMsgs(f.sum(Pregel.msg()))
        .withVertexColumn(
            colName='total_cost',
            initialExpr=f.lit(0),
            updateAfterAggMsgsExpr=f.col('cost') + f.coalesce(f.col('previous_items_cost'), f.lit(0)),
        )
        .run()
    )


def main() -> None:
    spark = spark_session()
    graph = build_graph(spark)
    graph.vertices.show()
    graph.edges.show()

    result = calculate_total_cost(graph)
    result.show(truncate=False)

    totals = {row['id']: row['total_cost'] for row in result.collect()}
    assert totals == EXPECTED_TOTALS, f'unexpected totals: {totals}'
    spark.stop()


if __name__ == '__main__':
    main()
