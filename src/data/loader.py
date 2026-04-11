import pandas as pd
import streamlit as st
import os


def load_data(uploaded_file=None):
    if uploaded_file is not None:
        filename = uploaded_file.name
        st.write(filename)
        return pd.read_csv(uploaded_file, encoding="ISO-8859-1")
    
    current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    default_data_path = os.path.join(current_dir, "Superstore.csv")
    return pd.read_csv(default_data_path, encoding="ISO-8859-1")


def process_dates(df):
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    return df


def get_date_range(df):
    min_date = df["Order Date"].min()
    max_date = df["Order Date"].max()
    return min_date, max_date


def filter_by_date(df, start_date, end_date):
    return df[(df["Order Date"] >= start_date) & (df["Order Date"] <= end_date)].copy()
