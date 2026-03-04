import ast
import streamlit as st
import pandas as pd
import numpy as np


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

    data["redshift_log"] = np.log10(data["redshift"].replace(0, np.nan))
    data["afterglow_fluence_log"] = np.log10(
        pd.to_numeric(data["afterglow_fluence"], errors="coerce").replace(0, np.nan)
    )
    data["total_flare_fluence_log"] = np.log10(
        data["total_flare_fluence"].replace(0, np.nan)
    )
    data["total_pulse_fluence_log"] = np.log10(
        data["total_pulse_fluence"].replace(0, np.nan)
    )

    return data


# @st.cache_data
def import_events(fl_path, pl_path):

    flares, pulses = pd.read_csv(fl_path), pd.read_csv(pl_path)

    events = pd.concat([flares.assign(event_type='flare'), pulses.assign(event_type='pulse')], ignore_index=True)
    

    return events
