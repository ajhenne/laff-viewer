import streamlit as st

st.set_page_config(page_title="LAFF - About")

st.title("Lightcurve and Flare Fitter (LAFF)")

st.markdown("""
            LAFF was written as part of my PhD at the University of Leicester, as an open source tool for the community to provide the automated fitting of *Swift* gamma-ray burst light curves. Originally inspired by the afterglow fits of the [*Swift*-XRT GRB Catalogue](https://www.swift.ac.uk/xrt_live_cat/) [1], this seeks to extend this work by including the modelling of flare components alongside XRT afterglows. Additionally, a separate algorthim works with BAT data to identify and fit pulses.
            
            This viewer was subsuequently written as a means of presenting this work in accessible manner, either look at individual burst fits, or various measured and calculated parameters within the complete set of *Swift* GRBs.
            """)

st.divider()

st.markdown("""
            **References**
            
            [1] Evans, P.A. et al. (2009) ‘Methods and results of an automatic analysis of a complete sample of Swift -XRT observations of GRBs’, Monthly Notices of the Royal Astronomical Society, 397(3), pp. 1177–1201. Available at: https://doi.org/10.1111/j.1365-2966.2009.14913.x.
            
            This work made use of data supplied by the UK Swift Science Data Centre at the University of Leicester.

            """, unsafe_allow_html=True)


st.divider()

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