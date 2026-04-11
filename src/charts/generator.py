"""
图表生成模块 - 负责创建各种图表
"""
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
from typing import Dict, Any, Optional
from src.charts.config import ChartConfig
from src.utils.constants import COLUMNS


class ChartGenerator:
    """图表生成器类 - 创建各种可视化图表"""
    
    def __init__(self):
        self.config = ChartConfig()
    
    def create_bar_chart(
        self,
        data: pd.DataFrame,
        x_column: str,
        y_column: str,
        text_format: str = "${:,.2f}"
    ) -> Any:
        """
        创建柱状图
        
        Args:
            data: 数据
            x_column: X轴列名
            y_column: Y轴列名
            text_format: 文本格式
            
        Returns:
            plotly.graph_objects.Figure: 柱状图
        """
        config = self.config.get_bar_config(text_format=text_format)
        
        fig = px.bar(
            data,
            x=x_column,
            y=y_column,
            text=[text_format.format(x) for x in data[y_column]],
            template=config["template"]
        )
        fig.update_layout(height=config["height"])
        return fig
    
    def create_pie_chart(
        self,
        data: pd.DataFrame,
        values_column: str,
        names_column: str,
        hole: float = None,
        text_position: str = "outside",
        template: str = None
    ) -> Any:
        """
        创建饼图
        
        Args:
            data: 数据
            values_column: 值列名
            names_column: 名称列名
            hole: 空心比例
            text_position: 文本位置
            template: 模板名称
            
        Returns:
            plotly.graph_objects.Figure: 饼图
        """
        config = self.config.get_pie_config(
            hole=hole,
            text_position=text_position,
            template=template
        )
        
        fig = px.pie(
            data,
            values=values_column,
            names=names_column,
            hole=config["hole"]
        )
        fig.update_layout(height=config["height"])
        fig.update_traces(textposition=config["text_position"])
        return fig
    
    def create_line_chart(
        self,
        data: pd.DataFrame,
        x_column: str,
        y_column: str,
        labels: Dict[str, str] = None
    ) -> Any:
        """
        创建折线图
        
        Args:
            data: 数据
            x_column: X轴列名
            y_column: Y轴列名
            labels: 标签映射
            
        Returns:
            plotly.graph_objects.Figure: 折线图
        """
        config = self.config.get_line_config()
        
        fig = px.line(
            data,
            x=x_column,
            y=y_column,
            labels=labels or {y_column: "Amount"},
            height=config["height"],
            width=config["width"],
            template=config["template"]
        )
        return fig
    
    def create_treemap(
        self,
        data: pd.DataFrame,
        path_columns: list,
        values_column: str,
        color_column: str = None,
        hover_data: list = None
    ) -> Any:
        """
        创建树状图
        
        Args:
            data: 数据
            path_columns: 路径列名列表
            values_column: 值列名
            color_column: 颜色列名
            hover_data: 悬停数据列名列表
            
        Returns:
            plotly.graph_objects.Figure: 树状图
        """
        config = self.config.get_treemap_config()
        
        fig = px.treemap(
            data,
            path=path_columns,
            values=values_column,
            hover_data=hover_data or [values_column],
            color=color_column
        )
        fig.update_layout(
            width=config["width"],
            height=config["height"]
        )
        return fig
    
    def create_scatter_plot(
        self,
        data: pd.DataFrame,
        x_column: str = None,
        y_column: str = None,
        size_column: str = None
    ) -> Any:
        """
        创建散点图
        
        Args:
            data: 数据
            x_column: X轴列名
            y_column: Y轴列名
            size_column: 气泡大小列名
            
        Returns:
            plotly.graph_objects.Figure: 散点图
        """
        x_column = x_column or COLUMNS["sales"]
        y_column = y_column or COLUMNS["profit"]
        size_column = size_column or COLUMNS["quantity"]
        
        config = self.config.get_scatter_config()
        
        fig = px.scatter(
            data,
            x=x_column,
            y=y_column,
            size=size_column
        )
        fig.update_layout(
            title=config["title"],
            xaxis_title=config["xaxis_title"],
            yaxis_title=config["yaxis_title"],
            xaxis_title_font=config["xaxis_title_font"],
            yaxis_title_font=config["yaxis_title_font"]
        )
        return fig
    
    def create_table(
        self,
        data: pd.DataFrame,
        colorscale: str = None
    ) -> Any:
        """
        创建表格
        
        Args:
            data: 数据
            colorscale: 颜色比例
            
        Returns:
            plotly.graph_objects.Figure: 表格
        """
        config = self.config.get_table_config(colorscale=colorscale)
        
        fig = ff.create_table(data, colorscale=config["colorscale"])
        return fig


def create_chart_generator() -> ChartGenerator:
    """
    便捷函数：创建图表生成器实例
    
    Returns:
        ChartGenerator: 图表生成器实例
    """
    return ChartGenerator()
