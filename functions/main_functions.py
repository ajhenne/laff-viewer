import ast
import math
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go 

from app import COL_PRIMARY, COL_SECONDARY, COL_TERTIARY
from functions.variables import PARAM_SETTINGS

###############################################################################
### BURST VIEWER

def get_table_value(df, colname, error=None, format="%.3g"):

    if df.empty or pd.isna(df[colname].iloc[0]):
        return "-"

    val = df[colname].iloc[0]

    try:
        if isinstance(val, str):
            val = float(val.strip()) 
        else:
            val = float(val)
    except (ValueError, TypeError):
        return str(val)

    if error and not pd.isna(df[error].iloc[0]):
        err_val = df[error].iloc[0]
        try:
            err = float(err_val)
            return f"{format % val} ± {format % err}"
        except (TypeError, ValueError):
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
        except ValueError:
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
### POPULATION STATS

def population_afterglow(plot_data, plot_cols, GRB_NAMES):

    if 'popstats_afterglow' not in st.session_state:
        st.session_state['popstats_afterglow'] = {
            'x_axis': plot_cols[0],
            'y_axis': plot_cols[1],
            'x_log': 'Log-scale',
            'y_log': 'Log-scale',
            'color_by': 'None',
            'selected_grbs': []
        }
    persistent = st.session_state['popstats_afterglow']
    
    if 'popstats_shared_grbs' not in st.session_state:
        st.session_state['popstats_shared_grbs'] = []
    shared_grbs = st.session_state['popstats_shared_grbs']
    selected_grbs = shared_grbs
    
        
    with st.container(border=True):
        xcol, ycol, lcol = st.columns(3)
        
        with xcol:
            x_idx = plot_cols.index(persistent['x_axis']) if persistent['x_axis'] in plot_cols else 0
            
            x_axis = st.selectbox(
                "X-Axis Parameter", plot_cols, index=x_idx,
                key="x_axis_afterglow",
                format_func=lambda x: PARAM_SETTINGS.get(x, {}).get('name', x)
                )
            
            x_log = st.segmented_control(
                "X-Axis scale", ("Linear-scale", "Log-scale"),
                selection_mode='single',
                default=persistent['x_log'],
                key='x_log_afterglow',
                label_visibility='collapsed')
            
        with ycol:
            y_idx = plot_cols.index(persistent['y_axis']) if persistent['y_axis'] in plot_cols else 1
            
            y_axis = st.selectbox(
                "Y-Axis Parameter", plot_cols, index=y_idx,
                key="y_axis_afterglow",
                format_func=lambda y: PARAM_SETTINGS.get(y, {}).get('name', y)
                )
            
            y_log = st.segmented_control(
                "Y-Axis scale", ("Linear-scale", "Log-scale"),
                selection_mode='single',
                default=persistent['y_log'],
                key='y_log_afterglow',
                label_visibility='collapsed'
                )
            
        with lcol:
            color_options = ["None", "Specific GRB"] + plot_cols
            c_idx = color_options.index(persistent['color_by']) if persistent['color_by'] in color_options else 0
            
            color_by = st.selectbox(
                "Color By", color_options,
                index=c_idx,
                key="color_by_flares",
                format_func=lambda c: PARAM_SETTINGS.get(c, {}).get('name', c)
                )
        
            if color_by == "Specific GRB":
                selected_grbs = st.multiselect(
                    "Enter GRB Names:",
                    GRB_NAMES,
                    placeholder='Select GRBs',
                    default=shared_grbs,
                    label_visibility='collapsed',
                    key="shared_grbs_afterglow")
                st.session_state['popstats_shared_grbs'] = selected_grbs
                selected_grbs = [x.replace(' ', '') for x in st.session_state['popstats_shared_grbs']]
        

    st.session_state['popstats_afterglow'] = {
        'x_axis': x_axis,
        'y_axis': y_axis,
        'x_log': x_log,
        'y_log': y_log,
        'color_by': color_by,
    }


    ############################################################
    ## COLOURING CONFIG

    legend_title = color_by
    color_column = None
    discrete_map = None
    sorted_categorical = {"event_type": ["pulse", "flare"]}
    color_seq = [COL_TERTIARY] + px.colors.qualitative.Plotly 
    
    
    if color_by == "Specific GRB":
        color_column = plot_data['GRBname'].apply(lambda x: x if x in selected_grbs else "Other GRBs")
        discrete_map = {"Other GRBs": "#a8a8a8"}
        
    elif color_by != "None":
        
        color_column = color_by
        legend_title = PARAM_SETTINGS[color_by].get('name', '')
        
        if PARAM_SETTINGS.get(color_column, {}).get('log'):
            color_column = color_by + '_log'
            legend_title = 'Log ' + legend_title

        plot_data = plot_data[plot_data[color_by].notna() & (plot_data[color_by] != '<NA>')]
        
        unique_vals = plot_data[color_by].unique() # sorting for categorical values
        sorted_values = sorted(unique_vals, key=lambda x: int(x))
        sorted_categorical = {color_column: sorted_values}


    ############################################################
    ## PLOTTING COMMANDS

    hover_dict = {
        x_axis: ':.3g',
        y_axis: ':.3g',
    }
    
    custom_labels = {
            x_axis: get_label(x_axis),
            y_axis: get_label(y_axis),
            color_by: get_label(color_by),
            'GRBname': 'GRB Name',
        }


    fig = px.scatter(
        plot_data,
        x=x_axis,
        y=y_axis,
        color=color_column,
        color_discrete_map=discrete_map,
        color_discrete_sequence=color_seq,
        color_continuous_scale='Inferno',
        category_orders=sorted_categorical,
        hover_name="GRBname",
        hover_data=hover_dict,
        custom_data=['GRBname'],
        log_x=(x_log == 'Log-scale'),
        log_y=(y_log == 'Log-scale'),
        labels=custom_labels,
        template='ggplot2'
    )
    
    ############################################################
    ## AXIS CONFIGS

    fig.update_traces(marker=dict(size=10, line=dict(width=0.7, color='black')))

    axis_settings = dict(showgrid=True, exponentformat="power")
    fig.update_xaxes(**axis_settings)
    fig.update_yaxes(**axis_settings)
    
    fig.update_coloraxes(colorbar_exponentformat="power", colorbar_title_text=legend_title)
    
    if x_log == 'Log-scale':
        fig.update_xaxes(dtick=1)
    if y_log == 'Log-scale':
        fig.update_yaxes(dtick=1)
        
    fig.update_layout(
        font=dict(size=16),
        margin=dict(t=30),
        legend_title_text=legend_title,
        paper_bgcolor='rgb(255,255,255)',
        font_color='black',
        plot_bgcolor='rgb(240,242,246)',
    )
    
    
    if color_by == "Specific GRB":
        color_cycle = px.colors.qualitative.Plotly
        color_index = 0
        
        for trace in fig.data:
            if trace.name in selected_grbs:
                trace.marker.color = color_cycle[color_index % len(color_cycle)]
                trace.marker.size = 15
                trace.marker.line = dict(width=2, color='black')
                color_index += 1
        
        traces = list(fig.data)
        traces.sort(key=lambda x: 1 if x.name in selected_grbs else 0)
        fig.data = traces



    ############################################################
    ## EVENT HANDLING
    
    with st.container(border=True):
                    
        event = st.plotly_chart(fig, width='stretch', height=600, theme=None, on_select='rerun', selection_mode='points')
        
        if event and ("selection" in event) and len(event['selection']['points']) > 0:
            clicked_grb = event['selection']['points'][0]['customdata'][0]
            clicked_grb = clicked_grb[0:3] + ' ' + clicked_grb[3:]
            
            st.session_state['viewer_grb'] = clicked_grb
            st.switch_page("pages/burst_viewer.py")
            
            
################################################################
################################################################      


def plot_histogram():
    
    return

def plot_scatter(data_table, plot_cols, population, GRB_NAMES):

    
    return
            
            
def population_flares(df_events, plot_cols, GRB_NAMES):
    
    if 'popstats_events' not in st.session_state:
        st.session_state['popstats_events'] = {
            'x_axis': plot_cols[0],
            'y_axis': plot_cols[1],
            'x_log': 'Log-scale',
            'y_log': 'Log-scale',
            'color_by': 'None',
            'selected_grbs': [],
        }
    persistent = st.session_state['popstats_events']
    
    if 'popstats_shared_grbs' not in st.session_state:
        st.session_state['popstats_shared_grbs'] = []
    shared_grbs = st.session_state['popstats_shared_grbs']
    selected_grbs = shared_grbs
    
    
    with st.container(border=True):
        tcol, xcol, ycol, lcol = st.columns([1, 3, 3, 3])
        
        with tcol:
            flare_toggle = st.toggle("Flares", True)
            pulse_toggle = st.toggle("Pulses", True)
        
        with xcol:
            x_idx = plot_cols.index(persistent['x_axis']) if persistent['x_axis'] in plot_cols else 0
            
            x_axis = st.selectbox(
                "X-Axis Parameter", plot_cols, index=x_idx,
                key="x_axis_flares",
                format_func=lambda x: PARAM_SETTINGS.get(x, {}).get('name', x)
                )
            
            x_log = st.segmented_control(
                "X-Axis scale", ("Linear-scale", "Log-scale"),
                selection_mode='single',
                default=persistent['x_log'],
                key='x_log_flares',
                label_visibility='collapsed')
            
        with ycol:
            y_idx = plot_cols.index(persistent['y_axis']) if persistent['y_axis'] in plot_cols else 1
            
            y_axis = st.selectbox(
                "Y-Axis Parameter", plot_cols, index=y_idx,
                key="y_axis_flares",
                format_func=lambda y: PARAM_SETTINGS.get(y, {}).get('name', y)
                )
            
            y_log = st.segmented_control(
                "Y-Axis scale", ("Linear-scale", "Log-scale"),
                selection_mode='single',
                default=persistent['y_log'],
                key='y_log_flares',
                label_visibility='collapsed'
                )
            
        with lcol:
            color_options = ["None", "Specific GRB"] + plot_cols
            c_idx = color_options.index(persistent['color_by']) if persistent['color_by'] in color_options else 0
            
            color_by = st.selectbox(
                "Color By", color_options,
                index=c_idx,
                key="color_by_flares",
                format_func=lambda c: PARAM_SETTINGS.get(c, {}).get('name', c)
                )
        
            if color_by == "Specific GRB":
                selected_grbs = st.multiselect(
                    "Enter GRB Names:",
                    GRB_NAMES,
                    placeholder='Select GRBs',
                    default=shared_grbs,
                    label_visibility='collapsed',
                    key="shared_grbs_flares")
                st.session_state['popstats_shared_grbs'] = selected_grbs
                selected_grbs = [x.replace(' ', '') for x in st.session_state['popstats_shared_grbs']]
        
    st.session_state['popstats_events'] = {
        'x_axis': x_axis,
        'y_axis': y_axis,
        'x_log': x_log,
        'y_log': y_log,
        'color_by': color_by,
    }
    
    
    ############################################################
    ## COMBINING TABLES

    selected_types = []
    if flare_toggle:
        selected_types.append('flare')
    if pulse_toggle:
        selected_types.append('pulse')

    plot_data = df_events[df_events['event_type'].isin(selected_types)]
    filter_cols = [x_axis, y_axis]
    
    if color_by not in ["None", "Specific GRB"]:
        filter_cols.append(color_by)

    plot_data = plot_data.dropna(subset=filter_cols)
    
    ############################################################
    ## COLOURING CONFIG

    legend_title = color_by
    color_column = None
    discrete_map = None
    sorted_categorical = {"event_type": ["pulse", "flare"]}

    background_map = {"pulse": COL_PRIMARY, "flare": COL_SECONDARY}
    symbol_map = {"flare": 'circle', "pulse": 'circle' if color_by in ('None') else 'diamond'}

    if color_by == "Specific GRB":
            plot_data['ColorGroup'] = plot_data.apply(
                lambda row: row['GRBname'] if row['GRBname'] in selected_grbs 
                else f"Other {row['event_type'].capitalize()}s", 
                axis=1
            )
            color_column = 'ColorGroup'
            
            discrete_map = {
                "Other Pulses": str(COL_PRIMARY[:-3] + '0.5)'),
                "Other Flares": str(COL_SECONDARY[:-3] + '0.5)'),
            }
        
    elif color_by != "None":
        
        color_column = color_by
        legend_title = PARAM_SETTINGS[color_by].get('name', '')
        
        if PARAM_SETTINGS.get(color_column, {}).get('log'):
            color_column = color_by + '_log'
            legend_title = 'Log ' + legend_title
            
        plot_data = plot_data[plot_data[color_by].notna() & (plot_data[color_by] != '<NA>')]
        
        unique_vals = plot_data[color_by].unique()
        sorted_values = sorted(unique_vals, key=lambda x: int(x))
        sorted_categorical = {color_column: sorted_values}


    ############################################################
    ## PLOTTING COMMANDS

    hover_dict = {
        'event_type': True,
        'event_num': True,
        x_axis: ':.3g',
        y_axis: ':.3g',
    }

    custom_labels = {
            x_axis: get_label(x_axis),
            y_axis: get_label(y_axis),
            color_by: get_label(color_by),
            'event_type': PARAM_SETTINGS['event_type']['name'],
            'event_num': PARAM_SETTINGS['event_num']['name'],
            'GRBname': 'GRB Name',
            'flare': 'Flares',
            'pulse': 'Pulses',
        }

    fig = px.scatter(
        plot_data,
        x=x_axis,
        y=y_axis,
        color=color_column if color_by != "None" else "event_type",
        symbol="event_type",
        color_discrete_map=discrete_map if color_by == "Specific GRB" else background_map,
        symbol_map=symbol_map,
        color_continuous_scale='Inferno',
        color_discrete_sequence=px.colors.qualitative.Plotly,
        category_orders=sorted_categorical,
        hover_name="GRBname",
        hover_data=hover_dict,
        custom_data=['GRBname'],
        log_x=(x_log == 'Log-scale'),
        log_y=(y_log == 'Log-scale'),
        labels=custom_labels,
        template='ggplot2'
    )
    
    ############################################################
    ## AXIS CONFIGS
    
    fig.for_each_trace(lambda t: t.update(name=custom_labels.get(t.name, t.name)))

    fig.update_traces(marker=dict(size=8, line=dict(width=0.5, color='DarkSlateGrey')))
    
    axis_settings = dict(showgrid=True, exponentformat="power")
    fig.update_xaxes(**axis_settings)
    fig.update_yaxes(**axis_settings)
    
    fig.update_coloraxes(colorbar_exponentformat="power",
                         colorbar_title_text=legend_title,
                         colorbar_len=0.8,
                         colorbar_y = 0.8,
                         colorbar_yanchor='top')
    
    if x_log == 'Log-scale':
        fig.update_xaxes(dtick=1)
    if y_log == 'Log-scale':
        fig.update_yaxes(dtick=1)


    fig.update_layout(
        font=dict(size=16),
        margin=dict(t=30),
        paper_bgcolor='rgb(255,255,255)',
        font_color='black',
        plot_bgcolor='rgb(240,242,246)',
        legend = dict(title_text="", y=0.96)
    )


    if color_by == "Specific GRB":
        
        color_cycle = px.colors.qualitative.Plotly
        grb_color_map = {name: color_cycle[i % len(color_cycle)] for i, name in enumerate(selected_grbs)}
        
        for trace in fig.data:
            matched_grb = next((name for name in selected_grbs if name in trace.name), None)
            
            if matched_grb:
                trace.marker.color = grb_color_map[matched_grb]
                trace.marker.size = 12
                trace.marker.line = dict(width=2, color='black')
                trace.legendgroup = matched_grb
        
        traces = list(fig.data)
        traces.sort(key=lambda x: 0 if "Other" in x.name else 1)
        fig.data = traces
        
        
    ############################################################
    ## LEGEND CONFIG

    seen_groups = set()
    
    for trace in fig.data:
        is_highlighted = any(grb in trace.name for grb in selected_grbs)
        
        if is_highlighted:
            trace.showlegend = False
            continue

        base_label = trace.name.split(',')[0].strip()
        trace.legendgroup = base_label    
        trace.name = base_label
        
        if base_label in seen_groups:
            trace.showlegend = False
        else:
            trace.showlegend = True
            seen_groups.add(base_label)

    if color_by == "Specific GRB" and selected_grbs:
        
        for grb_name in selected_grbs:

            color = grb_color_map.get(grb_name, 'black')
            
            fig.add_trace(go.Scatter(
                x=[None], y=[None],
                mode='markers',
                name=grb_name,
                legendgroup=grb_name,
                marker=dict(
                    symbol='square',
                    size=12,
                    color=color,
                    line=dict(width=0)
                ),
                showlegend=True
            ))

    new_data = list(fig.data)
    proxies = [t for t in new_data if t.name in selected_grbs and t.showlegend]
    others = [t for t in new_data if t not in proxies]
    fig.data = others + proxies
    
    
    ############################################################
    ## INTERACTION CONFIG
    
    for trace in fig.data:
        is_other = "Other" in (trace.name or "")
        is_proxy = trace.x[0] is None if hasattr(trace, 'x') and len(trace.x) > 0 else False

        if is_other:
            trace.hoverinfo = 'skip'
            trace.hovertemplate = None 
            
        elif not is_proxy:
            trace.hoverinfo = 'all'
            trace.customdata = trace.customdata 


    ############################################################
    ## EVENT HANDLING
    
    with st.container(border=True):
        
        event = st.plotly_chart(fig, width='stretch', height=600, theme=None, on_select='rerun', selection_mode='points')
        
        if event and ("selection" in event) and len(event['selection']['points']) > 0:
            clicked_grb = event['selection']['points'][0]['customdata'][0]
            clicked_grb = clicked_grb[0:3] + ' ' + clicked_grb[3:]
            
            st.session_state['viewer_grb'] = clicked_grb
            st.switch_page("pages/burst_viewer.py")
            
               
def get_label(col):
    cfg = PARAM_SETTINGS.get(col, {})
    name = cfg.get('name', col)
    units = cfg.get('units')
    return f"{name} ({units})" if units else name