import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash import Dash, dcc, html

# Initialize the Dash app
app = Dash(__name__)
server = app.server

# Load the datasets
aus_data = pd.read_csv('data/acap/solar_waste_aus.csv')
states_data = pd.read_csv('data/acap/solar_waste_aus_states.csv')

# Pivot the Australia data to have Small-Scale and Large-Scale as columns
aus_pivot = aus_data.pivot(index='Year', columns='System_Type', values='Waste_Tonnes').reset_index()

# Create the Plotly figure with secondary y-axis
fig = make_subplots(specs=[[{"secondary_y": True}]])

# Add stacked bar traces for state-level annual waste (excluding Total column)
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

# Update layout
fig.update_layout(
    title='Solar Panel Waste in Australia: Annual by State and Cumulative by System Type (2023-2035)',
    xaxis_title='Year',
    yaxis_title='Annual Waste (Tonnes)',
    yaxis2_title='Cumulative Waste (Tonnes)',
    barmode='stack',
    legend=dict(x=0.01, y=0.99, bgcolor='rgba(255,255,255,0.5)'),
    template='plotly_white',
    height=600
)

# Update axes
fig.update_yaxes(title_text='Annual Waste (Tonnes)', secondary_y=False)
fig.update_yaxes(title_text='Cumulative Waste (Tonnes)', secondary_y=True)

# Define the Dash layout
app.layout = html.Div([
    html.H1('Solar Panel Waste in Australia', style={'textAlign': 'center'}),
    html.P('Annual solar panel waste by state and cumulative waste by system type (2023-2035).', style={'textAlign': 'center'}),
    dcc.Graph(id='solar-waste-plot', figure=fig),
    html.P('Data Source: ACAP (Australian Centre of Advanced Photovoltaics).', style={'textAlign': 'center', 'fontSize': 12})
])

# Run the app (only for local development, not needed on Render)
if __name__ == '__main__':
    app.run_server(debug=True)