from django.contrib.auth.models import User


class HeroProxy(User):

    class Meta:
        proxy = True

class HeroProxy2(User):

    class Meta:
        proxy = True
