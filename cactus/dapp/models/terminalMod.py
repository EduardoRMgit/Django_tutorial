from django.db import models


class Terminal(models.Model):

    class Meta:
        verbose_name_plural = "Terminal"

    employee = models.CharField(
        max_length=100,
        verbose_name="Empleado",
        null=False, blank=False
    )
    name = models.CharField(
        max_length=50,
        verbose_name="Nombre de terminal",
        null=False,
        blank=False
    )

    def __str__(self):
        return "{}{}".format(self.employee, self.name)
