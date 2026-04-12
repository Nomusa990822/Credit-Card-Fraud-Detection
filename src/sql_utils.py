from __future__ import annotations

from pathlib import Path
from typing import Iterable, Optional

import duckdb
import pandas as pd


class SQLPipelineError(Exception):
    """Raised when the SQL pipeline encounters a recoverable project-level error."""


class SQLRunner:
    """
    Utility class for running project SQL files against DuckDB.

    Typical usage:
        runner = SQLRunner(db_path="fraud.db", project_root=".")
        runner.load_csvs_to_tables(
            train_csv="data/raw/train.csv",
            test_csv="data/raw/test.csv",
        )
        result = runner.run_sql_file("sql/target_distribution.sql")
        runner.export_df(result, "artifacts/target_distribution.csv")
        runner.close()
    """

    def __init__(
        self,
        db_path: str | Path = ":memory:",
        project_root: str | Path = ".",
        read_only: bool = False,
    ) -> None:
        self.project_root = Path(project_root).resolve()
        self.db_path = str(db_path)
        self.con = duckdb.connect(database=self.db_path, read_only=read_only)

    def close(self) -> None:
        """Close the DuckDB connection."""
        try:
            self.con.close()
        except Exception:
            pass

    def __enter__(self) -> "SQLRunner":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

    def _resolve_path(self, path: str | Path) -> Path:
        path = Path(path)
        if path.is_absolute():
            return path
        return (self.project_root / path).resolve()

    def _read_sql_text(self, sql_path: str | Path) -> str:
        resolved = self._resolve_path(sql_path)
        if not resolved.exists():
            raise FileNotFoundError(f"SQL file not found: {resolved}")
        return resolved.read_text(encoding="utf-8")

    def execute_sql(self, sql: str) -> None:
        """
        Execute one or more SQL statements that do not need a returned dataframe.
        Useful for CREATE TABLE, CREATE VIEW, DROP TABLE, etc.
        """
        self.con.execute(sql)

    def query_sql(self, sql: str) -> pd.DataFrame:
        """
        Execute a SQL query and return the result as a pandas DataFrame.
        """
        return self.con.execute(sql).df()

    def run_sql_file(
        self,
        sql_path: str | Path,
        return_last_select: bool = True,
    ) -> Optional[pd.DataFrame]:
        """
        Run a SQL file.

        Parameters
        ----------
        sql_path:
            Path to the .sql file.
        return_last_select:
            If True, attempts to return a dataframe from the final statement.
            If False, executes the file and returns None.

        Notes
        -----
        - Use return_last_select=False for files like schema.sql or fraud_summary_views.sql.
        - Use return_last_select=True for analytical query files that end in a SELECT.
        """
        sql_text = self._read_sql_text(sql_path)

        if not return_last_select:
            self.execute_sql(sql_text)
            return None

        return self.query_sql(sql_text)

    def table_exists(self, table_name: str) -> bool:
        """
        Check whether a table exists in the current DuckDB connection.
        """
        query = f"""
        SELECT COUNT(*) AS n
        FROM information_schema.tables
        WHERE table_name = '{table_name}'
        """
        result = self.query_sql(query)
        return bool(result.loc[0, "n"] > 0)

    def view_exists(self, view_name: str) -> bool:
        """
        Check whether a view exists in the current DuckDB connection.
        """
        query = f"""
        SELECT COUNT(*) AS n
        FROM information_schema.views
        WHERE table_name = '{view_name}'
        """
        result = self.query_sql(query)
        return bool(result.loc[0, "n"] > 0)

    def load_csvs_to_tables(
        self,
        train_csv: str | Path,
        test_csv: str | Path,
        train_table: str = "train_raw",
        test_table: str = "test_raw",
        combined_table: str = "transactions",
    ) -> None:
        """
        Load train and test CSV files into DuckDB and create a combined transactions table.

        This method is a Python alternative to sql/load_data.sql.
        """
        train_csv = self._resolve_path(train_csv)
        test_csv = self._resolve_path(test_csv)

        if not train_csv.exists():
            raise FileNotFoundError(f"Training CSV not found: {train_csv}")
        if not test_csv.exists():
            raise FileNotFoundError(f"Testing CSV not found: {test_csv}")

        self.execute_sql(f"DROP TABLE IF EXISTS {train_table}")
        self.execute_sql(f"DROP TABLE IF EXISTS {test_table}")
        self.execute_sql(f"DROP TABLE IF EXISTS {combined_table}")

        self.execute_sql(
            f"""
            CREATE TABLE {train_table} AS
            SELECT * FROM read_csv_auto('{train_csv.as_posix()}', HEADER=TRUE)
            """
        )

        self.execute_sql(
            f"""
            CREATE TABLE {test_table} AS
            SELECT * FROM read_csv_auto('{test_csv.as_posix()}', HEADER=TRUE)
            """
        )

        self.execute_sql(
            f"""
            CREATE TABLE {combined_table} AS
            SELECT * FROM {train_table}
            UNION ALL
            SELECT * FROM {test_table}
            """
        )

    def register_dataframe(self, df: pd.DataFrame, table_name: str) -> None:
        """
        Register a pandas dataframe as a DuckDB view-like object, then persist it as a table.
        """
        temp_name = f"_{table_name}_temp"
        self.con.register(temp_name, df)
        self.execute_sql(f"DROP TABLE IF EXISTS {table_name}")
        self.execute_sql(f"CREATE TABLE {table_name} AS SELECT * FROM {temp_name}")
        self.con.unregister(temp_name)

    def export_df(
        self,
        df: pd.DataFrame,
        output_path: str | Path,
        index: bool = False,
    ) -> Path:
        """
        Export a dataframe to CSV or Parquet based on file extension.
        """
        output_path = self._resolve_path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        suffix = output_path.suffix.lower()
        if suffix == ".csv":
            df.to_csv(output_path, index=index)
        elif suffix == ".parquet":
            df.to_parquet(output_path, index=index)
        else:
            raise SQLPipelineError(
                f"Unsupported export format '{suffix}'. Use .csv or .parquet"
            )

        return output_path

    def run_query_and_export(
        self,
        sql_path: str | Path,
        output_path: str | Path,
    ) -> Path:
        """
        Run a SQL file that ends with a SELECT and export its result.
        """
        df = self.run_sql_file(sql_path, return_last_select=True)
        if df is None:
            raise SQLPipelineError(f"No dataframe returned from SQL file: {sql_path}")
        return self.export_df(df, output_path)

    def run_many_sql_files(
        self,
        sql_files: Iterable[str | Path],
        return_last_select: bool = False,
    ) -> list[Optional[pd.DataFrame]]:
        """
        Run multiple SQL files in order.
        """
        results: list[Optional[pd.DataFrame]] = []
        for sql_file in sql_files:
            result = self.run_sql_file(sql_file, return_last_select=return_last_select)
            results.append(result)
        return results


def get_project_root(start_path: str | Path = ".") -> Path:
    """
    Resolve the project root path.

    This is a lightweight helper in case you want a single place to update path logic later.
    """
    return Path(start_path).resolve()


def run_standard_sql_setup(
    db_path: str | Path = ":memory:",
    project_root: str | Path = ".",
    train_csv: str | Path = "data/raw/train.csv",
    test_csv: str | Path = "data/raw/test.csv",
) -> SQLRunner:
    """
    Convenience function to:
    1. create a runner
    2. load raw train/test CSVs
    3. create summary views

    Returns
    -------
    SQLRunner
        An initialized SQLRunner ready for analytical queries.
    """
    runner = SQLRunner(db_path=db_path, project_root=project_root)
    runner.load_csvs_to_tables(train_csv=train_csv, test_csv=test_csv)
    views_path = Path("sql/fraud_summary_views.sql")
    runner.run_sql_file(views_path, return_last_select=False)
    return runner


def preview_query_result(
    sql_path: str | Path,
    db_path: str | Path = ":memory:",
    project_root: str | Path = ".",
    train_csv: str | Path = "data/raw/train.csv",
    test_csv: str | Path = "data/raw/test.csv",
    n: int = 10,
) -> pd.DataFrame:
    """
    Quick helper for testing a SQL file end-to-end.
    """
    with run_standard_sql_setup(
        db_path=db_path,
        project_root=project_root,
        train_csv=train_csv,
        test_csv=test_csv,
    ) as runner:
        df = runner.run_sql_file(sql_path, return_last_select=True)
        if df is None:
            raise SQLPipelineError(f"No dataframe returned from SQL file: {sql_path}")
        return df.head(n)
