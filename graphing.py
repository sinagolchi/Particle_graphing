import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.lines import Line2D
import matplotlib as mpl
import streamlit as st
mpl.rcParams['figure.dpi'] = 400 #increasing the resolution of created plots



# mpl.rcParams['font.family'] = ['serif']
# mpl.rcParams['font.serif'] = ['Times New Roman']
mpl.rcParams['font.size'] = 11 #setting the font size to 11 pt

class range_set():  #a specific class to represent a set of results with ranges as individual enteries as opposed to points
    def __init__(self,dataframe): #initialization of class, the subset of dataset is required for initiation
        self.data = dataframe #loading the sub dataframe as data
        self.DWTP = self.data['DWTPs'][0] #Identifying the Drinking Water Treatment Plant (DWTP) that the subset represents
        self.Study = self.data['Study'][0] #Identifying the study (publication) that the subset is extracted from

    def plot(self,handle:list(),color,marker,offset,alpha,show_trend_line,trend_line_alpha): #The rendering instructions for ploting the data, The plot is similar to a scatter plot, however, each entery is consisiting of single Y value and a rang of X values, as opposed to single X value
        x = [] #generating empty arrays (lists) for story x , y points, the x value here is the average value of the range provided
        y = []
        for index, row in self.data.iterrows(): #For loop to iterate over the subset enteries
            if row['Removal efficiency'] == 1: #plotting scenario when y value is 1 (or 100%)
                plt.plot([row['Size range 1'],row['Size range 2']],[row['Removal efficiency']*100 + offset,row['Removal efficiency']*100+ offset],color,marker='|',alpha=alpha) #plotting a horizontal line at the removal efficiency of y with "|" marker on each end to specify the range, the range limists are "size range 1" and "size range 2"
                x.append((row['Size range 2']+row['Size range 1'])/2)#adding the average of the size range as x of the scatter point
                y.append(row['Removal efficiency']*100+offset) #adding the removal efficiency as y of the scatter point, the point has an offset to avoid overlaying multiple lines at y = 1 or 100%
            else: #same process for other y values but without the offset
                plt.plot([row['Size range 1'], row['Size range 2']],
                         [row['Removal efficiency'] * 100, row['Removal efficiency'] * 100], color, marker='|',alpha=alpha)
                x.append((row['Size range 2'] + row['Size range 1']) / 2)
                y.append(row['Removal efficiency'] * 100)
        if show_trend_line: #if enabled by the user, a dashed trendline will connect the averages (scatter points) for each subset
            plt.plot(x,y,color=color,linestyle='--',alpha=trend_line_alpha) #drawing the scatter line
        plt.scatter(x, y, marker=marker, color=color) #plotting the averages (scatter points) for the subset

        handle.append(Line2D([0], [0], color=color, marker=marker, linestyle='-', markerfacecolor=color,label=self.DWTP + ', ' + self.Study))#generating legend handles based on the treatment plant and study of the subsets


class data_set(): #class for loading and processing data sets
    def __init__(self,path):#class initializing
        self.data_set = pd.read_csv(path, header=0) #read dataset as a dataframe from the csv
        self.DWTPs = self.data_set['DWTPs'].to_list() #Extract drinking water treatment plant names from the dataset
        self.DWTPs = list(dict.fromkeys(self.DWTPs)) #Making the entries in treatment plant names unique (remove all duplicates)
        self.sub_frames = [] #creating an empty list to store sub datasets based on the treatment plant they originated from
        for item in self.DWTPs: #looping through the treatment plants to divide the main dataset
            df_temp = self.data_set[self.data_set['DWTPs']==item] #selecting sub_sets from the main dataset
            df_temp.reset_index(inplace=True) #reset the index on the subset
            self.sub_frames.append(df_temp) #store the subset

        self.processed_sets = [range_set(s) for s in self.sub_frames] #process the subsets using the "range_set" function defined earlier

    def plot_all(self,legend_style='outside'): #A class method to render the plots, "legend_style" argument determines whether the legend is placed inside or outside the plot's frame
        handles = [] #a list to store legend handles (entries)
        self.colors = (c for c in ['#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#46f0f0', '#f032e6', '#bcf60c', '#fabebe', '#008080', '#e6beff', '#9a6324', '#fffac8', '#800000', '#aaffc3', '#808000', '#ffd8b1', '#000075', '#808080', '#ffffff', '#000000','#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#46f0f0', '#f032e6', '#bcf60c', '#fabebe', '#008080', '#e6beff', '#9a6324', '#fffac8', '#800000', '#aaffc3', '#808000', '#ffd8b1', '#000075', '#808080', '#ffffff', '#000000', '#fabebe', '#008080', '#e6beff', '#9a6324', '#fffac8', '#800000', '#aaffc3', '#808000', '#ffd8b1', '#000075', '#808080', '#ffffff', '#000000','#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#46f0f0', '#f032e6', '#bcf60c', '#fabebe', '#008080', '#e6beff']) #generator object returning colors for the plot
        self.markers = (m for m in ['v','s','o','d','^','<','>','8','1','3','4','v','s','o','d','^','<','>','8','1','3','4','v','s','o','d','^','<','>','8','1','3','4']) #a generator object returning marker styles for scatters
        self.offset = (t for t in [-3.4,-3.3,-3.2,-3.1,-3,-2.9,-2.8,-2.7,-2.5,-2,-1.5,-1,-0.5,0,0.5,1,1.5,2,2.5,2.7,2.8,2.9,3,3.1,3.2,3.2,3.3,3.4]) #a generator object returning values for 100% offset
        #self.offset = (t for t in [0,-0.5,+0.5,-1,1,-1.5,+1.5]) #depricated offset values
        self.num_keys1 = (k for k in range(1,100)) #generating unique keys for interface components
        self.num_keys2 = (k for k in range(101,200))
        self.check_keys = (k for k in range(200,300))
        self.text_keys = (k for k in range(300,400))
        self.color_keys = (k for k in range(500, 600))
        self.num_keys3 = (k for k in range(600, 700))
        for set in self.processed_sets: #for loop to generate interface for each processed set
            with st.expander(label=set.DWTP + ' ' + set.Study + ': propertise'): #generating a dedicated expander for each sub set
                col1, col2 , col3 , col4 = st.columns(4) #making columns for organization
                with col1: #refer to streamlit documentation for detailed explanation of the objects below, the streamlit interface feed the desired values for color, marker style, offset value and whether a trendline should be drawn to the class methods above
                    color = st.color_picker(label='Color', value=next(self.colors),key=next(self.color_keys))
                    trend = st.checkbox(label='Show trend-line',value=True,key=next(self.check_keys))
                with col2:
                    marker = st.text_input(label='Marker style',value=next(self.markers),key=next(self.text_keys))
                with col3:
                    offset = st.number_input(label='Offset at 100%',value=float(next(self.offset)),step=0.1,key=next(self.num_keys3))
                with col4:
                    alpha = st.number_input(label='Transparency',value=1.0,min_value=0.2,max_value=1.0,step=0.1,key=next(self.num_keys1))
                    t_alpha = st.number_input(label='Trend-line Transparency',value=1.0,min_value=0.2,max_value=1.0,step=0.1,key=next(self.num_keys2))

            set.plot(handle=handles,color=color,marker=marker,offset=offset,show_trend_line=trend,alpha=alpha,trend_line_alpha=t_alpha) #calling the "plot" method of the class to render the plot using the inputs from the interface (objects above) as arguments
        if legend_style == 'outside': #deciding where to locate the legend using the logic flow below
            plt.legend(handles=handles,fontsize=11,loc='upper center',bbox_to_anchor=[0.5,-0.15]) #bbox_to_anchor=[1.6,0.5]

        elif legend_style == 'inside':
            plt.legend(handles=handles,fontsize=9)
        else:
            pass

#%%
#initializing the main interface using Streamlit (refer to Streamlit documentation, when in doubt :) )

st.set_page_config(layout='wide',page_title='Graphing tool')  #configuring the page style
st.title('Graphing tool for particle removal efficiency data') #setting a title for the app
st.caption('Developed by Sina Golchi for NSERC Chair in Water Treatment') #a tiny caption

with st.sidebar: #rendering interface components in the sidebar
    csv = st.file_uploader(label='Upload CSV file',) #loading the csv file containing the main datasets using the file loader


dft = data_set(csv) #process the CSV file using the data_set class

with st.sidebar: #getting some input from the user regarding the axis of the plot
    st.markdown('''___''')
    st.caption('Axis options')
    col1, col2  = st.columns(2)
    with col1:
        xmin = st.number_input(label='x min',value=-5) #acquiring the minimum of x axis
        ymin = st.number_input(label='y min', value=-1) #acquiring the maximum of x axis
    with col2:
        xmax = st.number_input(label='x max',value=100) #acquiring the minimum of y axis
        ymax = st.number_input(label='y max', value=110) #acquiring the maximum of y axis
    xlog = st.checkbox(label='Logarithmic x axis') #whether the x axis type to be set as logarithmic
    ylog = st.checkbox(label='Logarithmic y axis') #whether the y axis type to be set as logarithmic

    st.markdown('''___''')
    st.caption('Legend option')
    L_type = st.selectbox(label='Legend type',options=['outside','inside','no legend']) #acquiring the legend style

# try:
dft.plot_all(legend_style=L_type) #calling the plot_all method to render the main plot

if xlog:
    plt.xscale('log') #setting the x scale logarithmic if requested
if ylog:
    plt.yscale('log') #setting the y scale logarithmic if requested

plt.xlim(xmin, xmax) #setting the limits of the x axis
plt.ylim(ymin, ymax) #setting the limits of the x axis

plt.xlabel(r'Particle size range [$ \rm \mu m$]') #setting the x axis label
plt.ylabel('Removal efficiency [%]') #setting the y axis label
plt.grid(axis='y',alpha=0.4) #setting up a grid
plt.gcf().set_size_inches(7,4) #setting the size of the graph

st.pyplot(plt.gcf()) #passing the matplotlib (plot) object to the interface for final visualization

# except Exception as ex: #experimental error handling component
#
#     st.error(str(ex))
#     st.sidebar.warning('No file uploaded or format is incompatible')
