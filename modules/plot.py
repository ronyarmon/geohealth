import pandas as pd
import numpy as np
import re
import os
from bokeh.models import Circle, ColumnDataSource, ColorBar,HoverTool,\
Select, CustomJS,CustomJSFilter,CDSView,IndexFilter
from bokeh.plotting import figure, show, output_notebook,output_file
from bokeh.tile_providers import Vendors, get_provider
from bokeh.palettes import brewer, all_palettes, Spectral6, Inferno
from bokeh.transform import linear_cmap
from bokeh.layouts import column, gridplot
from bokeh.io import output_file, show
from bokeh.models import Dropdown, Panel
from bokeh.layouts import column, row, WidgetBox, layout

# lists of geo values
lists_dir_path='/Users/rony/Projects/Health_Geo_app/lists/'
ccgs,regions,sub_regions=[],[],[]
ccgs = open (lists_dir_path+'ccg.txt').read().split('\n')[:-1]
ccgs = ['All']+ccgs
regions = open (lists_dir_path+'region.txt').read().split('\n')[:-1]
regions = ['All']+regions
sub_regions = open (lists_dir_path+'sub_region.txt').read().split('\n')[:-1]
sub_regions = ['All']+sub_regions

def map_plot(data,title):
    full_source = ColumnDataSource(data) # a CDS version of the data obtained
    # a CDS version of the data to plot, modifiable by geo dropdowns, to be produced in the callback

    num_instances=len(data)
    ##print ('all instances count=',num_instances)

    geo_columns=['practice_code', 'practice', 'ccg', 'region','sub_region','longitudemerc','latitudemerc']
    value_columns=[h for h in data.columns if h not in geo_columns]
    #print ('values columns:',value_columns)
    first_value = value_columns[0]
    hover_first_value='@{fv}'.format (fv=first_value)

    if len (value_columns)==2:
        second_value = value_columns[1]
        sv_column=np.array(data[second_value])
        svinterp=np.interp(sv_column, (sv_column.min(), sv_column.max()), (0,10))
        norm_header=second_value+'_norm'
        data[norm_header]=svinterp

    source = ColumnDataSource(data)
    filter = IndexFilter(indices=list(data.index))
    view = CDSView(source=source, filters=[filter])

    plot = figure(x_axis_type="mercator", y_axis_type="mercator",
               plot_height=700, plot_width=700,
               title=title)
    tooltips=[('Practice', '@practice'), ('CCG', '@ccg'), (first_value.capitalize(),hover_first_value)]

    # Color bar
    if first_value=='deprivation':
        low_boundary,high_boundary = max (source.data[first_value]), min (source.data[first_value])
    else:
        high_boundary,low_boundary = max (source.data[first_value]), min (source.data[first_value])

    mapper = linear_cmap(field_name=first_value, palette=Spectral6,\
    low=low_boundary, high=high_boundary) #brewer['YlOrRd'][9]
    #add map tiles
    map_tile=get_provider(Vendors.CARTODBPOSITRON)
    plot.add_tile(map_tile)

    if len (value_columns)==2:
        hover_second_value='@{sv}'.format (sv=second_value)
        tooltips.append((second_value.capitalize(),hover_second_value))
        plot.circle(source=source, x='latitudemerc',y='longitudemerc',\
        hover_color='red', color=mapper,size=norm_header, alpha=0.4, view = view)

    else:
        plot.circle(source=source, view=view, x='latitudemerc',y='longitudemerc',\
        hover_color='red', color=mapper)


    #print ('tooltips:',tooltips)
    hover = HoverTool(tooltips = tooltips)

    color_bar = ColorBar(color_mapper=mapper['transform'], width=8,  location=(0,0))
    plot.add_layout(color_bar, 'right')
    plot.add_tools(hover)

    # Bojeh widgets using CustomJS
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

    select_ccg = Select(title='Clinical Commissioning Group', value=ccgs[0], options=ccgs)
    select_ccg.js_on_change('value', callback)
    select_region = Select(title='Region', value=regions [0], options=regions)
    select_region.js_on_change('value', callback)
    select_sub_region = Select(title='Sub-Region', value=sub_regions [0], options=sub_regions)
    select_sub_region.js_on_change('value', callback)

    view = CDSView(source=source, filters=[filter])

    output_notebook()

    #output_file('test.html')
    show(column(row(select_region,select_sub_region,select_ccg), plot))
