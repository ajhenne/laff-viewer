import streamlit as st

from functions.main_functions import population_afterglow, population_flares

st.set_page_config(page_title="LAFF - Population Statistics")

tab_afterglow = st.session_state["tab_afterglow"].copy()
tab_events = st.session_state["tab_events"].copy()

GRB_NAMES = sorted(set(tab_afterglow["GRBname"]) | set(tab_events["GRBname"]))

st.title("Population Statistics")


if "plot_choice_population" not in st.session_state:
    st.session_state["plot_choice_population"] = "Afterglows"

selected_dataset = st.segmented_control(
    "Select population:",
    ["Afterglows", "Pulses/Flares"],
    width="stretch",
    default=st.session_state["plot_choice_population"],
    selection_mode="single",
)

if selected_dataset is None:
    selected_dataset = st.session_state["plot_choice_population"]

if selected_dataset != st.session_state["plot_choice_population"]:
    st.session_state["plot_choice_population"] = selected_dataset
    st.rerun()


if "plot_choice_type" not in st.session_state:
    st.session_state["plot_choice_type"] = "Scatter"

# selected_plottype = st.segmented_control(
#     "Plot type:", ["Scatter", "Histogram"], label_visibility="collapsed"
# )


############################################################

if selected_dataset == "Afterglows":
    plot_cols = [
        "T90",
        "redshift",
        "breaknum",
        "flare_count",
        "pulse_count",
        "afterglow_fluence",
        "total_flare_fluence",
        "total_pulse_fluence",
        "dimple"
    ]

    population_afterglow(tab_afterglow, plot_cols, GRB_NAMES)


############################################################

elif selected_dataset == "Pulses/Flares":
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

    population_flares(tab_events, plot_cols, GRB_NAMES)
