import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

from webapp_auth import WebappAuth, RequestRedirect, HttpException
from gaema import auth

class GoogleAuth(WebappAuth, auth.GoogleMixin):
    pass


class BaseHandler(webapp.RequestHandler):
    def render_template(self, filename, **template_vals):
        path = os.path.join(os.path.dirname(__file__), 'templates', filename)
        self.response.out.write(template.render(path, template_vals))


class MainHandler(BaseHandler):
    def get(self):
        self.render_template('index.html', user=None,
            current_url=self.request.url)


class LoginHandler(BaseHandler):
    def get(self):
        google_auth = GoogleAuth(self)

        try:
            if self.request.GET.get("openid.mode", None):
                google_auth.get_authenticated_user(self._on_auth)
                return

            google_auth.authenticate_redirect()
        except RequestRedirect, e:
            return self.redirect(e.url, permanent=True)

        self.render_template('index.html', user=None)

    def _on_auth(self, user):
        """This function is called immediatelly after an authentication attempt.
        Use it to save the login information in a session or secure cookie.

        :param user:
            A dictionary with user data if the authentication was successful,
            or ``None`` if the authentication failed.
        """
        if user:
            # Authentication was successful. Create a session or secure cookie
            # to keep the user logged in.
            pass
        else:
            # Login failed. Show an error message or do nothing.
            pass

        # After cookie is persisted, redirect user to the original URL, using
        # the home page as fallback.
        self.redirect(self.request.GET.get('redirect', '/'))


application = webapp.WSGIApplication(
    [
        ('/', MainHandler),
        ('/login', LoginHandler),
    ],
    debug=True
)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
