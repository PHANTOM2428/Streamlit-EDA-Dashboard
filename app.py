import warnings
import streamlit as st

warnings.filterwarnings('ignore')

from src.data import (
    load_data,
    process_dates,
    filter_by_date,
    apply_hierarchical_filters,
    aggregate_by_category,
    aggregate_by_region,
    create_timeseries_data,
    create_monthly_subcategory_pivot
)
from src.charts import (
    create_bar_chart,
    create_pie_chart,
    create_line_chart,
    create_treemap,
    create_scatter_plot,
    create_table
)
from src.components import (
    render_page_config,
    render_file_uploader,
    render_date_filters,
    render_expander_data_download
)


def main():
    render_page_config()
    
    uploaded_file = render_file_uploader()
    df = load_data(uploaded_file)
    df = process_dates(df)
    
    start_date, end_date = render_date_filters(df)
    df = filter_by_date(df, start_date, end_date)
    
    filtered_df = apply_hierarchical_filters(df)
    
    category_df = aggregate_by_category(filtered_df)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Category wise Sales")
        fig_bar = create_bar_chart(category_df, x="Category", y="Sales")
        st.plotly_chart(fig_bar, use_container_width=True)
    
    with col2:
        st.subheader("Region wise Sales")
        fig_pie = create_pie_chart(filtered_df, values="Sales", names="Region")
        st.plotly_chart(fig_pie, use_container_width=True)
    
    cl1, cl2 = st.columns(2)
    with cl1:
        render_expander_data_download("Category_ViewData", category_df, "Category", "Blues")
    
    with cl2:
        region_df = aggregate_by_region(filtered_df)
        render_expander_data_download("Region_ViewData", region_df, "Region", "Oranges")
    
    st.subheader('Time Series Analysis')
    linechart_df = create_timeseries_data(filtered_df)
    fig2 = create_line_chart(linechart_df, x="month_year", y="Sales", labels={"Sales": "Amount"})
    st.plotly_chart(fig2, use_container_width=True)
    
    with st.expander("View Data of TimeSeries:"):
        st.write(linechart_df.T.style.background_gradient(cmap="Blues"))
        csv = linechart_df.to_csv(index=False).encode("utf-8")
        st.download_button('Download Data', data=csv, file_name="TimeSeries.csv", mime='text/csv')
    
    st.subheader("Hierarchical view of Sales using TreeMap")
    fig3 = create_treemap(
        filtered_df,
        path=["Region", "Category", "Sub-Category"],
        values="Sales",
        hover_data=["Sales"],
        color="Sub-Category"
    )
    st.plotly_chart(fig3, use_container_width=True)
    
    chart1, chart2 = st.columns(2)
    with chart1:
        st.subheader('Segment wise Sales')
        fig = create_pie_chart(
            filtered_df,
            values="Sales",
            names="Segment",
            template="plotly_dark",
            textposition="inside"
        )
        fig.update_traces(text=filtered_df["Segment"])
        st.plotly_chart(fig, use_container_width=True)
    
    with chart2:
        st.subheader('Category wise Sales')
        fig = create_pie_chart(
            filtered_df,
            values="Sales",
            names="Category",
            template="gridon",
            textposition="inside"
        )
        fig.update_traces(text=filtered_df["Category"])
        st.plotly_chart(fig, use_container_width=True)
    
    st.subheader(":point_right: Month wise Sub-Category Sales Summary")
    with st.expander("Summary_Table"):
        df_sample = df[0:5][["Region", "State", "City", "Category", "Sales", "Profit", "Quantity"]]
        fig = create_table(df_sample, colorscale="Cividis")
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("Month wise sub-Category Table")
        sub_category_pivot = create_monthly_subcategory_pivot(filtered_df)
        st.write(sub_category_pivot.style.background_gradient(cmap="Blues"))
    
    data1 = create_scatter_plot(
        filtered_df,
        x="Sales",
        y="Profit",
        size="Quantity",
        title="Relationship between Sales and Profit using Scatter Plot"
    )
    st.plotly_chart(data1, use_container_width=True)


if __name__ == "__main__":
    main()
