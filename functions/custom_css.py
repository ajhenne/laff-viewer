import streamlit as st

selectbox_dropdown = """
<style>
.st-d1 {
    box-shadow: rgba(204, 204, 204, 0.16) 0px 4px 16px;
}

</style>"""

page_headers = """
    <style>
    #population-statistics {
        margin-top: -80px;
    }

    .st-key-burst_viewer_entry {
        margin-top: -50px;
    }

    #laff-viewer {
        margin-top: -80px;
    }
    </style>"""


about_tabs = """
    <style>
    .st-key-about_tab {
        width: 100%;
        border-bottom: 2px solid rgba(49, 51, 63, 0.1);
    }
    
    .st-key-about_tab > div{
        width: 600px;
    }
    
    .st-key-about_tab > div > div > button {
        border-top: None;
        border-left: None;
        border-right: None;
        border-radius: 0px !important;
        margin-bottom: -2px;
        border-bottom: 2px solid rgba(49, 51, 63, 0.1);
    }
    .st-key-about_tab > div > div > .st-emotion-cache-bnbx0a {
        border-bottom: 2px solid rgb(255, 140, 24) !important;
        background-color: rgba(0,0,0,0);
    }
    </style>"""

about_table = """
    <style>
        table {
            width: 100%;
        }
        th {
            text-align: left !important;
            background-color: rgba(150, 150, 150, 0.1);
        }
        td {
            vertical-align: top !important;
        }
    </style>"""


def load_css():
    
    css_to_load = [
        selectbox_dropdown,
        page_headers,
        about_table,
        about_tabs
    ]

    for css in css_to_load:
        st.markdown(css, unsafe_allow_html=True)