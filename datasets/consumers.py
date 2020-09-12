import json
from channels.generic.websocket import WebsocketConsumer
import os
import threading
from pandas import read_csv,get_dummies
from sklearn.model_selection import train_test_split
from .helper_functions import optimizer_options,loss_options,create_model
from machine_learning_gui import settings
from tensorflow.keras.losses import (
        MeanSquaredError,
        MeanAbsoluteError,
        MeanAbsolutePercentageError,
        MeanSquaredLogarithmicError,
        CosineSimilarity,
        Huber,
        LogCosh,
        CategoricalCrossentropy,
        Poisson,
        KLDivergence
    )
from tensorflow.keras.optimizers import (
        Adam,
        SGD,
        Adamax,
        RMSprop,
        Adagrad,
        Adadelta,
        Nadam,
        Ftrl
    )
from urllib.parse import unquote
import requests
from tensorflow.keras import Sequential
from keras.layers import Dense
from tensorflow.keras.callbacks import  Callback

first_time  = True
quit_training = [False]
in_training = [False]
def remove_column(dataframe):

    '''
    removes the index column

    '''
    try:
        return dataframe.drop('Unnamed: 0',axis=1)
    except:
        return dataframe

def train_model(model,x_train,y_train,x_test,y_test,batch_size,self): ## the reason this is here, is so it can be run in the background using threads
    model.fit(x_train,y_train,epochs=1000000000,callbacks=[myCallback(self,x_test,y_test)],verbose=0,batch_size=batch_size)


def terminate_training_model():

    quit_training[0] = True 
        
class myCallback(Callback):

    def __init__(self,consumer_instance,x_test,y_test):


        self.consumer_instance = consumer_instance
        self.x_test = x_test
        self.y_test = y_test
        
    def on_epoch_end(self, epoch, logs):
        
        if epoch == 0:
            in_training[0] = True

        if quit_training[0]:
            self.model.stop_training = True  # stop training the current model
            quit_training[0] = False ## set this to false so the next model can train.

        
        test_loss,test_accuracy = self.model.evaluate(self.x_test,self.y_test,verbose=0)
        training_loss = logs['loss']
        if str(training_loss) != 'nan' and str(test_loss) !='nan':
            self.consumer_instance.send(text_data=json.dumps({
                    'training_loss': training_loss,
                    'test_loss': test_loss,
                    'numbers_got_too_big': 'No'
                }))
        else:
            print('numbers_got_too_big')
            self.consumer_instance.send(text_data=json.dumps({
                    'numbers_got_too_big': 'Yes',
                }))
            self.model.stop_training = True

    def on_train_end(self,logs=None):
        in_training[0] = False
       
def get_dataframe(data_frame_location):

    return remove_column(read_csv(data_frame_location))


def another_model_running():
    return in_training[0] == True
class ErrorGraphConsumer(WebsocketConsumer):
    def connect(self):
        dataframe_file = self.scope['cookies']['sessionid']+'formated_dataset.csv'
        media_path = os.path.join(settings.MEDIA_ROOT,'datasets/')
        dataframe_file_path = os.path.join(media_path,dataframe_file)
        self.dataframe = get_dataframe(data_frame_location = dataframe_file_path)
        self.accept()

    def disconnect(self, close_code):
        if in_training[0]:
            terminate_training_model()

    def receive(self, text_data):
        global first_time
        
        if not first_time and another_model_running():
            terminate_training_model()

        text_data_json = json.loads(text_data)
        layers = text_data_json['layers'] 
        layer_activations = text_data_json['layer_activations']
        optimizer_params = text_data_json['optimizer_params']
        label_type = text_data_json['label_type']
        label_column = text_data_json['label_column']
        chosen_optimizer = text_data_json['optimizer']
        chosen_loss = text_data_json['loss']
        batch_size = int(text_data_json['batch_size'])
        test_size = float(text_data_json['test_size'])/100
        optimizer_params = dict([(key,value) for key,value in optimizer_params.items() if value != None]) #if an input is not provided, the value is None
        x = self.dataframe.drop(label_column,axis=1).values
        y = get_dummies(self.dataframe[label_column],drop_first=True).values if label_type == 'discrete' else self.dataframe[label_column].values
        x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=test_size)
        number_of_classes = len(y[0]) if label_type == 'discrete' else 1
        model = create_model(layers,number_of_classes = number_of_classes,activations=layer_activations,label_type=label_type,number_of_inputs = x_train.shape[1])
        optimizer = optimizer_options(**optimizer_params)[chosen_optimizer]
        loss = loss_options()[chosen_loss]
        model.compile(optimizer=optimizer, loss=loss, metrics=["acc"])

        thread = threading.Thread(target=train_model, args=(model,x_train,y_train,x_test,y_test,batch_size,self)) 
        thread.start() 
        first_time = False
        
    
print('running')


