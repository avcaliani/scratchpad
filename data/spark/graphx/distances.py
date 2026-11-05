"""
GraphFrames: distances challenge.

Calculate, for each node in the tree, the sum of `distance (edge) * multiplier (vertex)`.
Edges count on the node they arrive at, with that node's multiplier.
Example, node 4: 12.0 * 1.0 + 8.0 * 1.0 = 20.0

Diagram: .docs/basic-graph.png (editable source: .docs/graphs.excalidraw)

Notes:
- GraphFrames needs a column called "id" on the vertices.
- The GraphFrames jar comes from `spark.jars.packages`, so the first run needs internet access.

Run: uv run python distances.py
"""
from graphframes import GraphFrame
from graphframes.lib import AggregateMessages as AM
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as f

EXPECTED_DISTANCES = {1: 0.0, 2: 7.5, 3: 14.0, 4: 20.0}


def spark_session() -> SparkSession:
    spark = SparkSession.builder \
        .master('local[*]') \
        .appName('graphx-distances') \
        .config('spark.jars.packages', 'io.graphframes:graphframes-spark4_2.13:0.12.3') \
        .getOrCreate()
    spark.sparkContext.setLogLevel('ERROR')
    return spark


def build_graph(spark: SparkSession) -> GraphFrame:
    vertices = spark.createDataFrame(
        data=[(1, 1.0), (2, 1.5), (3, 2.0), (4, 1.0)],
        schema=['id', 'multiplier'],
    )
    edges = spark.createDataFrame(
        data=[(1, 2, 5.0), (1, 3, 7.0), (2, 4, 12.0), (3, 4, 8.0)],
        schema=['src', 'dst', 'distance'],
    )
    return GraphFrame(vertices, edges)


def calculate_distances(graph: GraphFrame) -> DataFrame:
    messages = graph.aggregateMessages(
        f.sum(AM.msg).alias('total_distance'),
        sendToDst=AM.edge['distance'] * AM.dst['multiplier'],
    )
    return (
        graph.vertices
        .join(messages, on='id', how='left')
        .withColumn('total_distance', f.coalesce('total_distance', f.lit(0.0)))
        .orderBy('id')
    )


def main() -> None:
    spark = spark_session()
    graph = build_graph(spark)
    graph.vertices.show()
    graph.edges.show()

    result = calculate_distances(graph)
    result.show()

    distances = {row['id']: row['total_distance'] for row in result.collect()}
    assert distances == EXPECTED_DISTANCES, f'unexpected distances: {distances}'
    spark.stop()


if __name__ == '__main__':
    main()
