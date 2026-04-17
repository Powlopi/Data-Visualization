import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px


df = pd.read_csv('Coffe_sales.csv')
df['Date'] = pd.to_datetime(df['Date'])
weekly_sales = df.groupby([pd.Grouper(key='Date', freq='W'), 'coffee_name'])['money'].sum().reset_index()
coffee_options = weekly_sales['coffee_name'].unique().tolist()


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
server = app.server  


app.layout = dbc.Container([
    html.Br(), 
    html.H1("Coffee Sales Dashboard", className="text-center text-light mb-4"),
    
    html.Div([
        html.Label("Select Coffee Type(s):", className="fw-bold text-light mb-2"),
        dcc.Dropdown(
            id='coffee-dropdown',
            options=[{'label': coffee, 'value': coffee} for coffee in coffee_options],
            value=coffee_options,
            multi=True,
            style={'color': '#000000'} 
        ),
    ], className="shadow p-4 mb-4 rounded border xl border-secondary"), 

    html.Div([
        dcc.Graph(id='coffee-graph')
    ], className="shadow p-2 rounded border border-secondary")
    
], fluid=False) 
 
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
        height=700, 
        labels={'money': 'Revenue ($)', 'Date': 'Date', 'coffee_name': 'Coffee Type'}
    )
    
    fig.update_layout(
        hovermode="x unified", 
        hoverlabel=dict(
            bgcolor="#2b2b2b", 
            font_color="white",
            bordercolor="#888888",
            font_size=12
        ),
        margin=dict(l=40, r=40, t=60, b=40),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    fig.update_xaxes(
        showspikes=True, 
        spikecolor="#535151", 
        spikethickness=0,     
        spikedash="dash"
    )
    
    return fig

if __name__ == '__main__':
    app.run(debug=False)