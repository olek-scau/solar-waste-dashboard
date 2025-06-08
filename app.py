import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

# Initialize the Dash app
app = Dash(__name__, title="Solar Panel Waste Projection Dashboard")

# Explicitly define server for Gunicorn
server = app.server

# Load data
df = pd.read_csv('data/acap/solar_waste_aus.csv')

# Layout
app.layout = html.Div([
    html.H1("Solar Panel Waste Projections - Victoria, Australia"),
    html.P("Interactive dashboard to visualize solar panel waste projections based on UNSW/ACAP data."),
    dcc.Graph(id='waste-graph'),
    dcc.Slider(
        id='year-slider',
        min=df['Year'].min(),
        max=df['Year'].max(),
        step=1,
        value=df['Year'].min(),
        marks={str(year): str(year) for year in df['Year'].unique()},
        tooltip={"placement": "bottom", "always_visible": True}
    ),
    html.Footer("Data Source: UNSW/ACAP Study, 2024. Built for solar recycling business.")
], style={'padding': '20px', 'fontFamily': 'Arial'})

# Callback to update graph
@app.callback(
    Output('waste-graph', 'figure'),
    [Input('year-slider', 'value'),
     Input('region-filter', 'value'),
     Input('system-type-filter', 'value')]
)
def update_graph(selected_year, selected_region, selected_system):
    filtered_df = df[(df['Year'] <= selected_year) & 
                     (df['Region'] == selected_region) & 
                     (df['System_Type'] == selected_system)]
    fig = px.line(filtered_df, x='Year', y='Waste_Tonnes', 
                  title=f'Solar Panel Waste ({selected_region}, {selected_system})',
                  labels={'Waste_Tonnes': 'Waste (Tonnes)'})
    fig.update_layout(transition_duration=500)
    return fig

# Run server (use for local testing)
if __name__ == '__main__':
    app.run_server(debug=True)