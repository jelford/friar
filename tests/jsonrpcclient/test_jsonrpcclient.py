import unittest
from unittest import mock
from unittest.mock import ANY
import json

from jsonrpcclient import *

from jsonrpcclient_test_matchers import *


class TestJsonRpcClient(unittest.TestCase):
    def setUp(self):
        self.synchronous_endpoint = lambda: None
        self.synchronous_endpoint.send = mock.MagicMock(return_value=None)

    def test_endpoint_maps_method_calls_onto_json_rpc_requests(self):

        e = Endpoint(self.synchronous_endpoint)
        e.methodA()

        self.synchronous_endpoint.send.\
            assert_called_with(
                JsonMatching(
                    {'jsonrpc': '2.0', 'method': 'methodA', 'id': 1}
                ))

    def test_endpoint_prefixes_methods(self):

        e = Endpoint(
                self.synchronous_endpoint, method_name_prefix='prefix-')

        e.methodA()

        self.synchronous_endpoint.send.\
            assert_called_with(
                JsonMatching(
                    {'jsonrpc': '2.0', 'method': 'prefix-methodA', 'id': 1}
                ))

    def test_endpoint_passes_parameters(self):
        e = Endpoint(self.synchronous_endpoint)
        e.methodA(12)

        self.synchronous_endpoint.send.\
            assert_called_with(
                JsonMatching(
                    {
                        'jsonrpc': '2.0',
                        'method': 'methodA',
                        'params': [12],
                        'id': 1
                    }
                ))

    def test_endpoint_passes_named_parameters(self):
        e = Endpoint(self.synchronous_endpoint)
        e.methodA(param=12)

        self.synchronous_endpoint.send.\
            assert_called_with(
                JsonMatching(
                    {
                        'jsonrpc': '2.0',
                        'method': 'methodA',
                        'params': {'param': 12},
                        'id': 1
                    }
                ))

    def test_endpoint_returns_result(self):
        self.synchronous_endpoint.send = mock.MagicMock(
                                            return_value=json.dumps(
                                                {
                                                    'jsonrpc': '2.0',
                                                    'result': 'result-string',
                                                    'id': 1
                                                }
                                            ))

        e = Endpoint(self.synchronous_endpoint)
        result = e.methodA()

        assert result == 'result-string'

    def test_endpoint_raises_errors(self):
        self.synchronous_endpoint.send = mock.MagicMock(
                                            return_value=json.dumps(
                                                {
                                                    'jsonrpc': '2.0',
                                                    'error': {
                                                        'code': 12,
                                                        'message': 'error-description',
                                                        'data': {'extra-data': 1}
                                                    },
                                                    'id': 1
                                                }
                                            ))

        e = Endpoint(self.synchronous_endpoint)

        with self.assertRaises(RemoteError) as remote_error:
            result = e.methodA()

        assert that(remote_error.exception, has(code=12))
        assert that(remote_error.exception, has(data={'extra-data': 1}))
        assert that(remote_error.exception, has(message='error-description'))

    def test_enpoint_can_send_batch_messages(self):
        e = Endpoint(self.synchronous_endpoint)

        e.batch()\
            .methodA()\
            .methodB(arg=1)\
            .methodC(2)\
            .send()

        self.synchronous_endpoint.send.\
            assert_called_with(
                JsonMatching([
                    {'jsonrpc': '2.0', 'method': 'methodA', 'id': ANY},
                    {'jsonrpc': '2.0', 'method': 'methodB', 'params': {'arg': 1}, 'id': ANY},
                    {'jsonrpc': '2.0', 'method': 'methodC', 'params': [2], 'id': ANY},
                ]))

    def test_endpoint_returns_batch_results(self):
        self.synchronous_endpoint.send = mock.MagicMock(
                                            return_value=json.dumps([
                                                {
                                                    'jsonrpc': '2.0',
                                                    'result': 'methodB-result',
                                                    'id': 2
                                                },
                                                {
                                                    'jsonrpc': '2.0',
                                                    'result': 'methodA-result',
                                                    'id': 1
                                                }
                                            ]))

        e = Endpoint(self.synchronous_endpoint)

        result = e.batch()\
                  .methodA()\
                  .methodB()\
                  .send()

        assert result == ['methodA-result', 'methodB-result']

    def test_enpoint_does_not_send_id_if_message_is_notification(self):
        e = Endpoint(self.synchronous_endpoint)

        e.methodA(async=True)

        self.synchronous_endpoint.send.\
            assert_called_with(
                JsonMatching(
                    {'jsonrpc': '2.0', 'method': 'methodA'}
                ))

    def test_endpoint_does_not_send_message_ids_if_batch_method_is_notification(self):
        e = Endpoint(self.synchronous_endpoint)

        e.batch()\
            .methodA()\
            .methodB(arg=1)\
            .methodC(2)\
            .send(async=True)

        self.synchronous_endpoint.send.\
            assert_called_with(
                JsonMatching([
                    {'jsonrpc': '2.0', 'method': 'methodA'},
                    {'jsonrpc': '2.0', 'method': 'methodB', 'params': {'arg': 1}},
                    {'jsonrpc': '2.0', 'method': 'methodC', 'params': [2]},
                ]))
