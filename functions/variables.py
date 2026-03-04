PARAM_SETTINGS = {
    # GENERAL
    'T90': {'units': 's', 'log': True},
    'redshift': {'log': False},
    'dimple': {},

    # FLARE SPECIFIC
    'fluence': {'units': 'erg\u2009cm<sup>-2</sup>', 'log': True},
    'duration': {'units': 's', 'log': True},
    't_peak': {'units': 's', 'log': True},
    't_ratio': {},
    'underlying_index': {},
    
    'peak_flux': {'units': 'erg\u2009cm<sup>-2</sup>\u2009s<sup>-1</sup>', 'log': True},
    'e_iso': {'units': 'erg', 'log': True},
    'L_p': {'units': 'erg\u2009s<sup>-1</sup>', 'log': True},
    'L_iso': {'units': 'erg\u2009s<sup>-1</sup>', 'log': True},
    
    # AFTERGLOW SPECIFIC
    'afterglow_fluence': {'units': 'erg\u2009cm<sup>-2</sup>', 'log': True},
    'total_flare_fluence': {'units': 'erg\u2009cm<sup>-2</sup>', 'log': True},
    'total_pulse_fluence': {'units': 'erg\u2009cm<sup>-2</sup>', 'log': True},
}