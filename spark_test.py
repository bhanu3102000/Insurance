"""Small session standalone Spark join job with time to inspect the Spark UI."""

import argparse
import time

from pyspark.sql import SparkSession


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--hold-seconds", type=int, default=3600)
    args = parser.parse_args()

    spark = (
        SparkSession.builder.appName("EmployeeDepartmentJoinDemo")
        .config("spark.sql.shuffle.partitions", "4")
        .config("spark.sql.autoBroadcastJoinThreshold", "-1")
        .config("spark.sql.adaptive.enabled", "false")
        .getOrCreate()
    )

    try:
        employees_df = spark.createDataFrame(
            [
                (101, "Alice", 1, 120000),
                (102, "Bob", 1, 95000),
                (103, "Carol", 2, 90000),
                (104, "David", 2, 85000),
                (105, "Eva", 3, 100000),
                (106, "Frank", 99, 75000),
            ],
            ["employee_id", "employee_name", "department_id", "salary"],
        )
        departments_df = spark.createDataFrame(
            [(1, "Engineering"), (2, "Analytics"), (3, "Finance")],
            ["department_id", "department_name"],
        )

        joined_df = employees_df.join(departments_df, "department_id", "inner")

        print("\n=== Join physical plan ===", flush=True)
        joined_df.explain("formatted")
        print("\n=== Executing join ===", flush=True)
        #joined_df.show(truncate=False)
        print(f"Joined rows: {joined_df.count()}", flush=True)

        print(f"\nSpark application ID: {spark.sparkContext.applicationId}", flush=True)
        print(f"Spark application UI: {spark.sparkContext.uiWebUrl}", flush=True)
        print(
            f"Keeping the job alive for {args.hold_seconds} seconds. "
            "Open the application UI and inspect SQL, Jobs, and Stages.",
            flush=True,
        )
        remaining = max(args.hold_seconds, 0)
        try:
            while remaining > 0:
                interval = min(60, remaining)
                time.sleep(interval)
                remaining -= interval
                print(f"Spark UI still available; {remaining} seconds remaining.", flush=True)
        except KeyboardInterrupt:
            print("Stopping the Spark application.", flush=True)
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
