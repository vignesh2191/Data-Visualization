#from os.path import join, dirname
import datetime
from bokeh.models import OpenURL, TapTool,HoverTool
from bokeh.layouts import gridplot

import pandas as pd
from scipy.signal import savgol_filter

from bokeh.io import curdoc
from bokeh.layouts import row, column
from bokeh.models import ColumnDataSource, DataRange1d, Select
from bokeh.palettes import Spectral6,Greys256
from bokeh.plotting import figure

All_record = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN','JUL','AUG','SEP','OCT','NOV','DEC']

def get_input(src, name, distribution):
    df = src[src.SUBDIVISION == name].copy()
    del df['SUBDIVISION']
    #df['YEAR'] = pd.to_datetime(df.YEAR)
    # timedelta here instead of pd.DateOffset to avoid pandas bug < 0.18 (Pandas issue #11925)
    df['YEAR']=df.YEAR
    #df['left'] =df.YEAR - datetime.timedelta(days=.5)
    #df['right'] = df.YEAR + datetime.timedelta(days=.5)
    df = df.set_index(['YEAR'])
    df.sort_index(inplace=True)
    if distribution == 'Smoothed':
        window, order = 51, 3
		#for key in All_record:
           # exec("%s = %d" % (codes[code][0], code))
        for key in All_record:
            df[key] = savgol_filter(df[key], window, order)

    return ColumnDataSource(data=df)

def make_plot(source, title):
    plot = figure(tools="pan,wheel_zoom,box_zoom,reset,tap,lasso_select,save,hover",toolbar_location="above",plot_width=1100, plot_height=600)
    #plot2=figure()
    
    plot.title.text = title
    
    legends=["January","february","March","April","May","June","July","August","September","October","November","December"]
    color_list=["Red","orange","yellow","maroon","black","blue","blue","black","green","blue","blue","Red"]
    
    for i,j,k in zip(All_record,legends,color_list):
        
        plot.line(x='YEAR',y=i,source=source,color=k, legend=str(j),line_cap='butt',line_width=2)
        


#    plot.line(x='YEAR',y='JAN',source=source,color="black", legend="january",line_cap='butt',line_width=4)
#    plot.line(x='YEAR',y='FEB',source=source,color="yellow", legend="February")
#    plot.line(x='YEAR',y='MAR',source=source, legend="March",color="green")
#    plot.line(x='YEAR',y='APR',source=source, legend="April",color="red")
#    plot.line(x='YEAR',y='JUN',source=source, legend="june",color="orange")
#    plot.line(x='YEAR',y='JUL',source=source, legend="july")
#    plot.line(x='YEAR',y='AUG',source=source, legend="august")
#    plot.line(x='YEAR',y='SEP',source=source, legend="september")
#    plot.line(x='YEAR',y='OCT',source=source, legend="october")
#    plot.line(x='YEAR',y='NOV',source=source, legend="november")
#    plot.line(x='YEAR',y='DEC',source=source, legend="december")
    url = "https://data.gov.in/keywords/annual-rainfall"
    taptool = plot.select(type=TapTool)
    taptool.callback = OpenURL(url=url)
 
    #chup=source._df_index_name
    plot.xaxis.axis_label = "Year"
    plot.yaxis.axis_label = "Rain (mm)"
    plot.legend.click_policy="hide"
    
    hover = plot.select(dict(type=HoverTool))
    hover.tooltips = [("Year", "@YEAR"),]
    hover.mode = 'mouse'
    
    return plot

def update_plot(attrname, old, new):
    city = city_select.value
    plot.title.text = "Rain In " + cities[city]['SUBDIVISION']
    src = get_input(df, cities[city]['SUBDIVISION'], distribution_select.value)
    source.data.update(src.data)
    
    

    

city = 'ANDAMAN & NICOBAR ISLANDS'
distribution = 'Discrete'
type_plot='circle'

cities = {
    'ANDAMAN & NICOBAR ISLANDS': {
        'SUBDIVISION': 'ANDAMAN & NICOBAR ISLANDS',
        'title': ' WA',
    },
    'ARU0CHAL PRADESH': {
        'SUBDIVISION': 'ARU0CHAL PRADESH',
        'title': ' MA',
    },
    'ASSAM & MEGHALAYA': {
        'SUBDIVISION': 'ASSAM & MEGHALAYA',
        'title': ' WA',
    }
    ,
    'BIHAR': {
        'SUBDIVISION': 'BIHAR',
        'title': ' WA',
    }
    ,
    'CHHATTISGARH': {
        'SUBDIVISION': 'CHHATTISGARH',
        'title': ' WA',
    }
    ,
    'COASTAL ANDHRA PRADESH': {
        'SUBDIVISION': 'COASTAL ANDHRA PRADESH',
        'title': 'WA',
    }
    ,
    'COASTAL KAR0TAKA': {
        'SUBDIVISION': 'COASTAL KAR0TAKA',
        'title': 'WA',
    }
    ,
    'EAST MADHYA PRADESH': {
        'SUBDIVISION': 'EAST MADHYA PRADESH',
        'title': 'WA',
    }
    ,
    'ORISSA': {
        'SUBDIVISION': 'ORISSA',
        'title': 'WA',
    },
    'PUNJAB': {
        'SUBDIVISION': 'PUNJAB',
        'title': 'WA',
    },
    'RAYALSEEMA': {
        'SUBDIVISION': 'RAYALSEEMA',
        'title': 'WA',
    },
    'UTTARAKHAND': {
        'SUBDIVISION': 'UTTARAKHAND',
        'title': 'WA',
    }
}

city_select = Select(value=city, title='State', options=sorted(cities.keys()))
distribution_select = Select(value=distribution, title='Distribution', options=['Discrete', 'Smoothed'])
#plot_type = Select(value=type_plot, title='type of graph', options=['line', 'circle'])

df = pd.read_csv('datafile_Actual_1.csv')
source = get_input(df, cities[city]['SUBDIVISION'], distribution)
plot = make_plot(source, "Weather data for " + cities[city]['SUBDIVISION'])

city_select.on_change('value', update_plot)
distribution_select.on_change('value', update_plot)
#plot_type.on_change('value', update_plot)

controls = column(city_select, distribution_select)

curdoc().add_root(row(plot, controls))
curdoc().title = "Rain in India"

