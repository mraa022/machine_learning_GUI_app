import pandas as pd
import os
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense
from keras.utils import np_utils
import numpy as np
from random import shuffle
from collections import deque
import asyncio
import pandas as pd
import os
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense
from keras.utils import np_utils
import numpy as np
from random import shuffle
from collections import deque
import asyncio
  	
def get_file_path(file_type):
	base_path = os.path.dirname(os.getcwd())

	return os.path.join(base_path,'media/datasets/formated_dataset.csv') if file_type == 'dataframe' else os.path.join(base_path,'media/datasets/contain_some_cookies_data')

def return_cookies_file():
	with open(get_file_path(file_type='cookies_file'),'r') as f:
		result = eval(f.read())
		
	return result

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

dataset = tf.data.Dataset.from_tensor_slices((X, Y))
x_train,x_test,y_train,y_test = train_test_split(X,Y,test_size=0.2)
model = tf.keras.Sequential()
input_layer = model.add(Dense(11,activation='relu',input_shape=(None,x_train.shape[1])))
hidden_1 = model.add(Dense(4,activation='relu'))
hidden_2  = model.add(Dense(4,activation='relu'))
hidden_3 = model.add(Dense(4,activation='relu'))
output = model.add(Dense(len(Y[0]),activation='softmax')) if label_type == 'discrete' else model.add(Dense(1))

def get_loss_and_gradients(model, inputs, targets):
  with tf.GradientTape() as tape:

    loss_value = loss(model, inputs, targets, training=True)
  return loss_value, tape.gradient(loss_value, model.trainable_variables)

def loss(model, x, y, training):

  y_ = model(x, training=training)

  loss_object = tf.keras.losses.categorical_crossentropy(y_true=y,y_pred=y_) if label_type == 'discrete' else tf.keras.losses.MSE(y_true=y,y_pred=y_)

  return loss_object


optimizer = tf.keras.optimizers.Adam(
    learning_rate=0.001, beta_1=0.9, beta_2=0.999, epsilon=1e-07, amsgrad=False,
    name='Adam'
)
async def train():
	global dataset
	epoch = 0
	while True:
		dataset = dataset.shuffle(buffer_size=100000)
		epoch_loss_avg = tf.keras.metrics.Mean()
		
		# Training loop - using batches of 32
		for x, y in dataset.batch(32):
	  
	  	
			loss_value, gradients = get_loss_and_gradients(model, x, y) 
			optimizer.apply_gradients(zip(gradients, model.trainable_variables))

			epoch_loss_avg.update_state(loss_value)  # Add current batch loss

	  
		print("Epoch {:03d}: Loss: {:.3f}".format(epoch,epoch_loss_avg.result()))
		epoch+=1
		await asyncio.sleep(0.00000000001)


async def show_graph(n):
	while True:
		print('Graph will go here'*n)
		await asyncio.sleep(0.00000000001)
	

async def main():
	task2 = asyncio.create_task(train())
	task1 = asyncio.create_task(show_graph(2))
	await asyncio.gather(task1,task2)

asyncio.run(main())









