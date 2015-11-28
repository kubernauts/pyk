"""
The main pyk toolkit.

@author: Michael Hausenblas, http://mhausenblas.info/#i
@since: 2015-11-27
@status: init
"""

import logging
import requests
from pyk import util

class ResourceCRUDException(Exception):
    pass

class KubeHTTPClient(object):
    """
    Provides communication primitives for the Kubernetes API
    as defined here: http://kubernetes.io/v1.1/api-ref.html
    """

    def __init__(self, kube_version='1.1', api_server='http://localhost:8080', debug=False):
        """
        Creates an instance of the KubeHTTPClient.
 
        :Parameters:
           - `kube_version`: The Kubernetes API version to use, defaults to 1.1
           - `api_server`: The URL (IP or FQHN and port) of the Kubernetes API server to use, defaults to `http://localhost:8080`
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

    def execute_operation(self, method='GET', ops_path='', payload=''):
        """
        Executes a Kubernetes operation using the specified method against a path.
        This is part of the low-level API.

        :Parameters:
           - `method`: The HTTP method to use, defaults to `GET`
           - `ops_path`: The path of the operation, for example, `/api/v1/events` which would result in an overall: `GET http://localhost:8080/api/v1/events`
           - `payload`: The optional payload which is relevant for `POST` or `PUT` methods only
        """
        operation_path_URL = ''.join([self.api_server, ops_path])
        logging.debug('%s %s' %(method, operation_path_URL))
        if payload == '':
            res = requests.request(method, operation_path_URL)
        else:
            logging.debug('PAYLOAD:\n%s' %(payload))
            res = requests.request(method, operation_path_URL, data=payload)
        logging.debug('RESPONSE:\n%s' %(res.json()))
        return res

    def describe_resource(self, resource_path):
        """
        Describes a resource based on its resource path (the URL path modulo host part).

        :Parameters:
           - `resource_path`: The path of the resource to describe, for example, `/api/v1/namespaces/default/replicationcontrollers/webserver-rc`
        """
        res = self.execute_operation(method='GET', ops_path=resource_path)
        return res

    def delete_resource(self, resource_path):
        """
        Deletes a resource based on its resource path (the URL path modulo host part).

        :Parameters:
           - `resource_path`: The path of the resource to delete, for example, `/api/v1/namespaces/default/replicationcontrollers/webserver-rc`
        """
        res = self.execute_operation(method='DELETE', ops_path=resource_path)
        logging.info('Deleted resource %s' %(resource_path))
        return res

    def create_rc(self, manifest_filename, namespace='default'):
        """
        Creates an RC based on a manifest.

        :Parameters:
           - `manifest_filename`: The manifest file containing the ReplicationController definition, for example: `manifest/nginx-webserver-rc.yaml`
           - `namespace`: In which namespace the RC should be created, defaults to, well, `default`
        """
        rc_manifest, rc_manifest_json  = util.load_yaml(filename=manifest_filename)
        logging.debug('%s' %(rc_manifest_json))
        create_rc_path = ''.join(['/api/v1/namespaces/', namespace, '/replicationcontrollers'])
        res = self.execute_operation(method='POST', ops_path=create_rc_path, payload=rc_manifest_json)
        try:
            rc_url = res.json()['metadata']['selfLink']
        except KeyError:
            raise ResourceCRUDException(''.join(['Sorry, can not create the RC: ', rc_manifest['metadata']['name'], '. Maybe it exists already?']))
        logging.info('From %s I created the RC "%s" at %s' %(manifest_filename, rc_manifest['metadata']['name'], rc_url))
        return (res, rc_url)

    def scale_rc(self, manifest_filename, namespace='default', num_replicas=0):
        """
        Changes the replicas of an RC based on a manifest.
        Note that it defaults to 0, meaning to effectively disable this RC.

        :Parameters:
           - `manifest_filename`: The manifest file containing the ReplicationController definition, for example: `manifest/nginx-webserver-rc.yaml`
           - `namespace`: In which namespace the RC is, defaulting to `default`
           - `num_replicas`: How many copies of the pods that match the selector are supposed to run
        """
        rc_manifest, rc_manifest_json = util.load_yaml(filename=manifest_filename)
        logging.debug('%s' %(rc_manifest_json))
        rc_path = ''.join(['/api/v1/namespaces/', namespace, '/replicationcontrollers/', rc_manifest['metadata']['name']])
        rc_manifest['spec']['replicas'] = num_replicas
        res = self.execute_operation(method='PUT', ops_path=rc_path, payload=util.serialize_tojson(rc_manifest))
        try:
            rc_url = res.json()['metadata']['selfLink']
        except KeyError:
            raise ResourceCRUDException(''.join(['Sorry, can not scale the RC: ', rc_manifest['metadata']['name']]))
        logging.info('I scaled the RC "%s" at %s to %d replicas' %(rc_manifest['metadata']['name'], rc_url, num_replicas))
        return (res, rc_url)

    def create_svc(self, manifest_filename, namespace='default'):
        """
        Creates a service based on a manifest.

        :Parameters:
           - `manifest_filename`: The manifest file containing the service definition, for example: `manifest/webserver-svc.yaml`
           - `namespace`: In which namespace the service should be created, defaults to, well, `default`
        """
        svc_manifest, svc_manifest_json  = util.load_yaml(filename=manifest_filename)
        logging.debug('%s' %(svc_manifest_json))
        create_svc_path = ''.join(['/api/v1/namespaces/', namespace, '/services'])
        res = self.execute_operation(method='POST', ops_path=create_svc_path, payload=svc_manifest_json)
        try:
            svc_url = res.json()['metadata']['selfLink']
        except KeyError:
            raise ResourceCRUDException(''.join(['Sorry, can not create the service: ', svc_manifest['metadata']['name'], '. Maybe it exists already?']))
        logging.info('From %s I created the service "%s" at %s' %(manifest_filename, svc_manifest['metadata']['name'], svc_url))
        return (res, svc_url)

