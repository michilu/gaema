# -*- coding: utf-8 -*-

"""
kay.ext.gaema.urls

:Copyright: (c) 2009 Takashi Matsuo <tmatsuo@candit.jp>
                     All rights reserved.
:license: BSD, see LICENSE for more details.
"""

from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'login/(?P<service>\w+)', 'gaema.views.login'),
    (r'logout/(?P<service>\w+)', 'gaema.views.logout'),
    (r'marketplace_login/a/(?P<domain>\w+)', 'gaema.views.marketplace_login'),
    (r'marketplace_logout/(?P<domain>\w+)', 'gaema.views.marketplace_logout'),
    (r'select_service/(?P<targets>\w+)', 'gaema.views.select_service'),
)
