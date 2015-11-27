"""
Utility functions for pyk.
"""

import yaml

def load_yaml(filename):
    """
    Loads a YAML-formatted file.
    """
    with open(filename) as f:
        ydoc = yaml.safe_load(f.read())
    ydoc