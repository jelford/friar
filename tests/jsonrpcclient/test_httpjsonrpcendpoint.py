import unittest
from unittest import mock
from unittest.mock import ANY, patch
import json

from jsonrpcclient import *

from jsonrpcclient_test_matchers import *

import requests


_fake_session = mock.Mock()


@patch('requests.Session', new=lambda: _fake_session)
class HttpPostTransportTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_send_is_post_to_endpoint_url(self):
        under_test = HttpPostTransport('uri')

        payload = {"key": "value"}
        under_test.send(json.dumps(payload))

        _fake_session.post.assert_called_with('uri', data=JsonMatching(payload))
