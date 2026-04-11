import plotly.express as px
import plotly.figure_factory as ff


def create_bar_chart(data, x, y, text_template="${:,.2f}", template="seaborn", height=350):
    fig = px.bar(
        data,
        x=x,
        y=y,
        text=[text_template.format(val) for val in data[y]],
        template=template
    )
    fig.update_layout(height=height)
    return fig


def create_pie_chart(data, values, names, hole=0.5, template="plotly", height=350, textposition="outside"):
    fig = px.pie(
        data,
        values=values,
        names=names,
        hole=hole,
        template=template
    )
    fig.update_layout(height=height)
    fig.update_traces(textposition=textposition)
    return fig


def create_line_chart(data, x, y, labels=None, height=500, width=1000, template="gridon"):
    fig = px.line(data, x=x, y=y, labels=labels, height=height, width=width, template=template)
    return fig


def create_treemap(data, path, values, hover_data=None, color=None, width=800, height=650):
    fig = px.treemap(
        data,
        path=path,
        values=values,
        hover_data=hover_data,
        color=color
    )
    fig.update_layout(width=width, height=height)
    return fig


def create_scatter_plot(data, x, y, size=None, title="", title_font_size=20, axis_font_size=19):
    fig = px.scatter(data, x=x, y=y, size=size)
    fig.update_layout(
        title={"text": title, "font": {"size": title_font_size}},
        xaxis_title=x,
        yaxis_title=y,
        xaxis_title_font={"size": axis_font_size},
        yaxis_title_font={"size": axis_font_size}
    )
    return fig


def create_table(data, colorscale="Cividis"):
    return ff.create_table(data, colorscale=colorscale)
