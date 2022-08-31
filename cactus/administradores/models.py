from django.contrib.auth.models import User, UserManager, Group


class AdministradoreManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(is_superuser=False,
                                             is_staff=True)


class Administradore(User):
    objects = AdministradoreManager()

    class Meta:
        proxy = True


class Grupo(Group):

    class Meta:
        proxy = True
