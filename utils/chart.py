import altair as alt


def get_chart(data):
    hover = alt.selection_single(
        fields=["date"],
        nearest=True,
        on="mouseover",
        empty="none",
    )

    lines = (
        alt.Chart(data, title="Human Efficiency by Departments")
        .mark_line()
        .encode(
            x="WEEK",
            y="HUMAN_EFFICIENCY",
            color="DEPARTMENT",
            strokeDash="DEPARTMENT",
        )
    )

    # Draw points on the line, and highlight based on selection
    points = lines.transform_filter(hover).mark_circle(size=65)

    # Draw a rule at the location of the selection
    tooltips = (
        alt.Chart(data)
        .mark_rule()
        .encode(
            x="WEEK",
            y="HUMAN_EFFICIENCY",
            opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
            tooltip=[
                alt.Tooltip("WEEK", title="Date"),
                alt.Tooltip("HUMAN_EFFICIENCY", title="Price (USD)"),
            ],
        )
        .add_selection(hover)
    )

    return (lines + points + tooltips).interactive()