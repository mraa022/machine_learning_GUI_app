import dash
from django_plotly_dash import DjangoDash
import dash_core_components as dcc
import os
import pandas as pd
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense
from keras.utils import np_utils
import dash_html_components as html
from dash.dependencies import Input, Output,State
import plotly.graph_objects as go
from collections import deque

old_model = deque(maxlen=1)
new_model_layers = None
new_model_loss,new_model_optimizer = None,None
neural_network_graph_fig = go.Figure()
error_rate_graph_fig = go.Figure()
neural_network_graph_fig.update_xaxes(range=[0, 30])
neural_network_graph_fig.update_yaxes(range=[0, 30])
neural_network_graph_fig.update_layout(xaxis_showgrid=False, yaxis_showgrid=False,template='plotly_dark')
error_rate_graph_fig.update_layout(template='plotly_dark')
error_rate = deque()
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = DjangoDash('buildAndTrainModel', external_stylesheets=external_stylesheets) 
config = dict({'scrollZoom': True,'showAxisDragHandles':True})
first_time = 0
app.layout = html.Div([
    html.H1("Build And Train Your Neural Network"),
    html.Div(id='placeholder',style={'display':'none'},children=[]),
    dcc.Dropdown(
    id='Optimizer',
    options=[
        {'label': 'adam', 'value': 'adam'},
        {'label': 'Rmsprop', 'value': 'Rmsprop'},
        {'label': 'Adagrad', 'value': 'Adagrad'}
    ],
    value='adam'
),
    dcc.Dropdown(
    id='LearningRate',
    options=[
        {'label': '0.1', 'value': 0.1},
        {'label': '0.01', 'value': 0.01},
        {'label': '0.001', 'value': 0.001},
        {'label': '5', 'value': 5}
    ],
    value=5
),
    
   html.Div(
    id='input_boxes',
    children=[],
 
),
   html.Button("Add Layer",id='load-new-content',n_clicks=0),
   html.Br(),
   html.Button("Build And Train Neural Network",id='c'),
   dcc.Graph(
        style={'marginLeft':'50%','width': '50%','height':'50%','position':'absolute'},
        id='live-graph',
        figure=error_rate_graph_fig,
        config=config,
        animate=True,
    ),
    
    dcc.Graph(
        style={'width': '50%','height':'50%'},
        id='result',
        config=config,
        figure=neural_network_graph_fig,
        animate=True,

    ),
    dcc.Interval(
            id='graph-update',
            interval=1000
        ),


],
    # className="six columns",
    style={'textAlign':'center'}
)

@app.callback(
    Output('input_boxes','children'),
    [Input('load-new-content','n_clicks')],
    [State('input_boxes','children')])
def add_new_text_input(n_clicks,old_output):
    

    return old_output+[dcc.Input(type="number", placeholder="number of neurons")]



def connect_two_neurons(neuron1,neuron2):

    neural_network_graph_fig.add_trace(go.Scatter(x=[neuron1[0],neuron2[0]], y=[neuron1[1],neuron2[1]],
                    mode='lines+markers',
                    name='lines+markers'))
    
def get_previous_layer(x0):
    return [[x['x0']+1,x['y0']+1] for x in neural_network_graph_fig['layout']['shapes'] if x['x0'] == x0]  ## the neurons in each layer have the same x, this filters the neurons using that x

def connect_layers(l1,l2):
    
    for current_neuron in l1:
        for previous_neuron in l2:
           connect_two_neurons(current_neuron,previous_neuron)


def draw_layer(layer,center_layer_vertically,x_of_layer,can_connect_to_previous_layer):
    
    current_layer = []
    for neuron in range(layer):
                
        neural_network_graph_fig.add_shape(
            dict( 
                type="circle",
                xref="x",
                yref="y",
                x0=x_of_layer,
                y0=center_layer_vertically,
                x1=x_of_layer+1,  # 1 is radius of the neuron
                y1=center_layer_vertically+2, # 2 is diameter of the neuron
                line_color="LightSeaGreen",
            ))

        current_layer.append([x_of_layer,center_layer_vertically+1] ) ## get corners of neuron 'x' = left corner. 'y' = bottom corner
        center_layer_vertically += 2
    if can_connect_to_previous_layer:
      
      previous_layer = get_previous_layer(x_of_layer-5) 
      connect_layers(current_layer, previous_layer)


def not_first_layer(layer_number):
    return layer_number != 0

@app.callback(

        Output('result','figure'),
        [Input('c','n_clicks')],
        [State('input_boxes','children')]
    )

def get_result(n_clicks,children):
 
    layers  = [x['props'].get('value') for x in children if  x['props'].get('value')>0]  
    neural_network_graph_fig['layout']['shapes'] = []  # clear shapes (circles)
    neural_network_graph_fig['data'] = []  # clear connections
    horizontal_distance_between_layers = 0
    if children:

        for layer_number,layer in enumerate(layers):
            center_layer_vertically =  (max(layers) - layer) 

            connect_to_previous_layer = True if not_first_layer(layer_number) else False   
            draw_layer(layer,center_layer_vertically,horizontal_distance_between_layers,connect_to_previous_layer)
            horizontal_distance_between_layers +=5
    else:
        return neural_network_graph_fig


    return neural_network_graph_fig

##############################################################                      ##############################################################
##############################################################                      ##############################################################

############################################################## TRAIN NEURAL NETWORK ##############################################################
##############################################################                      ##############################################################
##############################################################                      ##############################################################
def get_file_path(file_type):
    base_path = os.path.dirname(os.getcwd())

    return os.path.join(base_path,'machine_learning_gui/media/datasets/formated_dataset.csv') if file_type == 'dataframe' else os.path.join(base_path,'machine_learning_gui/media/datasets/contain_some_cookies_data')

def return_cookies_file():
    with open(get_file_path(file_type='cookies_file'),'r') as f:
        result = eval(f.read())
        
    return result
def create_model(layers):
    layers = [1] if not layers else layers
    model = tf.keras.Sequential()
    input_layer = model.add(Dense(layers[0],activation='relu',input_shape=(None,x_train.shape[1])))
    if len(layers)>1:
        [model.add(Dense(x,activation='relu')) for x in layers[1:]]
    output = model.add(Dense(len(Y[0]),activation='softmax')) if label_type == 'discrete' else model.add(Dense(1))
    return model

train_dataset_path = get_file_path(file_type = 'dataframe')
df = pd.read_csv(get_file_path('dataframe'))
label_column_name = return_cookies_file()['label_column_name']
label_type = return_cookies_file()['model_type']
X = df.drop(label_column_name,axis=1).values
Y = df[label_column_name].values

if label_type == 'discrete':
    encoder = LabelEncoder()
    encoder.fit(Y)
    encoded_Y = encoder.transform(Y)
    Y = np_utils.to_categorical(encoded_Y)

x_train,x_test,y_train,y_test = train_test_split(X,Y,test_size=0.2)


def already_updated_params(old_params,new_params):

    return True if old_params == new_params else False



def update_graph(inp):
    with open('error_rate','r') as f:
      
        error_rate = eval(f.read())  ### sometimes this function runs while the training function is running. this causes an EOF error

      
        
    y = list(error_rate)
    x = list(range(len(error_rate)))
    data = go.Scatter(
            x=x,
            y=y,
            marker=dict(
            color='LightSkyBlue',
            size=0.1,
            line=dict(
                color='MediumPurple',
                width=0.5
            )
        ),
            name='Scatter',
            mode= 'lines+markers'
            )

    return {'data': [data],'layout' : go.Layout(xaxis=dict(range=[min(x),max(x)]),
                                                yaxis=dict(range=[min(y),max(y)]),template='plotly_dark')}

class myCallback(tf.keras.callbacks.Callback):
    
    def on_epoch_end(self, epoch, logs):
        if new_model_loss and new_model_optimizer and not already_updated_params(old_params=[self.model.optimizer,self.model.loss],new_params=[new_model_optimizer,new_model_loss]):
            self.model.optimizer = new_model_optimizer
            self.model.loss = new_model_loss


        error_rate.append(logs['loss'])
        with open('error_rate','w') as f:
            f.write(str(error_rate))


@app.callback(
    Output(component_id='placeholder',component_property='children'),
    [Input(component_id='Optimizer', component_property='value'),
    Input(component_id='LearningRate', component_property='value'),
    Input('c','n_clicks')],
    [State('input_boxes','children')])

def train_neural_network(optimizer,learning_rate,c,layers=[1]):
            global first_time
            global new_model_layers
            global new_model_loss,new_model_optimizer
            global error_rate
            layers  = [x['props'].get('value') for x in layers if x['props'].get('value')>0]
            optimizers = {
            'adam':tf.keras.optimizers.Adam(
                learning_rate=learning_rate, beta_1=0.9, beta_2=0.999, epsilon=1e-07, amsgrad=False,
                name='Adam'
            ),
            'Rmsprop': tf.keras.optimizers.RMSprop(
            learning_rate=learning_rate,
            rho=0.9,
            momentum=0.0,
            epsilon=1e-07,
            centered=False,
            name="RMSprop",
        ),

            'Adagrad':tf.keras.optimizers.Adagrad(
            learning_rate=learning_rate,
            initial_accumulator_value=0.1,
            epsilon=1e-07,
            name="Adagrad"
        )}
            loss = tf.keras.losses.categorical_crossentropy if label_type == 'discrete' else tf.keras.losses.MSE
            model_optimizer = optimizers[optimizer]
            first_time+=1
            if first_time == 1:
                model = create_model(layers)
                model.compile(optimizer=model_optimizer, loss=loss, metrics=["acc"])
                old_model.append(model)
                model.fit(x_train,y_train,epochs=10000000,callbacks=[myCallback()],verbose=0)      
            else:
                
                get_old_model = old_model[0]
                if [x.units for x in get_old_model.layers][:-1] != [x for x in layers][:-1]:
                    new_model = create_model(layers)
                    get_old_model.stop_training = True
                    new_model.compile(optimizer=model_optimizer, loss=loss, metrics=["acc"])
                    old_model.append(new_model)
                    error_rate = deque()
                    new_model.fit(x_train,y_train,epochs=10000000,callbacks=[myCallback()],verbose=0)
                new_model_loss = loss
                new_model_optimizer = model_optimizer
       
            return 'hello'


app.callback(Output('live-graph', 'figure'),[Input(component_id='graph-update', component_property='n_intervals')])(update_graph)



# def run_app():
#     app.run_server(debug=False)

# run_app()
