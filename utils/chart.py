import altair as alt

# There are 6 metrics in the final view: 
# Overheads per productive hour
def overhead_per_prod(data):
    hover = alt.selection_single(
        fields=["DATE"],
        nearest=True,
        on="mouseover",
        empty="none",
    )

    lines = (
        alt.Chart(data, title="Overheads per Productive Hour")
        .mark_line()
        .encode(
            x="DATE",
            y="OVERHEADS_PER_PRODUCTIVE",
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
            y="OVERHEADS_PER_PRODUCTIVE",
            opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
            tooltip=[
                alt.Tooltip("DATE", title="Date"),
                alt.Tooltip("OVERHEADS_PER_PRODUCTIVE", title="Overhead(s)"),
            ],
        )
        .add_selection(hover)
    )

    return (lines + points + tooltips).interactive()

# average daily artists
def avg_daily_artists(data):
    hover = alt.selection_single(
        fields=["DATE"],
        nearest=True,
        on="mouseover",
        empty="none",
    )

    lines = (
        alt.Chart(data, title="Overheads per Productive Hour")
        .mark_line()
        .encode(
            x="DATE",
            y="ARTISTS",
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
            y="ARTISTS",
            opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
            tooltip=[
                alt.Tooltip("DATE", title="Date"),
                alt.Tooltip("ARTISTS", title="Artist(s)"),
            ],
        )
        .add_selection(hover)
    )

    return (lines + points + tooltips).interactive()


# filesize productivity (size of files submitted)
def filesize_productivity(data):
    hover = alt.selection_single(
        fields=["DATE"],
        nearest=True,
        on="mouseover",
        empty="none",
    )

    lines = (
        alt.Chart(data, title="Filesize Productivity")
        .mark_line()
        .encode(
            x="DATE",
            y="FILESIZE_PRODUCTIVITY",
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
            y="FILESIZE_PRODUCTIVITY",
            opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
            tooltip=[
                alt.Tooltip("DATE", title="Date"),
                alt.Tooltip("FILESIZE_PRODUCTIVITY", title="mb"),
            ],
        )
        .add_selection(hover)
    )

    return (lines + points + tooltips).interactive()

# count productivity (number of files submitted including duplicate submissions)
def count_productivity(data):
    hover = alt.selection_single(
        fields=["DATE"],
        nearest=True,
        on="mouseover",
        empty="none",
    )

    lines = (
        alt.Chart(data, title="Count Productivity")
        .mark_line()
        .encode(
            x="DATE",
            y="COUNT_PRODUCTIVITY",
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
            y="COUNT_PRODUCTIVITY",
            opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
            tooltip=[
                alt.Tooltip("DATE", title="Date"),
                alt.Tooltip("COUNT_PRODUCTIVITY", title="File(s)"),
            ],
        )
        .add_selection(hover)
    )

    return (lines + points + tooltips).interactive()

# review productivity (their old one)
def review_productivity(data):
    hover = alt.selection_single(
        fields=["DATE"],
        nearest=True,
        on="mouseover",
        empty="none",
    )

    lines = (
        alt.Chart(data, title="Review Productivity")
        .mark_line()
        .encode(
            x="DATE",
            y="REVIEW_PRODUCTIVITY",
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
            y="REVIEW_PRODUCTIVITY",
            opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
            tooltip=[
                alt.Tooltip("DATE", title="Date"),
                alt.Tooltip("REVIEW_PRODUCTIVITY", title="File(s)"),
            ],
        )
        .add_selection(hover)
    )

    return (lines + points + tooltips).interactive()

# average wait time
def avg_wait_time(data):
    hover = alt.selection_single(
        fields=["DATE"],
        nearest=True,
        on="mouseover",
        empty="none",
    )

    lines = (
        alt.Chart(data, title="Review Productivity")
        .mark_line()
        .encode(
            x="DATE",
            y="AVG_WAITTIME",
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
            y="AVG_WAITTIME",
            opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
            tooltip=[
                alt.Tooltip("DATE", title="Date"),
                alt.Tooltip("REVIEW_PRODUCTIVITY", title="File(s)"),
            ],
        )
        .add_selection(hover)
    )

    return (lines + points + tooltips).interactive()