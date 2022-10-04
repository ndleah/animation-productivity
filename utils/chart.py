import altair as alt


def get_chart(data):
    hover = alt.selection_single(
        fields=["week"],
        nearest=True,
        on="mouseover",
        empty="none",
    )

    lines = (
        alt.Chart(data, title="Human Efficiency by Departments")
        .mark_line()
        .encode(
            x="week",
            y="human_efficiency",
            color="department",
            strokeDash="department",
        )
    )

    # Draw points on the line, and highlight based on selection
    points = lines.transform_filter(hover).mark_circle(size=65)

    # Draw a rule at the location of the selection
    tooltips = (
        alt.Chart(data)
        .mark_rule()
        .encode(
            x="week",
            y="human_efficiency",
            opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
            tooltip=[
                alt.Tooltip("week", title="Date"),
                alt.Tooltip("human_efficiency", title="Price (USD)"),
            ],
        )
        .add_selection(hover)
    )

    return (lines + points + tooltips).interactive()