# -*- coding: utf-8 -*-
"""
    A dummy reference for framework implementations. See in
    `/demos/webapp/webapp_auth.py` an example implementation of this interface.

    :copyright: 2010 by tipfy.org.
    :license: Apache License Version 2.0. See LICENSE.txt for more details.
"""

class RequestAdapter(object):
    """Adapter to transform a framework specific request into a request with the
    attributes expected by `tornado.auth`.

    It must define at least the following attributes or functions:

        request.arguments: a dictionary of GET parameters mapping to a list
                           of values.
        request.host: current request host.
        request.path: current request path.
        request.full_url(): a function returning the current full URL.
    """
    arguments = {}
    host = None
    path = None

    def full_url(self):
        raise NotImplementedError()


class BaseAuth(object):
    """Base auth class with common functions used by the mixin classes.

    To use gaema with your favorite framework, you must implement all methods
    from this class. You are free to implement __init__() in a way that
    best fits the framework.
    """
    #: Auth settings. Depending on the authentication mixin class in use, these
    #: are the required keywords:
    #:
    #:     'google_consumer_key'
    #:     'google_consumer_secret'
    #:
    #:     'twitter_consumer_key'
    #:     'twitter_consumer_secret'
    #:
    #:     'friendfeed_consumer_key'
    #:     'friendfeed_consumer_secret'
    #:
    #:     'facebook_api_key'
    #:     'facebook_secret'
    settings = {}

    #: A RequestAdapter instance.
    request = None

    def require_setting(name, feature='this feature'):
        """Raises an exception if the given setting is not defined.

        :param name:
            Setting name.
        :param feature:
            Setting description.
        :return:
            `None`.
        """
        raise NotImplementedError()

    def async_callback(self, callback, *args, **kwargs):
        """Wraps callbacks with this if they are used on asynchronous requests.

        Catches exceptions and properly finishes the request.

        :param callback:
            Callback function to be wrapped.
        :param args:
            Positional arguments fpr the callback.
        :param kwargs:
            Keyword arguments fpr the callback.
        :return:
            A wrapped callback.
        """
        raise NotImplementedError()

    def redirect(self, url):
        """Redirects to the given URL. For webapp, we raise a `RequestRedirect`
        exception and catch it in the `RequestHandler` instance.

        :param url:
            URL to redirect.
        :return:
            `None`.
        """
        raise NotImplementedError()

    _ARG_DEFAULT = []
    def get_argument(self, name, default=_ARG_DEFAULT, strip=True):
        """Returns the value of a request GET argument with the given name.

        If default is not provided, the argument is considered to be
        required, and we throw an HTTP 404 exception if it is missing.

        The returned value is always unicode.

        :param:
            Argument name to be retrieved from the request GET.
        :param default:
            Default value to be return if the argument is not in GET.
        :param strip:
            If `True`, returns the value after calling strip() on it.
        :return:
            A request argument, as unicode.
        """
        raise NotImplementedError()

    def get_cookie(self, name, default=None):
        """Gets the value of the cookie with the given name, else default.

        :param:
            Cookie name to be retrieved.
        :param default:
            Default value to be return if cookie is not set.
        :return:
            The cookie value.
        """
        raise NotImplementedError()

    def set_cookie(self, name, value, domain=None, expires=None, path='/',
                   expires_days=None):
        """Sets the given cookie name/value with the given options.

        :param name:
            Cookie name.
        :param value:
            Cookie value.
        :param domain:
            Cookie domain.
        :param expires:
            A expiration date as a `datetime` object.
        :param path:
            Cookie path.
        :param expires_days:
            Number of days to calculate expiration.
        :return:
            `None`.
        """
        raise NotImplementedError()
