import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

# Initialize the Dash app
app = Dash(__name__, title="Solar Panel Waste Dashboard")

# Load data
df = pd.read_csv('data/acap/solar_waste_aus.csv')

# Layout
app.layout = html.Div([
    html.H1("Solar Panel Waste Projections - Australia", style={'text-align': 'center'}),
    html.H3("Visualizing waste from small-scale and large-scale PV systems", style={'text-align': 'center'}),
    dcc.Dropdown(
        id='region-filter',
        options=[{'label': region, 'value': region} for region in df['Region'].unique()],
        value='Australia',
        style={'width': '50%', 'margin': 'auto'}
    ),
    dcc.Dropdown(
        id='system-type-filter',
        options=[{'label': system, 'value': system} for system in df['System_Type'].unique()],
        value='Small-Scale',
        style={'width': '50%', 'margin': 'auto', 'margin-top': '10px'}
    ),
    dcc.Graph(id='waste-graph'),
    dcc.Slider(
        id='year-slider',
        min=df['Year'].min(),
        max=df['Year'].max(),
        step=1,
        value=df['Year'].min(),
        marks={str(year): str(year) for year in df['Year'].unique()}
    )
], style={'padding': '20px'})

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