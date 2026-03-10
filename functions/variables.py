PARAM_SETTINGS = {
    
    # GENERAL
    'T90': {'name': 'T90', 'units': 's', 'log': True},
    'redshift': {'name': 'Redshift', 'log': False},
    'dimple': {'name': 'Dimple Grouping'},
    'breaknum': {'name': 'Break Count'},
    'flare_count': {'name': 'Flare Count'},
    'pulse_count': {'name': 'Pulse Count'},

    # FLARE SPECIFIC
    'event_num': {'name': 'Pulse/Flare Count'},
    'event_type': {'name': 'Type'},
    'fluence': {'name': 'Fluence', 'units': 'erg\u2009cm<sup>-2</sup>', 'log': True},
    'duration': {'name': 'Duration', 'units': 's', 'log': True},
    't_peak': {'name': 'Peak Time', 'units': 's', 'log': True},
    't_ratio': {'name': 'Rise/Decay Ratio'},
    'underlying_index': {'name': 'Underlying Afterglow Index'},
    
    'peak_flux': {'name': 'Peak Flux', 'units': 'erg\u2009cm<sup>-2</sup>\u2009s<sup>-1</sup>', 'log': True},
    'e_iso': {'name': 'Isotropic Energy', 'units': 'erg', 'log': True},
    'L_p': {'name': 'Peak Luminosity', 'units': 'erg\u2009s<sup>-1</sup>', 'log': True},
    'L_iso': {'name': 'Isotropic Luminosity', 'units': 'erg\u2009s<sup>-1</sup>', 'log': True},
    
    # AFTERGLOW SPECIFIC
    'afterglow_fluence': {'name': 'Afterglow Fluence', 'units': 'erg\u2009cm<sup>-2</sup>', 'log': True},
    'total_flare_fluence': {'name': 'Total Flare Fluence', 'units': 'erg\u2009cm<sup>-2</sup>', 'log': True},
    'total_pulse_fluence': {'name': 'Total Pulse Fluence', 'units': 'erg\u2009cm<sup>-2</sup>', 'log': True},
}


COL_PRIMARY = "rgba(255, 140, 24, 1)"
COL_SECONDARY = "rgba(72, 138, 139, 1)"
COL_TERTIARY = "rgba(63, 81, 181, 1)"