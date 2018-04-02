
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.covariance import EmpiricalCovariance, MinCovDet
import datetime


# In[2]:


df=pd.read_csv(r'C:\Users\mattk\hist_yc2.csv',index_col = 0,parse_dates=True)


# In[3]:


df = df.dropna()


# In[4]:


pts = ['1 YR', '2 YR', '3 YR', '5 YR', '7 YR', '10 YR', '20 YR', '30 YR']


# In[5]:


data = df.loc[:,pts].values


# In[6]:


data[-2,:]


# In[7]:


data_change = df - df.shift(1)


# In[8]:


data_change = data_change.dropna()


# In[9]:


data2 = data_change.loc[:,pts].values


# In[10]:


cov = np.cov(data2.T)


# In[11]:


cov2=pd.DataFrame(cov,columns=pts)


# In[12]:


cov2.T


# In[13]:


pca=PCA()


# In[14]:


P=pca.fit_transform(data2)


# In[15]:


evalues = pca.explained_variance_


# In[16]:


evalues


# In[17]:


plt.bar(range(8),pca.explained_variance_ratio_)
plt.title('var ratio explained by pc')
plt.show()


# In[18]:


pca.components_


# In[19]:


components = pd.DataFrame(pca.components_,columns=evalues)


# In[20]:


components

