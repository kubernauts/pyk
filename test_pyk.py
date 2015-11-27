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
from pyk import toolkit

DEBUG = False

def test_list_nodes():
    """
    Tests if I can list all nodes in the cluster.
    """
    print(80*'=')
    print('= Test case: list all nodes of the cluster\n\n')
    response = pyk_client.execute_operation(method='GET', ops_path='/nodes').json()
    print('kind: %s' %(response['kind']))
    for nodes in response['items']:
        pprint.pprint(nodes['status'])

def test_list_pods():
    """
    Tests if I can list all pods running in the cluster.
    """
    print(80*'=')
    print('= Test case: list all running pods\n\n')
    response = pyk_client.execute_operation(method='GET', ops_path='/pods').json()
    print('kind: %s' %(response['kind']))
    for nodes in response['items']:
        pprint.pprint(nodes['status'])

# If you add a test case above, don't forget to add it here as well:
tests = {
    'list nodes' : test_list_nodes,
    'list pods' : test_list_pods
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
