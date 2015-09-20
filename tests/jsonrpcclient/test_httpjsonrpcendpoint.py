import unittest
from unittest import mock
from unittest.mock import ANY, patch
import json
import requests
from functools import wraps

import jsonrpcclient
from jsonrpcclient import HttpPostTransport, http_rpc_endpoint

from jsonrpcclient_test_matchers import *


def _success_response_with_body(body='some-response-from-server'):
    response = mock.Mock()
    response.status_code = 200
    response.raise_for_status = mock.Mock()
    response.text = body
    return response


def mocking_session(test):
    @wraps(test)
    def wrapper(self, *args, **kwargs):
        fake_session_instance = mock.Mock()
        with patch('requests.Session') as fake_session:
            fake_session.return_value = fake_session_instance
            test(self, fake_session, fake_session_instance)

    return wrapper


class HttpPostTransportTest(unittest.TestCase):
    @mocking_session
    def test_send_is_post_to_endpoint_url(self, Session, session_instance):
        under_test = HttpPostTransport('uri')

        payload = {"key": "value"}
        under_test.send(json.dumps(payload))

        session_instance.post.assert_called_with('uri', data=JsonMatching(payload))

    @mocking_session
    def test_extra_parameters_are_passed_through_to_session(self, Session, session_instance):
        session_instance.headers = dict()
        under_test = HttpPostTransport('uri', headers={'key': 'value'})

        Session.assert_called_with()
        assert session_instance.headers == {'key': 'value'}

    @mocking_session
    def test_unwraps_response_objects(self, Session, session_instance):
        under_test = HttpPostTransport('uri')

        session_instance.post.return_value = _success_response_with_body()

        result = under_test.send('payload')
        assert result == 'some-response-from-server'


class HttpRpcSessionFactoryTest(unittest.TestCase):
    @mocking_session
    def test_constructs_endpoint_with_http_transport_layer(self, Session, session_instance):
        session_instance.post.return_value = _success_response_with_body('')

        result = http_rpc_endpoint(
                    url='http://some-host.com:80/api/v2',
                    headers={'X-Session': 'some-session-key'},
                    method_prefix='prefix')

        assert isinstance(result, jsonrpcclient.Endpoint)

        result.methodA(paramA=1)

        session_instance.post.assert_called_with(
            'http://some-host.com:80/api/v2',
            data=JsonMatching(
                {
                    'jsonrpc': '2.0',
                    'method': 'prefixmethodA',
                    'params': {'paramA': 1},
                    'id': ANY
                }))
