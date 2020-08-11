import plotly
import pandas as pd
import os
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense
from keras.utils import np_utils
import numpy as np
from collections import deque
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output,State
import plotly.graph_objects as go



error_rate = deque()
quit = True
previous_and_current_models = deque(maxlen=2)
first_time = 0
new_model_loss,new_model_optimizer = None,None


app = dash.Dash(__name__)
app.layout = html.Div(children=[
    
    html.Div(id='hi'),

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
    dcc.Graph(
        id='live-graph',
        animate=True,
    ),

    html.Div(id='placeholder',style={'display':'none'},children=[]),
    dcc.Interval(
            id='graph-update',
            interval=1000
        ),

])

def get_file_path(file_type):
	base_path = os.path.dirname(os.getcwd())

	return os.path.join(base_path,'media/datasets/formated_dataset.csv') if file_type == 'dataframe' else os.path.join(base_path,'media/datasets/contain_some_cookies_data')

def return_cookies_file():
	with open(get_file_path(file_type='cookies_file'),'r') as f:
		result = eval(f.read())
		
	return result
def create_model(layers):
	model = tf.keras.Sequential()

	input_layer = model.add(Dense(layers[0],activation='relu',input_shape=(None,x_train.shape[1])))
	[model.add(Dense(x,activation='relu')) for x in layers[1:]]
	output = model.add(Dense(len(Y[0]),activation='softmax')) if label_type == 'discrete' else model.add(Dense(1))
	return model


train_dataset_path = get_file_path(file_type = 'dataframe')
df = pd.read_csv(get_file_path('dataframe'))
label_column_name = return_cookies_file()['label_column_name']
f = []
label_type = return_cookies_file()['model_type']
X = df.drop(label_column_name,axis=1).values
Y = df[label_column_name].values

if label_type == 'discrete':
    encoder = LabelEncoder()
    encoder.fit(Y)
    encoded_Y = encoder.transform(Y)
    Y = np_utils.to_categorical(encoded_Y)

dataset = tf.data.Dataset.from_tensor_slices((X, Y))
x_train,x_test,y_train,y_test = train_test_split(X,Y,test_size=0.2)


def already_updated_params(old_params,new_params):

	return True if old_params == new_params else False

def update_graph(inp):
	with open('error_rate','r') as f:
 	  error_rate = eval(f.read())
 	  y = list(error_rate)
 	  x = list(range(len(error_rate)))
 	  data = plotly.graph_objs.Scatter(
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

	# print(min(y),max(y))
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

def train_neural_network(optimizer,learning_rate):
		global first_time
		global new_model_loss,new_model_optimizer
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
			model = create_model([10,20,5])
			model.compile(optimizer=model_optimizer, loss=loss, metrics=["acc"])
			model.fit(x_train,y_train,epochs=10000000,callbacks=[myCallback()],verbose=0)
		
		else:
			new_model_loss = loss
			new_model_optimizer = model_optimizer
		return 'hello'

app.callback(Output('live-graph', 'figure'),[Input(component_id='graph-update', component_property='n_intervals')])(update_graph)
app.callback(
	Output(component_id='placeholder',component_property='children'),
	[Input(component_id='Optimizer', component_property='value'),
	Input(component_id='LearningRate', component_property='value')])(train_neural_network)
app.run_server(debug=True)
 










