import ast
import math
import pandas as pd
import streamlit as st
import plotly.express as px

from app import name_options

###############################################################################
### BURST VIEWER

def get_table_value(df, colname, error=None, format="%.3g"):

    if df.empty or pd.isna(df[colname].iloc[0]):
        return "-"

    val = df[colname].iloc[0]

    if error and not pd.isna(df[error].iloc[0]):
        err = df[error].iloc[0]

        try:
            return f"{format % val} ± {format % err}"
        except TypeError:
            pass

    return format % val

def get_table_multiple_values(df, colname, format="%.3g"):

    value_list = list(df[colname])

    return [(format % val) for val in value_list]

def get_table_list(df, colname):

    values = ast.literal_eval(df[colname].iloc[0].replace('nan', 'None'))

    values_list = []

    for v in values:
        try:
            values_list.append(float(v))
        except:
            values_list.append(0)

    return values_list

def get_converted_fluence(df, fluence, conversion):

    try:
        total_fluence = ast.literal_eval(df[fluence].iloc[0])[0]
        conv = df[conversion].iloc[0]
    except IndexError: # afterglow doesn't exist
        return "-" 

    if df.empty or math.isnan(total_fluence) or math.isnan(conv):
        return "-"
    
    if (not total_fluence > 0) or (not conv > 0):
        return "-"
    
    return '%.3g' % (total_fluence * conv)

def print_grb_name(name):

    if name.startswith("GRB"):
        name = name[3:]

    return "GRB " + name


###############################################################################

UNITS = {
    'afterglow_fluence': ' (erg/cm^2)',
    'total_flare_fluence': ' (erg/cm^2)',
    'total_pulse_fluence': ' (erg/cm^2)',
    'T90': ' (s)'
}

###  POPULATION STATS

def create_plot(data, data_cols):
    xcol, ycol, lcol = st.columns(3)
    
    with xcol:
        x_axis = st.selectbox("X-Axis Parameter", options=list(data_cols.keys()), index=0)
        x_log = st.segmented_control("X-Axis scale", ("Linear-scale", "Log-scale"), selection_mode='single', default='Log-scale', key='xlogtoggle', label_visibility='collapsed')
        
    with ycol:
        y_axis = st.selectbox("Y-Axis Parameter", options=list(data_cols.keys()), index=1)
        y_log = st.segmented_control("Y-Axis scale", ("Linear-scale", "Log-scale"), selection_mode='single', default='Log-scale', key='ylogtoggle', label_visibility='collapsed')
        
    with lcol:
        color_by = st.selectbox("Color By (Optional)", ["None", "Specific GRB"] + list(data_cols.keys()))

        selected_grbs = []
        if color_by == "Specific GRB":
            selected_grbs = st.multiselect("Enter GRB Names:", options=name_options, placeholder='Select one or more GRBs', label_visibility='collapsed')
            selected_grbs = [x.replace(' ', '') for x in selected_grbs]


    color_map = None
    if color_by == "Specific GRB":
        color_map = {name: color for name, color in zip(selected_grbs, px.colors.qualitative.Plotly)}
        color_map["Other GRBs"] = "lightgrey"

    fig = px.scatter(
        data,
        x=data_cols[x_axis],
        y=data_cols[y_axis],
        color=get_color_logic(data, data_cols, color_by, selected_grbs),
        color_discrete_map=color_map,
        hover_name="GRBname",
        log_x=(x_log == 'Log-scale'),
        log_y=(y_log == 'Log-scale'),
        labels={data_cols[x_axis]: x_axis + UNITS.get(data_cols[x_axis], ''), data_cols[y_axis]: y_axis + UNITS.get(data_cols[y_axis], '')}
    )

    # Make selected GRBs prominent
    if color_by == "Specific GRB" and selected_grbs:
        fig.update_traces(marker=dict(size=12, line=dict(width=1, color='DarkSlateGrey')), 
                          selector=lambda t: t.name in selected_grbs)
        traces = list(fig.data)
        traces.sort(key=lambda t: 1 if t.name in selected_grbs else 0)
        fig.data = traces

    fig.update_xaxes(exponentformat="e")
    fig.update_yaxes(exponentformat="e")
    fig.update_coloraxes(colorbar_exponentformat="e")
    
    st.plotly_chart(fig, width='stretch', height=600)
    return


def get_color_logic(data, data_cols, color_var, grb_list):
    if color_var == "None":
        return None
    
    elif color_var == "Specific GRB":
        return data['GRBname'].apply(lambda x: x if x in grb_list else "Other GRBs")
    
    else:
        return data_cols[color_var]