import json
from channels.generic.websocket import WebsocketConsumer
import time
import random
import os
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
from tensorflow.keras import Sequential
from keras.layers import Dense

class ErrorGraphConsumer(WebsocketConsumer):
    def connect(self):
        self.quit_training = True
        self.accept()

    def disconnect(self, close_code):
        '''
            on disconnect, delete the file that contained that user's dataframe
        '''
        dataframe_file = self.scope['cookies']['sessionid']+'formated_dataset.csv'
        media_path = os.path.join(settings.MEDIA_ROOT,'datasets/')
        delete_file_path = os.path.join(media_path,dataframe_file)
        os.remove(delete_file_path)

    def receive(self, text_data):
        # self.quit_training = False
        text_data_json = json.loads(text_data)
        layers = text_data_json['layers'] # the numbers are strings
        layers = [int(x) for x in layers]
        layer_activations = text_data_json['layer_activations']
        a = 0
        
        while True:
            
            try:
                self.send(text_data=json.dumps({
                    'error_rate': a
                }))

            except Exception as e :
                print(e)
                break

            a = random.randint(1,1000)
            
            time.sleep(0.25)

print('HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH')