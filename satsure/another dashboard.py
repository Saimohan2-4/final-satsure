import pandas as pd
from datetime import datetime, timedelta
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objs as go

# Load the dataset

df = pd.read_csv('/home/saiharan/Documents/projects/travel agency analysis/satsure/sample_dataset_large.csv')

# Convert necessary columns to datetime
df['Date'] = pd.to_datetime(df['Date'])
df['Start_Date'] = pd.to_datetime(df['Start_Date'])
df['End_Date'] = pd.to_datetime(df['End_Date'])

# Calculate Cycle Time
df['Cycle_Time'] = (df['End_Date'] - df['Start_Date']).dt.days

# Calculate Sprints (assuming 2-week sprints)
df['Sprint'] = ((df['Date'] - df['Date'].min()) // pd.Timedelta(weeks=2)).astype(int) + 1

# Calculate Velocity
velocity = df[df['Status'] == 'Done'].groupby('Sprint')['Story_Points'].sum().reset_index()

# Calculate Defect Rate
defect_rate = df.groupby('Sprint')['Defects_Reported'].sum().reset_index()

# Initialize the Dash app
app = dash.Dash(__name__)

# Layout with 3 pages and navigation buttons
app.layout = html.Div(style={'background-color': 'black', 'color': 'white'}, children=[
    html.H1('Software Development Metrics Dashboard'),
    
    html.Div([
        html.Button('Page 1', id='page-1-button', n_clicks=0),
        html.Button('Page 2', id='page-2-button', n_clicks=0),
        html.Button('Page 3', id='page-3-button', n_clicks=0),
    ], style={'text-align': 'center'}),
    
    html.Div(id='page-content')
])

@app.callback(
    Output('page-content', 'children'),
    [Input('page-1-button', 'n_clicks'),
     Input('page-2-button', 'n_clicks'),
     Input('page-3-button', 'n_clicks')]
)
def display_page(page_1_clicks, page_2_clicks, page_3_clicks):
    ctx = dash.callback_context

    if not ctx.triggered:
        return render_page_1()
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == 'page-1-button':
        return render_page_1()
    elif button_id == 'page-2-button':
        return render_page_2()
    elif button_id == 'page-3-button':
        return render_page_3()

def render_page_1():
    return html.Div([
        html.Div([
            dcc.RadioItems(
                id='sprint-radioitems',
                options=[{'label': f'Sprint {i}', 'value': i} for i in velocity['Sprint'].unique()],
                value=velocity['Sprint'].unique()[0],
                inline=True
            )
        ], style={'text-align': 'left', 'color': 'white'}),
        html.Div([
            dcc.Graph(id='velocity-graph', style={'display': 'inline-block', 'width': '49%', 'padding-left': '10px', 'padding-right': '15px'}),
            dcc.Graph(id='cycle-time-graph', style={'display': 'inline-block', 'width': '49%'})
        ]),
        dcc.Graph(id='defect-rate-graph', style={'display': 'flex', 'width': '49%', 'padding-top': '5px', 'padding-bottom': '10px', 'align-items': 'center', 'margin': 'auto', 'padding-left': '10px'})
    ])

@app.callback(
    [Output('velocity-graph', 'figure'),
     Output('cycle-time-graph', 'figure'),
     Output('defect-rate-graph', 'figure')],
    [Input('sprint-radioitems', 'value')]
)
def update_page_1(selected_sprint):
    filtered_df = df[df['Sprint'] == selected_sprint]
    
    # Velocity Chart
    velocity_fig = px.bar(velocity, x='Sprint', y='Story_Points', title='Velocity')
    velocity_fig.update_traces(marker_color=['red' if sprint == selected_sprint else 'blue' for sprint in velocity['Sprint']])
    
    # Cycle Time Chart
    cycle_time_fig = px.line(filtered_df, x='Task_ID', y='Cycle_Time', title='Cycle Time')
    
    # Defect Rate Chart
    defect_rate_fig = px.bar(defect_rate, x='Sprint', y='Defects_Reported', title='Defect Rate')
    defect_rate_fig.update_traces(marker_color=['red' if sprint == selected_sprint else 'blue' for sprint in defect_rate['Sprint']])

    return velocity_fig, cycle_time_fig, defect_rate_fig

def render_page_2():
    return html.Div([
        # Add 4 more metrics here
        # Example:
        dcc.Graph(id='tasks-completed-graph'),
        dcc.Graph(id='hours-logged-graph'),
        dcc.Graph(id='defects-reported-graph'),
        dcc.Graph(id='defects-resolved-graph')
    ])

def render_page_3():
    return html.Div([
        html.Div([
            dcc.RadioItems(
                id='sprint-radioitems-page3',
                options=[{'label': f'Sprint {i}', 'value': i} for i in df['Sprint'].unique()],
                value=df['Sprint'].unique()[0],
                inline=True
            )
        ], style={'text-align': 'left', 'color': 'white'}),
        dcc.Graph(id='time-slippage-graph', style={'padding-top': '5px'}),
        dcc.Graph(id='task-distribution-graph', style={'padding-top': '5px'}),
        dcc.Graph(id='cumulative-flow-diagram', style={'padding-top': '5px'})
    ])

@app.callback(
    [Output('time-slippage-graph', 'figure'),
     Output('task-distribution-graph', 'figure'),
     Output('cumulative-flow-diagram', 'figure')],
    [Input('sprint-radioitems-page3', 'value')]
)
def update_page_3(selected_sprint):
    filtered_df = df[df['Sprint'] == selected_sprint]
    
    # Time Slippage Chart
    filtered_df['Time_Slippage'] = filtered_df['Actual_Hours'] - filtered_df['Estimated_Hours']
    time_slippage_fig = px.bar(filtered_df, x='Task_ID', y='Time_Slippage', title='Time Slippage')
    
    # Task Distribution Chart
    task_distribution_fig = px.pie(df, names='Task_Type', title='Task Distribution')
    
    # Cumulative Flow Diagram
    cumulative_flow = df.groupby(['Date', 'Status']).size().reset_index(name='Count')
    cumulative_flow_fig = px.area(cumulative_flow, x='Date', y='Count', color='Status', title='Cumulative Flow Diagram')

    return time_slippage_fig, task_distribution_fig, cumulative_flow_fig

if __name__ == '__main__':
    app.run_server(debug=True)
