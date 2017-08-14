# -*- coding: utf-8 -*-
import json

from braces.views import CsrfExemptMixin
from oauthlib.oauth2.rfc6749.endpoints.token import TokenEndpoint
from oauth2_provider.oauth2_backends import OAuthLibCore
from oauth2_provider.ext.rest_framework import OAuth2Authentication
from oauth2_provider.models import Application, AccessToken
from oauth2_provider.settings import oauth2_settings
from oauth2_provider.views.mixins import OAuthLibMixin
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_social_oauth2.oauth2_backends import KeepRequestCore
from rest_framework_social_oauth2.oauth2_endpoints import SocialTokenServer
from oauth2_provider.models import AccessToken
import serializers


class TokenView(CsrfExemptMixin, OAuthLibMixin, APIView):
    """
    Implements an endpoint to provide access tokens

    The endpoint is used in the following flows:

    * Authorization code
    * Password
    * Client credentials
    """
    server_class = oauth2_settings.OAUTH2_SERVER_CLASS
    validator_class = oauth2_settings.OAUTH2_VALIDATOR_CLASS
    oauthlib_backend_class = OAuthLibCore
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        # Use the rest framework `.data` to fake the post body of the django request.
        request._request.POST = request._request.POST.copy()
        for key, value in request.data.items():
            request._request.POST[key] = value

        url, headers, body, status = self.create_token_response(request._request)
        response = Response(data=json.loads(body), status=status)

        for k, v in headers.items():
            response[k] = v
        return response


class ConvertTokenView(CsrfExemptMixin, OAuthLibMixin, APIView):
    """
    Implements an endpoint to convert a provider token to an access token

    The endpoint is used in the following flows:

    * Authorization code
    * Client credentials
    """
    server_class = SocialTokenServer
    validator_class = oauth2_settings.OAUTH2_VALIDATOR_CLASS
    oauthlib_backend_class = KeepRequestCore
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        # Use the rest framework `.data` to fake the post body of the django request.
        request._request.POST = request._request.POST.copy()
       
        for key, value in request.data.items():
            if key in ["mobile","newsLetter","email","id"]:
                pass
            else:
                request._request.POST[key] = value

        url, headers, body, status = self.create_token_response(request._request)
        _data=eval(body)
        if _data.get("access_token",None):
            user = AccessToken.objects.get(token=_data["access_token"]).user
            _data["email"] = user.email
            _data["name"]  = user.name
            _data["id"] = 12
            


            _data["user"] = serializers.UserSerializer(user).data
            if request._request.GET.get("register",None):
                user.is_registered = True


                if request._request.POST.get("backend","") == "facebook":

                    if request._request.POST.get("newsLetter",None):
                        user.send_newsletter=True
                    

                       

                if request._request.POST.get("backend","") == "twitter":
                    if request._request.POST.get("newsLetter",None):
                        user.send_newsletter=True

                    if request._request.POST.get("mobile",None):
                        user.mobile=request._request.POST.get("mobile",None)
                    if request._request.POST.get("email",None):
                        user.mobile=request._request.POST.get("email",None)
                user.save()
            else:
                if (not user.is_registered) and request._request.POST.get("backend","") == "facebook":
                    _data["urb_code"] = "confirm_facebook_signup"
                    _data["facebook_user"] = dict(id=user.id,email=user.email,name=user.name)
                    status=403
                if (not user.is_registered) and  request._request.POST.get("backend","") == "twitter":
                    _data["urb_code"] = "confirm_twitter_signup"
                    _data["twitter_user"] = dict(id=user.id,email=user.email,name=user.name,mobile=user.mobile)
                    status=403

               
        response = Response(data=_data, status=status)

        for k, v in headers.items():
            response[k] = v
        #import pdb;pdb.set_trace()
        return response


class RevokeTokenView(CsrfExemptMixin, OAuthLibMixin, APIView):
    """
    Implements an endpoint to revoke access or refresh tokens
    """
    server_class = oauth2_settings.OAUTH2_SERVER_CLASS
    validator_class = oauth2_settings.OAUTH2_VALIDATOR_CLASS
    oauthlib_backend_class = OAuthLibCore
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        # Use the rest framework `.data` to fake the post body of the django request.
        request._request.POST = request._request.POST.copy()
        for key, value in request.data.items():
            request._request.POST[key] = value

        url, headers, body, status = self.create_revocation_response(request._request)
        response = Response(data=json.loads(body) if body else '', status=status if body else 204)

        for k, v in headers.items():
            response[k] = v
        return response


@api_view(['POST'])
@authentication_classes([OAuth2Authentication])
@permission_classes([permissions.IsAuthenticated])
def invalidate_sessions(request):
    client_id = request.POST.get("client_id", None)
    if client_id is None:
        return Response({
            "client_id": ["This field is required."]
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        app = Application.objects.get(client_id=client_id)
    except Application.DoesNotExist:
        return Response({
            "detail": "The application linked to the provided client_id could not be found."
        }, status=status.HTTP_400_BAD_REQUEST)

    tokens = AccessToken.objects.filter(user=request.user, application=app)
    tokens.delete()
    return Response({}, status=status.HTTP_204_NO_CONTENT)