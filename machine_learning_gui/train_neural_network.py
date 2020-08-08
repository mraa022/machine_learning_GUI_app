import pandas as pd
import os
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import pandas
from keras.models import Sequential
from keras.layers import Dense
from keras.utils import np_utils


class myCallback(tf.keras.callbacks.Callback):
  def on_epoch_end(self, epoch, log):
    print(log)




def get_file_path(file_type):
	base_path = os.path.dirname(os.getcwd())

	return os.path.join(base_path,'media/datasets/formated_dataset.csv') if file_type == 'dataframe' else os.path.join(base_path,'media/datasets/contain_some_cookies_data')

def return_cookies_file():
	with open(get_file_path(file_type='cookies_file'),'r') as f:
		result = eval(f.read())
		
	return result

callbacks = myCallback()

df = pd.read_csv(get_file_path('dataframe'))
label_column_name = return_cookies_file()['label_column_name']
label_type = return_cookies_file()['model_type']
X = df.drop(label_column_name,axis=1).values
Y = df[label_column_name].values

if label_type == 'discrete':
	encoder = LabelEncoder()
	encoder.fit(Y)
	encoded_Y = encoder.transform(Y)
	dummy_y = np_utils.to_categorical(encoded_Y)

model = Sequential()
model.add(Dense(10,activation='relu'))
model.add(Dense(4,activation='relu'))
model.add(Dense(4,activation='relu'))
model.add(Dense(4,activation='relu'))
model.add(Dense(len(dummy_y[0]),activation='softmax')) if label_type == 'discrete' else model.add(Dense(1))
loss = 'categorical_crossentropy' if label_type == 'discrete' else tf.keras.metrics.mean_squared_error
x_train,x_test,y_train,y_test = train_test_split(X,dummy_y) if label_type == 'discrete' else train_test_split(X,Y)
model.compile(optimizer = 'adam',loss=loss)
model.fit(x_train,y_train,epochs=10,callbacks=[callbacks],verbose=0)