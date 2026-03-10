import streamlit as st

# from functions.main_functions import population_afterglow, population_flares
from functions.popstats import population_afterglows, population_events
from functions.custom_st import st_segmented_control_no_deselect

st.set_page_config(page_title="LAFF - Population Statistics")

tab_afterglow = st.session_state["tab_afterglow"].copy()
tab_events = st.session_state["tab_events"].copy()

GRB_NAMES = sorted(set(tab_afterglow["GRBname"]) | set(tab_events["GRBname"]))

st.title("Population Statistics")

st_segmented_control_no_deselect('Select population:',
                                 ['Afterglows', 'Pulses/Flares'],
                                 key='plot_population',
                                 width='stretch',
)

st_segmented_control_no_deselect('Select plot type:',
                                 ['Scatter', 'Histogram'],
                                 key='plot_type',
                                 width='stretch'
)


############################################################

if st.session_state['plot_population'] == 'Afterglows':
    plot_cols = [
        "T90",
        "redshift",
        "breaknum",
        "flare_count",
        "pulse_count",
        "afterglow_fluence",
        "total_flare_fluence",
        "total_pulse_fluence",
        "dimple",
    ]

    population_afterglows(tab_afterglow, plot_cols, st.session_state['plot_type'], GRB_NAMES)


############################################################

elif st.session_state["plot_population"] == "Pulses/Flares":
    plot_cols = [
        "fluence",
        "duration",
        "t_peak",
        "t_ratio",
        "peak_flux",
        "e_iso",
        "L_p",
        "L_iso",
        "T90",
        "redshift",
        "afterglow_fluence",
        "underlying_index",
        "dimple",
    ]

    population_events(tab_events, plot_cols, st.session_state['plot_type'], GRB_NAMES)
