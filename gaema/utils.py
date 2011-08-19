# -*- coding: utf-8 -*-

"""
kay.ext.gaema.utils

:Copyright: (c) 2009 Takashi Matsuo <tmatsuo@candit.jp>
                     All rights reserved.
:license: BSD, see LICENSE for more details.
"""

from functools import wraps, update_wrapper

from django.conf import settings
from django.contrib.sessions.backends.db import SessionStore
from django.core.urlresolvers import reverse
from django.http import HttpResponseServerError
from werkzeug import (
  Local, LocalManager,
)

from gaema import services
from gaema import (
  NEXT_URL_KEY_FORMAT, GAEMA_USER_KEY_FORMAT
)

local = Local()
local_manager = LocalManager([local])

def get_valid_services():
  return getattr(settings, 'GAEMA_VALID_SERVICES', [services.GOOG_OPENID])

def create_gaema_login_url(service, nexturl="/"):
  next_url_key = NEXT_URL_KEY_FORMAT % service
  set_cookie(next_url_key, nexturl)
  return reverse("gaema.views.login", kwargs=dict(service=service))

def create_marketplace_login_url(domain, nexturl="/"):
  next_url_key = NEXT_URL_KEY_FORMAT % domain
  set_cookie(next_url_key, nexturl)
  return reverse("gaema.views.marketplace_login", kwargs=dict(domain=domain))

def create_gaema_logout_url(service, nexturl="/"):
  next_url_key = NEXT_URL_KEY_FORMAT % service
  set_cookie(next_url_key, nexturl)
  return reverse("gaema.views.logout", kwargs=dict(service=service))

def create_marketplace_logout_url(domain, nexturl="/"):
  next_url_key = NEXT_URL_KEY_FORMAT % domain
  set_cookie(next_url_key, nexturl)
  return reverse("gaema.views.marketplace_logout", kwargs=dict(domain=domain))

def get_gaema_user(service):
  try:
    gaema_user_key = GAEMA_USER_KEY_FORMAT % service
    if hasattr(settings, "GAEMA_STORAGE") and \
          settings.GAEMA_STORAGE == "cookie":
      user_data = local.request.cookies.get(gaema_user_key, None)
      if user_data:
        return SecureCookie.unserialize(user_data,
                                        secret_key=settings.SECRET_KEY)
    else:
      return local.request.session.get(gaema_user_key, None)
  except Exception, e:
    return HttpResponseServerError('Getting gaema_user failed, reason: %s' % e)

def set_gaema_user(service, user):
  gaema_user_key = GAEMA_USER_KEY_FORMAT % service
  local.request.session[gaema_user_key] = user
  local.request.session.modified = True

def set_cookie(key, value='', max_age=None, expires=None,
               path='/', domain=None, secure=None, httponly=False):
  if not hasattr(local, "override_cookies"):
    local.override_cookies = []
  local.override_cookies.append({"key": key, "value": value,
                                 "max_age": max_age, "expires": expires,
                                 "path": path, "domain": domain,
                                 "secure": secure, "httponly": httponly})

class MethodDecoratorAdaptor(object):
  """
  Generic way of creating decorators that adapt to being
  used on methods
  """
  def __init__(self, decorator, func):
    update_wrapper(self, func)
    # NB: update the __dict__ first, *then* set
    # our own .func and .decorator, in case 'func' is actually
    # another MethodDecoratorAdaptor object, which has its
    # 'func' and 'decorator' attributes in its own __dict__
    self.decorator = decorator
    self.func = func
  def __call__(self, *args, **kwargs):
    return self.decorator(self.func)(*args, **kwargs)
  def __get__(self, instance, owner):
    return self.decorator(self.func.__get__(instance, owner))

def auto_adapt_to_methods(decorator):
  """
  Takes a decorator function, and returns a decorator-like callable that can
  be used on methods as well as functions.
  """
  def adapt(func):
    return MethodDecoratorAdaptor(decorator, func)
  return wraps(decorator)(adapt)
