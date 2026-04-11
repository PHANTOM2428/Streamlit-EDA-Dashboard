import plotly.express as px
import plotly.figure_factory as ff
import pandas as pd
from typing import List, Optional
from .config import ChartTemplates, ChartLayouts


class ChartGenerator:
    @staticmethod
    def create_bar_chart(
        df: pd.DataFrame,
        x: str,
        y: str,
        text_format: str = "${:,.2f}",
        template: str = ChartTemplates.SEABORN,
        height: int = 350
    ):
        fig = px.bar(
            df,
            x=x,
            y=y,
            text=[text_format.format(val) for val in df[y]],
            template=template
        )
        fig.update_layout(height=height)
        return fig

    @staticmethod
    def create_pie_chart(
        df: pd.DataFrame,
        values: str,
        names: str,
        hole: float = 0.5,
        template: str = ChartTemplates.SEABORN,
        height: int = 350,
        text_position: str = "outside"
    ):
        fig = px.pie(
            df,
            values=values,
            names=names,
            hole=hole,
            template=template
        )
        fig.update_layout(height=height)
        fig.update_traces(textposition=text_position)
        return fig

    @staticmethod
    def create_pie_chart_inside(
        df: pd.DataFrame,
        values: str,
        names: str,
        template: str = ChartTemplates.SEABORN
    ):
        fig = px.pie(
            df,
            values=values,
            names=names,
            template=template
        )
        fig.update_traces(text=df[names], textposition="inside")
        return fig

    @staticmethod
    def create_line_chart(
        df: pd.DataFrame,
        x: str,
        y: str,
        labels: Optional[dict] = None,
        height: int = 500,
        width: int = 1000,
        template: str = ChartTemplates.GRIDON
    ):
        fig = px.line(
            df,
            x=x,
            y=y,
            labels=labels or {},
            height=height,
            width=width,
            template=template
        )
        return fig

    @staticmethod
    def create_treemap(
        df: pd.DataFrame,
        path: List[str],
        values: str,
        hover_data: Optional[List[str]] = None,
        color: Optional[str] = None,
        height: int = 650,
        width: int = 800
    ):
        fig = px.treemap(
            df,
            path=path,
            values=values,
            hover_data=hover_data or [values],
            color=color
        )
        fig.update_layout(height=height, width=width)
        return fig

    @staticmethod
    def create_scatter_plot(
        df: pd.DataFrame,
        x: str,
        y: str,
        size: str,
        title: str = "",
        xaxis_title: str = "",
        yaxis_title: str = ""
    ):
        fig = px.scatter(
            df,
            x=x,
            y=y,
            size=size
        )
        layout_config = ChartLayouts.get_scatter_layout(
            title=title,
            xaxis_title=xaxis_title,
            yaxis_title=yaxis_title
        )
        fig.update_layout(**layout_config)
        return fig

    @staticmethod
    def create_table(
        df: pd.DataFrame,
        colorscale: str = "Cividis"
    ):
        return ff.create_table(df, colorscale=colorscale)
