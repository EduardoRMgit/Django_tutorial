from rest_framework import exceptions
from rest_framework.authentication import (TokenAuthentication,
                                           get_authorization_header)

from django.utils.translation import gettext_lazy as _


class TokenAuthenticationMulti(TokenAuthentication):
    """
    Simple token based authentication.

    Clients should authenticate by passing the token key in the "Authorization"
    HTTP header, prepended with the string "Token ". It looks for "Token" in
    any pair position (when split by spaces) in the Authorization Header.
    For example:

        Authorization: Basic OAdsoifjoiwdfmdw Token 401f7ac837da42b97f613d789819ff93537bee6a  # noqa: E501
    """
    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth:
            return None

        token_ind = 0
        for i in range(1, len(auth)):
            j = i - 1

            if j % 2 == 0:
                if auth[j].lower() == self.keyword.lower().encode():
                    token_ind = i

        if token_ind == 0:
            return None

        if len(auth) == 1:
            msg = _('Invalid token header. No credentials provided.')
            raise exceptions.AuthenticationFailed(msg)

        try:
            token = auth[token_ind].decode()
        except UnicodeError:
            msg = _('Invalid token header. Token string should ' +
                    'not contain invalid characters.')
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(token)
