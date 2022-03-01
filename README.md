# Neural Network Playground
This web app is similar to [tensorflow's neural network playground](https://playground.tensorflow.org/#activation=tanh&batchSize=10&dataset=circle&regDataset=reg-plane&learningRate=0.03&regularizationRate=0&noise=0&networkShape=4,2&seed=0.46003&showTestData=false&discretize=false&percTrainData=50&x=true&y=true&xTimesY=false&xSquared=false&ySquared=false&cosX=false&sinX=false&cosY=false&sinY=false&collectStats=false&problem=classification&initZero=false&hideText=false), but it gives the user more options. like, being able to set the activation function of each layer,being able to add as many layers as they want, and being able to save upto 10 files (csv or url) to their account for easy access when training their model. The link: https://neural--network--playground.herokuapp.com/. Log in with the following user to get access 10 pre-uploaded datasets. 
username:a
password:1

  
# Features:

  - the user can add as many layers as they want
  - the user can save upto 10 csv files, or urls (that point to a table) to their account for easy access when training their model.
  - choose the activation function and number of neurons of each layer
  - change saved files/url to new files/url
  - choose the label,numerical, and categorical columns (unselected columns will be removed)
  - the user can see a live graph of the training and test loss of the network
  - the user can choose from all of the optimizers,losses, and activation functions that are available in keras.
  - the user can edit each parameter of the optimizer (learning_rate,rho,beta_1,beta_2,etc)
  
  

# Limitations!!
  - the sessionid is used to give the model the user customized dataset. so, opening multiple tabs will break the program. 
  - if the value of a cell is empty, the whole row is removed.
  - if a url is used, and the page contains more than 1 table. the first one will be selected
  - if a url is used. the table must be in a 'table' tag (canvas tags won't work)
  - it can only do densely connected neural networks ( and the label type must be either categorical or continuous)
  - cookies are heavily used, the user MUST not block them.
  - the boot time is quite long since the app has many dependencies 
  

# tech used
 - django: for the whole website
 - django-channels: to handle the live data of the error graph (websocket)
 - chartjs: to graph the error graph
 - threads: the training of the model is blocking so, its run in another thread
 - tensorflow/keras: for the neural network
 - SQLite: the database

# upcoming updates
 - Amazon S3 buckets will be used to store media/static files instead of heroku (this should decrease the boot time).
 - The website will be made faster by using chaching and rewriting parts of the code so it's more efficient. 
# running it locally:

 - the requirements.txt contains all of the libraries used in the project
 - python-3.7.9
 - don't forget to set debug to True in order to use the static files
