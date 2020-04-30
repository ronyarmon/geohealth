import pandas as pd
import numpy as np
import re
import os
import sys
from bokeh.models import Circle, ColumnDataSource, ColorBar,HoverTool,\
Select, CustomJS,CustomJSFilter,CDSView,IndexFilter,Title
from bokeh.plotting import figure, show, output_notebook,output_file
from bokeh.tile_providers import Vendors, get_provider
from bokeh.palettes import brewer, all_palettes, Spectral6, Inferno
from bokeh.transform import linear_cmap
from bokeh.layouts import column, gridplot
from bokeh.io import output_file, show
from bokeh.models import Dropdown, Panel
from bokeh.layouts import column, row, WidgetBox, layout

# lists of geo values
lists_dir_path='./lists/'
ccgs,regions,sub_regions=[],[],[]
ccgs = open (lists_dir_path+'ccgs.txt').read().split('\n')[:-1]
ccgs = ['All']+ccgs
regions = open (lists_dir_path+'regions.txt').read().split('\n')[:-1]
regions = ['All']+regions
sub_regions = open (lists_dir_path+'sub_regions.txt').read().split('\n')[:-1]
sub_regions = ['All']+sub_regions
def map_plot(data,features_titles, output_choice_selection):
    full_source = ColumnDataSource(data) # a CDS version of the data obtained

    # a CDS version of the data to plot, modifiable by geo dropdowns, to be produced in the callback
    num_instances=len(data)

    # Split the columns with the values to plot to build their marks and title
    geo_columns=['practice_code', 'practice', 'ccg', 'region','sub_region','longitudemerc','latitudemerc']
    value_columns=[h for h in data.columns if h not in geo_columns]

    # Assert gender-age as the second value (to be marked by size)
    if value_columns[0] in ['gender','age_groups','gender_age_groups']:
        value_columns = list(reversed(value_columns))

    first_value = value_columns[0]
    features_marks = {first_value: 'Color'}
    hover_first_value='@{fv}'.format (fv=first_value)

    # Normalized size values for the second feature if such exists
    if len (value_columns)==2:
        second_value = value_columns[1]
        sv_column=np.array(data[second_value])
        svinterp = np.interp(sv_column, (sv_column.min(), sv_column.max()), (0,2000)) #was 10 for size
        if second_value == 'deprivation':
            svinterp = max (svinterp)-svinterp
        norm_header=second_value+'_norm'
        data[norm_header] = svinterp
        features_marks [second_value] = 'Size'


    source = ColumnDataSource(data)
    filter = IndexFilter(indices=list(data.index))
    view = CDSView(source=source, filters=[filter])
    plot = figure(x_axis_type="mercator", y_axis_type="mercator",plot_height=700, plot_width=700)
    plot.title.text_color = 'purple'
    tooltips=[('Practice', '@practice'), ('CCG', '@ccg'), (first_value.capitalize(),hover_first_value)]

    # Title
    title_parts = []
    for feature,title in features_titles.items():
        title_part = '  {m}: {t}'.format (m = features_marks[feature], t = title)
        title_parts.append(title_part)

    title_parts = list (reversed(title_parts))
    for title_part in title_parts:
        plot.add_layout(Title(text = title_part, text_font_size="10pt", text_color = 'purple'), 'above')

    # Color mapper
    palette = list(reversed (brewer['YlOrRd'][9]))
    if first_value=='deprivation':
        low_boundary,high_boundary = max (source.data[first_value]), min (source.data[first_value])
    else:
        high_boundary,low_boundary = max (source.data[first_value]), min (source.data[first_value])

    mapper = linear_cmap(field_name=first_value, palette=palette,\
    low=low_boundary, high=high_boundary) #Spectral6

    # add map tiles
    map_tile=get_provider(Vendors.CARTODBPOSITRON)
    plot.add_tile(map_tile)

    if len (value_columns)==2:
        hover_second_value='@{sv}'.format (sv=second_value)
        tooltips.append((second_value.capitalize(),hover_second_value))

        plot.circle(source=source, x='latitudemerc',y='longitudemerc',\
        hover_color='red', color=mapper,radius = norm_header, alpha=0.2,\
        view = view)
    else:
        plot.circle(source=source, view=view, x='latitudemerc',y='longitudemerc',\
        hover_color='red', color=mapper)

    hover = HoverTool(tooltips = tooltips)
    color_bar = ColorBar(color_mapper=mapper['transform'], width=8, location=(0,0))
    plot.add_layout(color_bar, 'right')
    plot.add_tools(hover)

    # Plot widgets selection callback
    callback = CustomJS(args=dict(source=source, filter=filter), code='''
      var indices = []
      var selected_value = cb_obj.value
      if (selected_value=='All') {
        indices = source.index
        console.log ('all ccgs selected')
      } else {
      console.log('The selected area is ' + selected_value)
      for (var i = 0; i < source.get_length(); i++) {
        // console.log(i, source.data['ccg'][i], cb_obj.value)
        if ((source.data['ccg'][i] == selected_value) || (source.data['region'][i] == selected_value)\
        ||  (source.data['sub_region'][i] == selected_value)) {
          indices.push(i)
             }
            }
          }
      filter.indices = indices
      source.change.emit()
    ''')

    select_ccg = Select(title='CCG', value=ccgs[0], options=ccgs, width=120)
    select_ccg.js_on_change('value', callback)
    select_region = Select(title='Region', value=regions [0], options=regions, width=120)
    select_region.js_on_change('value', callback)
    select_sub_region = Select(title='Sub-Region', value=sub_regions [0], options=sub_regions, width=120)
    select_sub_region.js_on_change('value', callback)
    view = CDSView(source=source, filters=[filter])

    if output_choice_selection == 'Notebook':
        output_notebook()
    elif output_choice_selection == 'HTML File':
        output_file('plot.html')
    show(row (column(select_region,select_sub_region,select_ccg), plot))
