import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

# 1. Load Data
df = pd.read_csv('Coffe_sales.csv')
df['Date'] = pd.to_datetime(df['Date'])
weekly_sales = df.groupby([pd.Grouper(key='Date', freq='W'), 'coffee_name'])['money'].sum().reset_index()
coffee_options = weekly_sales['coffee_name'].unique().tolist()

# 2. Initialize the App
app = dash.Dash(__name__)
server = app.server  # <--- THIS IS CRITICAL FOR RENDER

# 3. App Layout
app.layout = html.Div([
    html.H1("Coffee Sales Dashboard", style={'textAlign': 'center', 'fontFamily': 'Arial'}),
    html.Label("Select Coffee Type(s):", style={'fontFamily': 'Arial', 'fontWeight': 'bold'}),
    
    dcc.Dropdown(
        id='coffee-dropdown',
        options=[{'label': coffee, 'value': coffee} for coffee in coffee_options],
        value=coffee_options,
        multi=True,
        style={'marginBottom': '20px'}
    ),
    dcc.Graph(id='coffee-graph')
])

# 4. Callback Logic
@app.callback(
    Output('coffee-graph', 'figure'),
    Input('coffee-dropdown', 'value')
)
def update_graph(selected_coffees):
    if not selected_coffees:
        return px.line(title="Please select at least one coffee type.")
        
    filtered_df = weekly_sales[weekly_sales['coffee_name'].isin(selected_coffees)]
    fig = px.line(
        filtered_df, x='Date', y='money', color='coffee_name', markers=True,
        title='Weekly Coffee Revenue', template='plotly_white',
        labels={'money': 'Revenue ($)', 'Date': 'Date', 'coffee_name': 'Coffee Type'}
    )
    fig.update_layout(hovermode="x unified")
    return fig

# 5. Run the App (Render handles the port automatically)
if __name__ == '__main__':
    app.run(debug=False)