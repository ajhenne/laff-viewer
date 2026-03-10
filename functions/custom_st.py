import streamlit as st


def st_segmented_control_no_deselect(
    label, options, key, default=None, container=st, **kwargs
):
    """A wrapper around the standard st.segmented_control to prevent deselection.

    - Prevents deselection, reverts to last selection.
    - Stores as key to persist across pages.
    
    TODO redundant if this issue is resolved https://github.com/streamlit/streamlit/issues/9870
    
    Definitions follow [st.segmented_control](https://docs.streamlit.io/develop/api-reference/widgets/st.segmented_control), summarised here.
    
    Args:
        label (str): Text label.
        options (Iterable of V): Labels for options - often list of strings.
        key (str): Unique key for the widget, storing as session state.
        default (Iteravle of V, V, or None, optional): Select which option is default. Defaults to None.
        container (optional): Container to hold the widget in. Usually just the default st, but you may want to use the navbar or a custom container. Defaults to st.

    Returns:
        st.segmented_control: Returns the st.segmented_control object.
    """

    actual_default = options[0] if default is None else default

    prev_key = f"_{key}_prev_value"

    if prev_key not in st.session_state:
        st.session_state[prev_key] = actual_default

    if key not in st.session_state:
        st.session_state[key] = st.session_state[prev_key]

    def handle_change():
        new_val = st.session_state[key]
        if new_val is None:
            st.session_state[key] = st.session_state[prev_key]
        else:
            st.session_state[prev_key] = new_val

    return container.segmented_control(
        label,
        options=options,
        key=key,
        on_change=handle_change,
        **kwargs,
    )
