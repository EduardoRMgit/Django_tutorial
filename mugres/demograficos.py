# Codigo eliminado para que no se muestre Prospecto RAW y deposito RAW
# La ruta en la cual se quito este codigo es la siguiente
# ***************************************************+***************
# Se quita el registro  de admin
# root:demograficos/admin/modelosNoregitrados
# Se quita el codigo de modelos   root:demograficos/models/calculoDeLines
# Tambien se quita del init root:demograficos/models/__int__.py
# class DepositosRaw(models.Model):
#     identificador = models.IntegerField()
#     fecha = models.DateField()
#     importe = models.FloatField()
#     Tarjeta = models.IntegerField()
#     # prospecto = models.ForeignKey(Prospectos, on_delete=models.CASCADE)
#
#     class Meta:
#         verbose_name_plural = 'Depositos Raw'
#
#
# class ProspectosRaw(models.Model):
#     depositosID = models.IntegerField()
#
#     class Meta:
#         verbose_name_plural = 'Prospectos Raw'
# ******************************************************************
# Se quita nip temporal de userProfile
# root:demograficos/models/userProfile
# class NipTemporal(models.Model):
#
#     user = models.ForeignKey(
#         User,
#         related_name='user_nipTemp',
#         on_delete=models.CASCADE,
#         blank=True,
#         null=True
#     )
#     fecha = models.DateTimeField(default=timezone.now)
#     nip_temp = models.CharField(max_length=6, blank=True, null=True)
#     attempts = models.PositiveSmallIntegerField(default=0, blank=True,
#                                                 null=True)
#     activo = models.BooleanField(default=True)
#
#     def save(self, check=None, *args, **kwargs):
#         if check is None:
#             self.nip_temp = randint(100000, 999999)
#             super().save(*args, **kwargs)
#
#     def __str__(self):
#         return str(self.fecha)
# **********************************************************************
# se elimina nip temporal de root:
