import streamlit as st
import pandas as pd
from typing import List, Optional, Tuple
from io import StringIO


class UIComponents:
    @staticmethod
    def render_page_config():
        st.set_page_config(
            page_title="Superstore!!!",
            page_icon=":bar_chart:",
            layout="wide"
        )

    @staticmethod
    def render_title():
        st.title(" :bar_chart: Sample SuperStore EDA")

    @staticmethod
    def render_file_uploader() -> Optional[st.runtime.uploaded_file_manager.UploadedFile]:
        return st.file_uploader(
            ":file_folder: Upload a file",
            type=(["csv", "txt", "xlsx", "xls"])
        )

    @staticmethod
    def render_date_inputs(
        start_date,
        end_date
    ) -> Tuple[pd.Timestamp, pd.Timestamp]:
        col1, col2 = st.columns((2))
        with col1:
            date1 = pd.to_datetime(st.date_input("Start Date", start_date))
        with col2:
            date2 = pd.to_datetime(st.date_input("End Date", end_date))
        return date1, date2, col1, col2

    @staticmethod
    def render_sidebar_filters(df: pd.DataFrame) -> Tuple[List, List, List]:
        st.sidebar.header("Choose your filter: ")

        region = st.sidebar.multiselect(
            "Pick your Region",
            df["Region"].unique()
        )

        state = st.sidebar.multiselect(
            "Pick the State",
            df["State"].unique()
        )

        city = st.sidebar.multiselect(
            "Pick the City",
            df["City"].unique()
        )

        return region, state, city

    @staticmethod
    def render_subheader(text: str):
        st.subheader(text)

    @staticmethod
    def render_plotly_chart(fig, use_container_width: bool = True):
        st.plotly_chart(fig, use_container_width=use_container_width)

    @staticmethod
    def render_expander_data(
        title: str,
        df: pd.DataFrame,
        gradient_cmap: str = "Blues",
        download_filename: str = "data.csv"
    ):
        with st.expander(title):
            st.write(df.style.background_gradient(cmap=gradient_cmap))
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                "Download Data",
                data=csv,
                file_name=download_filename,
                mime="text/csv",
                help='Click here to download the data as a CSV file'
            )

    @staticmethod
    def render_expander_table(
        title: str,
        df: pd.DataFrame,
        gradient_cmap: str = "Blues"
    ):
        with st.expander(title):
            st.write(df.T.style.background_gradient(cmap=gradient_cmap))
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                'Download Data',
                data=csv,
                file_name=f"{title.replace(' ', '_')}.csv",
                mime='text/csv'
            )

    @staticmethod
    def render_markdown(text: str):
        st.markdown(text)
