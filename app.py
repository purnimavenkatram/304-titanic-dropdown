######### Import your libraries #######
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly as py
import plotly.graph_objs as go
import numpy as np


###### Define your variables #####
tabtitle = 'IMDb'
color1='#92A5E8'
color2='#8E44AD'
color3='#FFC300'
sourceurl = 'https://www.kaggle.com/c/titanic'
githublink = 'https://github.com/purnimavenkatram/304-titanic-dropdown.git'


###### Import a dataframe #######
df = pd.read_csv("assets/imdb.csv")
genres_to_keep=['Drama','Comedy','Action']
df['genre_class']=np.where(df.genre.isin(genres_to_keep),df['genre'],'Other')
variables_list=['Star Rating', 'Duration']

########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle

####### Layout of the app ########
app.layout = html.Div([
    html.H3('Choose a variable for summary statistics:'),
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in variables_list],
        value=variables_list[0]
    ),
    html.Br(),
    dcc.Graph(id='display-value'),
    html.A('Code on Github', href=githublink),
    html.Br(),
    html.A("Data Source", href=sourceurl),
])


######### Interactive callbacks go here #########
@app.callback(Output('display-value', 'figure'),
              [Input('dropdown', 'value')])
def display_value(continuous_var):
    grouped_mean=df.groupby(['genre_class','Content Rating'])[continuous_var].mean()
    results=pd.DataFrame(grouped_mean)
    # Create a grouped bar chart
    mydata1 = go.Bar(
        x=results.loc['Drama'].index,
        y=results.loc['Drama'][continuous_var],
        name='Drama',
        marker=dict(color=color1)
    )
    mydata2 = go.Bar(
        x=results.loc['Comedy'].index,
        y=results.loc['Comedy'][continuous_var],
        name='Comedy',
        marker=dict(color=color2)
    )
    mydata3 = go.Bar(
        x=results.loc['Action'].index,
        y=results.loc['Action'][continuous_var],
        name='Action',
        marker=dict(color=color3)
    )

    mydata4 = go.Bar(
        x=results.loc['Other'].index,
        y=results.loc['Other'][continuous_var],
        name='Other',
        marker=dict(color=color4)
    )

    mylayout = go.Layout(
        title='Grouped bar chart',
        xaxis = dict(title = 'Genre of Movies'), # x-axis label
        yaxis = dict(title = str(continuous_var)), # y-axis label

    )
    fig = go.Figure(data=[mydata1, mydata2, mydata3, mydata4], layout=mylayout)
    return fig


######### Run the app #########
if __name__ == '__main__':
    app.run_server(debug=True)
