#!/usr/bin/env python
#
# Copyright 2009 Facebook
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""HTTP client to support `tornado.auth` on Google App Engine."""

import functools
import logging

from google.appengine.api import urlfetch


class HttpResponseError(object):
    """A dummy response used when urlfetch raises an exception."""
    code = 404
    body = '404 Not Found'
    error = 'Error 404'


class AsyncHTTPClient(object):
    """An non-blocking HTTP client that uses `google.appengine.api.urlfetch`."""
    def fetch(self, url, callback, **kwargs):
        # Replace kwarg keys.
        kwargs['payload'] = kwargs.pop('body', None)

        rpc = urlfetch.create_rpc()
        rpc.callback = create_rpc_callback(rpc, callback)
        urlfetch.make_fetch_call(rpc, url, **kwargs)
        rpc.wait()


def create_rpc_callback(rpc, callback, *args, **kwargs):
    """Returns a wrapped callback for an async request."""
    if callback is None:
        return None

    if args or kwargs:
        callback = functools.partial(callback, *args, **kwargs)

    def wrapper(*args, **kwargs):
        try:
            result = rpc.get_result()
            code = result.status_code
            # Add 'body' and 'error' attributes expected by tornado.
            setattr(result, 'body', result.content)
            if code < 200 or code >= 300:
                setattr(result, 'error', 'Error %d' % code)
            else:
                setattr(result, 'error', None)

        except urlfetch.DownloadError, e:
            result = HttpResponseError()

        try:
            args += (result,)
            return callback(*args, **kwargs)
        except Exception, e:
            logging.error("Exception during callback", exc_info=True)

    return wrapper
