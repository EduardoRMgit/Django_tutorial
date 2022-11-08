from django.db import models


class Category(models.Model):

    class Meta:
        verbose_name_plural = "Categoria"

    category = models.IntegerField(
        verbose_name="Categoria",
        null=False,
        blank=False
    )
    name = models.CharField(
        max_length=100,
        verbose_name="Nombre",
        null=True,
        blank=True
    )

    def __str__(self):
        txt = "Cat: {} / Nombre: {} "
        return txt.format(self.category, self.name)
