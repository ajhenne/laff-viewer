import ast
import streamlit as st
import pandas as pd
import numpy as np

from functions.variables import PARAM_SETTINGS


# @st.cache_data
def import_afterglow(filepath):

    data = pd.read_csv(filepath)

    def get_afterglow_fluence(x):
        fluence, conversion = x
        fluence = ast.literal_eval(fluence)[0]
        return fluence * conversion

    data["afterglow_fluence"] = data.apply(
        lambda row: get_afterglow_fluence((row["fluence"], row["conversion"])), axis=1
    )

    data["dimple"] = (
        pd.to_numeric(data["dimple"], errors="coerce").astype("Int64").astype(str)
    )
    data["breaknum"] = data["breaknum"].astype(str)
    
    data = apply_log(data, PARAM_SETTINGS)

    return data


# @st.cache_data
def import_events(fl_path, pl_path):

    flares, pulses = pd.read_csv(fl_path), pd.read_csv(pl_path)

    flares['event_num'], pulses['event_num'] = flares['flarenum'], pulses['pulse_num']
    
    events = pd.concat([flares.assign(event_type='flare'), pulses.assign(event_type='pulse')], ignore_index=True)
    
    events['underlying_index'] = events['underlying_index'].replace('False', np.nan).astype(float)
    events['dimple'] = pd.to_numeric(events['dimple'], errors='coerce').astype('Int64').astype(str)
    
    events = apply_log(events, PARAM_SETTINGS)

    return events


def apply_log(df, settings):
    
    for col, config in settings.items():
        if config.get('log') is True and col in df.columns:
            
            numeric_data = pd.to_numeric(df[col], errors='coerce').replace(0, np.nan)
            df[f'{col}_log'] = np.log10(numeric_data)
            
            
    return df