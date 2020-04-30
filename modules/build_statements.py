class statement:
    '''
    Build SQL statements for individual features
    '''

    def __init__(self,feature,df):
        self.value = df.loc[feature,'value']+('zzzzz',)
        self.table = df.loc[feature,'table']
        self.value_header = df.loc[feature,'value_header']
        self.measure_header = df.loc[feature,'measure_header']

    # Build the select column/table part of the statements
    def select (self,feature):
        statement_select="SELECT practice_code,sum({vm}) FROM {t}"\
                .format (vm=self.measure_header, t=self.table)
        return statement_select

    # Build the conditional selection part of the statement
    def where (self,feature):
        if feature == 'prescribing':
            statement_where = ''
        else:
            statement_where="WHERE {vh} in {v}".format(v=self.value,vh=self.value_header)
        return statement_where

    # Build the aggregation part of the statement    
    def groupby (self,feature):
        if feature == 'prescribing':
            bnf_sections = []
            for item in self.value:
                bnf_section = '^{i}'.format(i=item.split(':')[0])
                bnf_sections.append (bnf_section)
            bnf_sections = ('|').join (bnf_sections)
            statement_group_by = "GROUP BY practice_code,regexp_matches({vc},'{v}')"\
            .format(vc=self.value_header,v=bnf_sections)
        else:
            statement_group_by= "GROUP BY practice_code"
        return statement_group_by


class genderANDage_statement:

    '''
    Build query statements for queries combining both age and gender for the gender_age feature.
    '''

    def __init__(self,df):
        self.measure_header = df.loc['gender','measure_header']
        self.table = df.loc['gender','table']
        self.age_group_value = df.loc ['age_groups','value']+('zzzzz',)
        self.gender_value = df.loc ['gender','value']+('zzzzz',)
        self.age_group_value_header = df.loc ['age_groups','value_header']
        self.gender_value_header = df.loc ['gender','value_header']

    def build (self):
        built_statement="SELECT practice_code,sum ({vm}) FROM {t}\
                    WHERE {vc1} in {v1}\
                    AND {vc2} in {v2}\
                    Group by practice_code"\
                    .format (vm=self.measure_header, t=self.table,\
                             vc1=self.gender_value_header, v1=self.gender_value,\
                             vc2=self.age_group_value_header,v2 =self.age_group_value)

        return built_statement
