# -*- coding: utf-8 -*-

"""
kay.ext.gaema.decorators

:Copyright: (c) 2009 Takashi Matsuo <tmatsuo@candit.jp>
                     All rights reserved.
:license: BSD, see LICENSE for more details.
"""

import logging
from functools import update_wrapper

from django.core.urlresolvers import reverse
from django.http import HttpResponseServerError
from django.shortcuts import redirect
from django.utils.http import urlquote_plus

from gaema.utils import (
  get_gaema_user, create_gaema_login_url, create_marketplace_login_url,
  get_valid_services,
  local,
)
from gaema.services import (
  GOOG_OPENID, GOOG_HYBRID, TWITTER, FACEBOOK,
)

from gaema.utils import auto_adapt_to_methods

def create_inner_func_for_auth(func, *targets):
  def inner(request, *args, **kwargs):
    local.request = request
    for service in targets:
      result = get_gaema_user(service)
      if isinstance(result, HttpResponseServerError):
        return result
      if result:
        return func(request, *args, **kwargs)
    return redirect(reverse("gaema.views.select_service",
                                kwargs=dict(
                                  targets='|'.join(targets)))\
                    #+"?next_url="+urlquote_plus(request.build_absolute_uri())
                    )
  return inner

def gaema_login_required(*services):
  def outer(func):
    inner = create_inner_func_for_auth(func, *services)
    update_wrapper(inner, func)
    return inner
  return auto_adapt_to_methods(outer)

def marketplace_login_required(func):
  def inner(request, *args, **kwargs):
    if get_gaema_user(kwargs['domain_name']):
      return func(request, *args, **kwargs)
    return redirect(create_marketplace_login_url(kwargs['domain_name'],
                                                 nexturl=request.url))
  return inner

marketplace_login_required = auto_adapt_to_methods(marketplace_login_required)
