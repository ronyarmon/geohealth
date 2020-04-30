# Prepare geo-location data
import pandas as pd
import string
import re
import math

geo_path='../data/raw_data/geo/'
def merc(lat,lon):
    """Calcaulate mecarator projections per lattitude/longitude coordinates
    Source: https://bit.ly/2DqW3S7"""
    r_major = 6378137.000
    x = r_major * math.radians(lon)
    scale = x/lon
    y = 180.0/math.pi * math.log(math.tan(math.pi/4.0 +
        lat * (math.pi/180.0)/2.0)) * scale
    return (x, y)

location=pd.read_csv(geo_path+'GPs_locations_Eng.csv')
location.rename(columns = {'Practice Name':'Practice','Practice Code':'Practice_Code'}, inplace = True)
del location ['Unnamed: 0']
regional=pd.read_csv(geo_path+'GPs_CCGs_NHS_Regions.csv')
regional.rename(columns = {'Practice code':'Practice_Code','Region name':'Region_name' }, inplace = True)

location_region=pd.merge (location,regional)

# Calculate and load geo-projections
latitudemerc=[]
longitudemerc=[]
for index, row in location_region.iterrows():
    latitude,longitude=merc (row ['latitude'], row ['longitude'])
    latitudemerc.append (latitude)
    longitudemerc.append (longitude)

# Combine geo-projections with prevalence data
location_region['latitudemerc']=latitudemerc
location_region['longitudemerc']=longitudemerc

del location_region['Practice name']

headers=location_region.columns
headers=[('_'.join(h.split(' '))) for h in location_region.columns]
headers=[string.capwords(h) for h in headers]
headers=[re.sub('Ccg','CCG',h) for h in headers]
headers=[re.sub('_name','',h) for h in headers]
headers[3]='Status'
location_region.columns=headers

location_region=location_region[['Practice','Status','Postcode', 'CCG', 'Region','Sub-region',\
     'Practice_code','CCG_geography_code','Region_geography_code', 'Sub-region_geography_code',\
    'Latitude', 'Longitude','Easting', 'Northing', 'Latitudemerc','Longitudemerc']]
#location_region.columns=location_region[headers]

capitalize_headers=['Practice','CCG','Region','Sub-region']
for header in capitalize_headers:
    location_region[header]=location_region[header]\
    .apply(lambda x:re.sub('NHS | CCG','',x))\
    .apply(lambda x:re.sub(' AND ',' & ',x))\
    .apply(lambda x:string.capwords(x))

capitalize_headers=['Practice','CCG','Region','Sub-region']
for header in capitalize_headers:
    location_region[header]=location_region[header]\
    .apply(lambda x:re.sub('NHS | CCG','',x))\
    .apply(lambda x:re.sub(' AND ',' & ',x))\
    .apply(lambda x:string.capwords(x))
location_region['CCG']=['Hartlepool & Stockton-on-Tees' if h == 'Hartlepool & Stockton-on-tees' else h\
                       for h in location_region['CCG']]
location_region['CCG']=['Stockton-on-Trent' if h == 'Stoke On Trent' else h\
                       for h in location_region['CCG']]
location_region['CCG']=[re.sub(' Of ',' of ', c) for c in location_region['CCG']]
location_region['Region']=[re.sub(' Of ',' of ', c) for c in location_region['Region']]
location_region['Sub-region']=['{t0}: {t1}'.format(t0=h.split(' ')[0],t1=re.sub(h.split(' ')[0]+' ','',h))\
       for h in location_region['Sub-region']]

location_region.to_csv('../location_data.csv',index=False)

# Clean commas
file_path='/Users/rony/Projects/GeoHealth_Dev/data/location_data.csv'
df=pd.read_csv('../location_data.csv')
headers=list(df.columns)
print (len(df))
for header in headers:
    if type (header[0])==str:
        print (header)
        items=list(df[header])
        items=[re.sub(', ','_',str(i)) for i in items]
        items=[re.sub(',','',str(i)) for i in items]
        print (len (items))
        df[header]=items

results_path = '../location_data_no_commas.csv'
df.to_csv(results_path,index=False)
