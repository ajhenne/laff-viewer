import ast
import streamlit as st
import numpy as np
import pandas as pd

from app import tab_flares, tab_pulses
from functions.main_functions import population_afterglow, population_flares
from functions.variables import PARAM_SETTINGS

st.set_page_config(page_title="LAFF - Population Statistics")

tab_afterglow = st.session_state['tab_afterglow'].copy()
tab_events = st.session_state['tab_events'].copy()


GRB_NAMES = sorted(list(set(tab_afterglow['GRBname']) | set(tab_flares['GRBname']) | set(tab_pulses['GRBname'])))

st.title("Population Statistics")


if 'plot_choice_population' not in st.session_state:
    st.session_state['plot_choice_population'] = 'Afterglows'

selected_dataset = st.segmented_control("Select population:", ["Afterglows", "Pulses/Flares"], width='stretch', default=st.session_state['plot_choice_population'], selection_mode='single')

if selected_dataset is None:
    selected_dataset = st.session_state['plot_choice_population']

if selected_dataset != st.session_state['plot_choice_population']:
    st.session_state['plot_choice_population'] = selected_dataset
    st.rerun()
    
    
if 'plot_choice_type' not in st.session_state:
    st.session_state['plot_choice_type'] = 'Scatter'
    
selected_plottype = st.segmented_control("Plot type:", ["Scatter", "Histogram"], label_visibility='collapsed')
    

############################################################

if selected_dataset == 'Afterglows':
            
    plot_cols = {
        'T90': 'T90',
        'Redshift': 'redshift',
        'Break Count': 'breaknum',
        'Flare Count': 'flare_count',
        'Pulse Count': 'pulse_count',
        'Afterglow Fluence': 'afterglow_fluence',
        'Total Flare Fluence': 'total_flare_fluence',
        'Total Pulse Fluence': 'total_pulse_fluence',
        # 'Dimple': 'dimple',
    }
    population_afterglow(tab_afterglow, plot_cols, PARAM_SETTINGS, GRB_NAMES)

    
############################################################
elif selected_dataset == 'Pulses/Flares':
    
    flare_data = tab_flares.copy()
    pulse_data = tab_pulses.copy()
    
    flare_data['dimple'] = pd.to_numeric(flare_data['dimple'], errors='coerce').astype('Int64').astype(str)
    pulse_data['dimple'] = pd.to_numeric(pulse_data['dimple'], errors='coerce').astype('Int64').astype(str)
    
    flare_data['Pulse/Flare Number'] = flare_data['flarenum']
    pulse_data['Pulse/Flare Number'] = pulse_data['pulse_num']
    
    flare_data['underlying_index'] = flare_data['underlying_index'].replace("False", np.nan).astype(float)
    pulse_data['underlying_index'] = pulse_data['underlying_index'].replace("False", np.nan).astype(float)
    
    for param, settings in PARAM_SETTINGS.items():
        if settings.get('log') == True:
            if param in flare_data.columns:
                flare_data[f'{param}_log'] = np.log10(flare_data[param].replace(0, np.nan))
            if param in pulse_data.columns:
                pulse_data[f'{param}_log'] = np.log10(pulse_data[param].replace(0, np.nan))
    
    plot_cols = {
        'Fluence': 'fluence',
        'Duration': 'duration',
        'Peak Time': 't_peak',
        'Rise/Decay Ratio': 't_ratio',
        'Peak Flux': 'peak_flux',
        'Isotropic Energy': 'e_iso',
        'Peak Luminosity': 'L_p',
        'Isotropic Luminosity': 'L_iso',
        'T90': 'T90',
        'Redshift': 'redshift',
        'Afterglow Fluence': 'afterglow_fluence',
        'Underlying Afterglow Index': 'underlying_index',
        # 'Dimple': 'dimple',
        # 'chisq': 'bat_conversion_rchisq',
    }
    
    population_flares(flare_data, pulse_data, plot_cols, PARAM_SETTINGS, GRB_NAMES)
