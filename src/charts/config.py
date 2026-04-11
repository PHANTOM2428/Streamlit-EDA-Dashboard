from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class ChartConfig:
    height: int = 350
    width: Optional[int] = None
    template: str = "seaborn"


class ChartTemplates:
    SEABORN = "seaborn"
    GRIDON = "gridon"
    PLOTLY_DARK = "plotly_dark"


class ChartLayouts:
    @staticmethod
    def get_bar_layout(height: int = 350) -> Dict[str, Any]:
        return {"height": height}

    @staticmethod
    def get_pie_layout(height: int = 350) -> Dict[str, Any]:
        return {"height": height}

    @staticmethod
    def get_line_layout(height: int = 500, width: int = 1000) -> Dict[str, Any]:
        return {"height": height, "width": width}

    @staticmethod
    def get_treemap_layout(height: int = 650, width: int = 800) -> Dict[str, Any]:
        return {"height": height, "width": width}

    @staticmethod
    def get_scatter_layout(
        title: str,
        xaxis_title: str,
        yaxis_title: str,
        title_font_size: int = 20,
        axis_font_size: int = 19
    ) -> Dict[str, Any]:
        return {
            "title": {
                "text": title,
                "font": {"size": title_font_size}
            },
            "xaxis_title": xaxis_title,
            "yaxis_title": yaxis_title,
            "xaxis_title_font": {"size": axis_font_size},
            "yaxis_title_font": {"size": axis_font_size}
        }
