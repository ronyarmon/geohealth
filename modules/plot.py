import pandas as pd
import numpy as np
import re
import os
from bokeh.models import ColumnDataSource, ColorBar
from bokeh.plotting import figure, show, output_notebook,output_file
from bokeh.tile_providers import Vendors, get_provider
from bokeh.models import HoverTool, Select, CheckboxGroup,WidgetBox
from bokeh.palettes import Spectral6
from bokeh.transform import linear_cmap
from bokeh.layouts import column
from bokeh.layouts import gridplot

def map_plot(data,title):
    source=ColumnDataSource(data)
    geo_columns=['practice_code', 'practice', 'ccg', 'longitudemerc','latitudemerc']
    value_columns=[h for h in data.columns if h not in geo_columns]
    first_value=value_columns[0]
    hover_value='@{fv}'.format (fv=first_value)

    print (first_value,hover_value)

    plot = figure(x_axis_type="mercator", y_axis_type="mercator",
               plot_height=700, plot_width=700,
               title=title)

    hover = HoverTool(tooltips=[('Practice', '@practice'), ('CCG', '@ccg'), ('Value',hover_value)]) #define hover tooltip
    plot.add_tools(hover)

    #Color mapping
    if first_value=='deprivation':
        mapper = linear_cmap(field_name=first_value, palette=Spectral6,low=max (source.data[first_value])\
                             ,high=min (source.data[first_value]))
    else:
        mapper = linear_cmap(field_name=first_value, palette=Spectral6,low=min(source.data[first_value])\
                             ,high=max(source.data[first_value]))

    color_bar = ColorBar(color_mapper=mapper['transform'], width=8,  location=(0,0))
    plot.add_layout(color_bar, 'right')

    #add map tiles
    map_tile=get_provider(Vendors.CARTODBPOSITRON)
    plot.add_tile(map_tile)
    plot.circle(source=source, x='latitudemerc',y='longitudemerc',hover_color='red', color=mapper) # alpha=0.5

    # Print data head
    print_columns=['practice', 'ccg']+value_columns
    print ('{n} data points'.format(n=len(data)))
    print (data[print_columns].head())

    output_notebook()
    #output_file('test.html')
    show(plot)
