import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

# 1. Load Data
df = pd.read_csv('Coffe_sales.csv')
df['Date'] = pd.to_datetime(df['Date'])
weekly_sales = df.groupby([pd.Grouper(key='Date', freq='W'), 'coffee_name'])['money'].sum().reset_index()
coffee_options = weekly_sales['coffee_name'].unique().tolist()

# 2. Initialize the App WITH Dark Mode Theme
# 'DARKLY' is a sleek, flat dark theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
server = app.server  

# 3. App Layout 
app.layout = dbc.Container([
    html.Br(), 
    # text-light makes the title pop against the dark background
    html.H1("Coffee Sales Dashboard", className="text-center text-light mb-4"),
    
    html.Div([
        html.Label("Select Coffee Type(s):", className="fw-bold text-light mb-2"),
        # We force the text inside the dropdown box to be black so it remains readable 
        dcc.Dropdown(
            id='coffee-dropdown',
            options=[{'label': coffee, 'value': coffee} for coffee in coffee_options],
            value=coffee_options,
            multi=True,
            style={'color': '#000000'} 
        ),
    ], className="shadow p-4 mb-4 rounded border border-secondary"), 

    html.Div([
        dcc.Graph(id='coffee-graph')
    ], className="shadow p-2 rounded border border-secondary")
    
], fluid=False) 

# 4. Callback Logic 
@app.callback(
    Output('coffee-graph', 'figure'),
    Input('coffee-dropdown', 'value')
)
def update_graph(selected_coffees):
    if not selected_coffees:
        return px.line(title="Please select at least one coffee type.", template='plotly_dark')
        
    filtered_df = weekly_sales[weekly_sales['coffee_name'].isin(selected_coffees)]
    
    fig = px.line(
        filtered_df, x='Date', y='money', color='coffee_name', markers=True,
        title='Weekly Coffee Revenue', template='plotly_dark',
        labels={'money': 'Revenue ($)', 'Date': 'Date', 'coffee_name': 'Coffee Type'}
    )
    
    fig.update_layout(
        hovermode="x unified", 
        # --- NEW CODE: Forces the hover box to be dark grey with white text ---
        hoverlabel=dict(
            bgcolor="#2b2b2b", 
            font_color="white",
            bordercolor="#888888"
        ),
        # ----------------------------------------------------------------------
        margin=dict(l=20, r=20, t=50, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    return fig

if __name__ == '__main__':
    app.run(debug=False)