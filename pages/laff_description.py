import streamlit as st

st.set_page_config(page_title="LAFF - About")

st.title("Lightcurve and Flare Fitter (LAFF)")

st.text("Will be a brief description of how LAFF works and the modelling functions.")

st.subheader("BAT")

st.latex(r"""
            
            F(t) =
            \begin{cases}
            A\times\exp\left(-\left(\frac{|t-t_m|}{r}\right)^s\right) & t \leq t_m\\
            A\times\exp\left(-\left(\frac{|t-t_m|}{d}\right)^s\right) & t > t_m
            \end{cases}
            """)

st.subheader("XRT")

st.subheader("Model Parameters")

st.divider()

st.link_button("LAFF GitHub Repository", "https://github.com/ajhenne/laff/", icon=":material/code:")