import pandas as pd
from ip2geotools.databases.noncommercial import DbIpCity
import plotly.express as px
import plotly.graph_objects as go
import dash
import gunicorn
from dash import dcc, html

# Load the CSV file
df = pd.read_csv('web_server_log.csv')

# Analyze number of visits
num_visits = df.shape[0]

# Analyze country of origin (using IP to geolocation service)
def get_country(ip):
    try:
        response = DbIpCity.get(ip, api_key='free')
        return response.country
    except:
        return 'Unknown'

df['Country'] = df['IP'].apply(get_country)
country_visits = df['Country'].value_counts()

# Analyze main interests (based on selected/viewed sports)
sports_resources = df['Resource'].apply(lambda x: x.split('/')[1].split('.')[0] if x.startswith('/') else 'Unknown')
sports_visits = sports_resources.value_counts()

# Calculate basic statistics
visit_times = pd.to_datetime(df['Time'], format='%Y-%m-%d %H:%M:%S').dt.hour
mean_visit_time = visit_times.mean()
std_visit_time = visit_times.std()

# Prepare data for plots
country_visits_plot = px.pie(values=country_visits, names=country_visits.index, title='Visits by Country')
sports_visits_plot = px.bar(sports_visits, title='Visits by Sport')

# Histogram of visit times
visit_times_hist = px.histogram(visit_times, nbins=24, title='Distribution of Visit Times (Hourly)')
visit_times_hist.update_layout(xaxis_title='Hour of Day', yaxis_title='Number of Visits')

# Mean and standard deviation bar chart
stats_fig = go.Figure(data=[
    go.Bar(name='Mean Visit Time', x=['Visit Time'], y=[mean_visit_time]),
    go.Bar(name='Std Dev Visit Time', x=['Visit Time'], y=[std_visit_time])
])
stats_fig.update_layout(barmode='group', title='Mean and Std Dev of Visit Times')

# Scatterplot of visit times by country
scatter_country_time = px.scatter(df, x=visit_times, y=df['Country'], title='Visit Times by Country')
scatter_country_time.update_layout(xaxis_title='Hour of Day', yaxis_title='Country')

# Box plot of visit times
box_visit_times = px.box(visit_times, title='Box Plot of Visit Times')
box_visit_times.update_layout(xaxis_title='Visit Time', yaxis_title='Frequency')

# Create Dash app
app = dash.Dash(__name__)
server app:server

app.layout = html.Div([
    html.H1("Web Server Log Analysis Dashboard"),
    html.Div([
        html.H2(f"Total Visits: {num_visits}"),
        dcc.Graph(figure=country_visits_plot),
        dcc.Graph(figure=sports_visits_plot),
        dcc.Graph(figure=visit_times_hist),
        dcc.Graph(figure=stats_fig),
        dcc.Graph(figure=scatter_country_time),
        dcc.Graph(figure=box_visit_times)
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)
