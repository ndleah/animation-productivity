import pandas as pd
import streamlit as st
import altair as alt


# average daily artists
def build_metric(data, metric, title):

    hover = alt.selection_single(
        fields=["DATE"],
        nearest=True,
        on="mouseover",
        empty="none",
    )

    lines = (
        alt.Chart(data, title=title)
        .mark_line()
        .encode(
            x="DATE",
            y=metric,
            color="DEPARTMENT_NAME",
            strokeDash="DEPARTMENT_NAME",
        )
    )

    # Draw points on the line, and highlight based on selection
    points = lines.transform_filter(hover).mark_circle(size=65)

    # Draw a rule at the location of the selection
    tooltips = (
        alt.Chart(data)
        .mark_rule()
        .encode(
            x="DATE",
            y=metric,
            opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
            tooltip=[
                alt.Tooltip("DATE", title="Date"),
                alt.Tooltip(metric),
            ],
        )
        .properties(height=600)
        .add_selection(hover)
    )

    return (lines + points + tooltips).interactive()