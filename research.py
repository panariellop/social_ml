from numpy import loadtxt
from keras.models import Sequential
from keras.layers import Dense
from sklearn.datasets import make_regression
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import autokeras as ak

dataset = loadtxt('post_data.csv', delimiter = ",")
x = dataset[:,0:3]
y = dataset[:,3]
scaler = MinMaxScaler(feature_range=(-1,1))
scaler.fit(x)
normalized = scaler.transform(x)
x = normalized
print(x[0])

# #define keras model
model = Sequential() #input layer has 8 dimensions
model.add(Dense(12, input_dim = 3, activation = 'linear')) # first hidden layer with 12 nodes
model.add(Dense(1028, activation = 'relu')) #second hidden layer has 40 nodes and uses the relu activation function
model.add(Dense(1028, activation = 'relu')) #second hidden layer has 40 nodes and uses the relu activation function
model.add(Dense(1, activation = 'linear')) #output layer which uses the sigmoid actiavtion function

#compile keras model --> takes the model and determines the best way to train it
model.compile(loss='mse', optimizer='adam', metrics = ['mse'])

#fit the keras model on the dataset
model.fit(x, y, epochs = 200, batch_size = 40, verbose = 2)

# # define the search
# search = ak.StructuredDataRegressor(max_trials=10, loss='mean_absolute_error')
# # perform the search
# search.fit(x=x, y=y, verbose=2, epochs = 40, validation_split=0.15)

#epochs: One pass through all of the rows in the training dataset.
#Batch: One or more samples considered by the model within an epoch before weights are updated.

# evaluate the keras model
_, acc = model.evaluate(x, y)
print('acc: %.2f' % (acc))


# mae, _ = search.evaluate(x, y, verbose=0)
# print('MAE: %.3f' % mae)

# use the model to make a prediction
X_new = np.array(x[0:10]).astype('float32')
yhat = model.predict(X_new)
print("Predictions", yhat)
