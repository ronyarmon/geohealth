def build_statements(features,measures,period):
    default='Ignore'
    features_default_count=list(features.values()).count(default)

    #print (bnf_code_dd,prescribing_measures_dd)
    if ((features['prescribing']!=default) & (measures['prescribing']==default))\
    | ((features['prevalence']!=default) & (measures['prevalence']==default)):
        print('You selected a prevalence feature without a measure.\
        Re-run to select both')

    elif features_default_count < 3:
        print ('Please select no more than 2 features to plot')

    # Collect the dd value (v) with the relevant measure (m) table (t) and column
    # headers for the value (vc) and measure (mc)
    else:
        statements={}

        # prescribing
        if features['prescribing']!=default:
            bnf_code=features['prescribing'].split(':')[0]

            if ((period['month']!=default)) & (period['year']!=default):
                table_name='t{y}{m}pdpi_bnft'.format(y=period['year'],m=period['month'])
            else:
                table_name='t201912pdpi_bnft'

            v,vc,vm,t=[bnf_code,'bnf_code',\
                       measures['prescribing'],\
                       table_name]
            statement="SELECT practice_code,sum({vm})\
                        FROM {t}\
                        group by practice_code,regexp_matches({vc},'^{v}')"\
                        .format(v=v,vc=vc,vm=vm,t=t)

            statements['bnf_code']=statement
            title='bnf_code: {m} {mo}/{ye}'\
                    .format(m=vm.capitalize(),mo=period['month'],ye=period['year'])


        # qof
        if features['prevalence']!=default:
            v,vc,vm,t=[features['prevalence'],'indication',\
                       measures['prevalence'],'prevalence_2018_2019']
            statement="SELECT practice_code,{vm} FROM {t}\
                        WHERE {vc}='{v}'".format(v=v,vc=vc,vm=vm,t=t)
            statements['qof']=statement
            title='{v}: {m}'.format(v=v,m=vm.capitalize())

        # gender
        if ((features['gender']!=default) & (features['age_groups']==(default,'0_4'))):
            v,vc,vm,t=[features['gender'],'sex','register','gender_age_2018_2019']
            statement="SELECT practice_code,{vc},{vm} FROM {t}\
                        WHERE {vc}='{v}'".format(v=v,vc=vc,vm=vm,t=t)
            statements['gender']=statement
            title='Gender: {v}'.format(v=v.upper())

        # age group
        if ((features['gender']==default) & (features['age_groups']!=(default,'0_4'))):
            v,vc,vm,t=[features['age_groups'],'age_group','register','gender_age_2018_2019']

            # Allowing multiple age groups selection
            statement="SELECT practice_code,sum({vm})\
                        FROM gender_age_2018_2019\
                        WHERE age_group in {v}\
                        Group by practice_code".format(v=v,vc=vc,vm=vm,t=t)
            statements['age_group']=statement
            title='Age Group: {v}'.format(v=v)

        # Gender and Age
        if ((features['gender']!=default) & (features['age_groups']!=default)):
            v1,v2,vc1,vc2,vm,t=[features['gender'],features['age_groups'],\
                                'sex','age_group','register',\
                                'gender_age_2018_2019']

            statement="SELECT practice_code,sum ({vm}) FROM {t}\
                        WHERE {vc1}='{v1}'\
                        AND {vc2} in {v2}\
                        Group by practice_code".format(v1=v1,v2=v2,vc1=vc1,vc2=vc2,vm=vm,t=t)
            statements['gender_age']=statement
            title='Gender: {v1} | Age Group: {v2}'.format(v1=v1.upper(),v2=v2)

        # Deprivation
        if features['deprivation']!=default:
            v,vc,vm,t=[features['deprivation'],'deprivation_index',\
                       measures['deprivation'],'deprivation_2019']
            statement="SELECT practice_code,{vm} FROM {t}\
                        WHERE {vc}='{v}'".format(v=v,vc=vc,vm=vm,t=t)
            statements['deprivation']=statement
            title='{v}: {m}'.format(v=v,m=vm.capitalize())

        # Locations data
        statement = "SELECT practice,practice_code,ccg,longitudemerc,latitudemerc\
                     FROM practices_locations"
        statements['location']=statement

        return statements,title
