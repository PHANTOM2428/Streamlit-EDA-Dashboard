"""
UI 组件模块 - 负责页面布局和交互组件
"""
import pandas as pd
import streamlit as st
from typing import Optional, List
from src.utils.constants import (
    PAGE_CONFIG,
    DATA_CONFIG,
    FILTER_CONFIG,
    TABLE_CONFIG,
    COLUMNS
)


class UIComponents:
    """UI 组件类 - 管理页面布局和交互元素"""
    
    @staticmethod
    def setup_page():
        """设置页面配置"""
        st.set_page_config(
            page_title=PAGE_CONFIG["page_title"],
            page_icon=PAGE_CONFIG["page_icon"],
            layout=PAGE_CONFIG["layout"]
        )
        st.title(f" {PAGE_CONFIG['page_icon']} Sample SuperStore EDA")
    
    @staticmethod
    def render_file_uploader() -> Optional[st.runtime.uploaded_file_manager.UploadedFile]:
        """
        渲染文件上传组件
        
        Returns:
            上传的文件对象或 None
        """
        return st.file_uploader(
            ":file_folder: Upload a file",
            type=DATA_CONFIG["supported_formats"]
        )
    
    @staticmethod
    def render_date_filters(start_date, end_date) -> tuple:
        """
        渲染日期筛选组件
        
        Args:
            start_date: 默认开始日期
            end_date: 默认结束日期
            
        Returns:
            tuple: (选择的开始日期, 选择的结束日期)
        """
        col1, col2 = st.columns((2))
        
        with col1:
            date1 = pd.to_datetime(st.date_input("Start Date", start_date))
        
        with col2:
            date2 = pd.to_datetime(st.date_input("End Date", end_date))
        
        return date1, date2
    
    @staticmethod
    def render_sidebar_filters(
        available_regions: List,
        available_states: List,
        available_cities: List
    ) -> tuple:
        """
        渲染侧边栏筛选组件
        
        Args:
            available_regions: 可用地区列表
            available_states: 可用州列表
            available_cities: 可用城市列表
            
        Returns:
            tuple: (选中的地区, 选中的州, 选中的城市)
        """
        st.sidebar.header(FILTER_CONFIG["sidebar_header"])
        
        region = st.sidebar.multiselect(
            FILTER_CONFIG["region_label"],
            available_regions
        )
        
        state = st.sidebar.multiselect(
            FILTER_CONFIG["state_label"],
            available_states
        )
        
        city = st.sidebar.multiselect(
            FILTER_CONFIG["city_label"],
            available_cities
        )
        
        return region, state, city
    
    @staticmethod
    def render_data_download(
        data: pd.DataFrame,
        filename: str,
        label: str = "Download Data",
        help_text: str = "Click here to download the data as a CSV file"
    ):
        """
        渲染数据下载按钮
        
        Args:
            data: 要下载的数据
            filename: 文件名
            label: 按钮标签
            help_text: 帮助文本
        """
        csv = data.to_csv(index=False).encode('utf-8')
        st.download_button(
            label,
            data=csv,
            file_name=filename,
            mime="text/csv",
            help=help_text
        )
    
    @staticmethod
    def render_data_viewer(
        data: pd.DataFrame,
        title: str,
        cmap: str = None,
        enable_download: bool = True,
        download_filename: str = None
    ):
        """
        渲染数据查看器（带样式和下载功能）
        
        Args:
            data: 要显示的数据
            title: 展开面板标题
            cmap: 颜色映射
            enable_download: 是否启用下载
            download_filename: 下载文件名
        """
        cmap = cmap or TABLE_CONFIG["category_cmap"]
        
        with st.expander(title):
            st.write(data.style.background_gradient(cmap=cmap))
            
            if enable_download and download_filename:
                UIComponents.render_data_download(data, download_filename)
    
    @staticmethod
    def render_transposed_data_viewer(
        data: pd.DataFrame,
        title: str,
        cmap: str = None,
        download_filename: str = None
    ):
        """
        渲染转置数据查看器
        
        Args:
            data: 要显示的数据
            title: 展开面板标题
            cmap: 颜色映射
            download_filename: 下载文件名
        """
        cmap = cmap or TABLE_CONFIG["category_cmap"]
        
        with st.expander(title):
            st.write(data.T.style.background_gradient(cmap=cmap))
            
            if download_filename:
                csv = data.to_csv(index=False).encode('utf-8')
                st.download_button(
                    'Download Data',
                    data=csv,
                    file_name=download_filename,
                    mime='text/csv'
                )
    
    @staticmethod
    def render_summary_table_section(df_sample: pd.DataFrame, pivot_data: pd.DataFrame):
        """
        渲染汇总表格区域
        
        Args:
            df_sample: 样本数据
            pivot_data: 透视表数据
        """
        st.subheader(":point_right: Month wise Sub-Category Sales Summary")
        
        with st.expander("Summary_Table"):
            # 样本表格
            from src.charts.generator import create_chart_generator
            generator = create_chart_generator()
            fig = generator.create_table(df_sample, colorscale=TABLE_CONFIG["summary_cmap"])
            st.plotly_chart(fig, use_container_width=True)
            
            # 透视表
            st.markdown("Month wise sub-Category Table")
            st.write(pivot_data.style.background_gradient(cmap=TABLE_CONFIG["category_cmap"]))


def get_ui_components() -> UIComponents:
    """
    便捷函数：获取 UI 组件实例
    
    Returns:
        UIComponents: UI 组件实例
    """
    return UIComponents()
