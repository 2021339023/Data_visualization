import streamlit as st
import plotly.express as px
import pandas as pd

def build_chart_ui():
    # Sidebar বা main UI তে chart type select করার জন্য
    return st.radio("Chart type", ["Line", "Bar", "Pie"], horizontal=True)

def render_chart(df: pd.DataFrame, chart_type: str, x_col: str, y_col: str):
    if chart_type == "Line":
        fig = px.line(df, x=x_col, y=y_col, markers=True)
    elif chart_type == "Bar":
        fig = px.bar(df, x=x_col, y=y_col)
    elif chart_type == "Pie":
        if x_col == y_col or not pd.api.types.is_numeric_dtype(df[y_col]):
            fig = px.pie(df, names=x_col)
        else:
            fig = px.pie(df, names=x_col, values=y_col)
    else:
        fig = px.scatter(df, x=x_col, y=y_col)

    fig.update_layout(margin=dict(l=10, r=10, t=30, b=10), height=500)
    return fig
