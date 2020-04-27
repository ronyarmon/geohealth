# GeoHealth #

[GeoHealth](https://medium.com/@rony_armon/geohealth-a-unified-dashboard-for-medical-and-social-data-d33a03b94c2e) is a model for a public health dashboard set up for the purpose of presenting and connecting medical and social data from diverse sources. The current version is focused on England using public health and socio-demographic information available at the level of General Practice from around 8,000 surgeries. Their datasets, which were collected and prepared as part of this project, can be queried to produce a geo-spatial representation of the prevalence of diseases, risk factors and social deprivation on the national, regional and local levels.

The following features are available for exploration:
1. Practice level prescribing data
2. The prevalence of a selection of chronic conditions as reported in each practice.
3. The number and percentage of patients from each gender or age-group.
4. Social deprivation indices ranking each practice by its regional characteristics.

See info/measures_and_features.xlsx for a detailed explanation of the feature and the measures available to query and map for each.

## Licenses
Code: MIT licence (attached)  
Data: [Open Government Licence](http://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/)

## Installation
1. Set up the run time environment by installing [Anaconda](https://docs.anaconda.com/anaconda/install/) or standalone [Python](https://www.python.org/downloads/) followed by the installation of [Jupyter Notebooks](https://jupyter.org/install).
2. Set up a directory for the project.
3. Navigate to the directory and clone this repository:  
git clone https://github.com/ronyarmon/geo_health.git
4. Install the projects' dependencies:   
pip install -r requirements.txt
5. Open a Jupyter notebook from Anaconda Navigator or open a terminal and run (terminal):  
jupyter notebook
6. The notebook should start in a tab on your default browser, showing your directory tree. Navigate to the project's directory and click on main.ipynb holding the dashboard code.

## Query and Plot
1. Run the dashboard using the following meun bar options:  
Kernel->Restart & Clean Output
Cell -> Run All
2. Select 1-2 features to query and for each use the suitable menu to select the value and measure of interest.
3. Prescribing data: Each treatment is encoded using the [therapeutic classifications](https://digital.nhs.uk/data-and-information/areas-of-interest/prescribing/practice-level-prescribing-in-england-a-summary/practice-level-prescribing-glossary-of-terms) defined in the British National Formulary (BNF), a reference book containing the information on the indications, dosages and side effects for over 70,000 medicines. The code is composed of 15 characters with the first 6 encoding the treatment in three levels called chapter, section and paragraph. For example, the “Antidiabetic Drugs” paragraph (02) is nested under “Drugs Used In Diabetes” section (01) which is part of the “Endocrine System” chapter (06). The user can access the measures for treatments at the level of section and chapter thus exploring prescribing, or related morbidities, in these levels of granularity. **The main caveat for this feature is that as a result of their large size (~ 10 million rows and 1GB of data) their queries take between 40-60 seconds to complete.**   
4. Select the period of interest. Selection of month is obligatory for Prescribing and for Gender and Age as they use monthly datasets. Queries for Prevalence and Deprivation will include year but ignore the month. For example, a combination of Gender Age and Prevalence search for 04/2019 will provide a plot using the 04/2019 data for Gender Age and the 2019 for Prevalence. For deprivation, the data for 2015 will be used for 2014 queries and the years 2016,2017,2018 will retrieve the data for 2019.
5. Select whether to keep or remove outliers in the data. Outliers are calculated following [Tukey’s rule] (https://math.stackexchange.com/questions/966331/why-john-tukey-set-1-5-iqr-to-detect-outliers-instead-of-1-or-2) as any point that is than 1.5 interquartile range below the first quartile or above the third quartile. The default and recommended option is to remove the outliers as they tend to mask the variation in normal values in the plot. The user gets a report of the percentage of outliers per feature and their removal is recommended due to their influence on the range of values and the intensities of the data points shown.
6. The data is available in a csv or excel file. If you need the files for consecutive queries rename the file as it will be over-written by the next query.
You can join the results of subsequent queries on the practice_code column.
7. The plot can be delivered to the notebook (Output = Notebook) or to be saved and opened in a different tab (Output = HTML file).
8. Click run and look out for error messages or the expected plot and files.
9. You can use the dropdown menus and sidebar to drill-down to the levels of region, sub-region and Clinical Commissioning Group and use the side to zoom in or enlarge specific areas. Before changing locations in the dropdown menu it is recommended to select 'All' to return to the general map.

## Development
The code is available to support data exploration, connect to additional data source, and develop user interfaces if desired. The modular architecture of the package should allow analysts, developers and data scientists to query of the data using their favourite BI software, build statistical and machine learning models, add datasets and selection menus, adapt the dashboard to data from other countries or improve the user interface.

## Architecture
The dashboard is written in Python (3.7.4) using the [ipywidgets](https://ipywidgets.readthedocs.io/en/latest/) and [bokeh](https://docs.bokeh.org/en/latest/index.html) libraries for data visualization and user interactions. The data is held in a PostgreSQL database hosted on AWS in a private account that is kept open with a read-only access to all users. Though not available as a web application, the dashboard can be downloaded and run in a Jupyter Notebook which is a convenient research environment for data science. The code for main.ipynb is available in the notebook though you may need to click the "toggle on/off" at the bottom to see the code. The functions and classes for the widgets, query execution and plotting are available in the modules directory. The value for the widgets' menus are stored in the list folder.
