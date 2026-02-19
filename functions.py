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

PARAM_SETTINGS = {
    'afterglow_fluence': {'unit': ' (erg/cm^2)', 'log': True},
    'total_flare_fluence': {'unit': ' (erg/cm^2)', 'log': True},
    'total_pulse_fluence': {'unit': ' (erg/cm^2)', 'log': True},
    'T90': {'unit': ' (s)', 'log': True},
    'redshift': {'log': False},
}

def create_plot(data, data_cols):
    xcol, ycol, lcol = st.columns(3)
    
    with xcol:
        x_axis = st.selectbox("X-Axis Parameter", options=list(data_cols.keys()), index=0)
        x_log = st.segmented_control("X-Axis scale", ("Linear-scale", "Log-scale"), selection_mode='single', default='Log-scale', key='xlogtoggle', label_visibility='collapsed')
        
    with ycol:
        y_axis = st.selectbox("Y-Axis Parameter", options=list(data_cols.keys()), index=1)
        y_log = st.segmented_control("Y-Axis scale", ("Linear-scale", "Log-scale"), selection_mode='single', default='Log-scale', key='ylogtoggle', label_visibility='collapsed')
        
    with lcol:
        color_options = ["None", "Specific GRB"] + list(data_cols.keys())
        color_by = st.selectbox("Color By", color_options)
        
        display_title = color_by if color_by != "None" else ""

        selected_grbs = []
        if color_by == "Specific GRB":
            name_options = sorted(data['GRBname'].unique())
            selected_grbs = st.multiselect("Enter GRB Names:", options=name_options, placeholder='Select GRBs', label_visibility='collapsed')
            selected_grbs = [x.replace(' ', '') for x in selected_grbs]

    color_column = None
    discrete_map = None

    color_seq = ['#ff8c18'] + px.colors.qualitative.Plotly 

    if color_by == "Specific GRB":
        color_column = data['GRBname'].apply(lambda x: x if x in selected_grbs else "Other GRBs")
        discrete_map = {"Other GRBs": "#a8a8a8"}
        
    elif color_by != "None":
        if PARAM_SETTINGS.get(data_cols[color_by], {}).get('log', '') == True:
            color_column = data_cols[color_by] + '_log'
            display_title = f"Log {color_by}" if color_by != "None" else ""
            
        else:
            color_column = data_cols[color_by]
            display_title = color_by if color_by != "None" else ""

    fig = px.scatter(
        data,
        x=data_cols[x_axis],
        y=data_cols[y_axis],
        color=color_column,
        color_discrete_map=discrete_map,
        color_discrete_sequence=color_seq,
        color_continuous_scale='Inferno',
        hover_name="GRBname",
        log_x=(x_log == 'Log-scale'),
        log_y=(y_log == 'Log-scale'),
        labels={
            data_cols[x_axis]: x_axis + PARAM_SETTINGS.get(data_cols[x_axis], {}).get('units', ''), 
            data_cols[y_axis]: y_axis + PARAM_SETTINGS.get(data_cols[y_axis], {}).get('units', '')
        },
        template='ggplot2'
    )

    fig.update_traces(marker=dict(size=8))

    if color_by == "Specific GRB":
        color_cycle = px.colors.qualitative.Plotly
        color_index = 0
        
        for trace in fig.data:
            if trace.name in selected_grbs:
                trace.marker.color = color_cycle[color_index % len(color_cycle)]
                trace.marker.size = 12
                trace.marker.line = dict(width=2, color='DarkSlateGrey')
                color_index += 1
        
        traces = list(fig.data)
        traces.sort(key=lambda x: 1 if x.name in selected_grbs else 0)
        fig.data = traces

    axis_settings = dict(showgrid=True, exponentformat="power")
    
    fig.update_xaxes(**axis_settings)
    fig.update_yaxes(**axis_settings)
    
    if x_log == 'Log-scale':
        fig.update_xaxes(dtick=1)
    if y_log == 'Log-scale':
        fig.update_yaxes(dtick=1)
        
    fig.update_layout(
        font=dict(size=16),
        margin=dict(t=30),
        legend_title_text=display_title,
    )

    fig.update_coloraxes(colorbar_exponentformat="power", colorbar_title_text=display_title)
    

    st.plotly_chart(fig, use_container_width=True, height=600, theme=None)