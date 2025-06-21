import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Load the datasets
aus_data = pd.read_csv('data/acap/solar_waste_aus.csv')
states_data = pd.read_csv('data/acap/solar_waste_aus_states.csv')

# Debug: Print data to verify loading
print("aus_data head:\n", aus_data.head())
print("states_data head:\n", states_data.head())

# Pivot the Australia data to have Small-Scale and Large-Scale as columns
aus_pivot = aus_data.pivot(index='Year', columns='System_Type', values='Waste_Tonnes').reset_index()
print("aus_pivot head:\n", aus_pivot.head())

# Create the Plotly figure with secondary y-axis
fig = make_subplots(specs=[[{"secondary_y": True}]])

# Add stacked bar traces for state-level annual waste
states = ['ACT', 'NSW', 'NT', 'QLD', 'SA', 'TAS', 'VIC', 'WA']
colors = ['#0000FF', '#87CEEB', '#000000', '#800000', '#FF0000', '#008000', '#000080', '#FFD700']
for state, color in zip(states, colors):
    fig.add_trace(
        go.Bar(
            x=states_data['Year'],
            y=states_data[state],
            name=state,
            marker_color=color,
            opacity=0.8
        ),
        secondary_y=False
    )

# Add line traces for cumulative waste (Small-Scale and Large-Scale)
fig.add_trace(
    go.Scatter(
        x=aus_pivot['Year'],
        y=aus_pivot['Small-Scale'],
        name='Small-Scale (Cumulative)',
        line=dict(color='blue', width=3, dash='dash')
    ),
    secondary_y=True
)
fig.add_trace(
    go.Scatter(
        x=aus_pivot['Year'],
        y=aus_pivot['Large-Scale'],
        name='Large-Scale (Cumulative)',
        line=dict(color='red', width=3, dash='dot')
    ),
    secondary_y=True
)

# Update layout with darker grey background
fig.update_layout(
    xaxis_title='Year',
    yaxis_title='Annual Waste (Tonnes)',
    yaxis2_title='Cumulative Waste (Tonnes)',
    barmode='stack',
    legend=dict(x=0.01, y=0.99, bgcolor='rgba(255,255,255,0.8)'),
    template='plotly_white',
    paper_bgcolor='#d3d3d3',  # Darker grey background
    plot_bgcolor='#d3d3d3',  # Darker grey plotting area
    height=None,
    margin=dict(l=80, r=7, t=20, b=50),  # Reduce right margin for balance
    autosize=True
)

# Update axes to balance spacing
fig.update_yaxes(
    title_text='Annual Waste (Tonnes)',
    title_standoff=5,  # Consistent left y-axis title distance
    secondary_y=False
)
fig.update_yaxes(
    title_text='Cumulative Waste (Tonnes)',
    title_standoff=20,  # Reduce right y-axis title distance
    gridcolor='black',
    secondary_y=True
)

# Generate Plotly HTML content (without full HTML)
plot_html = fig.to_html(include_plotlyjs='cdn', full_html=False)

# Define complete HTML with custom title, CSS, and JavaScript for dynamic axis visibility
html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Solar Waste Dashboard</title>
    <script src="https://cdn.plot.ly/plotly-2.34.0.min.js"></script>
    <style>
        body {{
            margin: 0;
            padding: 0;
            font-family: Arial, sans-serif;
            display: flex;
            flex-direction: column;
            min-height: 100vh;
            background-color: #d3d3d3;
        }}
        h1 {{
            text-align: center;
            color: #333;
            margin: 20px 0;
            font-size: 1.8em;
        }}
        h2 {{
            text-align: center;
            color: #233;
            margin: 3px 0;
            font-size: 1.3em;
        }}
        .plotly-graph-div {{
            flex: 1;
            width: 100% !important;
            height: calc(100vh - 110px) !important;
        }}
        @media (max-width: 600px) {{
            h1 {{ font-size: 1.2em; }}
            h2 {{ font-size: 1.2em; }}
            .plotly-graph-div {{ height: calc(100vh - 60px) !important; }}
        }}
    </style>
</head>
<body>
    <h1>Estimated Solar Panel Waste in Australia (2023-2035)</h1>
    <h2>Annual by State and Cumulative by System Type</h2>
    {plot_html}
    <script>
        // Get the Plotly plot div (assuming it's the first plotly-graph-div)
        var plotDiv = document.getElementsByClassName('plotly-graph-div')[0];

        // Listen for legend click events
        plotDiv.on('plotly_legendclick', function(data) {{
            // Check visibility of cumulative waste traces (last two traces: Small-Scale and Large-Scale)
            var smallScaleVisible = data.data[data.data.length - 2].visible === true;
            var largeScaleVisible = data.data[data.data.length - 1].visible === true;

            // Determine if secondary y-axis should be visible
            var showSecondaryAxis = smallScaleVisible || largeScaleVisible;

            // Update layout to show/hide secondary y-axis
            Plotly.relayout(plotDiv, {{
                'yaxis2.showticklabels': showSecondaryAxis,
                'yaxis2.ticks': showSecondaryAxis ? 'outside' : '',
                'yaxis2.gridcolor': showSecondaryAxis ? 'black' : null,
                'yaxis2.title.text': showSecondaryAxis ? 'Cumulative Waste (Tonnes)' : '',
                'yaxis2.showgrid': showSecondaryAxis
            }});

            // Return false to prevent default legend click behavior (if needed)
            return true;
        }});
    </script>
</body>
</html>
"""

# Save directly to visualization.html
with open('docs/visualization.html', 'w') as f:
    f.write(html_content)