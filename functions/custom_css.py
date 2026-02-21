import streamlit as st

selectbox_dropdown = """
<style>
.st-d1 {
    box-shadow: rgba(204, 204, 204, 0.16) 0px 4px 16px;
}

</style>"""

popstats_title = """
<style>
#population-statistics {
    margin-top: -80px;
}
</style>"""

burstviewer_searchbar = """
<style>
.st-key-burst_viewer_entry {
    margin-top: -50px;
}
</style>"""


def load_css():
    
    css_to_load = [
        selectbox_dropdown,
        popstats_title,
        burstviewer_searchbar
    ]

    for css in css_to_load:
        st.markdown(css, unsafe_allow_html=True)