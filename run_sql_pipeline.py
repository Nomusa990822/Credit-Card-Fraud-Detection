# run_sql_pipeline.py

from pathlib import Path

from src.sql_utils import SQLRunner


PROJECT_ROOT = Path(".")
DB_PATH = "artifacts/fraud.db"

TRAIN_PATH = "data/raw/train.csv"
TEST_PATH = "data/raw/test.csv"

SQL_DIR = PROJECT_ROOT / "sql"
OUTPUT_DIR = PROJECT_ROOT / "artifacts/sql_outputs"


def main():
    print("=" * 50)
    print("Starting SQL Pipeline")
    print("=" * 50)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with SQLRunner(db_path=DB_PATH, project_root=PROJECT_ROOT) as runner:

        print("\n[1] Loading data into DuckDB...")
        runner.load_csvs_to_tables(
            train_csv=TRAIN_PATH,
            test_csv=TEST_PATH,
        )

        print("[OK] Data loaded")

        print("\n[2] Creating SQL views...")
        runner.run_sql_file("sql/fraud_summary_views.sql", return_last_select=False)
        print("[OK] Views created")

        print("\n[3] Running SQL analyses...\n")

        sql_jobs = [
            ("target_distribution.sql", "target_distribution.csv"),
            ("amount_analysis.sql", "amount_analysis.csv"),
            ("demographic_analysis.sql", "demographic_analysis.csv"),
            ("geographic_analysis.sql", "geographic_analysis.csv"),
            ("category_analysis.sql", "category_analysis.csv"),
            ("merchant_analysis.sql", "merchant_analysis.csv"),
            ("temporal_analysis.sql", "temporal_analysis.csv"),
        ]

        for sql_file, output_file in sql_jobs:
            sql_path = SQL_DIR / sql_file
            output_path = OUTPUT_DIR / output_file

            print(f"Running: {sql_file}")

            try:
                df = runner.run_sql_file(sql_path, return_last_select=True)

                if df is not None:
                    runner.export_df(df, output_path)
                    print(f"[OK] Saved → {output_path}")
                else:
                    print(f"[WARNING] No output returned for {sql_file}")

            except Exception as e:
                print(f"[ERROR] Failed: {sql_file}")
                print(f"Reason: {e}")

        print("\n[4] Pipeline completed successfully")

    print("\nDatabase saved at:", DB_PATH)
    print("Outputs saved in:", OUTPUT_DIR)
    print("=" * 50)


if __name__ == "__main__":
    main()
