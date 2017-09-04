#Machine learning project: cleans up multivariate data, appends geographic reference, restricting to 7 variables, formats, get dummies for text data, more cleaning up, and trains a gradient boosting classifer, test on test data.
import pandas as pd
import numpy as np

def blight_model():
    from sklearn.ensemble import GradientBoostingClassifier
    train_df=pd.read_csv('train.csv', encoding = 'ISO-8859-1' ).set_index('ticket_id')
    test_df=pd.read_csv('test.csv', encoding = 'ISO-8859-1' ).set_index('ticket_id')
    #removing fields not available in test data
    drop_these=['payment_amount','payment_status', 'balance_due', 'agency_name', 'inspector_name',
                'payment_date','collection_status','compliance_detail']
    train_df=train_df.drop(drop_these, axis=1)
    #merging with geo coordinates
    addresses_df=pd.read_csv('addresses.csv')
    latlons_df=pd.read_csv('latlons.csv')
    lladd_df=addresses_df.merge(latlons_df, how='left', left_on='address', right_on='address').drop('address',axis=1)
    train_df=train_df.merge(lladd_df, how='left', left_index=True, right_on='ticket_id').set_index('ticket_id')
    train_df=train_df[(train_df['compliance']==1.0)|(train_df['compliance']==0.0)]
    test_df=test_df.merge(lladd_df, how='left', left_index=True, right_on='ticket_id').set_index('ticket_id')
    #using X_test[X_test['lat'].isnull()].index, test_df['zip_code'] and google map to fill in NaN.
    missing_coords=[(317124, 42.520195, -83.264904), (329689, 42.495269, -83.289801),
                    (329393, 43.622624, -84.832194), (333990, 42.367620, -83.143220),
                    (367165, 42.349607, -83.060984)]
    for mindex,mlat,mlon in missing_coords:
        test_df.set_value(mindex,'lat',mlat)
        test_df.set_value(mindex,'lon',mlon)
    #keeping selected fields for casual relevance
    keep_these_train=['violation_code','fine_amount','disposition','country',
                'grafitti_status','lat','lon','compliance']
    keep_these_test=keep_these_train.copy()
    keep_these_test.remove('compliance')
    cleaned_train_df=pd.get_dummies(train_df[keep_these_train]).dropna()
    X_train_pre=cleaned_train_df.drop('compliance', axis=1)
    #converting text fields to dummies, loops to remove non-overlaps in test and train data
    X_test_pre=pd.get_dummies(test_df[keep_these_test])
    bucket_train=X_train_pre.columns.tolist()
    bucket_test=X_test_pre.columns.tolist()
    for x in X_test_pre.columns.tolist():
        try: bucket_train.remove(x)
        except: continue
    for x in X_train_pre.columns.tolist():
        try: bucket_test.remove(x)
        except: continue
    X_test=X_test_pre.drop(bucket_test, axis=1)#.dropna()
    X_train=X_train_pre.drop(bucket_train, axis=1)
    y_train=cleaned_train_df['compliance']
    clf = GradientBoostingClassifier(random_state = 0)
    y_proba=clf.fit(X_train, y_train).predict_proba(X_test)
    y_proba=clf.predict_proba(X_test)
    X_test_copy=X_test.copy()
    X_test_copy['compliance']=y_proba[:,1]
    return X_test_copy['compliance']
blight_model()




#Subplots investigating effect of christmas day on stock price movements on various stock indices
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

%matplotlib notebook

stockindices=[('^AORD.csv','Australia (All Ordinaries)'),('^GSPC.csv','USA (S&P 500)'),
              ('^N100.csv', 'Europe (Euronext 100)'),('^HSI.csv','Hong Kong (Hang Seng)'),
              ('^NSEI.csv','India (NIFTY 50)')]

#loads, manipulates the data, consolidate in combined dataframe
x=0
for file, title in stockindices:
    df = pd.read_csv(file)
    #extract the month and date from string without the "-"
    df['md']=df['Date'].apply(lambda x: int(x[5:7]+x[8:10]))
    #extract just the december date range in question
    df=df[((df['md']>1215)&(df['md']<1231)&(df['Low']!=df['High']))]
    df['Change']=(df['Close'].astype(float)-df['Open'].astype(float)).div(df['Open'].astype(float))*100
    df['d']=df['md']-1200
    df['y']=df['Date'].apply(lambda x: int(x[:4]))
    df=df.set_index(['y','d'])
    df = df[['Change']].unstack(level=-1).reset_index()
    df['Market']=title
    if x==0:
        combined=df
        x+=1
    elif x==1:
        combined=combined.append(df)
        
#cleans up data abit
del combined['y']
combined = combined.groupby('Market').agg(np.mean).T.reset_index().set_index('d')
del combined['level_0']
combined=combined.T
#adds christmas day
combined[25]=np.nan
#shrinking the data into just the period around christmas
combined=combined[list(range(16,31))].T


#defines a 6x1 space
fig = plt.figure()
gspec = gridspec.GridSpec(6, 1)

#for the bottom subplot
bottom = fig.add_subplot(gspec[5,:])
combinedall=combined.T.apply(lambda x: np.mean(x))
bottom.plot(combinedall, color='gray')
bottom.axhline(0, color='black')
bottom.set_ylim((-.25,.25))
bottom.set_xlim((16,30))
plt.gca().fill_between(range(24,27), -.3, .6,
                       facecolor='gray', 
                       alpha=0.1)
plt.tick_params(top='off', bottom='on', left='off', right='off', labelleft='off', labelbottom='on')
bottom.set_xlabel('Day')
bottom.set_ylabel('All')

#top subplot
top = fig.add_subplot(gspec[:5,:])
#workabout to set color, since direct in plot not working
top.set_prop_cycle('color', [(.673,0,.327),(.7518,0,.2482),
                                    (.14,.43,.43),(.025,0,.975),(.784,.216,0)])
top.plot(combined)
#combined.plot(gspec[:5,:],color=[(.673,0,.327),(.7518,0,.2482),(.14,.43,.43),(.025,0,.975),(.784,.216,0)])
plt.ylabel('Average Stock Movement (%)')
plt.gca().fill_between(range(24,27), -.3, .6,
                       facecolor='gray', 
                       alpha=0.1)
plt.tick_params(top='off', bottom='off', left='on', right='off', labelleft='on', labelbottom='off')
#plt.grid(True)
top.axhline(0, color='black')
top.set_ylim((-.3,.6))
top.set_xlim((16,30))
plt.title('Averaged Historical Stock Index \nMovements Around Christmas Period', alpha=0.8)

#workabout legend, because passing the dataframe into subplot interferes with the plot
st=['Australia (All Ordinaries)','Europe (Euronext 100)',
    'Hong Kong (Hang Seng)','India (NIFTY 50)','USA (S&P 500)']
plt.legend(st,loc= 'upper left', fontsize= 7);




#Interactive visual
%matplotlib notebook
import matplotlib.pyplot as plt

#plt.figure()
dfmean = np.mean(df2, axis=1)
dfstd = np.std(df2, axis=1)
colors=[]

# Value of interest
y=70000

# Bar color conditions
for x in df.index:
    if y>(dfmean.loc[x]+2.5*dfstd.loc[x]): colors.append('darkblue')
    elif y>(dfmean.loc[x]+1.5*dfstd.loc[x]): colors.append('blue') 
    elif y>(dfmean.loc[x]+0.5*dfstd.loc[x]): colors.append('lightblue')   
    elif y>(dfmean.loc[x]-0.5*dfstd.loc[x]): colors.append('silver')    
    elif y>(dfmean.loc[x]-1.5*dfstd.loc[x]): colors.append('pink')
    elif y>(dfmean.loc[x]-2.5*dfstd.loc[x]): colors.append('red')
    else: colors.append('darkred')
plt.bar(list(df.index), list(dfmean), color=colors,yerr=list(dfstd), alpha=0.6)
plt.xticks(list(df.index))
plt.axhline(yvalue, color='gray')
plt.xlabel('Years')
plt.ylabel('Mean Value')
plt.title('Probabilistic Likelihood of Value- \n-in-Interest Within Year', alpha=0.8)
plt.legend(['Value of Interest: '+str(y)])


#Visualizing Melbourne's historical High-low temperatures, highlighting record temperatures for the year
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


import pandas as pd
import numpy as np
from scipy.stats import ttest_ind

# **Hypothesis**: University towns have their mean housing prices less effected by recessions.(`price_ratio=quarter_before_recession/recession_bottom`)

states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}

def get_list_of_university_towns():
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

def get_recession_start():
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

def get_recession_end():
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

def get_recession_bottom():
    import pandas as pd
    df=(pd.read_excel('gdplev.xls', index_col=None, skiprows=219)[['1999q4', 12323.3]]
    .rename(columns={'1999q4':'Period',12323.3:'realGDP'}))
    worst=(get_recession_start(), df.loc[df[df['Period']==get_recession_start()].index[0]]['realGDP'])
    for x in range(df[df['Period']==get_recession_start()].index[0], len(df)): 
        if df.loc[x]['realGDP'] < worst[1]: 
            worst=(df.loc[x]['Period'], df.loc[x]['realGDP'])
    return worst[0]
get_recession_bottom()

def convert_housing_data_to_quarters():
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

def run_ttest():
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


import pandas as pd
df = pd.read_csv('olympics.csv', index_col=0, skiprows=1)
for col in df.columns:
    if col[:2]=='01':
        df.rename(columns={col:'Gold'+col[4:]}, inplace=True)
    if col[:2]=='02':
        df.rename(columns={col:'Silver'+col[4:]}, inplace=True)
    if col[:2]=='03':
        df.rename(columns={col:'Bronze'+col[4:]}, inplace=True)
    if col[:1]=='№':
        df.rename(columns={col:'#'+col[1:]}, inplace=True)
names_ids = df.index.str.split('\s\(') # split the index by '('
df.index = names_ids.str[0] # the [0] element is the country name (new index) 
df['ID'] = names_ids.str[1].str[:3] # the [1] element is the abbreviation or ID (take first 3 characters from that)
df = df.drop('Totals')
df.head()

def answer_zero():
    return df.iloc[0]
answer_zero() 

def answer_one():
    return df[df['Gold'] == df['Gold'].max()].index[0]
answer_one()

def answer_two():
    diff = (df['Gold'] - df['Gold.1']).abs()
    return diff[(diff == diff.max())].index[0]
answer_two()

def answer_three():
    dfb = df[(df['Gold'] > 0) & (df['Gold.1'] > 0)]
    dfbf = ((dfb['Gold'] - dfb['Gold.1'])/dfb['Gold.2'])
    return dfbf[(dfbf == dfbf.abs().max())].index[0]
answer_three()

def answer_four(): 
    Points = df['Gold.2']*3 + df['Silver.2']*2 + df['Bronze.2']*1
    return Points
answer_four()

import pandas as pd
census_df = pd.read_csv('census.csv')
census_df.head()

def answer_five():
    state_df = pd.DataFrame()
    cdf = census_df[census_df['SUMLEV'] == 50]
    scdf = cdf.set_index(['STNAME'])
    state_df['State'] = cdf['STNAME'].unique()
    state_df['CountyCnt'] = 0
    state_df.set_index('State',inplace=True)
    for st in state_df.index:
        state_df.loc[st]['CountyCnt'] = len(scdf.loc[st])
    return state_df.where(state_df == state_df.max()).dropna().index[0]
answer_five()

def answer_six():
    census_df = pd.read_csv('census.csv')
    cen = census_df[census_df['SUMLEV'] == 50]
    cen_pop_sort = cen.sort_values(['STNAME', 'CENSUS2010POP'], ascending=[True, False]).set_index(["STNAME", "CTYNAME"])
    cen_pop_sort3 = cen_pop_sort.groupby(level=0, group_keys=False).apply(lambda x: x.nlargest(3, ['CENSUS2010POP']))
    cps3 = cen_pop_sort3.reset_index().set_index('STNAME')
    state_df = pd.DataFrame()
    cdf = census_df[census_df['SUMLEV'] == 50]
    scdf = cdf.set_index(['STNAME'])
    state_df['State'] = cdf['STNAME'].unique()
    state_df['C2010POP3'] = 0
    state_df.set_index('State',inplace=True)
    for st in state_df.index:
        try: state_df.loc[st]['C2010POP3'] = sum(cps3.loc[st]['CENSUS2010POP'])
        except: state_df.loc[st]['C2010POP3'] = cps3.loc[st]['CENSUS2010POP'] #Since bloody State of Columbia only has one row in.
    s3df = state_df.sort_values('C2010POP3', ascending=False)
    y = [s3df[:3].index[x] for x in range(0, len(s3df[:3].index))]
    return y
answer_six()

def answer_seven():
    cdf = census_df[census_df['SUMLEV'] == 50]
    scdf = cdf.set_index(['STNAME', 'CTYNAME'])
    cty_df = scdf.index
    a = []
    for x in range(2010,2016):
        for y in range(2010,2016):
            if not x == y:
                diff = scdf['POPESTIMATE'+str(x)] - scdf['POPESTIMATE'+str(y)]
                countyname = diff[(diff.abs() == diff.abs().max())].index[0]#[1]
                abschange = diff.abs().loc[diff[(diff.abs() == diff.abs().max())].index[0]]
                #print(countyname, abschange, x, y)
                a.append((abschange, countyname))
    a.sort()
    return a[-1][1][1]
answer_seven()     

def answer_eight():
    cdf = census_df[census_df['SUMLEV'] == 50]
    reg12 = cdf[((cdf['REGION'] == 1) | (cdf['REGION'] == 2))]
    reg12[(reg12['POPESTIMATE2015'] > reg12['POPESTIMATE2014'])]
    querry = reg12[(reg12['POPESTIMATE2015'] > reg12['POPESTIMATE2014'])][['STNAME', 'CTYNAME']]
    return querry[(querry['CTYNAME'] == 'Washington County')]
answer_eight()



import xml.etree.ElementTree as ET
import sqlite3
conn = sqlite3.connect('trackdb.sqlite')
cur = conn.cursor()
# Make some fresh tables using executescript()
cur.executescript('''
DROP TABLE IF EXISTS Artist;
DROP TABLE IF EXISTS Genre;
DROP TABLE IF EXISTS Album;
DROP TABLE IF EXISTS Track;
CREATE TABLE Artist (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);
CREATE TABLE Genre (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);
CREATE TABLE Album (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    artist_id  INTEGER,
    title   TEXT UNIQUE
);
CREATE TABLE Track (
    id  INTEGER NOT NULL PRIMARY KEY 
        AUTOINCREMENT UNIQUE,
    title TEXT  UNIQUE,
    album_id  INTEGER,
    genre_id  INTEGER,
    len INTEGER, rating INTEGER, count INTEGER
);
''')
fname = input('Enter file name: ')
if ( len(fname) < 1 ) : fname = 'Library.xml'
# <key>Track ID</key><integer>369</integer>
# <key>Name</key><string>Another One Bites The Dust</string>
# <key>Artist</key><string>Queen</string>
def lookup(d, key):
    found = False
    for child in d:
        if found : return child.text
        if child.tag == 'key' and child.text == key :
            found = True
    return None
stuff = ET.parse(fname)
all = stuff.findall('dict/dict/dict')
print('Dict count:', len(all))
for entry in all:
    if ( lookup(entry, 'Track ID') is None ) : continue
    name = lookup(entry, 'Name')
    genre = lookup(entry, 'Genre')
    artist = lookup(entry, 'Artist')
    album = lookup(entry, 'Album')
    count = lookup(entry, 'Play Count')
    rating = lookup(entry, 'Rating')
    length = lookup(entry, 'Total Time')
    if name is None or artist is None or genre is None or album is None : 
        continue
    print(name, artist, album, genre, count, rating, length)
    cur.execute('''INSERT OR IGNORE INTO Artist (name) 
        VALUES ( ? )''', ( artist, ) )
    cur.execute('SELECT id FROM Artist WHERE name = ? ', (artist, ))
    artist_id = cur.fetchone()[0]    
    cur.execute('''INSERT OR IGNORE INTO Genre (name) 
        VALUES ( ? )''', ( genre, ) )
    cur.execute('SELECT id FROM Genre WHERE name = ? ', (genre, ))
    genre_id = cur.fetchone()[0]
    cur.execute('''INSERT OR IGNORE INTO Album (title, artist_id) 
        VALUES ( ?, ? )''', ( album, artist_id ) )
    cur.execute('SELECT id FROM Album WHERE title = ? ', (album, ))
    album_id = cur.fetchone()[0]
    cur.execute('''INSERT OR REPLACE INTO Track
        (title, genre_id, album_id, len, rating, count) 
        VALUES ( ?, ?, ?, ?, ?, ? )''', 
        ( name, genre_id, album_id, length, rating, count ) )
    conn.commit()



import sqlite3
conn = sqlite3.connect('orgdb.sqlite')
cur = conn.cursor()
cur.execute('''
DROP TABLE IF EXISTS Counts''')
cur.execute('''
CREATE TABLE Counts (org TEXT, count INTEGER)''')
fname = input('Enter file name: ')
if (len(fname) < 1): fname = 'mbox.txt'
fh = open(fname)
for line in fh:
    if not line.startswith('From: '): continue
    pieces = line.split()
    email = pieces[1]#.split(@)[1]
    org = email.split('@')[1]
    cur.execute('SELECT count FROM Counts WHERE org = ? ', (org,))
    row = cur.fetchone()
    if row is None:
        cur.execute('''INSERT INTO Counts (org, count)
                VALUES (?, 1)''', (org,))
    else:
        cur.execute('UPDATE Counts SET count = count + 1 WHERE org = ?',
                    (org,))
conn.commit()
# https://www.sqlite.org/lang_select.html
sqlstr = 'SELECT org, count FROM Counts ORDER BY count DESC LIMIT 10'
for row in cur.execute(sqlstr):
    print(str(row[0]), row[1])
cur.close()



import urllib.request, urllib.parse, urllib.error
import json
serviceurl = 'http://py4e-data.dr-chuck.net/geojson'
address = input('Enter location: ')
if len(address) < 1: address = 'De Anza College' #break
url = serviceurl + '?' + urllib.parse.urlencode({'sensor':'false', 'address': address})
print('Retrieving', url)
uh = urllib.request.urlopen(url)
data = uh.read().decode()
print('Retrieved', len(data), 'characters')
try: js = json.loads(data)
except: js = None
if not js or 'status' not in js or js['status'] != 'OK':
    print('==== Failure To Retrieve ====')
    print(data)
print(js["results"][0]["place_id"])



import urllib.request, urllib.parse, urllib.error
import json
uh = urllib.request.urlopen('http://py4e-data.dr-chuck.net/comments_2774.json')
data = uh.read()
try: js = json.loads(data)
except: js = None
#print(json.dumps(js, indent=4))
list1=[]
for j in js['comments']:
    x = int(j['count'])
    list1 = list1 + [x]
print(sum(list1)) 



import urllib.request, urllib.parse, urllib.error
import  xml.etree.ElementTree as ET
url = input('Enter url ')
if len(url) < 1: url = 'http://py4e-data.dr-chuck.net/comments_2773.xml'
data = urllib.request.urlopen(url).read()
tree = ET.fromstring(data)
comments=tree.findall('.//comment')
list1=[]
for stuff in comments:
    x = int(stuff.find('count').text)
    list1 = list1 + [x]
print(sum(list1))



import urllib.request, urllib.parse, urllib.error
import re
from bs4 import BeautifulSoup
import ssl
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
url = input('Enter first url ')
counts = input('Enter no. of times: ')
pos = input('Enter position: ')
count = 0
if len(url) < 1: url = 'http://py4e-data.dr-chuck.net/known_by_Clement.html'
if len(counts) < 1: counts = 7
if len(pos) < 1: pos = 18
print(url)
while count < counts:
    html = urllib.request.urlopen(url, context=ctx).read()
    soup = BeautifulSoup(html, 'html.parser')
    list1=[]
    tags = soup('a')
    for tag in tags:
        x = str(tag.get('href', None))
        #y =(re.findall('.*by_([A-Za-z]+)', x))
        list1 = list1 + [x]
    url = list1[pos-1]
    count = count + 1
    print(url)
    
    
    
from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
url = input('Enter - ')
if len(url) < 1: url = 'http://py4e-data.dr-chuck.net/comments_2771.html'
html = urlopen(url, context=ctx).read()
soup = BeautifulSoup(html, "html.parser")
list1=[]
tags = soup('span')
for tag in tags:
    x = int(tag.contents[0])
    list1 = list1 + [x]
sum=sum(list1)
print(sum)
while count < counts:
    html = urllib.request.urlopen(url, context=ctx).read()
    soup = BeautifulSoup(html, 'html.parser')
    list1=[]
    tags = soup('a')
    for tag in tags:
        x = str(tag.get('href', None))
        #y =(re.findall('.*by_([A-Za-z]+)', x))
        list1 = list1 + [x]
    url = list1[pos-1]
    count = count + 1
    print(url)
    print(count)
    
    
    
import socket
mysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mysock.connect(('data.pr4e.org', 80))
cmd = 'GET http://data.pr4e.org/intro-short.txt HTTP/1.0\r\n\r\n'.encode()
mysock.send(cmd)
while True:
    data = mysock.recv(512)
    if (len(data) < 1):
        break
    print(data.decode())
mysock.close()



name = input("Enter file:")
if len(name) < 1 : name = "regex_sum_2769.txt"
handle = open(name)
list1 = []
import re
for line in handle:
    line=line.rstrip()
    x = re.findall('[0-9]+', line)
    if len(x)>0: 
        for y in x:
            y=int(y)
            list1 = list1 + [y]
sum=sum(list1)
print(sum)



name = input("Enter file:")
if len(name) < 1 : name = "mbox-short.txt"
handle = open(name)
basket = {}
for line in handle:
    if not line.startswith('From '):continue
    line=line.rstrip()
    words=line.split()
    word=words[5]
    hour=word[:2]
    basket[hour]=basket.get(hour,0)+1
list=basket.items()
for x,y in sorted(list): print(x,y)



name = input("Enter file:")
if len(name) < 1 : name = "mbox-short.txt"
bucket = dict()
handle = open(name)
for line in handle:
    line=line.rstrip()
    if not line.startswith('From '): continue
    subs=line.split()
    bucket[subs[1]] = bucket.get(subs[1],0) + 1
busybee = None
work = None
for k,v in bucket.items():
    if v is None or v > work:
        busybee = k
        work = v
print(busybee, work)
