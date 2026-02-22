import streamlit as st

from app import dataset_name_map, LENGTHS

st.set_page_config(page_title="LAFF - About")


st.title("LAFF Viewer")

tab_overview, tab_xrt, tab_bat, tab_parameters = st.tabs(['Overview', 'XRT Fitting', 'BAT Fitting', 'Parameters'])

with tab_overview:

    st.markdown(f"""
                Lightcurve and Flare Fitter (LAFF) is a Python based data pipline, written as part of my PhD at the University of Leicester. It is an open source tool for the gamma-ray burst (GRB) community to provide hte automated fitting of *Swift* GRB light curves. Originally insprired by the afterglow fitter of the [*Swift*-XRT GRB Catalogue](https://www.swift.ac.uk/xrt_live_cat/), this code extends the functionality by providing modelling of the flare components, on top of identifying the underlying afterglow. Additionally, there is an algorthim for the BAT data to identify and fit gamma-ray pulses. This allows for the complete temporal modelling across the X-ray and gamma-ray regime of every GRB from entirety of the *Swift* mission.
                
                LAFF Viewer was subsequently written as a means of presenting this work in an acessible manner. The 'Burst Viewer' pages allows one to look at burst parameters and modelled light curves of each individual burst, while the 'Population Statistics' page allows one to plot various parameters across the whole population of afterglows, flares and pulses.
                
                Currently the dataset is complete for all bursts through to May 2025 -- resulting in the fitting of :primary[**{LENGTHS[0]} X-ray afterglows**], for which :primary[**{LENGTHS[1]} X-ray flares**] are found. In the BAT datasets, a total of :primary[**{LENGTHS[2]} gamma-ray pulses**] are found.
                
                In the other tabs of this page, a brief description of the modelling process is described each of the XRT and BAT datasets, as well as a description of the set of parameters calculated.
                
                """)

    st.link_button("LAFF GitHub Repository", "https://github.com/ajhenne/laff/", icon=":material/code:")

    st.divider()

    st.markdown("""
            #### Acknowledgements
            
            This work made use of data supplied by the UK Swift Science Data Centre at the University of Leicester.
            
            The XRT data modelled in this work are obtained from the [*Swift*-XRT GRB Catalogue](https://www.swift.ac.uk/xrt_live_cat/), described by Evans et al. (2007, 2009). The count to flux conversions used to convert the raw count rate light curves into native band flux data are acquired from the automatically fitted XRT spectral data (Evans et al. 2009).
            
            Several parameters are sourced from [*Swift-BAT* Catalog](https://swift.gsfc.nasa.gov/results/batgrbcat/) (Lien et al. 2016), including T90 and redshift values. Where values are not obtained strictly through my own work, the 'Parameters' tab in this page details the exact sources and calculations used to acquire them.
            
            **References**
            - Evans, P.A. et al. (2007) ‘An online repository of Swift/XRT light curves of gamma-ray bursts’, Astronomy & Astrophysics, 469(1), pp. 379–385. Available at: https://doi.org/10.1051/0004-6361:20077530.                
            - Evans, P.A. et al. (2009) ‘Methods and results of an automatic analysis of a complete sample of Swift -XRT observations of GRBs’, Monthly Notices of the Royal Astronomical Society, 397(3), pp. 1177–1201. Available at: https://doi.org/10.1111/j.1365-2966.2009.14913.x.
            - Lien, A. et al. (2016) ‘THE THIRD SWIFT BURST ALERT TELESCOPE GAMMA-RAY BURST CATALOG’, The Astrophysical Journal, 829(1), p. 7. Available at: https://doi.org/10.3847/0004-637X/829/1/7.
            """, unsafe_allow_html=True)

with tab_xrt:
    st.markdown("XRT")
    
    
with tab_bat:
    st.markdown("BAT")
    
    
with tab_parameters:
    st.markdown("Parameters")
    

# st.divider()

# st.text("Will be a brief description of how LAFF works and the modelling functions.")

# st.subheader("BAT")

# st.latex(r"""
            
#             F(t) =
#             \begin{cases}
#             A\times\exp\left(-\left(\frac{|t-t_m|}{r}\right)^s\right) & t \leq t_m\\
#             A\times\exp\left(-\left(\frac{|t-t_m|}{d}\right)^s\right) & t > t_m
#             \end{cases}
#             """)

# st.subheader("XRT")

# st.subheader("Model Parameters")

# st.divider()

