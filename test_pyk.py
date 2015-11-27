#!/usr/bin/env python

"""
Tests for the pyk toolkit.
"""

import os
import time
from pyk import toolkit

if __name__ == '__main__':
    pyk_client = toolkit.KubeHTTPClient(kube_version='1.1', api_server='http://localhost:25500')
    print pyk_client.execute_operation(method='GET', ops_path='/nodes')
