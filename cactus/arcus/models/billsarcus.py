from django.db import models
from django.contrib.auth.models import User


class Bills(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             blank=True,
                             null=True,
                             related_name="user_bills")
    bill_id = models.IntegerField()
    account_number = models.CharField(max_length=100)
    monto = models.FloatField()

    def __str__(self):
        return self.user
