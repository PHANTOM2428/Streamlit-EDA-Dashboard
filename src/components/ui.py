import streamlit as st
import pandas as pd


def render_data_download(df, filename, label, cmap="Blues"):
    st.write(df.style.background_gradient(cmap=cmap))
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        f"Download {label} Data",
        data=csv,
        file_name=f"{filename}.csv",
        mime="text/csv",
        help=f'Click here to download the data as a CSV file'
    )


def render_expander_data_download(title, df, filename, cmap="Blues"):
    with st.expander(title):
        render_data_download(df, filename, "", cmap)


def render_date_filters(df):
    col1, col2 = st.columns(2)
    min_date = df["Order Date"].min()
    max_date = df["Order Date"].max()
    
    with col1:
        start_date = pd.to_datetime(st.date_input("Start Date", min_date))
    with col2:
        end_date = pd.to_datetime(st.date_input("End Date", max_date))
    
    return start_date, end_date


def render_file_uploader():
    return st.file_uploader(
        ":file_folder: Upload a file",
        type=["csv", "txt", "xlsx", "xls"]
    )


def render_page_config():
    st.set_page_config(
        page_title="Superstore!!!",
        page_icon=":bar_chart:",
        layout="wide"
    )
    st.title(" :bar_chart: Sample SuperStore EDA")
