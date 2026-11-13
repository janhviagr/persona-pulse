
import streamlit as st
import plotly.express as px


# --------------------------------------------------
# COMMON CHART STYLING
# --------------------------------------------------

def format_chart(fig, height=390):

    fig.update_layout(
        height=height,
        font=dict(
            family="Arial",
            size=14,
            color="#334155"
        ),
        title_font=dict(
            size=19,
            color="#172554"
        ),
        margin=dict(
            l=45,
            r=30,
            t=65,
            b=65
        ),
        hoverlabel=dict(
            bgcolor="white",
            font_size=14,
            font_family="Arial"
        ),
        hovermode="closest"
    )

    fig.update_xaxes(
        showline=True,
        linecolor="#CBD5E1",
        gridcolor="#E2E8F0",
        tickfont=dict(size=12, color="#334155")
    )

    fig.update_yaxes(
        showline=False,
        gridcolor="#E2E8F0",
        tickfont=dict(size=12, color="#334155")
    )

    return fig


# --------------------------------------------------
# DISPLAY ANY PLOTLY CHART
# --------------------------------------------------

def show_chart(fig, height=390):

    fig = format_chart(fig, height)

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "displayModeBar": True,
            "responsive": True
        }
    )


# --------------------------------------------------
# BAR CHART
# --------------------------------------------------

def create_bar_chart(
    data,
    x,
    y,
    title,
    color=None,
    orientation="v"
):

    fig = px.bar(
        data,
        x=x,
        y=y,
        color=color,
        title=title,
        orientation=orientation,
        text_auto=True
    )

    return format_chart(fig)


# --------------------------------------------------
# PIE / DONUT CHART
# --------------------------------------------------

def create_pie_chart(
    data,
    names,
    values,
    title,
    donut=True
):

    fig = px.pie(
        data,
        names=names,
        values=values,
        hole=0.45 if donut else 0,
        title=title
    )

    fig.update_traces(
        textposition="inside",
        textinfo="percent+label"
    )

    return format_chart(fig)


# --------------------------------------------------
# HISTOGRAM
# --------------------------------------------------

def create_histogram(
    data,
    x,
    title,
    bins=12
):

    fig = px.histogram(
        data,
        x=x,
        nbins=bins,
        title=title
    )

    return format_chart(fig)


# --------------------------------------------------
# LINE CHART
# --------------------------------------------------

def create_line_chart(
    data,
    x,
    y,
    title,
    color=None
):

    fig = px.line(
        data,
        x=x,
        y=y,
        color=color,
        title=title,
        markers=True
    )

    return format_chart(fig)
