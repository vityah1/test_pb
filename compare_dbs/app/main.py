import os
# import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit
from functools import reduce


def create_spark_session():
    return SparkSession.builder \
        .appName("WarehouseInventoryComparison") \
        .config("spark.jars", "/app/postgresql-42.2.23.jar") \
        .getOrCreate()


def read_data_from_db(spark, db_url, table_name, properties):
    print(f"Attempting to connect to database: {db_url}")
    print(f"Using properties: {properties}")
    return spark.read.jdbc(url=db_url, table=table_name, properties=properties)


def compare_inventories(df1, df2):
    # Items in warehouse 1 but not in warehouse 2
    items_only_in_wh1 = df1.join(df2, "ProductId", "left_anti") \
        .select("ProductId", "ProductName", "qty", "TotalCost")

    # Items in warehouse 2 but not in warehouse 1
    items_only_in_wh2 = df2.join(df1, "ProductId", "left_anti") \
        .select("ProductId", "ProductName", "qty", "TotalCost")

    # Items with different properties
    property_columns = [f"ProductProperty{i}" for i in range(1, 11)] + ["qty", "price", "TotalCost"]

    df2_renamed = df2.select(
        ["ProductId"] +
        [col(c).alias(f"{c}_2") for c in property_columns]
    )

    diff_properties = df1.join(df2_renamed, "ProductId", "inner")

    diff_list = []
    for prop in property_columns:
        diff = diff_properties.filter(col(prop) != col(f"{prop}_2")) \
            .select(
            "ProductId",
            lit(prop).alias("PropertyName"),
            col(prop).alias("Value1"),
            col(f"{prop}_2").alias("Value2")
        )
        diff_list.append(diff)

    # Use reduce with a lambda function to union all DataFrames in diff_list
    diff_properties = reduce(lambda acc, x: acc.union(x), diff_list)

    return items_only_in_wh1, items_only_in_wh2, diff_properties


def save_to_csv(df, filename):
    # Convert Spark DataFrame to Pandas DataFrame
    pandas_df = df.toPandas()

    # Save to CSV
    pandas_df.to_csv(filename, index=False)
    print(f"Saved results to {filename}")


def main():
    print("Starting main function")
    spark = create_spark_session()

    # Database connection properties
    db_properties = {
        "user": os.environ.get("POSTGRES_USER"),
        "password": os.environ.get("POSTGRES_PASSWORD"),
        "driver": "org.postgresql.Driver"
    }

    # Read data from both warehouses
    db1_url = f"jdbc:postgresql://{os.environ.get('POSTGRES_HOST_DB1')}:{os.environ.get('POSTGRES_PORT1')}/{os.environ.get('POSTGRES_DB1')}"
    db2_url = f"jdbc:postgresql://{os.environ.get('POSTGRES_HOST_DB2')}:{os.environ.get('POSTGRES_PORT2')}/{os.environ.get('POSTGRES_DB2')}"

    print(f"DB1 URL: {db1_url}")
    print(f"DB2 URL: {db2_url}")

    try:
        print("Attempting to read from DB1")
        df_wh1 = read_data_from_db(spark, db1_url, "inventory", db_properties)
        print("Successfully read from DB1")

        print("Attempting to read from DB2")
        df_wh2 = read_data_from_db(spark, db2_url, "inventory", db_properties)
        print("Successfully read from DB2")

        # Compare inventories
        items_only_in_wh1, items_only_in_wh2, diff_properties = compare_inventories(df_wh1, df_wh2)

        # Save results to CSV files
        save_to_csv(items_only_in_wh1, "/app/output/items_only_in_wh1.csv")
        save_to_csv(items_only_in_wh2, "/app/output/items_only_in_wh2.csv")
        save_to_csv(diff_properties, "/app/output/items_with_diff_properties.csv")

        print("Data processing completed successfully")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

    spark.stop()
    print("Main function completed")


if __name__ == "__main__":
    main()
