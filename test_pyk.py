#!/usr/bin/env python

"""
Testing the crap out of the pyk toolkit.

@author: Michael Hausenblas, http://mhausenblas.info/#i
@since: 2015-11-27
@status: init
"""

import sys
import os
import time
import pprint
import logging
import json

from pyk import toolkit
from pyk import util

DEBUG = False

logging.getLogger("requests").setLevel(logging.WARNING)

def test_init_app():
    """
    Tests if I can deploy a simple Web app, comprising a
    single-replica RC backed pod that runs an nginx Web server 
    and a service for it.
    """
    print(80*'=')
    print('= Test case: init a simple app\n')
    
    # First, we create the RC from a YAML manifest:
    _, rc_url = pyk_client.create_rc(manifest_filename='manifest/nginx-webserver-rc.yaml')
    rc = pyk_client.describe_resource(rc_url)
    if DEBUG: pprint.pprint(rc.json())
    
    # Next, we create the service from a YAML manifest:
    _, svc_url = pyk_client.create_svc(manifest_filename='manifest/webserver-svc.yaml')
    svc = pyk_client.describe_resource(svc_url)
    if DEBUG: pprint.pprint(svc.json())
    
    # See if the service endpoint has come up
    _list_endpoints()
    
    if DEBUG:
        print('kind: %s' %(endpoints['kind']))
        for nodes in endpoints['items']:
            pprint.pprint(nodes['metadata'])
            pprint.pprint(nodes['subsets'])

def _list_endpoints():
    """
    Helper function that prints the endpoint paths to addresses info.
    """
    endpoints2address = dict()
    endpoints = pyk_client.execute_operation(method='GET', ops_path='/api/v1/namespaces/default/endpoints').json()
    logging.info('Found following endpoints: ')
    for ep in endpoints['items']:
        eppath = ''
        epaddress = ''
        for metadata_entry in ep['metadata']:
            if metadata_entry == 'selfLink':
                eppath = ep['metadata'][metadata_entry]
                break
        for subsets_entry in ep['subsets']:
            epaddress = json.dumps(subsets_entry, indent=2, sort_keys=True)
            break
        endpoints2address[eppath] = epaddress
    for k, v in endpoints2address.iteritems():
        logging.info('%s ->\n%s' %(k, v))

def test_init_destroy_app():
    """
    Tests if I can deploy a simple Web app, comprising a
    single-replica RC backed pod that runs an nginx Web server 
    and a service for it and then tear it down again.
    """
    print(80*'=')
    print('= Test case: init a simple app and tear it down again\n')
    
    # First, we create the RC from a YAML manifest:
    _, rc_url = pyk_client.create_rc(manifest_filename='manifest/nginx-webserver-rc.yaml')
    rc = pyk_client.describe_resource(rc_url)
    if DEBUG: pprint.pprint(rc.json())
    
    # Next, we create the service from a YAML manifest:
    _, svc_url = pyk_client.create_svc(manifest_filename='manifest/webserver-svc.yaml')
    svc = pyk_client.describe_resource(svc_url)
    if DEBUG: pprint.pprint(svc.json())
    
    # See if the service endpoint has come up
    time.sleep(2)
    endpoints = pyk_client.execute_operation(method='GET', ops_path='/api/v1/namespaces/default/endpoints').json()
    if DEBUG:
        print('kind: %s' %(endpoints['kind']))
        for nodes in endpoints['items']:
            pprint.pprint(nodes['metadata'])
            pprint.pprint(nodes['subsets'])
        
    # Now, tear down the whole thing
    zero_rc = pyk_client.scale_rc(manifest_filename='manifest/nginx-webserver-rc.yaml', namespace='default', num_replicas=0)
    delete_svc = pyk_client.delete_resource(svc_url)
    if DEBUG: pprint.pprint(delete_svc.json())
    print('Waiting a bit for things to settle ...')
    time.sleep(5)
    delete_rc = pyk_client.delete_resource(rc_url)
    if DEBUG: pprint.pprint(delete_rc.json())

def test_list_pods():
    """
    Tests if I can list all pods running in the cluster.
    """
    print(80*'=')
    print('= Test case: list all running pods\n')
    response = pyk_client.execute_operation(method='GET', ops_path='/api/v1/pods').json()
    print('kind: %s' %(response['kind']))
    for nodes in response['items']:
        pprint.pprint(nodes['status'])

def test_list_nodes():
    """
    Tests if I can list all nodes in the cluster.
    """
    print(80*'=')
    print('= Test case: list all nodes of the cluster\n')
    response = pyk_client.execute_operation(method='GET', ops_path='/api/v1/nodes').json()
    print('kind: %s' %(response['kind']))
    for nodes in response['items']:
        pprint.pprint(nodes['status'])

# If you add a test case above, don't forget to add it here as well:
tests = {
    'init app' : test_init_app,
    'init destroy app' : test_init_destroy_app,
    'list pods' : test_list_pods,
    'list nodes' : test_list_nodes
}

if __name__ == '__main__':
    try:
        api_server_url = sys.argv[1]
        try:
            select_test = sys.argv[2]
        except:
            select_test = 'all'
            
        pyk_client = toolkit.KubeHTTPClient(kube_version='1.1', api_server=api_server_url, debug=DEBUG)
        
        if select_test == 'all':
            for key_test, test in tests.iteritems():
                test()
        else:
            tests[select_test]()
    except IndexError, e:
        print '\nSorry, I need at least the Kubernetes API Server address, for example, run it like so:'
        print '  $ ./test_pyk.py http://localhost:8080 # local, where the API server runs'
        print '  $ ./test_pyk.py http://52.33.181.164/service/kubernetes/api/v1 # using DCOS, where 52.33.181.164 is the IP of the master'
        print '\nNote: per default I execute all tests; if you want to run a specific one, simply say so, for example: '
        print '  $ ./test_pyk.py http://localhost:8080 "list pods" # run only the "list pods" test case'
        print 'Here are all available test cases:'
        for key_test in tests.keys():
            print(" %s -> %s" %(key_test, tests[key_test]))
        sys.exit(1)
