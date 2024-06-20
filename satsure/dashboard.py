# Install necessary libraries (uncomment and run in a separate cell if not installed)
# !pip install dash plotly pandas

import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc

# Sample data creation
data =pd.read_csv('/home/saiharan/Downloads/sdlc_metrics_sample.csv')

# Convert to DataFrame
df = pd.DataFrame(data)

# Convert Date column to datetime
df['Date'] = pd.to_datetime(df['Date'])
df['Month'] = df['Date'].dt.to_period('M')

# Line chart for month-on-month trends for tasks completed
tasks_trend = df.groupby('Month')['Task Completed'].sum().reset_index()
line_chart = px.line(tasks_trend, x='Month', y='Task Completed', title='Month-on-Month Trends for Tasks Completed')

# Bar chart comparing bugs reported by each resource
bugs_reported = df.groupby('Resource')['Bugs Reported'].sum().reset_index()
bar_chart = px.bar(bugs_reported, x='Resource', y='Bugs Reported', title='Bugs Reported by Resource')

# Pie chart showing the distribution of code commits
code_commits = df.groupby('Resource')['Code Commits'].sum().reset_index()
pie_chart = px.pie(code_commits, names='Resource', values='Code Commits', title='Distribution of Code Commits')

# Build the dashboard
app = Dash(__name__)

app.layout = html.Div([
    html.Div([
        dcc.Graph(figure=line_chart)
    ], style={'width': '100%', 'display': 'inline-block', 'padding': '0 20'}),
    
    html.Div([
        html.Div([
            dcc.Graph(figure=bar_chart)
        ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),
        
        html.Div([
            dcc.Graph(figure=px.pie(code_commits, names='Resource', values='Code Commits', title='Distribution of Code Commits'))
        ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),
    ]),
])

if __name__ == '__main__':
    app.run_server(debug=True)
