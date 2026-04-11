import pandas as pd
from typing import List, Optional


class DataProcessor:
    @staticmethod
    def group_by_column(
        df: pd.DataFrame,
        group_column: str,
        agg_column: str = "Sales",
        agg_func: str = "sum"
    ) -> pd.DataFrame:
        return df.groupby(by=[group_column], as_index=False)[agg_column].agg(agg_func)

    @staticmethod
    def group_by_multiple(
        df: pd.DataFrame,
        group_columns: List[str],
        agg_column: str = "Sales",
        agg_func: str = "sum"
    ) -> pd.DataFrame:
        return df.groupby(by=group_columns, as_index=False)[agg_column].agg(agg_func)

    @staticmethod
    def add_month_year_column(
        df: pd.DataFrame,
        date_column: str = "Order Date"
    ) -> pd.DataFrame:
        df = df.copy()
        df["month_year"] = df[date_column].dt.to_period("M")
        return df

    @staticmethod
    def add_month_name_column(
        df: pd.DataFrame,
        date_column: str = "Order Date"
    ) -> pd.DataFrame:
        df = df.copy()
        df["month"] = df[date_column].dt.month_name()
        return df

    @staticmethod
    def aggregate_by_month(
        df: pd.DataFrame,
        date_column: str = "Order Date",
        agg_column: str = "Sales"
    ) -> pd.DataFrame:
        df = df.copy()
        df["month_year"] = df[date_column].dt.to_period("M")
        result = df.groupby(df["month_year"].dt.strftime("%Y : %b"))[agg_column].sum()
        return pd.DataFrame(result).reset_index()

    @staticmethod
    def create_pivot_table(
        df: pd.DataFrame,
        values: str,
        index: List[str],
        columns: str
    ) -> pd.DataFrame:
        return pd.pivot_table(
            data=df,
            values=values,
            index=index,
            columns=columns
        )

    @staticmethod
    def get_sample(df: pd.DataFrame, columns: List[str], n: int = 5) -> pd.DataFrame:
        return df[0:n][columns]
