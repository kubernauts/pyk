"""
Utility functions for the pyk toolkit.

@author: Michael Hausenblas, http://mhausenblas.info/#i
@since: 2015-11-27
@status: init
"""

import yaml

def load_yaml(filename):
    """
    Loads a YAML-formatted file.
    """
    with open(filename) as f:
        ydoc = yaml.safe_load(f.read())
    ydoc