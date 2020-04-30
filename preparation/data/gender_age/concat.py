import pandas as pd
import numpy as np
from concurrent.futures import ProcessPoolExecutor
import re
import os
import time

import warnings
from pandas.core.common import SettingWithCopyWarning
warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)

def gender_age_percentage (df_name,df):
    df=df.rename(columns={'NUMBER_OF_PATIENTS':'register'})
    practices_ids=list(set(df['ORG_CODE']))
    print ('number of practices',len (practices_ids))
    new_headers=['ORG_CODE', 'SEX', 'AGE_GROUP_5', 'register','percentage','End_date']
    new_month_df=pd.DataFrame(columns=new_headers)
    for id in practices_ids:
        practice_df=df[df['ORG_CODE']==id]
        registers=list(practice_df['register'])
        percentages=[round ((100* register/sum(registers)),2) for register in registers]
        practice_df.loc[:,'percentage'] = percentages
        practice_df=practice_df[new_headers]
        new_month_df=pd.concat([new_month_df,practice_df])
        #print (df_name, len(new_month_df))
    return (df_name, new_month_df)

months_years=[]
# Data preparation
files_path='/Users/rony/Projects/Health_Geo_app/data/gender_age/'
file_names=[f for f in os.listdir(files_path) if (('2018' in f)|('2019' in f))]
months_dfs=[]
df_lens=0
for index,file_name in enumerate(file_names):
    if file_name != 'gender_age_2018-2019.csv':
        print ('file_name:',file_name)
        file_name='{fp}{fn}'.format(fp=files_path,fn=file_name)
        mydf = pd.read_csv(file_name)
        month_year=('').join(str(mydf['End_date'][0]).split('-')[0:2])
        months_years.append(month_year)
        df_lens += len (mydf)
        print (len(mydf),df_lens)
        months_dfs.append(mydf)
        print (30*'*')

print ('month years for names:',months_years)
months_years_names=['gender_age_{d}.csv'.format(d=my) for my in months_years]
print ('month years names:',months_years_names)

dfs_names=dict(zip(months_years_names,months_dfs))

print ('dfs_names:\n',dfs_names)

def controller():
    results_path='/Users/rony/Projects/Health_Geo_app/data/gender_age/with_percentages/'
    print ('Calculating percentages')
    clusters=[]
    executor=ProcessPoolExecutor(8)
    for result in executor.map(gender_age_percentage,dfs_names.keys(),dfs_names.values()):
        file_name,df = result[0],result[1]
        print ('calculated for',file_name)
        print (result[1].head())
        print (result[1].info())
        df.to_csv('{rp}{fn}'.format(rp=results_path,fn=file_name),index=False)
        print ('********')

    executor.shutdown()

if __name__=="__main__":
    controller ()
