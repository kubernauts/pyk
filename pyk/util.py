"""
Utility functions for the pyk toolkit.

@author: Michael Hausenblas, http://mhausenblas.info/#i
@since: 2015-11-27
@status: init
"""

import yaml
import json 

def load_yaml(filename):
    """
    Loads a YAML-formatted file.
    """
    with open(filename) as f:
        ydoc = yaml.safe_load(f.read())
    return (ydoc, serialize_tojson(ydoc))

def serialize_yaml_tofile(filename, resource):
    """
    Serializes a K8S resource to YAML-formatted file.
    """
    stream = file(filename, "w")
    yaml.dump(resource, stream, default_flow_style=False)

def serialize_tojson(resource):
    """
    Serializes a K8S resource to JSON-formatted string.
    """
    return json.dumps(resource)
