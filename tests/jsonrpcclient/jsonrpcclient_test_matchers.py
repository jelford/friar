import json


def that(actual, matcher):
    return matcher == actual


class has():
    def __init__(self, **kwargs):
        self.attributes = kwargs

    def __eq__(self, actual):
        for name, value in self.attributes.items():
            if not hasattr(actual, name):
                return False
            elif getattr(actual, name) != value:
                return False
        return True


class JsonMatching():
    def __init__(self, expected_dict):
        self.expected_dict = expected_dict

    def __eq__(self, actual):
        return json.loads(actual) == self.expected_dict

    def __repr__(self):
        return 'JsonMatching({})'.format(self.expected_dict)
