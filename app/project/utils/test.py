from functools import partial
from flask import url_for

from project.utils.auth import get_token


class TestRequest(object):

    json = {}

    def __init__(self, json):
        self.json = json


def request_call(endpoint, method='get', **url_kwargs):
    def wrapper(client, data=None, user=None, headers=None):
        if not headers:
            headers = []
        if user:
            token = get_token(user)
            headers.append(('Authorization', 'JWT {}'.format(token)))

        func = getattr(client, method)
        return func(url_for(endpoint, **url_kwargs),
                    data=data, headers=headers)

    return wrapper


post = partial(request_call, method='post')
get = partial(request_call, method='get')
put = partial(request_call, method='put')
