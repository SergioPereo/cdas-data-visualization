from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

import datetime as date
from datetime import timedelta

format_months = {'Enero': 1, 'Febrero': 2, 'Marzo': 3,'Abril': 4, 'Mayo': 5, 'Junio': 6, 'Julio': 7, 'Agosto': 8, 'Septiembre': 9, 'Octubre': 10, 'Noviembre': 11,'Diciembre': 12}
periodistas_asesinados = pd.read_excel("db_periodistas_asesinados.xlsx")
periodistas_asesinados['Fecha'] = periodistas_asesinados['Fecha'].apply(lambda x: date.datetime(int(x.split(" ")[4]), int(format_months[x.split(" ")[2]]), int(x.split(" ")[0])))

df = pd.read_csv('count_posts_date.csv', names=["date", "post_count"], dtype={'date': 'str', 'post_count': 'int'}, parse_dates=['date'])

#print(df.dtypes)

initial_date = df['date'].min()
final_date = df['date'].max()

years = list(range(initial_date.year, final_date.year+1))
#print(years)

max_posts = df[df['post_count']==df['post_count'].max()].values[0]

al_deathline = np.datetime64('2022-03-15')
al_deathline_annotation = np.datetime64('2022-05-15')
ma_deathline = np.datetime64('2020-03-30')
ma_deathline_annotation = np.datetime64('2020-06-12')

#print(df[(df['date']>='2014-01-01')&(df['date']<'2014-02-01')])


app = Dash(__name__)
app.layout = html.Div([
    html.H1(children="Frecuencia de posts mencionando 'Periodistas Asesinados'", style={'textAlign':'center'}),
    html.Div(children=[
        html.Div(children=[html.H3(children="Fecha inicial", style={'textAlign':'center'}),dcc.Dropdown(years, years[0], id='year')],className="date_selector"),
    ], className="dropdowns-container"),
    dcc.Graph(id='graph-content')
])

@callback(
    Output('graph-content', 'figure'),
    [Input('year', 'value')]
)
def update_graph(year):
    initial_range = date.datetime(int(year), 1, 1)
    final_range = date.datetime(int(year+1), 1, 1)
    dff = df[(df['date']>=initial_range)&(df['date']<final_range)]
    #print(dff.loc[dff["date"]==pd.to_datetime(date.datetime(2014,1,2))]["post_count"][0])
    #print(dff['date'])
    delta = final_range-initial_range
    full_dates_list = [initial_range+timedelta(days=i) for i in range(delta.days)]
    #print(full_dates_list)
    full_counts = []
    for fecha in full_dates_list:
        values = dff.loc[dff["date"]==pd.to_datetime(fecha)]["post_count"]
        if len(values)==0:
            full_counts.append(0)
        else:
            full_counts.append(values.iloc[0])
    
    #print(full_dates_list, full_counts)
    #date, post_count
    texts=[]
    for fecha in full_dates_list:
        values = periodistas_asesinados.loc[periodistas_asesinados["Fecha"]==pd.to_datetime(fecha)]
        print(values)
        if len(values)==0:
            texts.append('')
        else:
            texts.append(f'<b>Nombre</b>:{values["Nombre"].iloc[0]}')
    #print(texts)
    #print([f'<b>Nombre</b>:{(periodistas_asesinados.loc[periodistas_asesinados["Fecha"]==pd.to_datetime(fecha)]["post_count"])}' if fecha in periodistas_asesinados['Fecha'] else '' for fecha in dff['date']])
    fig = go.Figure(go.Scatter(
    x = full_dates_list,
    y = full_counts,
    text = texts,
    hovertemplate =
    '<b>Post_count</b>: %{y}<br><b>Date</b>: %{x}<br>%{text}',
    showlegend = False))
    periodistas = periodistas_asesinados[(periodistas_asesinados['Fecha']>=initial_range)&(periodistas_asesinados['Fecha']<final_range)]
    for index, row in periodistas.iterrows():
        fig = fig.add_vline(x=row['Fecha'], line_dash="dash")
    """

        if al_deathline_annotation in dff.date.values:
            fig = fig\
            .add_vline(al_deathline, line_dash="dash")\
            .add_annotation( # add a text callout with arrow
                text="Asesinato Al", x=al_deathline_annotation, y=max_posts[1]+10, arrowhead=1, showarrow=False, align='left'
            )
        
        if ma_deathline_annotation in dff.date.values:
            fig = fig\
            .add_vline(ma_deathline, line_dash="dash")\
            .add_annotation( # add a text callout with arrow
                text="Asesinato MEF", x=ma_deathline_annotation, y=max_posts[1]+10, arrowhead=1, showarrow=False, align='left'
            ).add_trace
"""

    return fig

if __name__ == '__main__':
    app.run(debug=True)

