import dash
from django_plotly_dash import DjangoDash

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output,State
import plotly.graph_objects as go
from collections import deque

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


preivous_neuron = deque(maxlen=1)
preivous_neuron.append('empty') # it could have been anything, i just wanted to populate its 0th index so i can do stuff like preivous_neuron[0]
fig = go.Figure()
fig.update_xaxes(range=[0, 30])
fig.update_yaxes(range=[0, 30])
fig.update_layout(width=800, height=800,xaxis_showgrid=False, yaxis_showgrid=False)
app = DjangoDash('hello_world', external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H6("Build Neural Network"),
   html.Div(
    id='output',
    children=[],


    
   
),
    html.Button("Add Hidden Layer",id='load-new-content',n_clicks=0),
     html.Button("Build Neural Network",id='c'),
    dcc.Graph(
        id='result',
        style={'marginLeft':'20%'}
    )

],
    
    style={'textAlign':'center'}
)




def get_left_corner_of_neuron(neuron):
    return {'x':neuron['x0'],'y':neuron['y0']+0.5} # y is the bottom corner  + radius (which is 0.5)

def get_right_corner_of_neuron(neuron):
    return {'x':neuron['x1'],'y':neuron['y0']+0.5} # y is the bottom corner  + radius (which is 0.5)
@app.callback(
    Output('output','children'),
    [Input('load-new-content','n_clicks')],
    [State('output','children')])
def more_output(n_clicks,old_output):
    

    return old_output+[dcc.Input(type="number", placeholder="number of neurons",value=1)]
        
@app.callback(

        Output('result','figure'),
        [Input('c','n_clicks')],
        [State('output','children')]
    )
def get_result(n_clicks,children):


    hidden_layers  = [x['props'].get('value') for x in children if x['props'].get('value') !=0]  
    fig['layout']['shapes'] = []  # clear fig
    gap_x = 0
    try:
        for layer in hidden_layers:
            for neuron in range(layer):
                

                fig.add_shape(
                    dict( 
                        type="circle",
                        xref="x",
                        yref="y",
                        x0=gap_x,
                        y0=neuron,
                        x1=gap_x+1,
                        y1=neuron+1,
                        line_color="LightSeaGreen",

                    ))
            gap_x +=5
    except:
        return fig


    if len(fig['layout']['shapes']) >0:

        neurons = fig['layout']['shapes']
        layers = {}


        ### group the hidden layers
        for i in neurons:
            current_layer = str(i['x0'])
            if current_layer in layers.keys():

                layers[current_layer].append(i)
            else:
                layers[current_layer] = [i]


        for layer,current_layer in layers.items():


            try:

                next_layer =  layers[str(int(layer)+5)]
        
            except:

                break
            
            
            for current_neuron in current_layer: 
                for next_neuron in next_layer:
                    fig.add_shape(
                            dict( 
                                type="line",
                                xref="x",
                                yref="y",
                                x0=get_right_corner_of_neuron(current_neuron)['x'],
                                y0=get_right_corner_of_neuron(current_neuron)['y'],
                                x1=get_left_corner_of_neuron(next_neuron)['x'],
                                y1=get_left_corner_of_neuron(next_neuron)['y'],
                                line_color="LightSeaGreen",
                            ))




    fig.update_layout(width=800, height=800)
    return fig
    
if __name__ == '__main__':
    app.run_server(debug=True)