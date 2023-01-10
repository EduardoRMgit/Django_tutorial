from django.contrib.auth import get_user_model
from demograficos.models.telefono import Telefono
from django.contrib.auth.backends import ModelBackend
from django.http import JsonResponse


class EmailBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is not None:
            UserModel = get_user_model()

            user = None
            try:
                """Primero buscamos por email."""
                user = UserModel.objects.get(email=username)
            except Exception:
                pass
            else:
                if user is not None:
                    if user.check_password(password) and user.is_active:
                        return user

            try:
                """Si no recuperamos al usuario, lo buscamos por username"""
                user = UserModel.objects.get(username=username)
            except Exception:
                pass
            else:
                if user is not None:
                    if user.check_password(password) and user.is_active:
                        return user

            try:
                """Finalmente, intentamos recuperarlo por telefono"""
                user = Telefono.objects.get(telefono=username).user
            except Exception:
                pass
            else:
                if user is not None:
                    if user.check_password(password) and user.is_active:
                        return user

        return None


def lockout(request, credentials, *args, **kwargs):
    return JsonResponse(
        {"status": "Cuenta bloqueada por exceso de intentos."},
        status=403)
