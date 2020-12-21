#!/usr/bin/env python
# coding: utf-8

# In[ ]:





# In[1]:


import pandas as pd
import numpy as np
from sklearn import preprocessing
import matplotlib.pyplot as plt 
from sklearn.metrics import mean_absolute_error
from sklearn.ensemble import RandomForestRegressor
import plotly.graph_objects as go


# In[2]:


df = pd.read_csv(
  "~/Desktop/rsdata/whip.csv",
  parse_dates=['date'], 
  index_col="date"
)


# In[3]:


# First Difference = 1 
df["Price_Diff"] = df["Price"].diff()
# Rolling window 
df["Price_rolling"] = df["Price"].rolling(window = 7).mean()


# In[4]:


for i in range(4,0,-1):
    df['t-'+str(i)] = df["Price"].shift(i)
df=df.dropna()


# In[5]:


df.tail()


# In[6]:


x=df.iloc[:,1:]
y=df.iloc[:,0]
x_train, x_valid = x.loc[x.index < '2020-11-10'], x.loc[x.index >= '2020-11-10']
y_train, y_valid = y.loc[y.index < '2020-11-10'], y.loc[y.index >= '2020-11-10']


# In[7]:


mdl = rf = RandomForestRegressor(n_estimators=100)


# In[8]:


mdl.fit(x_train, y_train)


# In[9]:


pred=mdl.predict(x_valid)


# In[10]:


mean_absolute_error(y_valid, pred)


# In[11]:


pred=pd.Series(pred, index=y_valid.index)


# In[12]:


fig = go.Figure()
fig.add_trace(go.Scatter(x=y_valid.index, y=y_valid.values, mode='lines', name='Abyssal whip'))
fig.add_trace(go.Scatter(x=pred.index, y=pred.values, mode='lines', name='Abyssal whip - Forecasting'))


# In[13]:


fig = go.Figure()
fig.add_trace(go.Scatter(x=y_train.loc[y_train.index > '2020-08-20'].index,
                         y=y_train.loc[y_train.index > '2020-08-20'].values, mode='lines', name='Abyssal Whip before'))

fig.add_trace(go.Scatter(x=y_valid.index, y=y_valid.values, mode='lines', name='Abyssal Whip observed'))
fig.add_trace(go.Scatter(x=pred.index, y=pred.values, mode='lines', name='Abyssal Whip - Forecasting'))


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[124]:





# In[ ]:





# In[126]:





# In[ ]:





# In[ ]:





# In[ ]:




