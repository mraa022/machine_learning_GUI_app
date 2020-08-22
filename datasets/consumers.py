import json
from channels.generic.websocket import WebsocketConsumer
import time
import random

def optimizer_options(learning_rate):
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
            epsilon=1e-07
        )}

    return optimizers

def loss_options(label_type):
    # model_type = regression or classification
    is_binary_classification = True if number_of_classes == 1 and label_type == 'discrete' else False
    print('fffffffff',label_type)
    if label_type == 'continuous':

        losses = {
            'MeanSquaredError':tf.keras.losses.MeanSquaredError(reduction="auto"),
            'MeanAbsoluteError':tf.keras.losses.MeanAbsoluteError(reduction="auto"),
            'MeanAbsolutePercentageError':tf.keras.losses.MeanAbsolutePercentageError(reduction="auto"),
            'MeanSquaredLogarithmicError':tf.keras.losses.MeanSquaredLogarithmicError(reduction="auto"),
            'CosineSimilarity':tf.keras.losses.CosineSimilarity(axis=-1, reduction="auto"),
            'Huber':tf.keras.losses.Huber(delta=1.0, reduction="auto"),
            'LogCosh':tf.keras.losses.LogCosh(reduction="auto", name="log_cosh")

        }

    else:

        losses = {

            'CategoricalCrossentropy':   tf.keras.losses.CategoricalCrossentropy(from_logits=False,label_smoothing=0,reduction="auto"),
            'Poisson':tf.keras.losses.Poisson(reduction="auto", name="poisson"),
            'KLDivergence':tf.keras.losses.KLDivergence(reduction="auto", name="kl_divergence")
        }

    
    if is_binary_classification:
        losses.update({'BinaryCrossentropy':tf.keras.losses.BinaryCrossentropy(from_logits=False, label_smoothing=0, reduction="auto")})
    return losses

class ErrorGraphConsumer(WebsocketConsumer):
    def connect(self):
        self.quit_training = True
        self.accept()

    def disconnect(self, close_code):
        self.quit_training = False
        pass

        
        

    def receive(self, text_data):
        # self.quit_training = False
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        a = 0
        
        while True:
            print(self.quit_training)
            try:
                self.send(text_data=json.dumps({
                    'message': a
                }))

            except Exception as e :
                print(e)
                break

            a = random.randint(1,1000)
            
            time.sleep(0.25)