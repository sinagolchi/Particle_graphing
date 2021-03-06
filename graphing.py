import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.lines import Line2D
import matplotlib as mpl
import streamlit as st
mpl.rcParams['figure.dpi'] = 400
#%%

class range_set():
    def __init__(self,dataframe):
        self.data = dataframe
        self.DWTP = self.data['DWTPs'][0]
        self.Study = self.data['Study'][0]

    def plot(self,handle:list(),color,marker,offset,alpha,show_trend_line,trend_line_alpha):
        x = []
        y = []
        for index, row in self.data.iterrows():
            if row['Removal efficiency'] == 1:
                plt.plot([row['Size range 1'],row['Size range 2']],[row['Removal efficiency']*100 + offset,row['Removal efficiency']*100+ offset],color,marker='|',alpha=alpha)
                x.append((row['Size range 2']+row['Size range 1'])/2)
                y.append(row['Removal efficiency']*100+offset)
            else:
                plt.plot([row['Size range 1'], row['Size range 2']],
                         [row['Removal efficiency'] * 100, row['Removal efficiency'] * 100], color, marker='|',alpha=alpha)
                x.append((row['Size range 2'] + row['Size range 1']) / 2)
                y.append(row['Removal efficiency'] * 100)
        if show_trend_line:
            plt.plot(x,y,color=color,linestyle='--',alpha=trend_line_alpha)
        plt.scatter(x, y, marker=marker, color=color)

        handle.append(Line2D([0], [0], color=color, marker=marker, linestyle='-', markerfacecolor=color,label=self.DWTP + ', ' + self.Study))


class data_set():
    def __init__(self,path):
        self.data_set = pd.read_csv(path, header=0)
        self.DWTPs = self.data_set['DWTPs'].to_list()
        self.DWTPs = list(dict.fromkeys(self.DWTPs))
        self.sub_frames = []
        for item in self.DWTPs:
            df_temp = self.data_set[self.data_set['DWTPs']==item]
            df_temp.reset_index(inplace=True)
            self.sub_frames.append(df_temp)

        self.processed_sets = [range_set(s) for s in self.sub_frames]

    def plot_all(self,legend_style='outside'):
        handles = []
        self.colors = (c for c in ['#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#46f0f0', '#f032e6', '#bcf60c', '#fabebe', '#008080', '#e6beff', '#9a6324', '#fffac8', '#800000', '#aaffc3', '#808000', '#ffd8b1', '#000075', '#808080', '#ffffff', '#000000','#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#46f0f0', '#f032e6', '#bcf60c', '#fabebe', '#008080', '#e6beff', '#9a6324', '#fffac8', '#800000', '#aaffc3', '#808000', '#ffd8b1', '#000075', '#808080', '#ffffff', '#000000'])
        self.markers = (m for m in ['v','s','o','d','^','<','>','8','1','3','4','v','s','o','d','^','<','>','8','1','3','4'])
        self.offset = (t for t in [-2.8,-2.5,-2,-1.5,-1,-0.5,0,0.5,1,1.5,2,2.5,2.8])
        self.num_keys1 = (k for k in range(1,50))
        self.num_keys2 = (k for k in range(50,100))
        self.check_keys = (k for k in range(100,150))
        self.text_keys = (k for k in range(150,200))
        for set in self.processed_sets:
            with st.expander(label=set.DWTP + ' ' + set.Study + ': propertise'):
                col1, col2 , col3 , col4 = st.columns(4)
                with col1:
                    color = st.color_picker(label='Color', value=next(self.colors))
                    trend = st.checkbox(label='Show trend-line',value=True,key=next(self.check_keys))
                with col2:
                    marker = st.text_input(label='Marker style',value=next(self.markers),key=next(self.text_keys))
                with col3:
                    offset = st.number_input(label='Offset at 100%',value=float(next(self.offset)),step=0.1)
                with col4:
                    alpha = st.number_input(label='Transparency',value=1.0,min_value=0.2,max_value=1.0,step=0.1,key=next(self.num_keys1))
                    t_alpha = st.number_input(label='Trend-line Transparency',value=1.0,min_value=0.2,max_value=1.0,step=0.1,key=next(self.num_keys2))

            set.plot(handle=handles,color=color,marker=marker,offset=offset,show_trend_line=trend,alpha=alpha,trend_line_alpha=t_alpha)
        if legend_style == 'outside':
            plt.legend(handles=handles,fontsize=9,loc='center right',bbox_to_anchor=[1.6,0.5])
        elif legend_style == 'inside':
            plt.legend(handles=handles,fontsize=9)
        else:
            pass

#%%

# dft = data_set('Copy of Data.csv')
# dft.plot_all()
# plt.xscale('log')
# plt.grid(alpha=0.5)
# plt.xlim(-2,1000)
# plt.xlabel('Particle size')
# plt.ylabel('Removal efficiency')
# plt.gcf().set_size_inches([6,4])
# plt.show()
st.set_page_config(layout='wide',page_title='Graphing tool')
st.title('Graphing for particle removal')
st.caption('Developed by Sina Golchi for NSERC Chair in Water Wreatment')

with st.sidebar:
    csv = st.file_uploader(label='Upload CSV file',)


dft = data_set(csv)

with st.sidebar:
    st.markdown('''___''')
    st.caption('Axis options')
    col1, col2  = st.columns(2)
    with col1:
        xmin = st.number_input(label='x min',value=-5)
        ymin = st.number_input(label='y min', value=-1)
    with col2:
        xmax = st.number_input(label='x max',value=100)
        ymax = st.number_input(label='y max', value=110)
    xlog = st.checkbox(label='Logarithmic x axis')
    ylog = st.checkbox(label='Logarithmic y axis')

    st.markdown('''___''')
    st.caption('Legend option')
    L_type = st.selectbox(label='Legend type',options=['outside','inside','no legend'])

try:
    dft.plot_all(legend_style=L_type)

    if xlog:
        plt.xscale('log')
    if ylog:
        plt.yscale('log')

    plt.xlim(xmin, xmax)
    plt.ylim(ymin, ymax)

    plt.xlabel('Particle range [$\mu m$]')
    plt.ylabel('Removal efficiency [%]')
    plt.grid(axis='y',alpha=0.4)
    plt.gcf().set_size_inches(7,4)
    st.pyplot(plt.gcf())

except Exception as ex:
    
    st.error(str(ex))
    st.sidebar.warning('No file uploaded or format is incompatible')
