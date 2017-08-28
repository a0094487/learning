
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

#leaflet_plot_stations(400,'fe827567d56c440d073c979fc5b1add34f500c5ea0c784ccf4f0ea38')
```


```python
#%matplotlib notebook
pd.read_csv('data/C2A2_data/BinnedCsvs_d400/fe827567d56c440d073c979fc5b1add34f500c5ea0c784ccf4f0ea38.csv')
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>ID</th>
      <th>Date</th>
      <th>Element</th>
      <th>Data_Value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>ASN00086071</td>
      <td>2012-06-12</td>
      <td>TMAX</td>
      <td>165</td>
    </tr>
    <tr>
      <th>1</th>
      <td>ASN00086104</td>
      <td>2014-11-24</td>
      <td>TMAX</td>
      <td>217</td>
    </tr>
    <tr>
      <th>2</th>
      <td>ASN00086077</td>
      <td>2010-06-14</td>
      <td>TMIN</td>
      <td>76</td>
    </tr>
    <tr>
      <th>3</th>
      <td>ASN00087031</td>
      <td>2007-01-16</td>
      <td>TMAX</td>
      <td>412</td>
    </tr>
    <tr>
      <th>4</th>
      <td>ASN00086068</td>
      <td>2011-10-13</td>
      <td>TMIN</td>
      <td>36</td>
    </tr>
    <tr>
      <th>5</th>
      <td>ASN00086104</td>
      <td>2011-09-17</td>
      <td>TMAX</td>
      <td>243</td>
    </tr>
    <tr>
      <th>6</th>
      <td>ASN00086104</td>
      <td>2014-11-24</td>
      <td>TMIN</td>
      <td>120</td>
    </tr>
    <tr>
      <th>7</th>
      <td>ASN00086071</td>
      <td>2005-09-07</td>
      <td>TMIN</td>
      <td>102</td>
    </tr>
    <tr>
      <th>8</th>
      <td>ASN00086104</td>
      <td>2012-04-22</td>
      <td>TMIN</td>
      <td>142</td>
    </tr>
    <tr>
      <th>9</th>
      <td>ASN00086383</td>
      <td>2005-03-08</td>
      <td>TMAX</td>
      <td>199</td>
    </tr>
    <tr>
      <th>10</th>
      <td>ASN00086104</td>
      <td>2012-04-22</td>
      <td>TMAX</td>
      <td>231</td>
    </tr>
    <tr>
      <th>11</th>
      <td>ASN00086372</td>
      <td>2005-03-08</td>
      <td>TMAX</td>
      <td>142</td>
    </tr>
    <tr>
      <th>12</th>
      <td>ASN00086282</td>
      <td>2005-08-20</td>
      <td>TMAX</td>
      <td>152</td>
    </tr>
    <tr>
      <th>13</th>
      <td>ASN00086038</td>
      <td>2007-05-12</td>
      <td>TMIN</td>
      <td>62</td>
    </tr>
    <tr>
      <th>14</th>
      <td>ASN00086038</td>
      <td>2007-05-12</td>
      <td>TMAX</td>
      <td>192</td>
    </tr>
    <tr>
      <th>15</th>
      <td>ASN00086077</td>
      <td>2007-01-30</td>
      <td>TMIN</td>
      <td>137</td>
    </tr>
    <tr>
      <th>16</th>
      <td>ASN00086282</td>
      <td>2012-09-28</td>
      <td>TMAX</td>
      <td>165</td>
    </tr>
    <tr>
      <th>17</th>
      <td>ASN00086282</td>
      <td>2012-09-28</td>
      <td>TMIN</td>
      <td>87</td>
    </tr>
    <tr>
      <th>18</th>
      <td>ASN00085283</td>
      <td>2011-09-20</td>
      <td>TMAX</td>
      <td>125</td>
    </tr>
    <tr>
      <th>19</th>
      <td>ASN00086077</td>
      <td>2008-11-29</td>
      <td>TMIN</td>
      <td>137</td>
    </tr>
    <tr>
      <th>20</th>
      <td>ASN00086351</td>
      <td>2011-07-01</td>
      <td>TMAX</td>
      <td>164</td>
    </tr>
    <tr>
      <th>21</th>
      <td>ASN00087031</td>
      <td>2005-03-18</td>
      <td>TMAX</td>
      <td>225</td>
    </tr>
    <tr>
      <th>22</th>
      <td>ASN00086038</td>
      <td>2011-06-30</td>
      <td>TMAX</td>
      <td>164</td>
    </tr>
    <tr>
      <th>23</th>
      <td>ASN00086351</td>
      <td>2006-10-15</td>
      <td>TMIN</td>
      <td>51</td>
    </tr>
    <tr>
      <th>24</th>
      <td>ASN00086351</td>
      <td>2006-10-15</td>
      <td>TMAX</td>
      <td>155</td>
    </tr>
    <tr>
      <th>25</th>
      <td>ASN00086383</td>
      <td>2007-07-21</td>
      <td>TMIN</td>
      <td>9</td>
    </tr>
    <tr>
      <th>26</th>
      <td>ASN00087031</td>
      <td>2005-03-18</td>
      <td>TMIN</td>
      <td>94</td>
    </tr>
    <tr>
      <th>27</th>
      <td>ASN00086068</td>
      <td>2015-09-10</td>
      <td>TMAX</td>
      <td>154</td>
    </tr>
    <tr>
      <th>28</th>
      <td>ASN00086038</td>
      <td>2011-06-30</td>
      <td>TMIN</td>
      <td>50</td>
    </tr>
    <tr>
      <th>29</th>
      <td>ASN00086077</td>
      <td>2008-04-29</td>
      <td>TMAX</td>
      <td>147</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>80898</th>
      <td>ASN00086351</td>
      <td>2008-08-01</td>
      <td>TMIN</td>
      <td>84</td>
    </tr>
    <tr>
      <th>80899</th>
      <td>ASN00086351</td>
      <td>2011-05-26</td>
      <td>TMAX</td>
      <td>138</td>
    </tr>
    <tr>
      <th>80900</th>
      <td>ASN00086077</td>
      <td>2014-06-30</td>
      <td>TMAX</td>
      <td>126</td>
    </tr>
    <tr>
      <th>80901</th>
      <td>ASN00086071</td>
      <td>2008-02-26</td>
      <td>TMIN</td>
      <td>142</td>
    </tr>
    <tr>
      <th>80902</th>
      <td>ASN00086104</td>
      <td>2009-05-01</td>
      <td>TMIN</td>
      <td>69</td>
    </tr>
    <tr>
      <th>80903</th>
      <td>ASN00087031</td>
      <td>2005-05-01</td>
      <td>TMAX</td>
      <td>172</td>
    </tr>
    <tr>
      <th>80904</th>
      <td>ASN00086071</td>
      <td>2010-10-27</td>
      <td>TMIN</td>
      <td>127</td>
    </tr>
    <tr>
      <th>80905</th>
      <td>ASN00086071</td>
      <td>2013-08-21</td>
      <td>TMIN</td>
      <td>68</td>
    </tr>
    <tr>
      <th>80906</th>
      <td>ASN00086077</td>
      <td>2011-05-24</td>
      <td>TMIN</td>
      <td>100</td>
    </tr>
    <tr>
      <th>80907</th>
      <td>ASN00086372</td>
      <td>2009-10-03</td>
      <td>TMAX</td>
      <td>134</td>
    </tr>
    <tr>
      <th>80908</th>
      <td>ASN00087031</td>
      <td>2006-03-15</td>
      <td>TMIN</td>
      <td>110</td>
    </tr>
    <tr>
      <th>80909</th>
      <td>ASN00086071</td>
      <td>2008-02-26</td>
      <td>TMAX</td>
      <td>232</td>
    </tr>
    <tr>
      <th>80910</th>
      <td>ASN00086282</td>
      <td>2009-09-22</td>
      <td>TMIN</td>
      <td>95</td>
    </tr>
    <tr>
      <th>80911</th>
      <td>ASN00086351</td>
      <td>2014-10-04</td>
      <td>TMIN</td>
      <td>54</td>
    </tr>
    <tr>
      <th>80912</th>
      <td>ASN00086038</td>
      <td>2005-12-14</td>
      <td>TMAX</td>
      <td>243</td>
    </tr>
    <tr>
      <th>80913</th>
      <td>ASN00086351</td>
      <td>2011-05-26</td>
      <td>TMIN</td>
      <td>85</td>
    </tr>
    <tr>
      <th>80914</th>
      <td>ASN00086068</td>
      <td>2014-02-23</td>
      <td>TMAX</td>
      <td>257</td>
    </tr>
    <tr>
      <th>80915</th>
      <td>ASN00086282</td>
      <td>2012-11-11</td>
      <td>TMIN</td>
      <td>58</td>
    </tr>
    <tr>
      <th>80916</th>
      <td>ASN00087031</td>
      <td>2006-10-14</td>
      <td>TMIN</td>
      <td>114</td>
    </tr>
    <tr>
      <th>80917</th>
      <td>ASN00086372</td>
      <td>2009-10-03</td>
      <td>TMIN</td>
      <td>49</td>
    </tr>
    <tr>
      <th>80918</th>
      <td>ASN00086038</td>
      <td>2011-05-17</td>
      <td>TMIN</td>
      <td>95</td>
    </tr>
    <tr>
      <th>80919</th>
      <td>ASN00086351</td>
      <td>2007-08-03</td>
      <td>TMAX</td>
      <td>130</td>
    </tr>
    <tr>
      <th>80920</th>
      <td>ASN00086104</td>
      <td>2006-01-09</td>
      <td>TMAX</td>
      <td>311</td>
    </tr>
    <tr>
      <th>80921</th>
      <td>ASN00087031</td>
      <td>2006-03-15</td>
      <td>TMAX</td>
      <td>222</td>
    </tr>
    <tr>
      <th>80922</th>
      <td>ASN00087031</td>
      <td>2006-10-14</td>
      <td>TMAX</td>
      <td>237</td>
    </tr>
    <tr>
      <th>80923</th>
      <td>ASN00086282</td>
      <td>2007-12-08</td>
      <td>TMAX</td>
      <td>259</td>
    </tr>
    <tr>
      <th>80924</th>
      <td>ASN00086077</td>
      <td>2005-06-08</td>
      <td>TMAX</td>
      <td>237</td>
    </tr>
    <tr>
      <th>80925</th>
      <td>ASN00086104</td>
      <td>2013-08-24</td>
      <td>TMAX</td>
      <td>148</td>
    </tr>
    <tr>
      <th>80926</th>
      <td>ASN00086038</td>
      <td>2015-11-24</td>
      <td>TMIN</td>
      <td>113</td>
    </tr>
    <tr>
      <th>80927</th>
      <td>ASN00086077</td>
      <td>2014-05-01</td>
      <td>TMIN</td>
      <td>73</td>
    </tr>
  </tbody>
</table>
<p>80928 rows × 4 columns</p>
</div>




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
