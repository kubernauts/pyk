# pyk: a simple, yet useful Kubernetes toolkit in Python


![https://img.shields.io/pypi/v/pyk.svg](https://pypi.python.org/pypi/pyk/)

![https://img.shields.io/pypi/dm/pyk.svg](https://pypi.python.org/pypi/pyk/)

This is a simple, yet useful toolkit that supports you in writing microservices-style apps with Kubernetes. 

The pyk toolkit is meant to be used by tools such as [kploy](https://github.com/mhausenblas/kploy) or from your own app.
It is manifest-oriented, that is, it expects the resource definitions in YAML files; currently pyk's API is as follows:

- execute an arbitrary [operation](http://kubernetes.io/v1.1/docs/api-reference/v1/operations.html) and return the resource, if any:  `execute_operation(method='GET', ops_path='', payload='')`
- return a description of a resource: `describe_resource(resource_path)`
- delete a resource: `delete_resource(resource_path)`
- create a Replication Controller (RC): `create_rc(manifest_filename, namespace='default')`
- scale a RC: `scale_rc(manifest_filename, namespace='default', num_replicas=0)`
- create a service: `create_svc(manifest_filename, namespace='default')`

## Dependencies

All of these are included in the [setup](setup.py):

* Python [Requests](http://docs.python-requests.org/en/latest/) (note: I've tested with version `2.6.2`)
* Python [PyYAML](http://pyyaml.org/wiki/PyYAML) (note: I've tested with version `3.11`)

## Using pyk

A simple usage pattern is, for example, to create a [Replication Controller](http://kubernetes.io/v1.1/docs/user-guide/replication-controller.html):

    import pprint
    from pyk import toolkit
    
    pyk_client = toolkit.KubeHTTPClient() # assumes local API Server at http://localhost:8080
    _, rc_url = pyk_client.create_rc(manifest_filename='manifest/nginx-webserver-rc.yaml')
    rc = pyk_client.describe_resource(rc_url)
    pprint.pprint(rc.json())

## Testing pyk

In order to run the tests, use `test_pyk.py $KUBERNETES_API_SERVER_URL`, for example:

    $ ./test_pyk.py http://52.33.181.164/service/kubernetes

Above runs all the tests. You can also specify a particular test, like so:

    $ ./test_pyk.py http://52.33.181.164/service/kubernetes "init app"
    ================================================================================
    = Test case: init a simple app

    2015-11-28T05:13:16 From manifest/nginx-webserver-rc.yaml I created the RC "webserver-rc" at /api/v1/namespaces/default/replicationcontrollers/webserver-rc
    2015-11-28T05:13:17 From manifest/webserver-svc.yaml I created the service "webserver-svc" at /api/v1/namespaces/default/services/webserver-svc
    2015-11-28T05:13:18 Found following endpoints:
    2015-11-28T05:13:18 /api/v1/namespaces/default/endpoints/k8sm-scheduler ->
    {
      "addresses": [
        {
          "ip": "10.0.3.45"
        }
      ],
      "ports": [
        {
          "port": 25504,
          "protocol": "TCP"
        }
      ]
    }
    2015-11-28T05:13:18 /api/v1/namespaces/default/endpoints/kubernetes ->
    {
      "addresses": [
        {
          "ip": "10.0.3.45"
        }
      ],
      "ports": [
        {
          "port": 25502,
          "protocol": "TCP"
        }
      ]
    }
    2015-11-28T05:13:18 /api/v1/namespaces/default/endpoints/webserver-svc ->

## To Do

- [x] Use in kploy
- [x] Docs and PyPI submission
- [ ] Add Travis build
