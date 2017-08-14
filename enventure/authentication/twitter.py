"""
Twitter OAuth1 backend, docs at:
    http://psa.matiasaguirre.net/docs/backends/twitter.html
"""
from social.backends.oauth import BaseOAuth1,AuthTokenError,OAuth1
from social.exceptions import AuthCanceled
from social.utils import url_add_parameters, parse_qs, handle_http_errors
from oauthlib.oauth1 import SIGNATURE_TYPE_AUTH_HEADER
import six


class TwitterOAuth(BaseOAuth1):
    """Twitter OAuth authentication backend"""
    name = 'twitter'
    EXTRA_DATA = [('id', 'id')]
    REQUEST_TOKEN_METHOD = 'POST'
    ACCESS_TOKEN_METHOD = 'POST'
    AUTHORIZATION_URL = 'https://api.twitter.com/oauth/authenticate'
    REQUEST_TOKEN_URL = 'https://api.twitter.com/oauth/request_token'
    ACCESS_TOKEN_URL = 'https://api.twitter.com/oauth/access_token'
    REDIRECT_STATE = True

    def process_error(self, data):
        if 'denied' in data:
            raise AuthCanceled(self)
        else:
            super(TwitterOAuth, self).process_error(data)


    def oauth_auth(self, token=None, oauth_verifier=None,
                   signature_type=SIGNATURE_TYPE_AUTH_HEADER):
       
        key, secret = self.get_key_and_secret()
        oauth_verifier = oauth_verifier or self.data.get('oauth_verifier')
        if token:
            if token.get("oauth_token") and (not token.get("oauth_token_secret")):
                resource_owner_key,resource_owner_secret = token.get("oauth_token").split("&oauth_token_secret=")
            else:    
                resource_owner_key = token.get('oauth_token') 
                resource_owner_secret = token.get('oauth_token_secret') 
            if not resource_owner_key:
                raise AuthTokenError(self, 'Missing oauth_token')
            if not resource_owner_secret:
                raise AuthTokenError(self, 'Missing oauth_token_secret')
        else:
            resource_owner_key = None
            resource_owner_secret = None
        # decoding='utf-8' produces errors with python-requests on Python3
        # since the final URL will be of type bytes
        decoding = None if six.PY3 else 'utf-8'
        state = self.get_or_create_state()
        return OAuth1(key, secret,
                      resource_owner_key=resource_owner_key,
                      resource_owner_secret=resource_owner_secret,
                      callback_uri=self.get_redirect_uri(state),
                      verifier=oauth_verifier,
                      signature_type=signature_type,
                      decoding=decoding)

    def get_user_details(self, response):
        """Return user details from Twitter account"""
        #import pdb;pdb.set_trace()
        fullname, first_name, last_name = self.get_user_names(response.get('name',""))
        return {'username': response.get('screen_name',""),
                'email': response.get('email', ''),
                'fullname': fullname,
                'first_name': first_name,
                'last_name': last_name}

    def user_data(self, access_token, *args, **kwargs):
        """Return user data provided"""
        return self.get_json('https://api.twitter.com/1.1/account/verify_credentials.json',params={'include_email': 'true'},auth=self.oauth_auth(access_token))
