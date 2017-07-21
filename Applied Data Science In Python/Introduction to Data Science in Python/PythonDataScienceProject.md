
---

_You are currently looking at **version 1.1** of this notebook. To download notebooks and datafiles, as well as get help on Jupyter notebooks in the Coursera platform, visit the [Jupyter Notebook FAQ](https://www.coursera.org/learn/python-data-analysis/resources/0dhYG) course resource._

---


```python
import pandas as pd
import numpy as np
from scipy.stats import ttest_ind
```

# Assignment 4 - Hypothesis Testing
This assignment requires more individual learning than previous assignments - you are encouraged to check out the [pandas documentation](http://pandas.pydata.org/pandas-docs/stable/) to find functions or methods you might not have used yet, or ask questions on [Stack Overflow](http://stackoverflow.com/) and tag them as pandas and python related. And of course, the discussion forums are open for interaction with your peers and the course staff.

Definitions:
* A _quarter_ is a specific three month period, Q1 is January through March, Q2 is April through June, Q3 is July through September, Q4 is October through December.
* A _recession_ is defined as starting with two consecutive quarters of GDP decline, and ending with two consecutive quarters of GDP growth.
* A _recession bottom_ is the quarter within a recession which had the lowest GDP.
* A _university town_ is a city which has a high percentage of university students compared to the total population of the city.

**Hypothesis**: University towns have their mean housing prices less effected by recessions. Run a t-test to compare the ratio of the mean price of houses in university towns the quarter before the recession starts compared to the recession bottom. (`price_ratio=quarter_before_recession/recession_bottom`)

The following data files are available for this assignment:
* From the [Zillow research data site](http://www.zillow.com/research/data/) there is housing data for the United States. In particular the datafile for [all homes at a city level](http://files.zillowstatic.com/research/public/City/City_Zhvi_AllHomes.csv), ```City_Zhvi_AllHomes.csv```, has median home sale prices at a fine grained level.
* From the Wikipedia page on college towns is a list of [university towns in the United States](https://en.wikipedia.org/wiki/List_of_college_towns#College_towns_in_the_United_States) which has been copy and pasted into the file ```university_towns.txt```.
* From Bureau of Economic Analysis, US Department of Commerce, the [GDP over time](http://www.bea.gov/national/index.htm#gdp) of the United States in current dollars (use the chained value in 2009 dollars), in quarterly intervals, in the file ```gdplev.xls```. For this assignment, only look at GDP data from the first quarter of 2000 onward.

Each function in this assignment below is worth 10%, with the exception of ```run_ttest()```, which is worth 50%.


```python
# Use this dictionary to map state names to two letter acronyms
states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}
```


```python
def get_list_of_university_towns():
    '''Returns a DataFrame of towns and the states they are in from the 
    university_towns.txt list. The format of the DataFrame should be:
    DataFrame( [ ["Michigan", "Ann Arbor"], ["Michigan", "Yipsilanti"] ], 
    columns=["State", "RegionName"]  )
    
    The following cleaning needs to be done:

    1. For "State", removing characters from "[" to the end.
    2. For "RegionName", when applicable, removing every character from " (" to the end.
    3. Depending on how you read the data, you may need to remove newline character '\n'. '''
    import pandas as pd
    openfile = open('university_towns.txt')
    readFile = openfile.readlines()
    d = {}
    d['State']=[]
    d['RegionName']=[]
    for linestring in readFile: 
        if linestring.endswith('[edit]\n'): state=linestring[:-7]
            #for x,y in states.items():
                #if y == (linestring[:-7]): state = x
        else: 
            d['State'].append(state)
            d['RegionName'].append(linestring[:linestring.find(' (')])
    openfile.close()
    return pd.DataFrame(d)[['State','RegionName']]
get_list_of_university_towns().head()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>State</th>
      <th>RegionName</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Alabama</td>
      <td>Auburn</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Alabama</td>
      <td>Florence</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Alabama</td>
      <td>Jacksonville</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Alabama</td>
      <td>Livingston</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Alabama</td>
      <td>Montevallo</td>
    </tr>
  </tbody>
</table>
</div>




```python
def get_recession_start():
    '''Returns the year and quarter of the recession start time as a 
    string value in a format such as 2005q3'''
    import pandas as pd
    df=(pd.read_excel('gdplev.xls', index_col=None, skiprows=219)[['1999q4', 12323.3]]
    .rename(columns={'1999q4':'Period',12323.3:'realGDP'}))
    years=[]
    for x in df.index: 
        try: 
            if ((df.loc[x+1]['realGDP'] < df.loc[x]['realGDP']) & 
                (df.loc[x]['realGDP'] < df.loc[x-1]['realGDP'])):
                years.append(df.loc[x]['Period'])
        except:continue
    return years[0]
get_recession_start()
```




    '2008q3'




```python
def get_recession_end():
    '''Returns the year and quarter of the recession end time as a 
    string value in a format such as 2005q3'''
    import pandas as pd
    df=(pd.read_excel('gdplev.xls', index_col=None, skiprows=219)[['1999q4', 12323.3]]
    .rename(columns={'1999q4':'Period',12323.3:'realGDP'}))
    years=[]
    for x in range(df[df['Period']==get_recession_start()].index[0], len(df)): 
        try: 
            if ((df.loc[x+1]['realGDP'] > df.loc[x]['realGDP']) & 
                (df.loc[x]['realGDP'] > df.loc[x-1]['realGDP'])):
                years.append(df.loc[x+1]['Period'])
        except:continue
    return years[0]
get_recession_end()
```




    '2009q4'




```python
def get_recession_bottom():
    '''Returns the year and quarter of the recession bottom time as a 
    string value in a format such as 2005q3'''
    import pandas as pd
    df=(pd.read_excel('gdplev.xls', index_col=None, skiprows=219)[['1999q4', 12323.3]]
    .rename(columns={'1999q4':'Period',12323.3:'realGDP'}))
    worst=(get_recession_start(), df.loc[df[df['Period']==get_recession_start()].index[0]]['realGDP'])
    for x in range(df[df['Period']==get_recession_start()].index[0], len(df)): 
        if df.loc[x]['realGDP'] < worst[1]: 
            worst=(df.loc[x]['Period'], df.loc[x]['realGDP'])
    return worst[0]
get_recession_bottom()
```




    '2009q2'




```python
def convert_housing_data_to_quarters():
    '''Converts the housing data to quarters and returns it as mean 
    values in a dataframe. This dataframe should be a dataframe with
    columns for 2000q1 through 2016q3, and should have a multi-index
    in the shape of ["State","RegionName"].
    
    Note: Quarters are defined in the assignment description, they are
    not arbitrary three month periods.
    
    The resulting dataframe should have 67 columns, and 10,730 rows.
    '''
    import numpy as np
    import pandas as pd
    df = pd.read_csv('City_Zhvi_AllHomes.csv', index_col=None, skiprows=0)
    for key in states:
        df.replace(key, states[key], inplace=True)
    list=[('q1',['-01','-02','-03']),('q2',['-04','-05','-06']),
          ('q3',['-07','-08','-09']),('q4',['-10','-11','-12'])]
    for y in range(2000,2017):
        for q in list:
            try: df[str(y)+q[0]]=np.mean(df[[(str(y)+q[1][0]),(str(y)+q[1][1]),
                                             (str(y)+q[1][2])]], axis=1)
            except:
                try:df[str(y)+q[0]]=np.mean(df[[(str(y)+q[1][0]),
                                                (str(y)+q[1][1])]], axis=1)
                except: continue
    for y in range(1996,2017):
        for m in ['01','02','03','04','05','06','07','08','09','10','11','12']:
            try: del df[str(y)+'-'+m]
            except: continue
    df = df.set_index(['State','RegionName']).drop(['RegionID','Metro','CountyName','SizeRank'],axis=1)
    return df
convert_housing_data_to_quarters().head()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th></th>
      <th>2000q1</th>
      <th>2000q2</th>
      <th>2000q3</th>
      <th>2000q4</th>
      <th>2001q1</th>
      <th>2001q2</th>
      <th>2001q3</th>
      <th>2001q4</th>
      <th>2002q1</th>
      <th>2002q2</th>
      <th>...</th>
      <th>2014q2</th>
      <th>2014q3</th>
      <th>2014q4</th>
      <th>2015q1</th>
      <th>2015q2</th>
      <th>2015q3</th>
      <th>2015q4</th>
      <th>2016q1</th>
      <th>2016q2</th>
      <th>2016q3</th>
    </tr>
    <tr>
      <th>State</th>
      <th>RegionName</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>New York</th>
      <th>New York</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>515466.666667</td>
      <td>522800.000000</td>
      <td>528066.666667</td>
      <td>532266.666667</td>
      <td>540800.000000</td>
      <td>557200.000000</td>
      <td>572833.333333</td>
      <td>582866.666667</td>
      <td>591633.333333</td>
      <td>587200.0</td>
    </tr>
    <tr>
      <th>California</th>
      <th>Los Angeles</th>
      <td>207066.666667</td>
      <td>214466.666667</td>
      <td>220966.666667</td>
      <td>226166.666667</td>
      <td>233000.000000</td>
      <td>239100.000000</td>
      <td>245066.666667</td>
      <td>253033.333333</td>
      <td>261966.666667</td>
      <td>272700.000000</td>
      <td>...</td>
      <td>498033.333333</td>
      <td>509066.666667</td>
      <td>518866.666667</td>
      <td>528800.000000</td>
      <td>538166.666667</td>
      <td>547266.666667</td>
      <td>557733.333333</td>
      <td>566033.333333</td>
      <td>577466.666667</td>
      <td>584050.0</td>
    </tr>
    <tr>
      <th>Illinois</th>
      <th>Chicago</th>
      <td>138400.000000</td>
      <td>143633.333333</td>
      <td>147866.666667</td>
      <td>152133.333333</td>
      <td>156933.333333</td>
      <td>161800.000000</td>
      <td>166400.000000</td>
      <td>170433.333333</td>
      <td>175500.000000</td>
      <td>177566.666667</td>
      <td>...</td>
      <td>192633.333333</td>
      <td>195766.666667</td>
      <td>201266.666667</td>
      <td>201066.666667</td>
      <td>206033.333333</td>
      <td>208300.000000</td>
      <td>207900.000000</td>
      <td>206066.666667</td>
      <td>208200.000000</td>
      <td>212000.0</td>
    </tr>
    <tr>
      <th>Pennsylvania</th>
      <th>Philadelphia</th>
      <td>53000.000000</td>
      <td>53633.333333</td>
      <td>54133.333333</td>
      <td>54700.000000</td>
      <td>55333.333333</td>
      <td>55533.333333</td>
      <td>56266.666667</td>
      <td>57533.333333</td>
      <td>59133.333333</td>
      <td>60733.333333</td>
      <td>...</td>
      <td>113733.333333</td>
      <td>115300.000000</td>
      <td>115666.666667</td>
      <td>116200.000000</td>
      <td>117966.666667</td>
      <td>121233.333333</td>
      <td>122200.000000</td>
      <td>123433.333333</td>
      <td>126933.333333</td>
      <td>128700.0</td>
    </tr>
    <tr>
      <th>Arizona</th>
      <th>Phoenix</th>
      <td>111833.333333</td>
      <td>114366.666667</td>
      <td>116000.000000</td>
      <td>117400.000000</td>
      <td>119600.000000</td>
      <td>121566.666667</td>
      <td>122700.000000</td>
      <td>124300.000000</td>
      <td>126533.333333</td>
      <td>128366.666667</td>
      <td>...</td>
      <td>164266.666667</td>
      <td>165366.666667</td>
      <td>168500.000000</td>
      <td>171533.333333</td>
      <td>174166.666667</td>
      <td>179066.666667</td>
      <td>183833.333333</td>
      <td>187900.000000</td>
      <td>191433.333333</td>
      <td>195200.0</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 67 columns</p>
</div>




```python
def run_ttest():
    '''First creates new data showing the decline or growth of housing prices
    between the recession start and the recession bottom. Then runs a ttest
    comparing the university town values to the non-university towns values, 
    return whether the alternative hypothesis (that the two groups are the same)
    is true or not as well as the p-value of the confidence. 
    
    Return the tuple (different, p, better) where different=True if the t-test is
    True at a p<0.01 (we reject the null hypothesis), or different=False if 
    otherwise (we cannot reject the null hypothesis). The variable p should
    be equal to the exact p value returned from scipy.stats.ttest_ind(). The
    value for better should be either "university town" or "non-university town"
    depending on which has a lower mean price ratio (which is equivilent to a
    reduced market loss).'''
    import pandas as pd
    import numpy as np
    from scipy import stats
    utownlist = get_list_of_university_towns().set_index(['State','RegionName'])
    bottom = get_recession_bottom()
    start = get_recession_start()
    df = convert_housing_data_to_quarters()[[start,bottom]].dropna()
    utowndf = pd.merge(df,utownlist, how='inner', left_index=True, right_index=True)
    merged = pd.merge(df,utownlist, how='outer', left_index=True, right_index=True, indicator=True)
    notudf= merged[merged['_merge'] == 'left_only'][[start,bottom]]
    tteststats=stats.ttest_ind(utowndf[start].div(utowndf[bottom]), notudf[start].div(notudf[bottom]))
    p=tteststats[1]
    if tteststats[1]<0.01: different=True
    else: different=False
    if ((utowndf[start].div(utowndf[bottom])).mean()>(notudf[start].div(notudf[bottom])).mean()): 
        better='non-university town'
    elif ((utowndf[start].div(utowndf[bottom])).mean()<(notudf[start].div(notudf[bottom])).mean()): 
        better='university town'
    return (different,p,better)
run_ttest()
```




    (True, 0.005496427353694603, 'university town')




```python

```
