"""
Streamlit EDA Dashboard - 重构后的主应用入口

重构说明：
1. 将数据加载、筛选、处理逻辑分离到 src/data/ 模块
2. 将图表生成逻辑分离到 src/charts/ 模块
3. 将 UI 组件分离到 src/components/ 模块
4. 常量配置集中管理于 src/utils/constants.py
"""
import streamlit as st
import pandas as pd
import warnings

# 抑制警告
warnings.filterwarnings('ignore')

# 导入重构后的模块
from src.utils.constants import COLUMNS, TABLE_CONFIG
from src.data.loader import load_and_prepare_data
from src.data.filters import create_filter
from src.data.processor import process_data
from src.charts.generator import create_chart_generator
from src.components.ui import get_ui_components


def main():
    """主应用函数"""
    
    # 初始化 UI 组件
    ui = get_ui_components()
    
    # 设置页面
    ui.setup_page()
    
    # 文件上传
    uploaded_file = ui.render_file_uploader()
    
    # 加载数据
    df = load_and_prepare_data(uploaded_file)
    
    # 获取日期范围
    start_date = df[COLUMNS["order_date"]].min()
    end_date = df[COLUMNS["order_date"]].max()
    
    # 日期筛选
    date1, date2 = ui.render_date_filters(start_date, end_date)
    df = df[(df[COLUMNS["order_date"]] >= date1) & (df[COLUMNS["order_date"]] <= date2)].copy()
    
    # 初始化筛选器
    filter_engine = create_filter(df)
    
    # 侧边栏筛选
    region, state, city = ui.render_sidebar_filters(
        available_regions=df[COLUMNS["region"]].unique(),
        available_states=filter_engine.get_available_states(region),
        available_cities=filter_engine.get_available_cities(region, state)
    )
    
    # 应用级联筛选
    filtered_df = filter_engine.apply_cascading_filters(region, state, city)
    
    # 初始化数据处理器
    processor = process_data(filtered_df)
    
    # 初始化图表生成器
    chart_gen = create_chart_generator()
    
    # 类别销售额数据
    category_df = processor.group_by_category()
    
    # 第一行图表：类别柱状图 + 地区饼图
    col1, col2 = st.columns((2))
    
    with col1:
        st.subheader("Category wise Sales")
        fig_bar = chart_gen.create_bar_chart(
            data=category_df,
            x_column=COLUMNS["category"],
            y_column=COLUMNS["sales"]
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    
    with col2:
        st.subheader("Region wise Sales")
        fig_pie = chart_gen.create_pie_chart(
            data=filtered_df,
            values_column=COLUMNS["sales"],
            names_column=COLUMNS["region"]
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    # 数据下载区域
    cl1, cl2 = st.columns((2))
    
    with cl1:
        ui.render_data_viewer(
            data=category_df,
            title="Category_ViewData",
            cmap=TABLE_CONFIG["category_cmap"],
            enable_download=True,
            download_filename="Category.csv"
        )
    
    with cl2:
        region_df = processor.group_by_region()
        ui.render_data_viewer(
            data=region_df,
            title="Region_ViewData",
            cmap=TABLE_CONFIG["region_cmap"],
            enable_download=True,
            download_filename="Region.csv"
        )
    
    # 时间序列分析
    st.subheader('Time Series Analysis')
    linechart_df = processor.get_time_series_data()
    fig_line = chart_gen.create_line_chart(
        data=linechart_df,
        x_column="month_year",
        y_column=COLUMNS["sales"]
    )
    st.plotly_chart(fig_line, use_container_width=True)
    
    # 时间序列数据下载
    ui.render_transposed_data_viewer(
        data=linechart_df,
        title="View Data of TimeSeries:",
        cmap=TABLE_CONFIG["category_cmap"],
        download_filename="TimeSeries.csv"
    )
    
    # 树状图
    st.subheader("Hierarchical view of Sales using TreeMap")
    fig_treemap = chart_gen.create_treemap(
        data=filtered_df,
        path_columns=[COLUMNS["region"], COLUMNS["category"], COLUMNS["sub_category"]],
        values_column=COLUMNS["sales"],
        color_column=COLUMNS["sub_category"]
    )
    st.plotly_chart(fig_treemap, use_container_width=True)
    
    # 第二行饼图：细分 + 类别
    chart1, chart2 = st.columns((2))
    
    with chart1:
        st.subheader('Segment wise Sales')
        fig_segment = chart_gen.create_pie_chart(
            data=filtered_df,
            values_column=COLUMNS["sales"],
            names_column=COLUMNS["segment"],
            hole=0,
            text_position="inside",
            template="plotly_dark"
        )
        fig_segment.update_traces(text=filtered_df[COLUMNS["segment"]].unique())
        st.plotly_chart(fig_segment, use_container_width=True)
    
    with chart2:
        st.subheader('Category wise Sales')
        fig_category = chart_gen.create_pie_chart(
            data=filtered_df,
            values_column=COLUMNS["sales"],
            names_column=COLUMNS["category"],
            hole=0,
            text_position="inside",
            template="gridon"
        )
        fig_category.update_traces(text=filtered_df[COLUMNS["category"]].unique())
        st.plotly_chart(fig_category, use_container_width=True)
    
    # 汇总表格区域
    df_sample = processor.get_summary_sample()
    pivot_data = processor.get_monthly_subcategory_pivot()
    ui.render_summary_table_section(df_sample, pivot_data)
    
    # 散点图
    fig_scatter = chart_gen.create_scatter_plot(filtered_df)
    st.plotly_chart(fig_scatter, use_container_width=True)


if __name__ == "__main__":
    main()
