#  Lista de Medios disponibles que tiene el producto.
# Se elimina un archivo de banca/model el archivo se llama mediosDisponobles
# class MediosDisponibles(models.Model):
#
#     medio = models.CharField(max_length=200)
#     activo = models.BooleanField(default=True)
#
#     productos = models.ManyToManyField(Productos)
#
#     def __str__(self):
#         return self.medio
# ****************************************************************************

# **************************************************************************
# Se quita el modelo logExportado de la ruta banca/models/transaccion
# class LogExportadoTrans(models.Model):
#     transaccion = models.ForeignKey(
#         Transaccion,
#         on_delete=models.CASCADE,
#         related_name='transaccion_logExportadoTrans'
#     )
#     fechaExportacion = models.DateTimeField(blank=True, null=True)
#     referencia = models.CharField(max_length=120, blank=True, null=True)
#     fechaConfirmado = models.DateTimeField(blank=True, null=True)
#     fechaCobranza = models.DateTimeField(blank=True, null=True)
#     fechaConfirmadoCobranza = models.DateTimeField(blank=True, null=True)
#
#     class Meta():
#         verbose_name_plural = 'Logs de Transacciones'
#
#     def __str__(self):
#         return self.referencia
# ****************************************************************************
