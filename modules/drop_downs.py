import re
import ipywidgets as widgets
from ipywidgets import interact, interactive, fixed, Layout, HBox, VBox

# Drop down values
lists_dir='/Users/rony/Projects/Health_Geo_app/lists/'
bnf_codes=open('{ld}bnf_codes_sections.txt'.format(ld=lists_dir)).read().split('\n')[:-1]
age_groups=open('{ld}age_groups.txt'.format(ld=lists_dir)).read().split('\n')[:-1]
age_groups=[re.sub('-','_',i) for i in age_groups]
deprivation_indices=open('{ld}deprivation_indices.txt'.format(ld=lists_dir)).read().split('\n')[:-1]
deprivation_indices=[re.sub(' ','_',i) for i in deprivation_indices]
months=['Ignore','01','02','03','04','05','06','07','08','09','10','11','12']
years=['Ignore','2018','2019']

prevalence_indications=open('{ld}prevalence_indications.txt'.format(ld=lists_dir)).read().split('\n')[:-1]
prevalence_indications=[re.sub('-','_',i) for i in prevalence_indications]

gender=['Ignore','FEMALE','MALE']
deprivation_measures=['Ignore','rank','decile']
prescribing_measures=['Ignore','quantity','items','nic','act_cost']
prevalence_measures=['Ignore','register','prevalence']

# Selection widgets
default='Ignore'
style = {'description_width': 'initial'}

bnf_code_dd=widgets.Dropdown(options=bnf_codes,value=default,
    description='BNF Code:',style=style)
prescribing_measures_dd=widgets.Dropdown(options=prescribing_measures,value=default,
    description='Prescribing Measure:',style=style)
months_dd=widgets.Dropdown(options=months,value=default,
    description='Month:',style=style)
years_dd=widgets.Dropdown(options=years,value=default,
    description='   Year:',style=style)

prevalence_indications_dd=widgets.Dropdown(options=prevalence_indications,value=default,
    description='Prevalence indicator:',style=style)
prevalence_measures_dd=widgets.Dropdown(options=prevalence_measures,value=default,
    description=' Prevalence Measure:',style=style)
gender_dd=widgets.Dropdown(options=gender,value=default,
    description='Gender:')
age_groups_dd=widgets.SelectMultiple(options=age_groups,value=(default,'0_4'),
    description='Age Group:',style=style)
deprivation_dd=widgets.Dropdown(options=deprivation_indices,value=default,
    description='Deprivation Index:',style=style)
deprivation_measures_dd=widgets.Dropdown(options=deprivation_measures,value=default,
    description='Deprivation Measure:',style=style)

button = widgets.Button(description="Query and Plot") #,layout=Layout(width='100%', height='40px'))

prescribing_tab = VBox(children=[HBox(children=[bnf_code_dd,prescribing_measures_dd]),
                                 HBox(children=[months_dd,years_dd]),])

prevalence_tab = VBox(children=[prevalence_indications_dd,prevalence_measures_dd])
age_gender_tab = VBox(children=[age_groups_dd,gender_dd])
deprivation_tab= VBox(children=[deprivation_dd,deprivation_measures_dd])

tab = widgets.Tab(children=[prescribing_tab,prevalence_tab, age_gender_tab,deprivation_tab])
tab.set_title(0, 'Prescribing')
tab.set_title(1, 'Prevalence')
tab.set_title(2, 'Age and Gender')
tab.set_title(3, 'Deprivation')
