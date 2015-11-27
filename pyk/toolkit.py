"""
The main pyk toolkit.
"""

import requests
import util

class KubeHTTPClient(object):
    """
    Provides communication primitives for the Kubernetes API
    as defined here: http://kubernetes.io/v1.1/api-ref.html
    """
    K8S_V1_API_BASE_PATH = '/api/v1'

    def __init__(self, kube_version='1.1', api_server='http://localhost:8080'):
        """
        Creates an instance of the KubeHTTPClient.
 
        :Parameters:
           - `kube_version`: The Kubernetes API version to use, defaults to 1.1
           - `api_server`: The URL (IP or FQHN and port) of the Kubernetes API server to use, defaults to `http://localhost:8080`
        """
        self.kube_version = kube_version
        self.api_server = ''.join(api_server, K8S_V1_API_BASE_PATH)

    def execute_operation(self, method='GET', ops_path):
        """
        Executes a Kubernetes operation using the specified method against a path
        and returns a JSON-encoded response (if any).

        :Parameters:
           - `method`: The HTTP method to use, defaults to `GET`
           - `path`: The path of the operation, for example, `/events` which would result in an overall: `GET /api/v1/events`
        """
        operation_path_URL = ''.join(api_server, ops_path)
        res = requests.request(method, operation_path_URL)
        res.json()

