"""
数据处理模块 - 负责数据聚合、分组和转换
"""
import pandas as pd
from typing import List, Optional
from src.utils.constants import COLUMNS, DATE_COLUMN


class DataProcessor:
    """数据处理器类 - 处理数据聚合和转换"""
    
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
    
    def group_by_category(self) -> pd.DataFrame:
        """
        按类别分组并汇总销售额
        
        Returns:
            pd.DataFrame: 类别销售额汇总
        """
        return self.df.groupby(
            by=[COLUMNS["category"]],
            as_index=False
        )[COLUMNS["sales"]].sum()
    
    def group_by_region(self) -> pd.DataFrame:
        """
        按地区分组并汇总销售额
        
        Returns:
            pd.DataFrame: 地区销售额汇总
        """
        return self.df.groupby(
            by=COLUMNS["region"],
            as_index=False
        )[COLUMNS["sales"]].sum()
    
    def get_time_series_data(self) -> pd.DataFrame:
        """
        获取时间序列数据（按月汇总销售额）
        
        Returns:
            pd.DataFrame: 时间序列数据
        """
        # 创建月份年份列
        temp_df = self.df.copy()
        temp_df["month_year"] = temp_df[DATE_COLUMN].dt.to_period("M")
        
        # 按月份汇总
        result = pd.DataFrame(
            temp_df.groupby(
                temp_df["month_year"].dt.strftime("%Y : %b")
            )[COLUMNS["sales"]].sum()
        ).reset_index()
        
        return result
    
    def get_monthly_subcategory_pivot(self) -> pd.DataFrame:
        """
        获取月度子类别透视表
        
        Returns:
            pd.DataFrame: 透视表数据
        """
        temp_df = self.df.copy()
        temp_df["month"] = temp_df[DATE_COLUMN].dt.month_name()
        
        pivot = pd.pivot_table(
            data=temp_df,
            values=COLUMNS["sales"],
            index=[COLUMNS["sub_category"]],
            columns="month"
        )
        return pivot
    
    def get_summary_sample(self, columns: Optional[List[str]] = None, n_rows: int = 5) -> pd.DataFrame:
        """
        获取摘要数据样本
        
        Args:
            columns: 要包含的列，默认使用预定义的关键列
            n_rows: 行数
            
        Returns:
            pd.DataFrame: 样本数据
        """
        if columns is None:
            columns = [
                COLUMNS["region"],
                COLUMNS["state"],
                COLUMNS["city"],
                COLUMNS["category"],
                COLUMNS["sales"],
                COLUMNS["profit"],
                COLUMNS["quantity"]
            ]
        return self.df[columns].head(n_rows)


def process_data(df: pd.DataFrame) -> DataProcessor:
    """
    便捷函数：创建数据处理器实例
    
    Args:
        df: 原始数据
        
    Returns:
        DataProcessor: 数据处理器实例
    """
    return DataProcessor(df)
