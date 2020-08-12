import dash
from django_plotly_dash import DjangoDash

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output,State
import plotly.graph_objects as go
from collections import deque
fig = go.Figure()
fig.update_xaxes(range=[0, 15])
fig.update_yaxes(range=[0, 15])
fig.update_layout(width=800, height=800,xaxis_showgrid=False, yaxis_showgrid=False,template='plotly_dark')
app = DjangoDash('buildNeuralNetwork')
config = dict({'scrollZoom': True,'showAxisDragHandles':True})
app.layout = html.Div([
    html.H1("Build Neural Network"),
   html.Div(
    id='output',
    children=[],
 
),
    html.Button("Add Layer",id='load-new-content',n_clicks=0),
    html.Br(),
     html.Button("Build Neural Network",id='c'),
    dcc.Graph(
        id='result',
        style={'marginLeft':'20%','overflowY': 'scroll', 'height': 800},
        config=config,
        animate=True

    ),
    dcc.Interval(
            id='graph-update',
            interval=1*1000
        )

],
    
    style={'textAlign':'center'}
)

@app.callback(
    Output('output','children'),
    [Input('load-new-content','n_clicks')],
    [State('output','children')])
def add_new_text_input(n_clicks,old_output):
    

    return old_output+[dcc.Input(type="number", placeholder="number of neurons",value=1)]



def connect_two_neurons(neuron1,neuron2):

    fig.add_trace(go.Scatter(x=[neuron1[0],neuron2[0]], y=[neuron1[1],neuron2[1]],
                    mode='lines+markers',
                    name='lines+markers'))
    
def get_previous_layer(x0):
    return [[x['x0']+1,x['y0']+0.5] for x in fig['layout']['shapes'] if x['x0'] == x0]  ## the neurons in each layer have the same x, this filters the neurons using that x

def connect_layers(l1,l2):
    
    for current_neuron in l1:
        for previous_neuron in l2:
           connect_two_neurons(current_neuron,previous_neuron)


def draw_layer(layer,center_layer_vertically,x_of_layer,can_connect_to_previous_layer):
    
    current_layer = []
    for neuron in range(layer):
                
        fig.add_shape(
            dict( 
                type="circle",
                xref="x",
                yref="y",
                x0=x_of_layer,
                y0=center_layer_vertically,
                x1=x_of_layer+1,  # 1 is diameter of the neuron
                y1=center_layer_vertically+1, # 1 is diameter of the neuron
                line_color="LightSeaGreen",

            ))

        current_layer.append([x_of_layer,center_layer_vertically+0.5] ) ## get corners of neuron 'x' = left corner. 'y' = bottom corner
        center_layer_vertically += 1
    if can_connect_to_previous_layer:
      
      previous_layer = get_previous_layer(x_of_layer-5) 
      connect_layers(current_layer, previous_layer)


def not_first_layer(layer_number):
    return layer_number != 0

@app.callback(

        Output('result','figure'),
        [Input('c','n_clicks')],
        [State('output','children')]
    )

def get_result(n_clicks,children):
 
    layers  = [x['props'].get('value') for x in children if type(x['props'].get('value')) == int and x['props'].get('value')!=0]  
    fig['layout']['shapes'] = []  # clear shapes (circles)
    fig['data'] = []  # clear connections
    horizontal_distance_between_layers = 0
    if children:

        for layer_number,layer in enumerate(layers):
            center_layer_vertically =  (max(layers) - layer) / 2
            connect_to_previous_layer = True if not_first_layer(layer_number) else False   
            draw_layer(layer,center_layer_vertically,horizontal_distance_between_layers,connect_to_previous_layer)
            horizontal_distance_between_layers +=5
    else:
        return fig


    fig.update_layout(width=800, height=800)
    return fig





