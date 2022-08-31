from banca.models.catalogos import TipoTransaccion
from banca.models.transaccion import Transaccion, StatusTrans

from django.dispatch import receiver
from django.db.models.signals import post_save
from pagos.rapydcollect.models import Payment


@receiver(post_save, sender=Payment)
def rapyd_to_stptransaction(sender, instance, created, **kwargs):
    tipo = TipoTransaccion.objects.get(codigo=7)
    status = StatusTrans.objects.get(nombre="esperando respuesta")

    if (created):
        Transaccion.objects.create(
            user=instance.user,
            fechaValor=instance.fechaPago,
            monto=float(instance.amount),
            concepto=instance.description,
            tipoTrans=tipo,
            statusTrans=status,
            claveRastreo=instance.claveRastreoR
        )
