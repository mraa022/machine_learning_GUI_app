import json
from channels.generic.websocket import AsyncWebsocketConsumer
import os
import asyncio
import sys
import threading
from tensorflow.python.profiler import profiler_v2 as profiler
from pandas import read_csv,get_dummies
from sklearn.model_selection import train_test_split
from tensorflow.keras.losses import (
        MeanSquaredError,
        MeanAbsoluteError,
        MeanAbsolutePercentageError,
        MeanSquaredLogarithmicError,
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
from keras import backend as K
K.clear_session()
from tensorflow import GradientTape
from tensorflow.data import Dataset
from tensorflow.keras import Sequential
from keras.layers import Dense

from tensorflow.keras.losses import (
        MeanSquaredError,
        MeanAbsoluteError,
        MeanAbsolutePercentageError,
        MeanSquaredLogarithmicError,
        Huber,
        LogCosh,
        CategoricalCrossentropy,
        Poisson,
        KLDivergence,
        BinaryCrossentropy
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
import json
stop_training  = False
from tensorflow.data import Dataset
import asyncio
from tensorflow import GradientTape
from tensorflow.keras import Sequential
from keras.layers import Dense
import sys








def optimizer_options(
                      learning_rate=0.001,
                      beta_1=0.9,
                      beta_2=0.999,
                      rho=0.9,
                      momentum=0,
                      initial_accumulator_value=0.1,
                      l1_regularization_strength=0.0,
                      l2_regularization_strength=0.0,
                      l2_shrinkage_regularization_strength=0.0,
                      learning_rate_power=-0.5
                      ):
    optimizers = {
            'Adam':Adam(
                learning_rate=learning_rate, beta_1=beta_1, beta_2=beta_2, epsilon=1e-07, amsgrad=False,
                name='Adam'
                ),
            'Rmsprop':RMSprop(
                learning_rate=learning_rate,
                rho=rho,
                momentum=momentum,
                epsilon=1e-07,
                centered=False,
                name="RMSprop",
                ),
            'Adagrad':Adagrad(
                learning_rate=learning_rate,
                initial_accumulator_value=initial_accumulator_value,
                epsilon=1e-07
                ),
            'Adadelta':Adadelta(
                learning_rate=learning_rate, rho=rho, epsilon=1e-07
                ),
            'SGD':SGD(
                learning_rate=learning_rate, momentum=momentum, nesterov=False
                ),
            'Adamax':Adamax(
                learning_rate=learning_rate, beta_1=beta_1, beta_2=beta_2, epsilon=1e-07
                ),

            'Nadam':Nadam(
                learning_rate=learning_rate, beta_1=beta_1, beta_2=beta_2, epsilon=1e-07
                ),

            'Ftrl':Ftrl(
                learning_rate=learning_rate,
                learning_rate_power=learning_rate_power,
                initial_accumulator_value=initial_accumulator_value,
                l1_regularization_strength=l1_regularization_strength,
                l2_regularization_strength=l2_regularization_strength,
                l2_shrinkage_regularization_strength=l2_shrinkage_regularization_strength,
                )
            }
    return optimizers

def loss_options():
        losses = {
            'MeanSquaredError':MeanSquaredError(reduction="auto"),
            'MeanAbsoluteError':MeanAbsoluteError(reduction="auto"),
            'MeanAbsolutePercentageError':MeanAbsolutePercentageError(reduction="auto"),
            'MeanSquaredLogarithmicError':MeanSquaredLogarithmicError(reduction="auto"),
            'Huber':Huber(delta=1.0, reduction="auto"),
            'LogCosh':LogCosh(reduction="auto", name="log_cosh"),
            'CategoricalCrossentropy':CategoricalCrossentropy(from_logits=False,label_smoothing=0,reduction="auto"),
            'Poisson':Poisson(reduction="auto", name="poisson"),
            'KLDivergence':KLDivergence(reduction="auto", name="kl_divergence"),
            'BinaryCrossentropy':BinaryCrossentropy(label_smoothing=0, reduction="auto", name="binary_crossentropy")
        }
        return losses
def create_model(layers,number_of_inputs,activations,label_type,number_of_classes):
    layers = [1] if not layers else layers  # one layer with one neuron is the default if the user did not provide any layers
    activations = ['relu'] if not activations else activations
    model = Sequential(name="my_sequential")
    model.add(Dense(layers[0], input_shape=(number_of_inputs,),activation=activations[0]))
    if len(layers)>1:
        [model.add(Dense(units,activation=activation)) for units,activation in zip(layers[1:],activations[1:])]
    output = model.add(Dense(number_of_classes,activation='softmax',name='output_layer')) if label_type == 'discrete' else model.add(Dense(1))
    return model






def loss(model, x, y, training,loss_function):

  y_ = model(x, training=training)

  training_loss_object = loss_function(y_true=y,y_pred=y_)

  return training_loss_object



def get_loss_and_gradients(model, inputs, targets,loss_function):
  with GradientTape() as tape:

    training_loss_value = loss(model, inputs, targets,True,loss_function)
    # print(float(training_loss_value))
  return training_loss_value, tape.gradient(training_loss_value, model.trainable_variables)



stop_training = False

async def train(model,training_dataset,x_test,y_test,consumer_instance,batch_size,optimizer,loss_function):
    epoch = 0
   
    training_dataset = training_dataset.shuffle(buffer_size=len(list(training_dataset)))
    while True:
        training_loss_avg = []
        
        # print('BUFEERED')
        # Training loop - using batches of batch_size
        for x, y in training_dataset.batch(batch_size):


            training_loss_value, gradients = get_loss_and_gradients(model, x, y,loss_function) 
            
            training_loss_avg.append(float(training_loss_value))
            optimizer.apply_gradients(zip(gradients, model.trainable_variables))
            await asyncio.sleep(0.00000000000001)

        test_loss_value =0
        print(sum(training_loss_avg)/len(training_loss_avg), epoch ) 
        epoch+=1
        # training_dataset = training_dataset.shuffle(buffer_size=6)


async def look_for_stop_training_flag():
    global stop_training
    while not stop_training:
        # print('LOOKIING FOR FLAG')
        if stop_training:
            print('QUITED')
            stop_training = False
            break
        await asyncio.sleep(0.00000000000001)

async def main(model,training_dataset,x_test,y_test,consumer_instance,batch_size,optimizer,loss_function):
    task1 = asyncio.create_task(train(model,training_dataset,x_test,y_test,consumer_instance,batch_size,optimizer,loss_function))
    task2 = asyncio.create_task(look_for_stop_training_flag())
    await asyncio.gather(task1,task2)

def manage_tasks(model,training_dataset,x_test,y_test,consumer_instance,batch_size,optimizer,loss_function):
    asyncio.run(main(model,training_dataset,x_test,y_test,consumer_instance,batch_size,optimizer,loss_function))


def get_dataframe(data_frame_location):

    return remove_column(read_csv(data_frame_location))

  
dataframe = read_csv('/Users/adnanbadri/Documents/web_dev/Personal_Projects/machine_learning_gui/media/datasets/qgrejg4muc11ghwq04hfe63xexmnm9lcformated_dataset.csv')

test_size = 0.3
batch_size = 64
x = dataframe.drop('banking_crisis',axis=1).drop('Unnamed: 0',axis=1).values
y = get_dummies(dataframe['banking_crisis'].values,drop_first=True)
x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=test_size)
model = create_model(layers=[],activations=[],number_of_classes=2,label_type='discrete',number_of_inputs = x_train.shape[1])
model.compile(optimizer=optimizer_options()['Adam'],loss=loss_options()['BinaryCrossentropy'])


model.fit(x_train,y_train,epochs=1000)



