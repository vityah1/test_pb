import os
from typing import Tuple, Dict
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import col, lit
from functools import reduce


def create_spark_session() -> SparkSession:
    return SparkSession.builder \
        .appName("WarehouseInventoryComparison") \
        .config("spark.jars", "/app/postgresql-42.2.23.jar") \
        .getOrCreate()


def read_data_from_db(spark: SparkSession, db_url: str, table_name: str, properties: Dict[str, str]) -> DataFrame:
    print(f"Attempting to connect to database: {db_url}")
    print(f"Using properties: {properties}")
    return spark.read.jdbc(url=db_url, table=table_name, properties=properties)


def compare_inventories(df1: DataFrame, df2: DataFrame) -> Tuple[DataFrame, DataFrame, DataFrame]:
    items_only_in_wh1 = df1.join(df2, "ProductId", "left_anti") \
        .select("ProductId", "ProductName", "qty", "TotalCost")

    items_only_in_wh2 = df2.join(df1, "ProductId", "left_anti") \
        .select("ProductId", "ProductName", "qty", "TotalCost")

    property_columns = [f"ProductProperty{i}" for i in range(1, 11)] + ["qty", "price", "TotalCost"]

    df2_renamed = df2.select(
        ["ProductId"] +
        [col(c).alias(f"{c}_2") for c in property_columns]
    )

    diff_properties = df1.join(df2_renamed, "ProductId", "inner")

    diff_list = [
        diff_properties.filter(col(prop) != col(f"{prop}_2"))
        .select(
            "ProductId",
            lit(prop).alias("PropertyName"),
            col(prop).alias("Value1"),
            col(f"{prop}_2").alias("Value2")
        )
        for prop in property_columns
    ]

    # Use reduce with a lambda function to union all DataFrames in diff_list
    diff_properties = reduce(lambda acc, x: acc.union(x), diff_list)

    return items_only_in_wh1, items_only_in_wh2, diff_properties


def get_db_properties() -> Dict[str, str]:
    return {
        "user": os.environ["POSTGRES_USER"],
        "password": os.environ["POSTGRES_PASSWORD"],
        "driver": "org.postgresql.Driver"
    }


def get_db_url(host: str, port: str, db_name: str) -> str:
    return f"jdbc:postgresql://{host}:{port}/{db_name}"


def save_to_csv(df: DataFrame, filename: str) -> None:
    # Convert Spark DataFrame to Pandas DataFrame
    pandas_df = df.toPandas()

    # Save to CSV
    pandas_df.to_csv(filename, index=False)
    print(f"Saved results to {filename}")


def main() -> None:
    print("Starting main function")
    spark = create_spark_session()

    db_properties = get_db_properties()

    db1_url = get_db_url(
        os.environ["POSTGRES_HOST_DB1"],
        os.environ["POSTGRES_PORT1"],
        os.environ["POSTGRES_DB1"]
    )
    db2_url = get_db_url(
        os.environ["POSTGRES_HOST_DB2"],
        os.environ["POSTGRES_PORT2"],
        os.environ["POSTGRES_DB2"]
    )

    print(f"DB1 URL: {db1_url}")
    print(f"DB2 URL: {db2_url}")

    try:
        df_wh1 = read_data_from_db(spark, db1_url, "inventory", db_properties)
        print("Successfully read from DB1")

        df_wh2 = read_data_from_db(spark, db2_url, "inventory", db_properties)
        print("Successfully read from DB2")

        items_only_in_wh1, items_only_in_wh2, diff_properties = compare_inventories(df_wh1, df_wh2)

        save_to_csv(items_only_in_wh1, "/app/output/items_only_in_wh1.csv")
        save_to_csv(items_only_in_wh2, "/app/output/items_only_in_wh2.csv")
        save_to_csv(diff_properties, "/app/output/items_with_diff_properties.csv")

        print("Data processing completed successfully")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        spark.stop()
        print("Main function completed")


if __name__ == "__main__":
    main()
