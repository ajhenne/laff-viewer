import streamlit as st
import pandas as pd

from app import LENGTHS

st.set_page_config(page_title="LAFF - About")

st.title("LAFF Viewer")

# 1. Initialize session state
if 'about_tab_selection' not in st.session_state:
    st.session_state['about_tab_selection'] = 'Overview'

selected_tab = st.segmented_control(
    "Navigation",
    ['Overview', 'XRT Fitting', 'BAT Fitting', 'Parameters'],
    default=st.session_state['about_tab_selection'],
    key='about_tab',
    width=600,
    label_visibility="collapsed"
)

st.session_state['about_tab_selection'] = selected_tab


if selected_tab == 'Overview':
    
    st.markdown(f"""
                Lightcurve and Flare Fitter (LAFF) is a Python-based data pipeline, written as part of my PhD at the University of Leicester. It is an open source tool for the gamma-ray burst (GRB) community to provide hte automated fitting of *Swift* GRB light curves. Originally insprired by the afterglow fitter of the [*Swift*-XRT GRB Catalogue](https://www.swift.ac.uk/xrt_live_cat/), this code extends the functionality by providing modelling of the flare components, on top of identifying the underlying afterglow. Additionally, there is an algorthim for the BAT data to identify and fit gamma-ray pulses. This allows for the complete temporal modelling across the X-ray and gamma-ray regime of every GRB from entirety of the *Swift* mission.
                
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
            
            Several parameters for the overall GRB are sourced from [*Swift*-BAT Catalog](https://swift.gsfc.nasa.gov/results/batgrbcat/) (Lien et al. 2016), including T90 and redshift values. Where values are not obtained strictly through my own work, the 'Parameters' tab in this page details the exact sources and calculations used to acquire them.
            
            Raw *Swift*-BAT event files are processed into spectral data using `HEASoft` (version 6.35.1, NASA HEASARC 2014) using the standard processing pipeline for this data. Fitting of this data is performed with `Xspec` (version 12.15.0, Arnaud 1996).
            
            **References**
            - Evans, P.A. et al. (2007) ‘An online repository of Swift/XRT light curves of gamma-ray bursts’, Astronomy & Astrophysics, 469(1), pp. 379–385. Available at: https://doi.org/10.1051/0004-6361:20077530.                
            - Evans, P.A. et al. (2009) ‘Methods and results of an automatic analysis of a complete sample of Swift -XRT observations of GRBs’, Monthly Notices of the Royal Astronomical Society, 397(3), pp. 1177–1201. Available at: https://doi.org/10.1111/j.1365-2966.2009.14913.x.
            - Lien, A. et al. (2016) ‘THE THIRD SWIFT BURST ALERT TELESCOPE GAMMA-RAY BURST CATALOG’, The Astrophysical Journal, 829(1), p. 7. Available at: https://doi.org/10.3847/0004-637X/829/1/7.
            - NASA HEASARC (2014) ‘HEAsoft: Unified Release of FTOOLS and XANADU’, Astrophysics Source Code Library, p. ascl:1408.004.
            - Arnaud, K.A. (1996) ‘XSPEC: The First Ten Years’, Astronomical Data Analysis Software and Systems V, 101, p. 17.


            """, unsafe_allow_html=True)


elif selected_tab == 'XRT Fitting':
    
    st.markdown("""
                The basic premise is to identify regions of data where there may be flares ('deviations'), fit the afterglow to the rest of the data, before fitting flare models to the deviations. A full and detailed method is described in my thesis (accepted with corrections, link will be updated soon).
                
                Finding deviations is the most involved part of the process, they come in a vast array of shapes and sizes. A smoothing filter is used to filter out inherent noise, before looking for a period of sufficient rise. This can either be through several consecutive points rising, or sufficiently large relative rise above local noise. Once a deviation is found, the end of it is found by first looking for the peak, then tracking the decay of the data until it 'smooths' out back into the afterglow.
                
                With deviations found, this data can be excluded, leaving what should only represent the afterglow of the GRB. A series of power laws are fitted, with number of breaks 0 through 5. The best statistical fit is used, utilising a pentalty function to avoid overfitting.
                
                Finally, the deviations can be re-added and a flare component added. Each deviation may represent one or many flares, so components are iteratively added, and a similar weighted penalty function is used to determine if the addition of another component is statistically robust. The flare models used in this work are fast-rise exponential-decay (FRED), defined as:
                """)
                
    st.latex(r"""
            F(t) =
            \begin{cases}
                A\times\exp\left(-\left(\frac{|t-t_\textrm{peak}|}{r}\right)^s\right) & t \leq t_m\\
                A\times\exp\left(-\left(\frac{|t-t_\textrm{peak}|}{d}\right)^s\right) & t > t_m
            \end{cases}
            """)
    
    st.markdown(r"""
                where amplitude $A$ corresponds to the peak (count rate) of the flare, $t_\textrm{peak}$ the timing of the flare peak, and $r$ and $d$ are variables that control the rise and decay slopes, respectively; sharpness $s$ controls the overall pulse shape.
            """)
    
    st.markdown("""
                All components are summed together to produce the final model. Count rate is converted to flux using a conversion obtained from the automatic XRT spectral fits available for each burst on the *Swift* website (Evans et al. 2009). From there, fluence can be calculated by integrating across the model during the flare time, and further energetics calculated using GRB T90, redshift, etc. values.
                """)
    
    
elif selected_tab == 'BAT Fitting':
    
    st.markdown("""
                The BAT fitting procedure required a different algorthim due to the differing challenges of this data. While there is no multi-phase afterglow to track, the data is inherently often noisier. The energy band used in this analysis is 25-50 keV.
                
                The first step is to use several iterations of filtering and smoothing to first exclude any large pulses, to estimate local noise level across the data. Then deviations are marked for data that is above three times this final average rolling noise.
                
                For each deviation, several pulse components are attempted in a similar manner as the XRT data, where components are iteratively added and then statistically tested for a sufficient improvement in fit. FRED models, as described before, are also used for pulse components.
                
                This time, the conversion to flux from count rate is obtained by my own spectral fitting of the BAT prompt emission data in the same energy band. HEASoft is used to process the raw event files using the standard data processing pipeline for BAT data, and the response files were loaded in Xspec for fitting. A simple power law was used across all bursts -- of the 10% of bursts fit better with a cut-off power law in Lien et al. (2016), there were few that this was true for both the 1-second peak and full time light curves. Additionally, of these, the majority have a peak above the 25-50 keV energy band usde here anyway. From the fitted models, Xspec can output the model count rate and flux in this energy band, providing the conversion factor.
                """)
    
    
elif selected_tab == 'Parameters':
    
    st.markdown("Parameters")

    params_data = [
        ["$T_{90}$", "s", "Duration containing 90% of the total burst fluence. See [BAT Catalog](https://swift.gsfc.nasa.gov/results/batgrbcat/)."],
        ["$E_{peak}$", "keV", r"The photon energy at which the $F_{\nu}$ spectrum peaks: $E_{peak} = E_{0}(2+\alpha)$"],
        ["Fluence", "erg cm$^{-2}$", "Total energy flux integrated over the $T_{90}$ interval."],
        ["$\Gamma_{XRT}$", "index", "Power-law index of the X-ray afterglow decay."]
    ]
    
    df = pd.DataFrame(params_data, columns=["Parameter", "Unit", "Notes"])

    st.markdown(df.to_markdown(index=False))
