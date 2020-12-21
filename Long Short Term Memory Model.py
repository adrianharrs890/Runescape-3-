#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
from sklearn import preprocessing
import matplotlib.pyplot as plt 


import math
import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import RobustScaler 

from scipy import stats


# In[2]:


df = pd.read_csv(
  "~/Desktop/rsdata/whip.csv",
  parse_dates=['date'], 
  index_col="date"
)


# In[1069]:


df.head()


# In[3]:


# Featuring Eng
df['hour'] = df.index.hour
df['day_of_month'] = df.index.day
df['day_of_week'] = df.index.dayofweek
df['month'] = df.index.month
# First Difference = 1 
df["Price_Diff"] = df["Price"].diff()
# Rolling window 
df["Price_rolling"] = df["Price"].rolling(window = 7).mean()
for i in range(4,0,-1):
    df['t-'+str(i)] = df["Price"].shift(i)
df=df.dropna()


# In[4]:


df.tail()


# In[5]:


# Training / Testing 
train_size = int(len(df) * 0.80)
test_size = len(df) - train_size
train, test = df.iloc[0:train_size], df.iloc[train_size:len(df)]
print(len(train), len(test))


# In[6]:


f_columns = ['Price']

f_transformer = RobustScaler()

# tranforming the Prices 
f_transformer = f_transformer.fit(train[f_columns].to_numpy())

train.loc[:, f_columns] = f_transformer.transform(
  train[f_columns].to_numpy()
)

test.loc[:, f_columns] = f_transformer.transform(
  test[f_columns].to_numpy()
)


# In[7]:


def create_dataset(X, y, time_steps=1):
    Xs, ys = [], []
    for i in range(len(X) - time_steps):
        v = X.iloc[i:(i + time_steps)].values
        Xs.append(v)
        ys.append(y.iloc[i + time_steps])
    return np.array(Xs), np.array(ys)


# In[8]:


time_steps = 5


# In[9]:


X_train, y_train = create_dataset(train, train.Price, time_steps)
X_test, y_test = create_dataset(test, test.Price, time_steps)


# In[10]:


print(X_train.shape, y_train.shape)


# In[11]:


model = keras.Sequential()


# In[ ]:





# In[12]:


# units is the number of neurons 
model.add(
  keras.layers.Bidirectional(
    keras.layers.LSTM(
      units=128,
      input_shape=(X_train.shape[1], X_train.shape[2])
    )
  )
)

# Penaltize more Conplex models
model.add(keras.layers.Dropout(rate=0.1))
# Dense is the fully connected layer, Output layer so there is only one  
model.add(keras.layers.Dense(units=1, activation='relu'))
# Loss = Error term # Optim for to find the least error 
model.compile(loss='mean_squared_error', optimizer='adam', metrics=['acc'])


# In[13]:


history = model.fit(
    X_train, y_train,
    epochs=500,
    batch_size=20,
    validation_split=0.60,
    shuffle=False
)


# In[1086]:


plt.plot(history.history['loss'], label = 'loss')
plt.plot(history.history['val_loss'], label = 'val_loss')
plt.legend();


# In[1087]:


# Predicting on the testing data 
y_pred = model.predict(X_test)


# In[1088]:


y_train_inv = f_transformer.inverse_transform(y_train.reshape(-1,1))
y_test_inv = f_transformer.inverse_transform(y_test.reshape(-1,1))
y_pred_inv = f_transformer.inverse_transform(y_pred)


# In[1089]:


plt.plot(y_test_inv.flatten(), marker = '.', label = 'True')
plt.plot(y_pred_inv.flatten(),'r', marker = '.', label = 'Predicted')
plt.title('Abyssal whip')
plt.legend();


# In[1090]:


plt.plot(np.arange(0, len(y_train)), y_train_inv.flatten(), 'g', label="history")
plt.plot(np.arange(len(y_train), len(y_train) + len(y_test)), y_test_inv.flatten(), marker='+', label="true")
plt.plot(np.arange(len(y_train), len(y_train) + len(y_test)), y_pred_inv.flatten(), 'r', label="prediction")
plt.legend()
plt.title('Abyssal whip')
plt.show();




