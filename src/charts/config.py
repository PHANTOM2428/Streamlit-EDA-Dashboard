"""
图表配置模块 - 集中管理图表样式和配置
"""
from typing import Dict, Any, Optional
from src.utils.constants import CHART_CONFIG


class ChartConfig:
    """图表配置类 - 提供统一的图表配置管理"""
    
    @staticmethod
    def get_base_layout(height: Optional[int] = None, width: Optional[int] = None) -> Dict[str, Any]:
        """
        获取基础布局配置
        
        Args:
            height: 图表高度
            width: 图表宽度
            
        Returns:
            Dict: 布局配置字典
        """
        layout = {}
        if height:
            layout["height"] = height
        if width:
            layout["width"] = width
        return layout
    
    @staticmethod
    def get_bar_config(
        text_format: str = "${:,.2f}",
        template: str = None
    ) -> Dict[str, Any]:
        """
        获取柱状图配置
        
        Args:
            text_format: 文本格式
            template: 模板名称
            
        Returns:
            Dict: 柱状图配置
        """
        return {
            "text_format": text_format,
            "template": template or CHART_CONFIG["default_template"],
            "height": CHART_CONFIG["default_height"]
        }
    
    @staticmethod
    def get_pie_config(
        hole: float = None,
        text_position: str = "outside",
        template: str = None
    ) -> Dict[str, Any]:
        """
        获取饼图配置
        
        Args:
            hole: 空心比例
            text_position: 文本位置
            template: 模板名称
            
        Returns:
            Dict: 饼图配置
        """
        return {
            "hole": hole if hole is not None else CHART_CONFIG["pie_hole"],
            "text_position": text_position,
            "template": template or CHART_CONFIG["default_template"],
            "height": CHART_CONFIG["default_height"]
        }
    
    @staticmethod
    def get_line_config(
        template: str = "gridon",
        height: int = None
    ) -> Dict[str, Any]:
        """
        获取折线图配置
        
        Args:
            template: 模板名称
            height: 图表高度
            
        Returns:
            Dict: 折线图配置
        """
        return {
            "template": template,
            "height": height or CHART_CONFIG["time_series_height"],
            "width": 1000
        }
    
    @staticmethod
    def get_treemap_config() -> Dict[str, Any]:
        """
        获取树状图配置
        
        Returns:
            Dict: 树状图配置
        """
        return {
            "width": CHART_CONFIG["treemap_width"],
            "height": CHART_CONFIG["treemap_height"]
        }
    
    @staticmethod
    def get_scatter_config(
        title: str = "Relationship between Sales and Profit using Scatter Plot",
        x_title: str = "Sales",
        y_title: str = "Profit"
    ) -> Dict[str, Any]:
        """
        获取散点图配置
        
        Args:
            title: 图表标题
            x_title: X轴标题
            y_title: Y轴标题
            
        Returns:
            Dict: 散点图配置
        """
        return {
            "title": {
                "text": title,
                "font": {"size": 20}
            },
            "xaxis_title": x_title,
            "yaxis_title": y_title,
            "xaxis_title_font": {"size": 19},
            "yaxis_title_font": {"size": 19}
        }
    
    @staticmethod
    def get_table_config(colorscale: str = None) -> Dict[str, Any]:
        """
        获取表格配置
        
        Args:
            colorscale: 颜色比例
            
        Returns:
            Dict: 表格配置
        """
        return {
            "colorscale": colorscale or "Cividis"
        }


def get_chart_config() -> ChartConfig:
    """
    便捷函数：创建图表配置实例
    
    Returns:
        ChartConfig: 图表配置实例
    """
    return ChartConfig()
