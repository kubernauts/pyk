# pyk: a simple, yet useful Kubernetes toolkit in Python

This is a simple, yet useful toolkit that supports you in writing microservices-style apps with Kubernetes. 


## Dependencies

* Python [Requests](http://docs.python-requests.org/en/latest/) (note: I've tested with version `2.6.2`)
* Python [PyYAML](http://pyyaml.org/wiki/PyYAML) (note: I've tested with version `3.11`)

## Usage

TBD.


## Testing

In order to run the tests, use `test_pyk.py $KUBERNETES_API_SERVER_URL`, for example:

    $ ./test_pyk.py http://52.33.181.164/service/kubernetes

Above runs all the tests. You can also specify a particular test, like so:

    $ ./test_pyk.py http://52.33.181.164/service/kubernetes "init app"
    ================================================================================
    = Test case: init a simple RC

    2015-11-28T06:24:24 From manifest/nginx-webserver-rc.yaml I created the RC "webserver-rc" at /api/v1/namespaces/default/replicationcontrollers/webserver-rc
    {u'apiVersion': u'v1',
     u'kind': u'ReplicationController',
     u'metadata': {u'creationTimestamp': u'2015-11-28T06:24:24Z',
                   u'generation': 1,
                   u'labels': {u'app': u'webserver',
                               u'guard': u'pyk',
                               u'status': u'serving'},
                   u'name': u'webserver-rc',
                   u'namespace': u'default',
                   u'resourceVersion': u'755',
                   u'selfLink': u'/api/v1/namespaces/default/replicationcontrollers/webserver-rc',
                   u'uid': u'ab26d73b-9598-11e5-b608-06427e2246b7'},
     u'spec': {u'replicas': 1,
               u'selector': {u'app': u'webserver', u'status': u'serving'},
               u'template': {u'metadata': {u'creationTimestamp': None,
                                           u'labels': {u'app': u'webserver',
                                                       u'guard': u'pyk',
                                                       u'status': u'serving'}},
                             u'spec': {u'containers': [{u'image': u'nginx:1.9.7',
                                                        u'imagePullPolicy': u'IfNotPresent',
                                                        u'name': u'nginx',
                                                        u'resources': {},
                                                        u'terminationMessagePath': u'/dev/termination-log'}],
                                       u'dnsPolicy': u'ClusterFirst',
                                       u'restartPolicy': u'Always'}}},
     u'status': {u'observedGeneration': 1, u'replicas': 1}}
    2015-11-28T06:24:25 I scaled the RC "webserver-rc" at /api/v1/namespaces/default/replicationcontrollers/webserver-rc to 0 replicas
    Waiting a bit for things to settle ...
    2015-11-28T06:24:30 Deleted resource /api/v1/namespaces/default/replicationcontrollers/webserver-rc
    {u'apiVersion': u'v1',
     u'code': 200,
     u'kind': u'Status',
     u'metadata': {},
     u'status': u'Success'}


## To Do

- [ ] Complete toolkit
- [ ] Write example app
