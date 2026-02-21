import ast
import streamlit as st
import numpy as np
import pandas as pd

from app import tab_afterglow, tab_flares, tab_pulses
from functions.main_functions import population_afterglow, population_flares

st.set_page_config(page_title="LAFF - Population Statistics")

PARAM_SETTINGS = {
    # GENERAL
    'T90': {'units': 's', 'log': True},
    'redshift': {'log': False},
    'dimple': {},

    # FLARE SPECIFIC
    'fluence': {'units': 'erg\u2009cm<sup>-2</sup>', 'log': True},
    'duration': {'units': 's', 'log': True},
    't_peak': {'units': 's', 'log': True},
    't_ratio': {},
    'underlying_index': {},
    
    'peak_flux': {'units': 'erg\u2009cm<sup>-2</sup>\u2009s<sup>-1</sup>', 'log': True},
    'e_iso': {'units': 'erg', 'log': True},
    'L_p': {'units': 'erg\u2009s<sup>-1</sup>', 'log': True},
    'L_iso': {'units': 'erg\u2009s<sup>-1</sup>', 'log': True},
    
    # AFTERGLOW SPECIFIC
    'afterglow_fluence': {'units': 'erg\u2009cm<sup>-2</sup>', 'log': True},
    'total_flare_fluence': {'units': 'erg\u2009cm<sup>-2</sup>', 'log': True},
    'total_pulse_fluence': {'units': 'erg\u2009cm<sup>-2</sup>', 'log': True},
    
}

GRB_NAMES = sorted(list(set(tab_afterglow['GRBname']) | set(tab_flares['GRBname']) | set(tab_pulses['GRBname'])))

st.title("Population Statistics")


if 'plotting_tab_choice' not in st.session_state:
    st.session_state['plotting_tab_choice'] = "Afterglows"

selected_dataset = st.segmented_control("Select population:", ["Afterglows", "Pulses/Flares"], width='stretch', default=st.session_state['plotting_tab_choice'], selection_mode='single')

if selected_dataset is None:
    selected_dataset = st.session_state['plotting_tab_choice']

if selected_dataset != st.session_state['plotting_tab_choice']:
    st.session_state['plotting_tab_choice'] = selected_dataset
    st.rerun()
    

############################################################

if selected_dataset == 'Afterglows':
    
    data = tab_afterglow.copy()
    
    def get_afterglow_fluence(x):
        fluence, conversion = x
        fluence = ast.literal_eval(fluence)[0]
        return fluence * conversion
    
    data['afterglow_fluence'] = data.apply(lambda row: get_afterglow_fluence((row['fluence'], row['conversion'])), axis=1)
    
    data['dimple'] = pd.to_numeric(data['dimple'], errors='coerce').astype('Int64').astype('str')
    data['breaknum'] = data['breaknum'].astype(str)
    
    data['T90_log']                 = np.log10(data['T90'].replace(0, np.nan))
    data['redshift_log']            = np.log10(data['redshift'].replace(0, np.nan))
    data['afterglow_fluence_log']   = np.log10(data['afterglow_fluence'].replace(0, np.nan))
    data['total_flare_fluence_log'] = np.log10(data['total_flare_fluence'].replace(0, np.nan))
    data['total_pulse_fluence_log'] = np.log10(data['total_pulse_fluence'].replace(0, np.nan))
    
    
    plot_cols = {
        'T90': 'T90',
        'Redshift': 'redshift',
        'Break Count': 'breaknum',
        'Flare Count': 'flare_count',
        'Pulse Count': 'pulse_count',
        'Afterglow Fluence': 'afterglow_fluence',
        'Total Flare Fluence': 'total_flare_fluence',
        'Total Pulse Fluence': 'total_pulse_fluence',
        'Dimple': 'dimple',
    }
    population_afterglow(data, plot_cols, PARAM_SETTINGS, GRB_NAMES)
    #maybes
    # maybe_cols = {
    #     'Slopes': slopes,
    #     'Break Times': breaks,
    #     'Normal': normal,
    # 'dimple'
    # }
    
    
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
        'Dimple': 'dimple',
    }
    
    population_flares(flare_data, pulse_data, plot_cols, PARAM_SETTINGS, GRB_NAMES)
