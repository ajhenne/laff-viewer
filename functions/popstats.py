import plotly.express as px
import streamlit as st

from functions.custom_st import st_segmented_control_no_deselect
from functions.variables import PARAM_SETTINGS, COL_PRIMARY, COL_SECONDARY, COL_TERTIARY


def get_label(col):
    cfg = PARAM_SETTINGS.get(col, {})
    name = cfg.get('name', col)
    units = cfg.get('units')
    return f"{name} ({units})" if units else name


def plot_scatter(df, par, hover_dict, custom_labels):

    selected_grbs = st.session_state['popstats_shared_grbs']



    ###########################################################################

    color_column = None
    discrete_map = None
    sorted_categorical = None

    if par['color_by'] == "Specific GRB":
        df['Specific GRB'] = df['GRBname'].apply(
            lambda grb: grb if grb in selected_grbs else "Other GRBs"
        )
        color_column = "Specific GRB"
        discrete_map = {"Other GRBs": '#a8a8a8'}

    elif par['color_by'] != "None":
        color_column = par['color_by']

        if PARAM_SETTINGS.get(color_column, {}).get('log'):
            color_column = par['color_by'] + '_log'

        df = df[df[par['color_by']].notna() & (df[par['color_by']] != '<NA>')]

        sorted_categorical = {
            color_column: sorted(df[par['color_by']].unique(), key=lambda x: int(x))
        }

    ###########################################################################

    fig = px.scatter(
        df,
        x=par['x_axis'],
        y=par['y_axis'],
        log_x=(par['x_log'] == 'Log-scale'),
        log_y=(par['y_log'] == 'Log-scale'),
        color=color_column,
        color_continuous_scale='Inferno',
        color_discrete_map=discrete_map,
        color_discrete_sequence=[COL_TERTIARY] + px.colors.qualitative.Plotly,
        category_orders=sorted_categorical,
        labels=custom_labels,
        hover_name='GRBname',
        hover_data=hover_dict,
        custom_data=['GRBname'],
        template='ggplot2',
    )

    fig.update_layout(
        font=dict(size=16),
        margin=dict(t=30),
        paper_bgcolor='rgb(255,255,255)',
        font_color='black',
        plot_bgcolor='rgb(240,242,246)',
        coloraxis_colorbar=dict(title=dict(side='right')),
    )

    fig.update_traces(marker={'size': 10, 'line': {'width': 0.7, 'color': 'black'}})

    axis_settings = dict(showgrid=True, exponentformat="power")
    fig.update_xaxes(**axis_settings)
    fig.update_yaxes(**axis_settings)

    if par['x_log'] == 'Log-scale':
        fig.update_xaxes(dtick=1)
    if par['y_log'] == 'Log-scale':
        fig.update_yaxes(dtick=1)
        
    if color_column == "Specific GRB":
        color_cycle = px.colors.qualitative.Plotly
        color_index = 0
        
        fig.update_traces(marker={'opacity': 0.5, 'size': 8})
        
        for trace in fig.data:
            if trace.name in selected_grbs:
                trace.marker.color = color_cycle[color_index % len(color_cycle)]
                trace.marker.size = 15
                trace.marker.opacity = 1
                trace.marker.line = dict(width=2, color='black')
                color_index += 1
        
        traces = list(fig.data)
        traces.sort(key=lambda x: 1 if x.name in selected_grbs else 0)
        fig.data = traces

    ###########################################################################
    ## IGNORE HOVER ON GREY POINTS

    for trace in fig.data:
        is_other = "Other" in (trace.name or "")
        is_proxy = (
            trace.x[0] is None if hasattr(trace, 'x') and len(trace.x) > 0 else False
        )

        if is_other:
            trace.hoverinfo = 'skip'
            trace.hovertemplate = None

        elif not is_proxy:
            trace.hoverinfo = 'all'
            trace.customdata = trace.customdata

    ###########################################################################
    ## EVENT HANDLING

    with st.container(border=True):
        event = st.plotly_chart(
            fig,
            width='stretch',
            height=600,
            theme=None,
            on_select='rerun',
            selection_mode='points',
        )

        if event and ("selection" in event) and len(event['selection']['points']) > 0:
            clicked_grb = event['selection']['points'][0]['customdata'][0]
            clicked_grb = clicked_grb[0:3] + ' ' + clicked_grb[3:]

            st.session_state['viewer_grb'] = clicked_grb
            st.switch_page("pages/burst_viewer.py")

    return


def plot_histogram(df, par, hover_dict, custom_labels):

    selected_grbs = st.session_state['popstats_shared_grbs']
    
    fig = px.histogram(
        df,
        x=par['x_axis'] + '_log' if (par['x_log'] == 'Log-scale') else par['x_axis'],
        # log_x=(par['x_log'] == 'Log-scale'),
        labels=custom_labels,
        log_y=True,
        nbins=20,
        template='ggplot2'
    )
    
    fig.update_layout(bargap=0.2)
    
    st.plotly_chart(fig)
    return


def population_afterglows(data, cols, type, GRB_NAMES):

    scatter = type == 'Scatter'

    if 'popstats_afterglow' not in st.session_state:
        st.session_state['popstats_afterglow'] = {
            'x_axis': cols[0],
            'y_axis': cols[1],
            'x_log': "Log-scale",
            'y_log': "Log-scale",
            'color_by': "None",
            'selected_grbs': [],
        }
    persistent = st.session_state['popstats_afterglow']

    if 'popstats_shared_grbs' not in st.session_state:
        st.session_state['popstats_shared_grbs'] = []
    shared_grbs = st.session_state['popstats_shared_grbs']

    ###########################################################################

    axis_selection = st.container(border=True)

    xcol, ycol, ccol = axis_selection.columns(3)

    with xcol:
        x_idx = cols.index(persistent['x_axis']) if persistent['x_axis'] in cols else 0

        x_axis = st.selectbox(
            "X-axis Parameter",
            cols,
            index=x_idx,
            key='x_axis_afterglow',
            format_func=lambda x: PARAM_SETTINGS.get(x, {}).get('name', x),
        )

        x_log = st_segmented_control_no_deselect(
            "X-axis Scale",
            ("Linear-scale", "Log-scale"),
            key='x_log_afterglow',
            default='Log-scale',
            label_visibility='collapsed',
        )

    with ycol:
        y_idx = cols.index(persistent['y_axis']) if persistent['y_axis'] in cols else 1

        y_axis = st.selectbox(
            "Y-Axis Parameter",
            cols,
            index=y_idx,
            key='y_axis_afterglow',
            format_func=lambda y: PARAM_SETTINGS.get(y, {}).get('name', y),
            disabled=not scatter,
        )

        y_log = st.segmented_control(
            "Y-Axis scale",
            ("Linear-scale", "Log-scale"),
            key='y_log_afterglow',
            default='Log-scale',
            label_visibility='collapsed',
            disabled=not scatter,
        )

    with ccol:
        color_options = ["None", "Specific GRB"] + cols
        c_idx = (
            color_options.index(persistent['color_by'])
            if persistent['color_by'] in color_options
            else 0
        )

        color_by = st.selectbox(
            "Color By",
            color_options,
            index=c_idx,
            key='color_by_flares',
            format_func=lambda c: PARAM_SETTINGS.get(c, {}).get('name', c),
        )

        if color_by == "Specific GRB":
            selected_grbs = st.multiselect(
                "Enter GRB Names:",
                GRB_NAMES,
                placeholder='Select GRBs',
                default=shared_grbs,
                label_visibility='collapsed',
                key='shared_grbs_afterglow',
            )
            st.session_state['popstats_shared_grbs'] = selected_grbs
            selected_grbs = [
                x.replace(' ', '') for x in st.session_state['popstats_shared_grbs']
            ]

    st.session_state['popstats_afterglow'] = {
        'x_axis': x_axis,
        'y_axis': y_axis,
        'x_log': x_log,
        'y_log': y_log,
        'color_by': color_by,
    }

    ###########################################################################
    ## PLOTTING COMMANDS

    par = {
        'x_axis': x_axis,
        'y_axis': y_axis,
        'x_log': x_log,
        'y_log': y_log,
        'color_by': color_by,
    }
    
    hover_dict = {par['x_axis']: ':.3g', par['y_axis']: ':.3g'}

    custom_labels = {
        par['x_axis']: get_label(par['x_axis']),
        par['y_axis']: get_label(par['y_axis']),
        par['color_by']: get_label(par['color_by']),
        par['color_by'] + '_log': 'Log ' + get_label(par['color_by']),
        'GRBname': 'GRB Name',
    }

    if scatter:
        plot_scatter(data, par, hover_dict, custom_labels)
    else:
        plot_histogram(data, par, hover_dict, custom_labels)

    ###########################################################################

    if type == "Scatter":
        st.text("scatter")

    elif type == "Histogram":
        st.text("histogram")

    return


def population_events(data, cols, type, GRB_NAMES):

    if "popstats_events" not in st.session_state:
        st.session_state["popstats_events"] = {
            "x_axis": cols[0],
            "y_axis": cols[1],
            "x_log": "Log-scale",
            "y_log": "Log-scale",
            "color_by": "None",
            "selected_grbs": [],
        }
        persistent = st.session_state["popstats_events"]

    if "popstats_shared_grbs" not in st.session_state:
        st.session_state["popstats_shared_grbs"] = []
    shared_grbs = st.session_state["popstats_shared_grbs"]

    if type == "Scatter":
        st.text("scatter")

    elif type == "Histogram":
        st.text("histogram")

    return
