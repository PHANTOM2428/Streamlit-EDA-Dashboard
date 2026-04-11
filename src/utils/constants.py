"""
常量配置模块 - 集中管理项目中的常量配置
"""

# 页面配置
PAGE_CONFIG = {
    "page_title": "Superstore!!!",
    "page_icon": ":bar_chart:",
    "layout": "wide"
}

# 数据文件配置
DATA_CONFIG = {
    "default_file": "Superstore.csv",
    "encoding": "ISO-8859-1",
    "supported_formats": ["csv", "txt", "xlsx", "xls"]
}

# 日期列名
DATE_COLUMN = "Order Date"

# 关键列名
COLUMNS = {
    "region": "Region",
    "state": "State",
    "city": "City",
    "category": "Category",
    "sub_category": "Sub-Category",
    "segment": "Segment",
    "sales": "Sales",
    "profit": "Profit",
    "quantity": "Quantity",
    "order_date": "Order Date"
}

# 图表配置
CHART_CONFIG = {
    "default_template": "seaborn",
    "default_height": 350,
    "time_series_height": 500,
    "treemap_width": 800,
    "treemap_height": 650,
    "pie_hole": 0.5
}

# 表格样式配置
TABLE_CONFIG = {
    "category_cmap": "Blues",
    "region_cmap": "Oranges",
    "summary_cmap": "Cividis"
}

# 筛选器配置
FILTER_CONFIG = {
    "sidebar_header": "Choose your filter: ",
    "region_label": "Pick your Region",
    "state_label": "Pick the State",
    "city_label": "Pick the City"
}
