import warnings
import streamlit as st
import pandas as pd

from src.data import DataLoader, DataFilter, DataProcessor
from src.charts import ChartGenerator
from src.components import UIComponents

warnings.filterwarnings('ignore')


def main():
    UIComponents.render_page_config()
    UIComponents.render_title()

    uploaded_file = UIComponents.render_file_uploader()
    df = DataLoader.load_data(uploaded_file)
    df = DataLoader.parse_dates(df)

    min_date, max_date = DataLoader.get_date_range(df)
    date1, date2, col1, col2 = UIComponents.render_date_inputs(min_date, max_date)

    df = DataFilter.filter_by_date(df, date1, date2)

    region, state, city = UIComponents.render_sidebar_filters(df)
    filtered_df = DataFilter.apply_cascading_filters(df, region, state, city)

    render_category_and_region_charts(filtered_df, col1, col2)
    render_time_series_analysis(filtered_df)
    render_treemap(filtered_df)
    render_segment_and_category_pies(filtered_df)
    render_summary_table(filtered_df, df)
    render_scatter_plot(filtered_df)


def render_category_and_region_charts(filtered_df: pd.DataFrame, col1, col2):
    category_df = DataProcessor.group_by_column(filtered_df, "Category")

    with col1:
        UIComponents.render_subheader("Category wise Sales")
        fig_bar = ChartGenerator.create_bar_chart(
            df=category_df,
            x="Category",
            y="Sales"
        )
        UIComponents.render_plotly_chart(fig_bar)

    with col2:
        UIComponents.render_subheader("Region wise Sales")
        fig_pie = ChartGenerator.create_pie_chart(
            df=filtered_df,
            values="Sales",
            names="Region"
        )
        UIComponents.render_plotly_chart(fig_pie)

    cl1, cl2 = st.columns((2))
    with cl1:
        UIComponents.render_expander_data(
            "Category_ViewData",
            category_df,
            gradient_cmap="Blues",
            download_filename="Category.csv"
        )

    with cl2:
        region_df = DataProcessor.group_by_column(filtered_df, "Region")
        UIComponents.render_expander_data(
            "Region_ViewData",
            region_df,
            gradient_cmap="Oranges",
            download_filename="Region.csv"
        )


def render_time_series_analysis(filtered_df: pd.DataFrame):
    filtered_df = DataProcessor.add_month_year_column(filtered_df)
    UIComponents.render_subheader('Time Series Analysis')

    linechart = DataProcessor.aggregate_by_month(filtered_df)
    fig = ChartGenerator.create_line_chart(
        df=linechart,
        x="month_year",
        y="Sales",
        labels={"Sales": "Amount"}
    )
    UIComponents.render_plotly_chart(fig)

    UIComponents.render_expander_table(
        "View Data of TimeSeries:",
        linechart
    )


def render_treemap(filtered_df: pd.DataFrame):
    UIComponents.render_subheader("Hierarchical view of Sales using TreeMap")
    fig = ChartGenerator.create_treemap(
        df=filtered_df,
        path=["Region", "Category", "Sub-Category"],
        values="Sales",
        hover_data=["Sales"],
        color="Sub-Category"
    )
    UIComponents.render_plotly_chart(fig)


def render_segment_and_category_pies(filtered_df: pd.DataFrame):
    chart1, chart2 = st.columns((2))

    with chart1:
        UIComponents.render_subheader('Segment wise Sales')
        fig = ChartGenerator.create_pie_chart_inside(
            df=filtered_df,
            values="Sales",
            names="Segment",
            template="plotly_dark"
        )
        UIComponents.render_plotly_chart(fig)

    with chart2:
        UIComponents.render_subheader('Category wise Sales')
        fig = ChartGenerator.create_pie_chart_inside(
            df=filtered_df,
            values="Sales",
            names="Category",
            template="gridon"
        )
        UIComponents.render_plotly_chart(fig)


def render_summary_table(filtered_df: pd.DataFrame, original_df: pd.DataFrame):
    UIComponents.render_subheader(":point_right: Month wise Sub-Category Sales Summary")

    with st.expander("Summary_Table"):
        sample_columns = ["Region", "State", "City", "Category", "Sales", "Profit", "Quantity"]
        df_sample = DataProcessor.get_sample(original_df, sample_columns, n=5)
        fig = ChartGenerator.create_table(df_sample, colorscale="Cividis")
        UIComponents.render_plotly_chart(fig)

        UIComponents.render_markdown("Month wise sub-Category Table")
        filtered_df = DataProcessor.add_month_name_column(filtered_df)
        sub_category_pivot = DataProcessor.create_pivot_table(
            df=filtered_df,
            values="Sales",
            index=["Sub-Category"],
            columns="month"
        )
        st.write(sub_category_pivot.style.background_gradient(cmap="Blues"))


def render_scatter_plot(filtered_df: pd.DataFrame):
    fig = ChartGenerator.create_scatter_plot(
        df=filtered_df,
        x="Sales",
        y="Profit",
        size="Quantity",
        title="Relationship between Sales and Profit using Scatter Plot",
        xaxis_title="Sales",
        yaxis_title="Profit"
    )
    UIComponents.render_plotly_chart(fig)


if __name__ == "__main__":
    main()
