import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Load SpaceX dataset
spacex_df = pd.read_csv("spacex_launch_dash.csv")

# Get min & max payload
min_payload = spacex_df['Payload Mass (kg)'].min()
max_payload = spacex_df['Payload Mass (kg)'].max()

# Initialize Dash app
app = dash.Dash(__name__)

# -------------------------
# App Layout
# -------------------------
app.layout = html.Div(children=[

    html.H1(
        'SpaceX Launch Records Dashboard',
        style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}
    ),

    # -------- TASK 1: Launch Site Dropdown --------
    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {'label': 'All Sites', 'value': 'ALL'},
            {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
            {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
            {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
            {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}
        ],
        value='ALL',
        placeholder='Select a Launch Site here',
        searchable=True
    ),

    html.Br(),

    # -------- TASK 2: Pie Chart --------
    dcc.Graph(id='success-pie-chart'),

    html.Br(),

    html.P("Payload range (Kg):"),

    # -------- TASK 3: Payload Slider --------
    dcc.RangeSlider(
        id='payload-slider',
        min=0,
        max=10000,
        step=1000,
        value=[min_payload, max_payload],
        marks={i: str(i) for i in range(0, 10001, 2500)}
    ),

    html.Br(),

    # -------- TASK 4: Scatter Plot --------
    dcc.Graph(id='success-payload-scatter-chart')
])

# -------------------------
# TASK 2: Pie Chart Callback
# -------------------------
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)
def update_pie_chart(site):
    if site == 'ALL':
        fig = px.pie(
            spacex_df,
            values='class',
            names='Launch Site',
            title='Total Success Launches By Site'
        )
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == site]
        fig = px.pie(
            filtered_df,
            names='class',
            title=f'Total Success Launches for site {site}'
        )
    return fig

# -------------------------
# TASK 4: Scatter Plot Callback
# -------------------------
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [
        Input('site-dropdown', 'value'),
        Input('payload-slider', 'value')
    ]
)
def update_scatter(site, payload_range):
    low, high = payload_range

    filtered_df = spacex_df[
        (spacex_df['Payload Mass (kg)'] >= low) &
        (spacex_df['Payload Mass (kg)'] <= high)
    ]

    if site == 'ALL':
        fig = px.scatter(
            filtered_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title='Correlation between Payload and Success for all Sites'
        )
    else:
        site_df = filtered_df[filtered_df['Launch Site'] == site]
        fig = px.scatter(
            site_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title=f'Correlation between Payload and Success for site {site}'
        )
    return fig

# -------------------------
# Run App
# -------------------------
if __name__ == '__main__':
    app.run(debug=True)
