import pandas as pd
from typing import List, Optional


class DataFilter:
    @staticmethod
    def filter_by_date(
        df: pd.DataFrame,
        start_date,
        end_date,
        date_column: str = "Order Date"
    ) -> pd.DataFrame:
        mask = (df[date_column] >= start_date) & (df[date_column] <= end_date)
        return df[mask].copy()

    @staticmethod
    def filter_by_column(
        df: pd.DataFrame,
        column: str,
        values: Optional[List]
    ) -> pd.DataFrame:
        if not values:
            return df.copy()
        return df[df[column].isin(values)].copy()

    @staticmethod
    def apply_cascading_filters(
        df: pd.DataFrame,
        region: Optional[List] = None,
        state: Optional[List] = None,
        city: Optional[List] = None
    ) -> pd.DataFrame:
        result = df.copy()

        if region:
            result = result[result["Region"].isin(region)]

        if state:
            result = result[result["State"].isin(state)]

        if city:
            result = result[result["City"].isin(city)]

        return result

    @staticmethod
    def get_unique_values(df: pd.DataFrame, column: str) -> List:
        return list(df[column].unique())
