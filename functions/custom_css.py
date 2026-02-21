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

#lightcurve-and-flare-fitter-laff {
    margin-top: -80px;
}
</style>"""


def load_css():
    
    css_to_load = [
        selectbox_dropdown,
        page_headers,
    ]

    for css in css_to_load:
        st.markdown(css, unsafe_allow_html=True)