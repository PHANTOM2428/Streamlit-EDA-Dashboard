"""
数据加载模块 - 负责数据的读取和初始化
"""
import os
import pandas as pd
import streamlit as st
from src.utils.constants import DATA_CONFIG, DATE_COLUMN


class DataLoader:
    """数据加载器类 - 处理数据文件的读取"""
    
    def __init__(self):
        self.encoding = DATA_CONFIG["encoding"]
        self.default_file = DATA_CONFIG["default_file"]
    
    def load_from_upload(self, uploaded_file) -> pd.DataFrame:
        """
        从上传的文件加载数据
        
        Args:
            uploaded_file: Streamlit 上传的文件对象
            
        Returns:
            pd.DataFrame: 加载的数据
        """
        if uploaded_file is not None:
            filename = uploaded_file.name
            st.write(filename)
            return pd.read_csv(uploaded_file, encoding=self.encoding)
        return None
    
    def load_default_data(self) -> pd.DataFrame:
        """
        加载默认数据文件
        
        Returns:
            pd.DataFrame: 默认数据
        """
        # 获取当前文件所在目录
        current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        file_path = os.path.join(current_dir, self.default_file)
        return pd.read_csv(file_path, encoding=self.encoding)
    
    def load_data(self, uploaded_file=None) -> pd.DataFrame:
        """
        加载数据的主入口方法
        优先使用上传的文件，否则使用默认文件
        
        Args:
            uploaded_file: Streamlit 上传的文件对象
            
        Returns:
            pd.DataFrame: 加载的数据
        """
        df = self.load_from_upload(uploaded_file)
        if df is not None:
            return df
        return self.load_default_data()
    
    def parse_dates(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        解析日期列
        
        Args:
            df: 原始数据
            
        Returns:
            pd.DataFrame: 解析日期后的数据
        """
        df = df.copy()
        df[DATE_COLUMN] = pd.to_datetime(df[DATE_COLUMN])
        return df
    
    def get_date_range(self, df: pd.DataFrame) -> tuple:
        """
        获取数据集的日期范围
        
        Args:
            df: 包含日期列的数据
            
        Returns:
            tuple: (开始日期, 结束日期)
        """
        dates = pd.to_datetime(df[DATE_COLUMN])
        return dates.min(), dates.max()


def load_and_prepare_data(uploaded_file=None) -> pd.DataFrame:
    """
    便捷函数：加载并准备数据
    
    Args:
        uploaded_file: Streamlit 上传的文件对象
        
    Returns:
        pd.DataFrame: 准备好的数据
    """
    loader = DataLoader()
    df = loader.load_data(uploaded_file)
    df = loader.parse_dates(df)
    return df
