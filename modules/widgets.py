import re
import ipywidgets as widgets
from ipywidgets import interact, interactive, fixed, Layout, HBox, VBox

default = ('ignore','   ')
style = {'description_width': 'initial'}
features_layout = {'width': 'max-content','height':'200px'}
age_groups_layout = {'width': '20px','height':'200px'}
measures_layout = {'width': 'max-content','height':'30px'}
lists_dir='./lists/'


''' Features '''
# Values
bnf_codes = list(default)+open('{ld}bnf_codes_sections.txt'.format(ld=lists_dir)).read().split('\n')[:-1]
prevalence_indications=['ignore']+open('{ld}prevalence_indications.txt'.format(ld=lists_dir)).read().split('\n')[:-1]
prevalence_indications=[re.sub('-','_',i) for i in prevalence_indications]
gender=list(default)+['FEMALE','MALE']
age_groups = list(default)+open('{ld}age_groups.txt'.format(ld=lists_dir)).read().split('\n')[:-1]
age_groups = [re.sub('-','_',i) for i in age_groups]
deprivation_indices = open('{ld}deprivation_indices.txt'.format(ld=lists_dir)).read().split('\n')[:-1]
deprivation_indices = ['ignore']+[re.sub(' ','_',i) for i in deprivation_indices]

# Drop Down menues
bnf_code_dd=widgets.SelectMultiple(options=bnf_codes,value=default,
    description='BNF Code:',style=style,layout=features_layout)
# prevalence_indications_dd=widgets.SelectMultiple(options=prevalence_indications,value=default,
#    description='Indicator:',style=style,layout=features_layout)

prevalence_indications_dd=widgets.Dropdown(options=prevalence_indications,value='ignore',
    description='Indicator:',style=style)#,layout=features_layout) # disabled=False,

age_groups_dd=widgets.SelectMultiple(options=age_groups,value=default,
    description='Age Group:',style=style ,layout=features_layout)
gender_dd=widgets.SelectMultiple(options=gender,value=default,
    description='Gender:',style=style,layout=features_layout)
deprivation_dd=widgets.Dropdown(options=deprivation_indices,value='ignore',
    description='Index:',style=style)


''' Measures '''
# Values
prescribing_measures=['quantity','items','nic','act_cost']
prevalence_measures=['register','prevalence']
gender_age_measures=['register','percentage']
deprivation_measures=['rank','decile']

# Drop Down menues
prescribing_measures_dd = widgets.Dropdown(options=prescribing_measures,value='quantity',
    description='  Measure:  ',style=style,layout=measures_layout)
prevalence_measures_dd=widgets.Dropdown(options=prevalence_measures,value='prevalence',
    description='  Measure:  ',style=style,layout=measures_layout)
gender_age_measures_dd=widgets.Dropdown(options=gender_age_measures,value='percentage',
    description='  Measure:  ',style=style,layout=measures_layout)
deprivation_measures_dd=widgets.Dropdown(options=deprivation_measures,value='decile',
    description='  Measure:  ',style=style,layout=measures_layout)

''' Period '''
# Values
months = ['   ','01','02','03','04','05','06','07','08','09','10','11','12']
years = ['2019','2018','2017','2016','2015','2014']

# Drop Down menues
month_dd=widgets.Dropdown(options=months,value='   ',
    description='Month:',style=style)
year_dd=widgets.Dropdown(options=years,value='2019',
    description='Year:',style=style)

# General choice menus
outliers_choice = widgets.RadioButtons(options=['Remove', 'Keep'],value = 'Remove', description='Ouliers:',style=style)
download_choice = widgets.RadioButtons(options=['CSV','Excel','None'],value = 'CSV', description='Download:',style=style)
output_choice = widgets.RadioButtons(options=['HTML File','Notebook'],value = 'HTML File', description='Output:',style=style)

button = widgets.Button(description = "Run",style=style)
button.style.button_color = 'lightgreen'

prescribing_tab = HBox(children=[bnf_code_dd,prescribing_measures_dd])
prevalence_tab = HBox(children=[prevalence_indications_dd,prevalence_measures_dd])
age_gender_tab = HBox(children=[age_groups_dd,gender_dd,gender_age_measures_dd])
deprivation_tab= HBox(children=[deprivation_dd,deprivation_measures_dd])

tabs = widgets.Tab(children=[prescribing_tab,prevalence_tab, age_gender_tab,deprivation_tab])
tabs.set_title(0, 'Prescribing')
tabs.set_title(1, 'Prevalence')
tabs.set_title(2, 'Age and Gender')
tabs.set_title(3, 'Deprivation')

button_date_box=HBox(children=[month_dd,year_dd,outliers_choice,download_choice,output_choice,button])
