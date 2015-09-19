
import unittest
from unittest import mock
import json

from jsonrpcclient import *

class TestJsonRpcClient(unittest.TestCase):
    def setUp(self):
        self.http_session = lambda: None
        self.http_session.post = mock.MagicMock()

    def test_endpoint_maps_method_calls_onto_json_rpc_requests(self):

        e = Endpoint('root-uri', self.http_session)
        e.methodA()

        self.http_session.post.assert_called_with('root-uri', data=json.dumps([{'jsonrpc': '2.0', 'method': 'methodA', 'id': 1}]))

    def test_endpoint_prefixes_methods(self):
        
        e = Endpoint('root-uri', self.http_session, method_name_prefix='prefix-')
        e.methodA()

        self.http_session.post.assert_called_with('root-uri', data=json.dumps([{'jsonrpc': '2.0', 'method': 'prefix-methodA', 'id': 1}]))

    def test_endpoint_passes_parameters(self):
        e = Endpoint('root-uri', self.http_session)
        e.methodA(12)

        self.http_session.post.assert_called_with('root-uri', data=json.dumps([{'jsonrpc': '2.0', 'method': 'methodA', 'params': [12], 'id': 1}]))

    def test_endpoint_passes_named_parameters(self):
        e = Endpoint('root-uri', self.http_session)
        e.methodA(param=12)

        self.http_session.post.assert_called_with('root-uri', data=json.dumps([{'jsonrpc': '2.0', 'method': 'methodA', 'params': {'param': 12}, 'id': 1}]))


