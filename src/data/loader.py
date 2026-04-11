import pandas as pd
import streamlit as st
from typing import Optional


class DataLoader:
    DEFAULT_ENCODING = "ISO-8859-1"
    DEFAULT_FILE = "Superstore.csv"

    @staticmethod
    def load_data(uploaded_file) -> pd.DataFrame:
        if uploaded_file is not None:
            return DataLoader._load_from_upload(uploaded_file)
        return DataLoader._load_default()

    @staticmethod
    def _load_from_upload(uploaded_file) -> pd.DataFrame:
        filename = uploaded_file.name
        st.write(filename)
        return pd.read_csv(filename, encoding=DataLoader.DEFAULT_ENCODING)

    @staticmethod
    def _load_default() -> pd.DataFrame:
        return pd.read_csv(DataLoader.DEFAULT_FILE, encoding=DataLoader.DEFAULT_ENCODING)

    @staticmethod
    def parse_dates(df: pd.DataFrame, date_column: str = "Order Date") -> pd.DataFrame:
        df = df.copy()
        df[date_column] = pd.to_datetime(df[date_column])
        return df

    @staticmethod
    def get_date_range(df: pd.DataFrame, date_column: str = "Order Date") -> tuple:
        min_date = pd.to_datetime(df[date_column]).min()
        max_date = pd.to_datetime(df[date_column]).max()
        return min_date, max_date
