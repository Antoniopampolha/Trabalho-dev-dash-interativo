from dash import html, dcc, Input, Output
from matplotlib import pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import dash_bootstrap_components as dbc
from app import *
from dash_bootstrap_templates import ThemeSwitchAIO


url_theme1 = dbc.themes.VAPOR
url_theme2 = dbc.themes.FLATLY

template_theme1 = 'vapor'
template_theme2 = 'flatly'



df = pd.read_csv("tabela-fipe-historico-precos.csv")
cars_manufacturer = [{'label': x, 'value': x} for x in df['marca'].unique()]


app.layout = dbc.Container([
    dbc.Row([
        
        dbc.Col([
            ThemeSwitchAIO(aio_id = 'theme', themes = [url_theme1, url_theme2]),
            html.H3('valor e marcas'),
            dcc.Dropdown(
                id = 'marcas',
                value = [valor['label'] for valor in cars_manufacturer[:3]],
                multi = True,
                options = cars_manufacturer
            ),
        ])
    ]),


    dbc.Row([
        dbc.Col([
           
            dcc.Graph(id = 'histogram')
        ])
    ]),
   dbc.Row([
       
        dbc.Col([
            dbc.Row([
                

                
          dcc.Dropdown(
          id='pizza',
          options=[ {'label': marca, 'value': marca}
          for marca in df['marca'].unique() ],
          multi=True,
          value=[valor['label'] for valor in cars_manufacturer[:3]],
        
    ),
    dcc.Graph(id='pie_chart'),
            ])
        ]),

    dbc.Row([
       
        dbc.Col([
            dbc.Row([
                
                dcc.Dropdown(
           
                id = 'marca1',
                value = cars_manufacturer[1]['label'],
                options = cars_manufacturer
                ), 
                dcc.Graph(id = 'indicator1'),
                dcc.Graph(id = 'box1')
            ])
        ]),

        dbc.Col([
            dbc.Row([
                dcc.Dropdown(
                    id='marca2',
                    value=cars_manufacturer[2]['label'],
                    options=cars_manufacturer
                ),
                dcc.Graph(id='indicator2'),
                dcc.Graph(id='box2')
            ])
        ])
    ])
])
])
    
@app.callback(
    Output('histogram', 'figure'),
    [Input('marcas', 'value'),
     Input(ThemeSwitchAIO.ids.switch('theme'), 'value')]
)
def histogram(marcas, toggle):
    templates = template_theme1 if toggle else template_theme2

    df_data = df.copy(deep=True)
    mask = df_data['marca'].isin(marcas)

    # Crie um histograma dos valores
    fig = px.histogram(df_data[mask], x='valor',y='modelo', template=templates, nbins=30)

    return fig
#pizza---------------------
@app.callback(
    [Output('pie_chart', 'figure')],
    Input('pizza', 'value'),
    Input(ThemeSwitchAIO.ids.switch('theme'), 'value') 
    
)
def update_graphs(pizza,toggle):
    templates = template_theme1 if toggle else template_theme2
    df_data = df.copy()
    mask = df_data['marca'].isin(pizza)

    manufacturer_counts = df_data[mask]['marca'].value_counts()
    values = manufacturer_counts.values
    labels = manufacturer_counts.index
    colors = ['lightcoral', 'gold', 'yellowgreen', 'lightskyblue'] 
    
    pie_fig = px.pie(values=values, names=labels, color_discrete_sequence=colors)
    pie_fig.update_traces(textinfo='percent+label', pull=[0.1] + [0] * (len(values) - 1))

        
    pie_fig.update_layout(template=templates)
    
    return [pie_fig]  

@app.callback(
    Output('indicator1', 'figure'),
    Output('indicator2', 'figure'),
    Input('marca1', 'value'),
    Input('marca2', 'value'),

    Input(ThemeSwitchAIO.ids.switch('theme'), 'value') 
)
def indicators(marca1, marca2, toggle):
    templates = template_theme1 if toggle else template_theme2

    df_data = df.copy(deep = True)

    data_marca1 = df_data[df_data['marca'].isin([marca1])]
    data_marca2 = df_data[df_data['marca'].isin([marca2])]

    iterable = [(marca1, data_marca1), (marca2, data_marca2)]
    indicators = []

    for marca, data in iterable:
        fig = go.Figure()
        fig.add_trace(go.Indicator(
            mode = 'number+delta',
            title = {'text': marca},
            value = data.at[data.index[-1], 'valor'],
            number = {'prefix': 'R$', 'valueformat': '.2f'},
            delta = {'relative': True, 'valueformat': '.1%', 'reference': data.at[data.index[0], 'valor']}
        ))

        fig.update_layout(template = templates)
        indicators.append(fig)
    
    return indicators


@app.callback(
    Output('box1', 'figure'),
    Input('marca1', 'value'),
    Input(ThemeSwitchAIO.ids.switch('theme'), 'value') 
)
def box1(marca1, toggle):
    templates = template_theme1 if toggle else template_theme2

    df_data = df.copy(deep = True)
    data_marca = df_data[df_data['marca'].isin([marca1])]

    fig = px.box(data_marca, x = 'valor', template = templates, points='all', title=marca1)

    return fig


@app.callback(
    Output('box2', 'figure'),
    Input('marca2', 'value'),
    Input(ThemeSwitchAIO.ids.switch('theme'), 'value') 
)
def box2(marca2, toggle):
    templates = template_theme1 if toggle else template_theme2

    df_data = df.copy(deep = True)
    data_marca = df_data[df_data['marca'].isin([marca2])]

    fig = px.box(data_marca, x = 'valor', template = templates, points='all', title=marca2)

    return fig


if __name__ == '__main__':
    app.run_server(debug = True, port='8041')