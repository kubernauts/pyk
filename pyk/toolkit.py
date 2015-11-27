"""
The main pyk toolkit.

@author: Michael Hausenblas, http://mhausenblas.info/#i
@since: 2015-11-27
@status: init
"""

import logging
import requests
import util


class KubeHTTPClient(object):
    """
    Provides communication primitives for the Kubernetes API
    as defined here: http://kubernetes.io/v1.1/api-ref.html
    """

    def __init__(self, kube_version='1.1', api_server='http://localhost:8080/api/v1', debug=False):
        """
        Creates an instance of the KubeHTTPClient.
 
        :Parameters:
           - `kube_version`: The Kubernetes API version to use, defaults to 1.1
           - `api_server`: The URL (IP or FQHN and port) of the Kubernetes API server to use, defaults to `http://localhost:8080/api/v1`
        """
        self.kube_version = kube_version
        self.api_server = api_server
        DEBUG=debug
        if DEBUG:
          FORMAT = '%(asctime)-0s %(levelname)s %(message)s [at line %(lineno)d]'
          logging.basicConfig(level=logging.DEBUG, format=FORMAT, datefmt='%Y-%m-%dT%I:%M:%S')
        else:
          FORMAT = '%(asctime)-0s %(message)s'
          logging.basicConfig(level=logging.INFO, format=FORMAT, datefmt='%Y-%m-%dT%I:%M:%S')

    def execute_operation(self, method='GET', ops_path=''):
        """
        Executes a Kubernetes operation using the specified method against a path.

        :Parameters:
           - `method`: The HTTP method to use, defaults to `GET`
           - `ops_path`: The path of the operation, for example, `/events` which would result in an overall: `GET http://localhost:8080/api/v1/events`
        """
        operation_path_URL = ''.join([self.api_server, ops_path])
        logging.debug('%s %s' %(method, operation_path_URL))
        res = requests.request(method, operation_path_URL)
        logging.debug('%s' %(res.json()))
        return res

