import ast
import streamlit as st
import plotly.express as px
import numpy as np

from app import tab_afterglow, tab_flares, tab_pulses
from functions import create_plot

st.set_page_config(page_title="LAFF - Population Statistics")


st.title("Population Statistics")


selected_dataset = st.segmented_control("Select population:", ["Afterglows", "Pulses/Flares"], width='stretch', default="Afterglows")

if selected_dataset == 'Afterglows':
    
    data = tab_afterglow
    
    def get_fluence_column(x):
        fluence, conversion = x
        fluence = ast.literal_eval(fluence)[0]
        return fluence * conversion
    
    data['afterglow_fluence'] = data.apply(lambda row: get_fluence_column((row['fluence'], row['conversion'])), axis=1)
    
    data['T90_log']                 = np.log10(data['T90'].replace(0, np.nan))
    data['redshift_log']            = np.log10(data['redshift'].replace(0, np.nan))
    data['afterglow_fluence_log']   = np.log10(data['afterglow_fluence'].replace(0, np.nan))
    data['total_flare_fluence_log'] = np.log10(data['total_flare_fluence'].replace(0, np.nan))
    data['total_pulse_fluence_log'] = np.log10(data['total_pulse_fluence'].replace(0, np.nan))
    
    plot_cols = {
        'T90': 'T90',
        'Redshift': 'redshift',
        'Break number': 'breaknum',
        'Flare Count': 'flare_count',
        'Pulse Count': 'pulse_count',
        'Afterglow Fluence': 'afterglow_fluence',
        'Total Flare Fluence': 'total_flare_fluence',
        'Total Pulse Fluence': 'total_pulse_fluence',
        'Dimple': 'dimple',
    }
    
    #maybes
    # maybe_cols = {
    #     'Slopes': slopes,
    #     'Break Times': breaks,
    #     'Normal': normal,
    # 'dimple'
    # }
    
create_plot(data, plot_cols)