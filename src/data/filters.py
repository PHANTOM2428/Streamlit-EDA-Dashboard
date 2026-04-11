"""
筛选逻辑模块 - 负责数据的筛选和过滤
"""
import pandas as pd
from typing import List, Optional
from src.utils.constants import COLUMNS, DATE_COLUMN


class DataFilter:
    """数据筛选器类 - 处理各种筛选逻辑"""
    
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self.filtered_df = df.copy()
    
    def filter_by_date_range(self, start_date, end_date) -> pd.DataFrame:
        """
        按日期范围筛选数据
        
        Args:
            start_date: 开始日期
            end_date: 结束日期
            
        Returns:
            pd.DataFrame: 筛选后的数据
        """
        self.filtered_df = self.filtered_df[
            (self.filtered_df[DATE_COLUMN] >= start_date) & 
            (self.filtered_df[DATE_COLUMN] <= end_date)
        ].copy()
        return self.filtered_df
    
    def filter_by_region(self, regions: List[str]) -> pd.DataFrame:
        """
        按地区筛选数据
        
        Args:
            regions: 地区列表
            
        Returns:
            pd.DataFrame: 筛选后的数据
        """
        if regions:
            self.filtered_df = self.filtered_df[
                self.filtered_df[COLUMNS["region"]].isin(regions)
            ].copy()
        return self.filtered_df
    
    def filter_by_state(self, states: List[str]) -> pd.DataFrame:
        """
        按州/省筛选数据
        
        Args:
            states: 州/省列表
            
        Returns:
            pd.DataFrame: 筛选后的数据
        """
        if states:
            self.filtered_df = self.filtered_df[
                self.filtered_df[COLUMNS["state"]].isin(states)
            ].copy()
        return self.filtered_df
    
    def filter_by_city(self, cities: List[str]) -> pd.DataFrame:
        """
        按城市筛选数据
        
        Args:
            cities: 城市列表
            
        Returns:
            pd.DataFrame: 筛选后的数据
        """
        if cities:
            self.filtered_df = self.filtered_df[
                self.filtered_df[COLUMNS["city"]].isin(cities)
            ].copy()
        return self.filtered_df
    
    def apply_cascading_filters(
        self,
        regions: Optional[List[str]] = None,
        states: Optional[List[str]] = None,
        cities: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """
        应用级联筛选（地区 -> 州 -> 城市）
        
        原代码中的复杂 if-else 逻辑被简化为清晰的链式调用
        
        Args:
            regions: 选中的地区列表
            states: 选中的州列表
            cities: 选中的城市列表
            
        Returns:
            pd.DataFrame: 筛选后的数据
        """
        # 重置筛选状态
        self.filtered_df = self.df.copy()
        
        # 应用地区筛选
        if regions:
            self.filter_by_region(regions)
        
        # 应用州筛选（基于地区筛选后的数据）
        if states:
            self.filter_by_state(states)
        
        # 应用城市筛选（基于前两级筛选后的数据）
        if cities:
            self.filter_by_city(cities)
        
        return self.filtered_df
    
    def get_unique_values(self, column: str) -> List:
        """
        获取某列的唯一值列表
        
        Args:
            column: 列名
            
        Returns:
            List: 唯一值列表
        """
        return self.filtered_df[column].unique().tolist()
    
    def get_available_states(self, regions: Optional[List[str]] = None) -> List:
        """
        获取可用的州列表（考虑地区筛选）
        
        Args:
            regions: 选中的地区列表
            
        Returns:
            List: 可用的州列表
        """
        temp_df = self.df.copy()
        if regions:
            temp_df = temp_df[temp_df[COLUMNS["region"]].isin(regions)]
        return temp_df[COLUMNS["state"]].unique().tolist()
    
    def get_available_cities(
        self,
        regions: Optional[List[str]] = None,
        states: Optional[List[str]] = None
    ) -> List:
        """
        获取可用的城市列表（考虑地区和州筛选）
        
        Args:
            regions: 选中的地区列表
            states: 选中的州列表
            
        Returns:
            List: 可用的城市列表
        """
        temp_df = self.df.copy()
        if regions:
            temp_df = temp_df[temp_df[COLUMNS["region"]].isin(regions)]
        if states:
            temp_df = temp_df[temp_df[COLUMNS["state"]].isin(states)]
        return temp_df[COLUMNS["city"]].unique().tolist()


def create_filter(df: pd.DataFrame) -> DataFilter:
    """
    便捷函数：创建筛选器实例
    
    Args:
        df: 原始数据
        
    Returns:
        DataFilter: 筛选器实例
    """
    return DataFilter(df)
