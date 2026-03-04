import os
import streamlit as st
import pandas as pd

from functions.custom_css import load_css
from functions.data_cleaning import import_afterglow, import_events

st.set_page_config(page_title="LAFF", layout="wide")

# @st.cache_data
def load_data(filepath):
    df = pd.read_csv(filepath)
    return df

load_css()

COL_PRIMARY = 'rgba(255, 140, 24, 1)'
COL_SECONDARY = 'rgba(72, 138, 139, 1)'
COL_TERTIARY = 'rgba(63, 81, 181, 1)'

###############################################################################
### DATASET SELECTION 

datasets = [dt for dt in os.listdir('results')]

def beautify_dataset_name(folder_name):
    date, version = folder_name.split('_')
    yy = date[:2]
    mm = date[2:4]
    return f"{mm}/20{yy} (laff v{version})"
dataset_name_map = {beautify_dataset_name(d): d for d in datasets}

selected_dataset = st.sidebar.selectbox("Select dataset", options=dataset_name_map.keys())
dataset_path = os.path.join('results', dataset_name_map[selected_dataset])

tab_afterglow = import_afterglow(dataset_path + '/afterglow.csv')
tab_events = import_events(dataset_path + '/flares.csv', dataset_path + '/pulses.csv')

st.session_state['tab_afterglow'] = tab_afterglow
st.session_state['tab_events'] = tab_events

LENGTHS = len(tab_afterglow), len(tab_events[tab_events['event_type'] == 'flare']), len(tab_events[tab_events['event_type'] == 'pulse'])

combined_names = tab_afterglow['GRBname'].unique().tolist() + tab_events['GRBname'].unique().tolist()
name_options = sorted(set(combined_names))
name_options = [x[0:3] + ' ' + x[3:] for x in name_options]


###############################################################################

pg = st.navigation([
    st.Page('pages/burst_viewer.py', title="Burst Viewer", icon=':material/search:'),
    st.Page('pages/population_stats.py', title="Population Statistics", icon=':material/insert_chart:'),
    st.Page('pages/about_laff.py', title="About LAFF", icon=':material/help:')
    ])

pg.run()    