from functools import wraps

from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import gettext as _

from graphene.utils.thenables import maybe_thenable

from graphql_jwt import exceptions
from graphql_jwt import signals
from django.contrib.auth.models import User
from django.utils import timezone
from graphql_jwt.decorators import (csrf_rotation,
                                    setup_jwt_cookie,
                                    refresh_expiration,
                                    on_token_auth_resolve)


__all__ = [
    "token_auth",
]


def token_auth(f):
    @wraps(f)
    @setup_jwt_cookie
    @csrf_rotation
    @refresh_expiration
    def wrapper(cls, root, info, password, **kwargs):
        context = info.context
        context._jwt_token_auth = True
        username = kwargs.get(get_user_model().USERNAME_FIELD)

        user = authenticate(
            request=context,
            username=username,
            password=password,
        )

        if user is None:
            username_ = username
            try:
                log = User.objects.get(username=username_)
                intento = log.Uprofile.login_attempts + 1
                log.Uprofile.login_attempts = intento
                log.save()
                if log.Uprofile.login_attempts >= 5:
                    log.Uprofile.status = "B"
                    log.Uprofile.blocked_reason = "T"
                    log.Uprofile.blocked_date = timezone.now()
                    log.save()
                    return Exception("Cuenta Bloqueada")
                return exceptions.JSONWebTokenError(
                    _("Contraseña incorrecta"),
                )
            except Exception:
                pass
            # return Exception("Inactive user")
            raise exceptions.JSONWebTokenError(
                _("Please enter valid credentials"),
            )

        user.last_login = timezone.now()
        user.save()

        if hasattr(context, "user"):
            context.user = user

        result = f(cls, root, info, **kwargs)
        signals.token_issued.send(sender=cls, request=context, user=user)
        return maybe_thenable((context, user, result), on_token_auth_resolve)

    return wrapper
