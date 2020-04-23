def get_tables(df,features):
    table_names=[]
    for feature in features:
        year = df.loc[feature,'year']
        month = df.loc[feature,'month']
        if feature in ['prevalence','deprivation']:
            table_name='{f}_{y}'.format(f=feature,y=year)
        elif feature in ['gender','age_groups']:
            feature='gender_age'
            table_name='{f}_{y}{m}'.format(f=feature,m=month,y=year)
        else:
            table_name='{f}_{y}{m}'.format(f=feature,m=month,y=year)
        table_names.append(table_name)
    return table_names

def check_errors (df,features):

    error = False
    comment = ''

    # Assert the selection of no more than 2 values (apart from gender)
    dfvalues = df[df.index.isin (['gender','age_groups'])]
    if len (dfvalues)==1:
        features_count = len (df)
    else:
        features_count = len (df) -1

    if features_count >2:
        error = True
        comment = 'Please select upto two features to show on the plot and run again'

    if error == False:
        # Assert the selection of month if gender, age, or prescribing were selected as features
        dfvalues = df[df.index.isin (['prescribing','gender','age_groups'])]
        month_values = list (df ['month'])
        month_values = [i for i in month_values if i != '   ']
        if not month_values:
            error = True
            comment = 'Please select month and run again'

        if error == False:
            # Assert availability of the value selected for the selected feature and period
            import psycopg2
            import pandas as pd
            import time
            conn = psycopg2.connect(
                    database="postgres",
                    user="dashboard_user",
                    password="healthgeo2020",
                    host="prescribinguk.czm1h03t4mrp.eu-central-1.rds.amazonaws.com",
                    port= '5432'
                    )
            cur = conn.cursor()


            start = time.time()
            for feature in features:
                values = df.loc[feature,'value']
                value_header = df.loc[feature,'value_header']
                table = df.loc[feature,'table']
                month,year = df.loc[feature,'month'],df.loc[feature,'year']

                if feature == 'prescribing':
                    bnf_sections = []
                    for item in values:
                        bnf_section = '^{i}'.format(i=item.split(':')[0])
                        bnf_sections.append (bnf_section)
                    valuesl = ('|').join (bnf_sections)

                    statement = "SELECT DISTINCT regexp_matches({vh},'{v}') FROM {t}"\
                    .format(vh=value_header,v=valuesl,t=table)
                    valuesl = [str(value.lstrip('^')) for value in valuesl.split('|')]
                    cur.execute(statement)
                    distinct_values = cur.fetchall()
                    distinct_values=[dv[0][0] for dv in distinct_values]

                else:
                    statement="SELECT DISTINCT {vh} FROM {t}".format (vh=value_header,t=table)
                    valuesl = list (values)
                    cur.execute(statement)
                    distinct_values = cur.fetchall()
                    distinct_values=[dv[0] for dv in distinct_values]



                for value in valuesl:

                    if value not in distinct_values:
                        error = True
                        comment = '{v} not found in the data for {f} in {m} {y}'.\
                              format (v=value,f=feature.capitalize(),m=month,y=year)

                        break
    return (error, comment)

def get_title(df):
    import re
    selected_features = set (df.index)
    gender_age = {'gender','age_groups'}
    ga_selected_intersect = gender_age.intersection(selected_features)==gender_age
    selected_features = list (selected_features)
    features_titles = {}
    print ('title created')
    for index, feature in enumerate (selected_features):
        measure = df.loc [feature, 'measure_header']
        val = df.loc [feature, 'value']
        feature_title = '{f}, {v}, {me}'.\
        format(f=feature.capitalize(), me= measure.capitalize(), v=val)
        feature_title = re.sub ("\(|\)|'",'',feature_title)
        feature_title = re.sub (",,",',',feature_title)
        print ('feature_title:',feature_title)
        features_titles[feature] = feature_title

    if ga_selected_intersect:
        ge = features_titles['gender'].split(', ')
        ag = features_titles ['age_groups'].split(', ')
        ge_ag = 'Gender and Age, {vg}, {va}, {me}'.format (vg=ge[1], va=ag[1], me = ge[2])
        del features_titles['gender']
        del features_titles ['age_groups']
        print ('ga feature_title:',ge_ag)
        features_titles ['gender_age_groups'] = ge_ag

    # add mark
    marks=['Color','Size']
    marks_feature_titles=[]
    print ('list(features_titles.keys()):',list(features_titles.keys()))
    for index, title in enumerate (list(features_titles.keys())):
        print (title)
        mark = marks [index]
        print (mark)
        feature_title = '{mark}: {ft}'.format(mark = mark, ft = features_titles[title].rstrip(','))
        print (feature_title)
        print ('----')
        marks_feature_titles.append (feature_title)

    title = ('\n').join(marks_feature_titles)

    return title
