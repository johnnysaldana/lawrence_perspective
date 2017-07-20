
# coding: utf-8

# In[3]:

#################################### Formats Excel Spreadsheet ################################


# In[245]:

import numpy as np
import pandas as pd


# In[246]:

# loads the surveys as dataframes

df2016 = pd.read_excel("accountability2016.xlsx")
df2015 = pd.read_excel("accountability2015.xlsx")
df2014 = pd.read_excel("accountability2014.xlsx")
df2013 = pd.read_excel("accountability2013.xlsx")
df2012 = pd.read_excel("accountability2012.xlsx")


# In[247]:

# removes unnecessary columns

# removes description column
del df2016['descriptor']
del df2015['descriptor']
del df2014['descriptor']
del df2013['descriptor']
del df2012['descriptor']

# removes all district columns keeping only the one from 2016
#district names will reflect the name in 2016
del df2015['district']
del df2014['district']
del df2013['district']
del df2012['district']


# In[248]:

# merges all data into one dataframe
# note: this only includes districts

df =  df2016.merge(df2015, on='org_code').merge(df2014, on='org_code').merge(df2013, on='org_code').merge(df2012, on='org_code')


# inquiry why are there 404 code overlaps but ~300 district name overlaps


# In[249]:

# remove rows with nan

dfperf = df[np.isfinite(df['cum_prog_perf_all_2016'])]
dfperf = dfperf[np.isfinite(dfperf['cum_prog_perf_all_2015'])]
dfperf = dfperf[np.isfinite(dfperf['cum_prog_perf_all_2014'])]
dfperf = dfperf[np.isfinite(dfperf['cum_prog_perf_all_2013'])]
dfperf = dfperf[np.isfinite(dfperf['cum_prog_perf_all_2012'])]
dfperf['index'] = range(len(dfperf))

dfperf


# In[251]:

from sklearn import linear_model


# uses linear regression to find the slope difference of every districts cumulative performance
# it returns a list of all slope coefficients

slopelst = []

def regression_func():
    for index in range(len(dfperf)):
        X = np.array(list(range(5)))
        y = []
        y.extend(((dfperf.loc[dfperf['index'] == index]['cum_prog_perf_all_2012'].values),
                 (dfperf.loc[dfperf['index'] == index]['cum_prog_perf_all_2013'].values),
                 (dfperf.loc[dfperf['index'] == index]['cum_prog_perf_all_2014'].values),
                 (dfperf.loc[dfperf['index'] == index]['cum_prog_perf_all_2015'].values),
                 (dfperf.loc[dfperf['index'] == index]['cum_prog_perf_all_2016'].values))
                )
        regr = linear_model.LinearRegression()
        regr.fit(X.reshape(len(X), 1), y)
        #print(regr.coef_)
        slopelst.append(int(regr.coef_))
        
regression_func()     


# In[252]:

len(slopelst)
len(dfperf)


# In[253]:

dfperf['slope'] = slopelst

dfperf


# In[254]:

writer = pd.ExcelWriter('dfperf.xlsx')
dfperf.to_excel(writer,'Sheet1')
writer.save()


# In[255]:

import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

#dfperf['slope'].plot.hist(orientation='vertical', cumulative=True)

dfperf['slope'].diff().hist(color='blue', alpha=0.4, bins=60).grid(False)

plt.xlabel('Delta in cumulative progress and performance score from 2012 to 2016')
plt.ylabel('frequency in districts')
plt.title(r'$\mathrm{Histogram\ of\ cumulative performance score by district:}$')
plt.axis([-15, 15, 1, 50])
plt.savefig('histogram of performance delta by district.png', dpi=500)

