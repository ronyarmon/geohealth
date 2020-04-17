#default='ignore'

def get_tables(df,features):
    #features_tables={}
    table_names=[]
    for feature in features:
        year = df.loc[feature,'year']
        month = df.loc[feature,'month']
        if month == '   ':
            month_year = '_{y}'.format(y = year)
        elif year=='not_selected':
            month_year = ''

        else:
            month_year='_{y}{m}'.format (m=month,y=year)

        if feature in ['gender','age_groups']:
            feature='gender_age'    
        table_name='{f}{my}'.format(f=feature,my=month_year)

        #features_tables[feature]=table_name
        table_names.append(table_name)

    return table_names

def query_format(df):
    comment=''
    features_count=4-list(df['value'].values).count(default)
    print ('features_count:',features_count)

    if features_count >2:
        comment = 'Please select no more than 2 features to plot'

    # prescribing and prevalence: value has measure
    if ((df.loc['prescribing','value']!=default) & (df.loc['prescribing','measure_header']==default))\
    | ((df.loc['prevalence','value']!=default) & (df.loc['prevalence','measure_header']==default)):
        comment = '\nPlease run again identifing a measure for the features selected.\n'

    # prescribing: value and measure has period
    if (  (df.loc['prescribing','value']!=default)
        & ((df.loc['prescribing','month']==default) | (df.loc['prescribing','year']==default))):
        comment = '\nPlease run again identifing a period for the prescribing measure selected.\n'

    return comment

def get_title(df):
    import re
    df=df.drop (['table'], axis=1)
    feature_rows=[]
    for feature in df.index:
        feature_row=list (df.loc[feature,:])
        feature_row=[str(i) for i in feature_row if i!='not_selected']
        if feature_row:
            feature_row1=(': ').join(feature_row)
            feature_rows.append(feature_row1)

    feature_rows=('\n').join(feature_rows)
    feature_rows = re.sub ('\(|\)','',feature_rows)
    feature_rows = re.sub (':\s{0}:',':',feature_rows)
    return feature_rows
