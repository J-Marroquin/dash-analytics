import plotly.graph_objects as go

def create_empty_fig(message: str) -> go.Figure:
    """
    Creates an empty Plotly figure with a centered annotation message.

    This function generates a placeholder figure that can be used to indicate
    the absence of data or display an informational message.

    Args:
    -----
    message (str): 
        The message to display in the center of the figure.

    Returns:
    --------
    plotly.graph_objects.Figure: 
        A Plotly figure with a centered annotation and no visible axes.

    Notes:
        - The figure includes a title "Aviso" to indicate a notification or warning.
        - The annotation is positioned at the center of the figure with a font size of 20.
        - The axes are hidden for a clean, message-only display.
    """
    fig = go.Figure()
    fig.add_annotation(
        text=message,
        xref="paper", yref="paper",
        x=0.5, y=0.5,
        showarrow=False,
        font=dict(size=20)
    )
    fig.update_layout(
        title="Aviso",
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        template="seaborn"
    )
    return fig