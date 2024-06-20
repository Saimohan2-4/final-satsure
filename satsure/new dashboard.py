import pandas as pd
from datetime import datetime
import dash
from dash import dcc, html, Input, Output
import plotly.express as px

# Load the dataset
df = pd.read_csv('/home/saiharan/Documents/projects/travel agency analysis/satsure/sample_dataset_large.csv')

# Convert 'Date' column to datetime
df['Date'] = pd.to_datetime(df['Date'])

# Calculate cycle time
df['Start_Date'] = pd.to_datetime(df['Start_Date'])
df['End_Date'] = pd.to_datetime(df['End_Date'])
df['Cycle_Time'] = (df['End_Date'] - df['Start_Date']).dt.days

# Calculate sprints (assuming 2-week sprints for demonstration)
df['Sprint'] = ((df['Date'] - df['Date'].min()) // pd.Timedelta(weeks=2)).astype(int) + 1

# Initialize the Dash app
external_stylesheets = ["https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css"]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Layout with 3 pages and navigation buttons
app.layout = html.Div([
    html.H1("Software Development Metrics Dashboard"),
    html.Div([
        html.Button("Page 1", id="page-1-button", n_clicks=0, className="btn btn-primary me-1"),
        html.Button("Page 2", id="page-2-button", n_clicks=0, className="btn btn-primary me-1"),
        html.Button("Page 3", id="page-3-button", n_clicks=0, className="btn btn-primary me-1"),
    ], className="mb-2"),
    dcc.RadioItems(
        id='sprint-selector',
        options=[{'label': f'Sprint {i}', 'value': i} for i in df['Sprint'].unique()],
        value=df['Sprint'].min(),
        inline=True,
        className="mb-4"
    ),
    html.Div(id='page-content')
])

# Callback for page navigation
@app.callback(
    Output('page-content', 'children'),
    [Input('page-1-button', 'n_clicks'),
     Input('page-2-button', 'n_clicks'),
     Input('page-3-button', 'n_clicks'),
     Input('sprint-selector', 'value')]
)
def display_page(page1, page2, page3, selected_sprint):
    ctx = dash.callback_context

    if not ctx.triggered:
        button_id = 'page-1-button'
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == 'page-1-button':
        return page_1_layout(selected_sprint)
    elif button_id == 'page-2-button':
        return page_2_layout(selected_sprint)
    elif button_id == 'page-3-button':
        return page_3_layout(selected_sprint)

def page_1_layout(selected_sprint):
    # Filter data by sprint
    filtered_df = df[df['Sprint'] == selected_sprint]

    # Velocity Chart
    velocity_df = filtered_df.groupby('Sprint').sum().reset_index()
    velocity_chart = px.bar(velocity_df, x='Sprint', y='Story_Points', title='Velocity')

    # Cycle Time Chart
    cycle_time_chart = px.line(filtered_df, x='Task_ID', y='Cycle_Time', title='Cycle Time')

    # Defect Rate Chart
    defect_rate_chart = px.bar(filtered_df, x='Task_ID', y='Defects_Reported', title='Defect Rate')

    return html.Div([
        dcc.Graph(figure=velocity_chart),
        dcc.Graph(figure=cycle_time_chart),
        dcc.Graph(figure=defect_rate_chart)
    ])

def page_2_layout(selected_sprint):
    # Placeholder for other metrics (4 metrics here)
    # Filter data by sprint
    filtered_df = df[df['Sprint'] == selected_sprint]

    return html.Div([
        # Example placeholder for metrics in page 2
        html.H3("Page 2 Metrics"),
        # Add actual charts and metrics here
    ])

def page_3_layout(selected_sprint):
    # Placeholder for other metrics (3 metrics here)
    # Filter data by sprint
    filtered_df = df[df['Sprint'] == selected_sprint]

    return html.Div([
        # Example placeholder for metrics in page 3
        html.H3("Page 3 Metrics"),
        # Add actual charts and metrics here
    ])

if __name__ == '__main__':
    app.run_server(debug=True)
