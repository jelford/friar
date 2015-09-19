import json


class BadJsonRpcParametersError(RuntimeError):
    pass


class _JsonRpcMethod():
    def __init__(self, url, name, session, method_prefix):
        self.url = url
        self.name = name
        self.session = session
        self.method_prefix = method_prefix

    def __call__(self, *args, **kwargs):
        if args and kwargs:
            raise BadJsonRpcParametersError()

        params = args if args else kwargs
        data = {
            'jsonrpc': '2.0',
            'method': '{prefix}{name}'.format(
                       prefix=self.method_prefix, name=self.name),
            'id': 1
        }

        if params:
            data['params'] = params

        self.session.post(self.url, data=json.dumps([data]))


class Endpoint():
    def __init__(self, http_url, http_session, method_name_prefix=None):
        self.http_url = http_url
        self.http_session = http_session
        self.method_prefix = method_name_prefix

    def __getattr__(self, attr):
        return _JsonRpcMethod(
                self.http_url,
                attr,
                self.http_session,
                self.method_prefix or '')
