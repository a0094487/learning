
# Assignment 2

Before working on this assignment please read these instructions fully. In the submission area, you will notice that you can click the link to **Preview the Grading** for each step of the assignment. This is the criteria that will be used for peer grading. Please familiarize yourself with the criteria before beginning the assignment.

An NOAA dataset has been stored in the file `data/C2A2_data/BinnedCsvs_d400/fe827567d56c440d073c979fc5b1add34f500c5ea0c784ccf4f0ea38.csv`. The data for this assignment comes from a subset of The National Centers for Environmental Information (NCEI) [Daily Global Historical Climatology Network](https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/readme.txt) (GHCN-Daily). The GHCN-Daily is comprised of daily climate records from thousands of land surface stations across the globe.

Each row in the assignment datafile corresponds to a single observation.

The following variables are provided to you:

* **id** : station identification code
* **date** : date in YYYY-MM-DD format (e.g. 2012-01-24 = January 24, 2012)
* **element** : indicator of element type
    * TMAX : Maximum temperature (tenths of degrees C)
    * TMIN : Minimum temperature (tenths of degrees C)
* **value** : data value for element (tenths of degrees C)

For this assignment, you must:

1. Read the documentation and familiarize yourself with the dataset, then write some python code which returns a line graph of the record high and record low temperatures by day of the year over the period 2005-2014. The area between the record high and record low temperatures for each day should be shaded.
2. Overlay a scatter of the 2015 data for any points (highs and lows) for which the ten year record (2005-2014) record high or record low was broken in 2015.
3. Watch out for leap days (i.e. February 29th), it is reasonable to remove these points from the dataset for the purpose of this visualization.
4. Make the visual nice! Leverage principles from the first module in this course when developing your solution. Consider issues such as legends, labels, and chart junk.

The data you have been given is near **Carlton North, Victoria, Australia**, and the stations the data comes from are shown on the map below.


```python
import matplotlib.pyplot as plt
import mplleaflet
import pandas as pd

def leaflet_plot_stations(binsize, hashid):

    df = pd.read_csv('data/C2A2_data/BinSize_d{}.csv'.format(binsize))

    station_locations_by_hash = df[df['hash'] == hashid]

    lons = station_locations_by_hash['LONGITUDE'].tolist()
    lats = station_locations_by_hash['LATITUDE'].tolist()

    plt.figure(figsize=(8,8))

    plt.scatter(lons, lats, c='r', alpha=0.7, s=200)

    return mplleaflet.display()

leaflet_plot_stations(400,'fe827567d56c440d073c979fc5b1add34f500c5ea0c784ccf4f0ea38')
```









```python
%matplotlib notebook
```




    <matplotlib.figure.Figure at 0x7f1a3436c8d0>




```python
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

#imports weather data from csv file
df = pd.read_csv('data/C2A2_data/BinnedCsvs_d400/fe827567d56c440d073c979fc5b1add34f500c5ea0c784ccf4f0ea38.csv')
df['Date']=pd.to_datetime(df['Date'])
#consolidates and averages different stations, splits into 2 groups according to as tmax or as tmin.
dfmin = df[df['Element']=='TMIN'].groupby('Date')['Data_Value'].agg({'mean': np.mean}).div(10)
dfmax = df[df['Element']=='TMAX'].groupby('Date')['Data_Value'].agg({'mean': np.mean}).div(10)

#for the high/lows linegraph, and groups according to month/day for various years
dfmin['m-d']=dfmin.index.strftime('%m%d')
dfminall = dfmin.groupby(['m-d'])['mean'].agg({'allmin': np.min}).drop(('0229'))
dfminhist = dfmin.iloc[:3652].groupby(['m-d'])['mean'].agg({'allmin': np.min}).drop(('0229'))
dfmax['m-d']=dfmax.index.strftime('%m%d')
dfmaxall = dfmax.groupby(['m-d'])['mean'].agg({'allmax': np.max}).drop(('0229'))
dfmaxhist = dfmax.iloc[:3652].groupby(['m-d'])['mean'].agg({'allmax': np.max}).drop(('0229'))

#for the 2015 records, appends to rows year
dfmin['year']=dfmin.index.year
dfmax['year']=dfmax.index.year
#seperates out the 2015 data, use to obtain only 2015 new records via multidex join
dfnewmin=dfminall.reset_index().join(dfmin[dfmin['year']==2015].reset_index()
                                     .set_index(['m-d','mean']), on=['m-d', 'allmin'])
dfnewmin = dfnewmin[np.isfinite(dfnewmin['year'])]
dfnewmax=dfmaxall.reset_index().join(dfmax[dfmax['year']==2015].reset_index()
                                     .set_index(['m-d','mean']), on=['m-d', 'allmax'])
dfnewmax = dfnewmax[np.isfinite(dfnewmax['year'])]
#obtaining corresponding lists for dates in accordance to j (e.g. 186th day of the year) 
dfnewmin['j']=dfnewmin['Date'].dt.strftime('%-j')
dfnewmax['j']=dfnewmax['Date'].dt.strftime('%-j')

plt.figure()

plt.plot(list(dfmaxhist['allmax']), '-', color='pink', linewidth=1, alpha=0.5)
plt.plot(list(dfminhist['allmin']), '-', color='lightblue', linewidth=1)
colors=['black']*17+['red']*14+['black']*9
plt.scatter(list(dfnewmin['j']),list(dfnewmin['allmin']), marker = 'v' ,s=9, color='black',zorder=3)
plt.scatter(list(dfnewmax['j']),list(dfnewmax['allmax']), marker = '^' ,s=9, color=colors,zorder=3)
#set x-ticks to monthly format
#'-1' rearranges the list to correct for strftime's auto rearrange of days
#'+timedelta to center ticks on middle of months
xticks = ((pd.date_range('1/1/2015', '31/12/2015',freq='M') - 1 + pd.Timedelta('15D'))
          .strftime('%-j').astype(int))
xticks_labels = pd.to_datetime(xticks, format='%j').strftime('%b')
plt.xticks(xticks,xticks_labels)
#fills gaps inbetween
plt.gca().fill_between(range(len(dfminall['allmin'])), 
                       list(dfminall['allmin']), list(dfmaxall['allmax']), 
                       facecolor='gray', 
                       alpha=0.2)

plt.grid(True)
plt.ylabel('Temperature ($^{\circ}$C)')
plt.title('Melbourne 2015 10-Year Record Temperatures', alpha=0.8, fontsize=9)
plt.legend(['2005-2014 Low', '2005-2014 High','2015 Record Low', '2015 Record High'],fontsize=7)
plt.show()
```


![png](output_3_0.png)



```python

```
