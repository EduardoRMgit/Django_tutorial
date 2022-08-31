# Se elimina de spei/models/recevirs.py
# Codigo que estaba provocando probnlemas al momento de
# modificar las transacaciones en STP Transacciones
# Seadjunta Codigo ****************************************
# @receiver(post_save, sender=stp_transaction_reviewed)
# def stp_transaction_pago(sender, transaccion, **kwargs):
#     """
#         Este reciever nunca es utilizado, se podra llamar en el futuro para
#         pedir ejecucion de un pago
#
#     """
#
#     stpTransList = StpTransaction.objects.get(transaccion=transaccion)
#     if stpTransList:
#         stpTrans = stpTransList[0]
#         stpTrans.transaccion = transaccion
#         stpTrans.save()
#         stpTrans.pago()
#     else:
#         print('oops... no stp transaccion associated to '+str(transaccion))
#
#
# def is_number(s):
#     try:
#         float(s)
#         return True
#     except ValueError:
#         return False
# **************************************************
# Se quita try debido a un cambion en el admin se  deja en mugres
# la ruta de done se elimina es.
# root:cactus/spei/models.py  line 160    PR:erroresadminbanca
# try:
#     err = ErroresTransaccion.objects.get(codigo=self.stpId)
# except Exception as e:
#     print(e)
#     err = ErroresTransaccion.objects.get(codigo=0)
# *************************************************************
