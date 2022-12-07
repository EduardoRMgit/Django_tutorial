import datetime
import re
import logging
from demograficos.utils.stringNormalize import normalize
from renapo.models import Renapo
from django.db import models
from django.contrib.auth.models import User
from demograficos.models.userProfile import (RespuestaSeguridad,
                                             StatusRegistro,
                                             UserProfile)
from demograficos.models.telefono import Telefono
from demograficos.models.adminUtils import adminUtils
from renapo.renapo_call import check_renapo
from django.forms import ValidationError
from django.dispatch import receiver
from django.db.models.signals import post_save
from demograficos.models.location import UDevice
from .documentos import sendOCR


db_logger = logging.getLogger("db")


"""definir aqui todos lo criterios de validación , dependiendo del campo"""
"""Usar infovalidator en cada mutation de user para validar
e.g approved = InfoValidator.test(nip) , if approved setear el componente"""


def register_device(user):
    try:
        uuid = user.location.last().device.uuid
    except Exception as e:
        msg = "[Register device] Fallo al obtener el uuid. Error: {} \
            .".format(e)
        db_logger.error(msg)
    UDevice.objects.filter(user=user).exclude(uuid=uuid).update(activo=False)
    device, created = UDevice.objects.get_or_create(uuid=uuid, activo=True)
    if not created:
        other = device.user
        if other == user:
            return
        if other.is_active:
            raise Exception('dispositivo ocupado por usuario activo')
        device.activo = False
        device = UDevice.objects.create(uuid=uuid, user=user)
        print('dispositivo {} se ha asignado al usuario {}'.format(uuid, user))
        return
    device.user = user
    device.save()
    print('dispositivo {} se ha registrado por el usuario {}'.format(uuid,
        user))


class InfoValidator(models.Model):
    NP = 'NP'
    IP = 'IP'
    BN = 'BN'
    IN = 'IN'
    DR = 'DIR'
    TEL = 'TEL'
    CBN = 'CBN'
    info_choices = (
        (NP, 'NIP'),
        (IP, 'Info personal'),
        (BN, 'Beneficiario'),
        (IN, 'INE'),
        (TEL, 'telefono'),
        (CBN, 'CreateBeneficiario')
        )

    @classmethod
    def setComponentValidated(cls, alias, user, valid, motivo=''):
        profile_component = ProfileComponent.objects.get(alias=alias)
        component_validated = ComponentValidated.objects.get(
                            user=user,
                            component=profile_component
                            )
        if valid:
            # print('setting checkpoint '+alias)
            component_validated.status = ComponentValidated.VALID
            component_validated.motivo_invalido = ''
        else:
            component_validated.motivo_invalido = motivo
            flag = adminUtils.objects.get(util='ApplyValidation').activo
            if flag or alias != 'InfoPersonal':
                component_validated.status = ComponentValidated.INVALID
            elif (motivo == 'curp inválido, rfc inválido, ' or
                  motivo == 'curp inválido, ' or
                  motivo == 'rfc inválido, '):
                component_validated.status = ComponentValidated.VALID
            else:
                component_validated.status = ComponentValidated.INVALID
        component_validated.save()

    @staticmethod
    def CURPValidado(curp, user):

        nombre = normalize(user.first_name.upper())
        a_paterno = normalize(user.last_name.upper())
        a_materno = normalize(user.Uprofile.apMaterno.upper())
        curp = curp.upper()

        fNacimiento = str(user.Uprofile.fecha_nacimiento).split('-')
        año = fNacimiento[0]
        mes = fNacimiento[1]
        dia = fNacimiento[2]
        nacimiento = "{}/{}/{}".format(dia, mes, año)

        data, mensaje = check_renapo(curp)
        valida = True

        try:
            if data:

                nombre_renapo = normalize(data['nombre_renapo'])
                ap_pat_renapo = normalize(data['ap_pat_renapo'])
                ap_mat_renapo = normalize(data['ap_mat_renapo'])
                fechNac_renapo = data['fechNac_renapo']

                if nombre != nombre_renapo:
                    valida = False
                    mensaje = "Nombre no coincide con la \
                        consulta a RENAPO"
                if a_paterno != ap_pat_renapo:
                    valida = False
                    mensaje = "Apellido paterno no coincide con la \
                        consulta a RENAPO"
                if a_materno != ap_mat_renapo:
                    valida = False
                    mensaje = "Apellido materno no coincide con la \
                        consulta a RENAPO"
                if nacimiento != fechNac_renapo:
                    valida = False
                    mensaje = "Fecha de nacimiento no coincide con la \
                        consulta a RENAPO"
                existe = Renapo.objects.filter(user=user)
                if not existe:
                    Renapo.objects.create(
                        user=user,
                        curp=curp,
                        renapo_resp=data,
                        renapo_nombre=nombre_renapo,
                        renapo_ap_pat=ap_pat_renapo,
                        renapo_ap_mat=ap_mat_renapo,
                        renapo_nacimiento=fechNac_renapo,
                        exitoso=valida,
                        msjError=mensaje
                    )
                else:
                    consulta = existe.first()
                    consulta.curp = curp
                    consulta.renapo_resp = data
                    consulta.renapo_nombre = nombre_renapo
                    consulta.renapo_ap_pat = ap_pat_renapo
                    consulta.renapo_ap_mat = ap_mat_renapo
                    consulta.renapo_nacimiento = fechNac_renapo
                    consulta.exitoso = valida
                    consulta.msjError = mensaje
                    consulta.save()
            else:
                valida = False
                if not existe:
                    Renapo.objects.create(
                        user=user,
                        curp=curp,
                        renapo_resp=data,
                        exitoso=valida,
                        msjError=mensaje
                    )
                else:
                    consulta = existe.first()
                    consulta.curp = curp
                    consulta.renapo_resp = data
                    consulta.exitoso = valida
                    consulta.msjError = mensaje
                    consulta.save()
            return valida, mensaje
        except Exception as ex:
            db_logger = logging.getLogger('db')
            mensaje = "[CONSULTA CURP RENAPO] Falló la validación. Error: \
                {} / mensaje: {} / valida: {}.".format(ex, mensaje, valida)
            db_logger.error(mensaje)

    @staticmethod
    def RFCValidado(rfc, user):

        """pasamos rfc a uppercase y comparamos con el patrón reggex"""
        pattern = re.compile(r'^([A-ZÑ&]{3,4})?(?:- ?)?(\d{2}(?:0[1-9]'
                             r'|1[0-2])(?:0[1-9]|[12]\d|3[01]))?(?:- ?)'
                             r'?([A-Z\d]{2})([A\d])')
        result = re.match(pattern, rfc)
        if not result:
            print('formato de rfc invalido')
            print(result)
            return False
        rfc = result.group()
        rfc_, digit = rfc[:-1], rfc[-1]
        length = len(rfc_)
        dict_ = '0123456789ABCDEFGHIJKLMN&OPQRSTUVWXYZ Ñ'
        indice = length + 1
        if length == 12:
            suma = 0
        else:
            suma = 481
        for i in range(0, length):
            suma += dict_.index(rfc_[i]) * (indice - i)

        digitoEsperado = 11 - suma % 11
        if digitoEsperado == 11:
            digitoEsperado = 0
        elif digitoEsperado == 10:
            digitoEsperado = "A"
        digitoEsperado = str(digitoEsperado)
        if digit != digitoEsperado:
            if rfc_ + digit != "XAXX010101000":
                print('digito verificador de rfc no es consistente')
                return False
        return rfc_ + digit

    @classmethod
    def get_postcode_validator(cls, country_code):
        if country_code == 'GB':
            country_code = 'UK'
        module_path = 'django.contrib.localflavor.%s' % country_code.lower()
        try:
            module = __import__(module_path, fromlist=['forms'])
        except ImportError:
            # No forms module for this country
            return lambda x: x

        fieldname_variants = ['%sPostcodeField',
                              '%sPostCodeField',
                              '%sPostalCodeField',
                              '%sZipCodeField']
        for variant in fieldname_variants:
            fieldname = variant % country_code.upper()
            if hasattr(module.forms, fieldname):
                return getattr(module.forms, fieldname)().clean
        return lambda x: x

    @classmethod
    def CPValidado(cls, cp, country_code):
        try:
            cls.get_postcode_validator(country_code)(cp)
        except ValidationError:
            return False
        return True

    @staticmethod
    def setCheckpoint(**kwargs):
        user = kwargs['user']
        concepto = kwargs['concepto']
        motivo = ''
        valid = True
        print('try setting checkpoint '+concepto+' for user '+user.username)
        if concepto == 'NIP':
            """verficar que sean exactamente 6 digitos """
            """checar que haya 2 respsde seguridad y exactamete 1 tipo np"""
            alias = 'NIP Asignado'
            nip_activo = user.Uprofile.statusNip == 'A'
            res = RespuestaSeguridad.objects.filter(user=user)
            resNip = res.filter(tipo_nip=True)
            print(user.Uprofile.statusNip)
            if not nip_activo:
                motivo += 'nip inactivo ,'
                valid = False
            if not res.count() == 2:
                motivo += ('no hay dos respuestas de seguridad'
                           'asociadas al usuario ,')
                # valid = False
            if not resNip.count() == 1:
                motivo += 'no hay exactamente una pregunta de ' \
                    'seguridad asociada al nip'
                # valid = False
        elif concepto == 'IP':
            alias = "InfoPersonal"
            uProfile = user.Uprofile
            fecha_nacimiento = uProfile.fecha_nacimiento
            curp = uProfile.curp
            rfc = uProfile.rfc
            mensajeCurp = ""
            try:
                año_nacimiento = fecha_nacimiento.year
            except Exception:
                valid = False
                motivo += 'no se envio fecha de nacimiento, '
                InfoValidator.setComponentValidated(alias, user, valid, motivo)
                print(motivo)
                return
            mes = fecha_nacimiento.month
            edad = datetime.date.today().year - año_nacimiento
            if datetime.date.today().month < mes:
                edad -= 1
            if curp:
                if not (InfoValidator.CURPValidado(curp, user))[0]:
                    valid = False
                    motivo += 'curp inválido'
                else:
                    mensajeCurp = "curp validado"
            if rfc:
                if not InfoValidator.RFCValidado(rfc, user):
                    valid = False
                    motivo += 'rfc inválido, '
                else:
                    print(motivo)
            """deberiamos verficar INE async ?"""
            if not (edad > 10 and edad <= 100):
                valid = False
                motivo += 'edad inválida'
            InfoValidator.setComponentValidated(alias, user, valid, motivo)
            return mensajeCurp
        elif concepto == 'DIR':
            """verif c_postal"""
            alias = 'direccion'
            cp = kwargs['data']['codPostal']
            country_code = kwargs['data']['country']
            if not InfoValidator.CPValidado(cp, country_code):
                valid = False
                motivo += 'CP inválido'
        elif concepto == 'BN':
            alias = 'Beneficiarios'
            valid = True
            # totalPartipacion = 0
            # for b in beneficiarios:
            #     # print('nombre : {}'.format(b.nombre))
            #     # print('participacion :{}'.format(b.participacion))
            #     # print('activo : {}'.format(b.activo))
            #     totalPartipacion += b.participacion
            # if totalPartipacion < 100:
            #     # print('participacion no da el 100')
            #     motivo += 'participacion {} no suma 100%'.format(
            #                                                   totalPartipacion)
            #     valid = False
            # elif totalPartipacion > 100:
            #     motivo += 'participacion {} excede al 100%'.format(
            #                                                   totalPartipacion)
            #     valid = False
        elif concepto == 'CBN':
            alias = 'CreateBeneficiario'
        elif concepto == "TEL":
            alias = 'telefono'
            telefonos = Telefono.objects.filter(user=user)
            valid = False
            for tel in telefonos:
                valid = valid or tel.activo

            if not valid:
                motivo += "Telefono no verificado"
            if kwargs.get('register'):
                try:
                    register_device(user=user)
                except Exception as e:
                    motivo += str(e)
                    valid = False
                    InfoValidator.setComponentValidated(alias,
                                                        user,
                                                        valid,
                                                        motivo)
                    raise Exception(e)
        elif concepto == 'UUID':
            alias = 'dispositivo'
            try:
                register_device(user=user)
            except Exception as e:
                motivo += str(e)
                InfoValidator.setComponentValidated(
                    alias='dispositivo',
                    user=user,
                    valid=False,
                    motivo=motivo
                )
                msg = "[Enrolamiento] Falla al usar register_device en set \
                    checkpoint con alias 'dispositivo'. Error: {}".format(e)
                db_logger.error(msg)
                raise Exception(e)

        elif concepto == 'bloqueo':
            alias = 'bloqueo'

        InfoValidator.setComponentValidated(alias, user, valid, motivo)


class ProfileComponent(models.Model):
    indice = models.IntegerField(default=0)
    alias = models.CharField(max_length=32)
    rn_screen = models.CharField(max_length=32)
    verified_status = models.ManyToManyField(
        User,
        through='ComponentValidated',
        through_fields=('component', 'user', 'status')
    )
    default_status = models.CharField(max_length=32, null=True, blank=True)

    def __str__(self):
        return self.alias


class ComponentValidated(models.Model):
    EMPTY = 'EP'
    INVALID = 'IN'
    VALID = 'VA'
    STATUS_OPTIONS = (
        (EMPTY, 'Empty'),
        (INVALID, 'Invalid'),
        (VALID, 'Valid')
    )
    motivo_invalido = models.CharField(max_length=255, blank=True, null=True)
    component = models.ForeignKey(ProfileComponent, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=2,
                              choices=STATUS_OPTIONS,
                              null=True,
                              blank=True,
                              )

    def __str__(self):
        return 'user {}, component: {}, status: {}'.format(
                                            self.user,
                                            self.component.alias, self.status)

    # def save(self, *args, **kwargs):
    #     if not self.pk:
    #         # means object is being created, i.e not in database
    #         if self.component.default_status:
    #             self.status = self.component.default_status
    #     super(ComponentValidated, self).save(*args, **kwargs)


@receiver(post_save, sender=ComponentValidated)
def status_registro(sender, instance, created, **kwargs):

    qs = ComponentValidated.objects.filter(user=instance.user)
    print(qs.__dict__)
    completo = True
    for check in qs:
        if check.status != 'VA':
            print("check: ", check, check.status)
            completo = False
    if completo:
        print("COMPLETO!")
        UserProfile.objects.filter(user=instance.user.id).update(
            statusRegistro_id=15)
        return

    if instance.component.indice == 5 and instance.status == 'VA':
        id_status = StatusRegistro.objects.filter(codigo='15').first().id
        UserProfile.objects.filter(user=instance.user.id).update(
            statusRegistro=id_status)
    if instance.component.indice == 1 and instance.status == 'VA':
        id_status = StatusRegistro.objects.filter(codigo='01').first().id
        UserProfile.objects.filter(user=instance.user.id).update(
            statusRegistro=id_status)
    if instance.component.indice == 3 and instance.status == 'VA':
        # Código 02 = DATOS DE COMPROBANTE CAPTURADOS
        id_status = StatusRegistro.objects.filter(codigo='02').first().id
        UserProfile.objects.filter(user=instance.user.id).update(
            statusRegistro=id_status)
    if instance.component.indice == 2 and instance.status == 'VA':
        id_status = StatusRegistro.objects.filter(codigo='06').first().id
        UserProfile.objects.filter(user=instance.user.id).update(
            statusRegistro=id_status)


@receiver(post_save, sender=User)
@receiver(post_save, sender=ProfileComponent)
def populate_profile_validation(sender, instance, created, **kwargs):
    if created:
        if sender == User:
            user = instance
            profileComponents = ProfileComponent.objects.all()
            for c in profileComponents:
                print('adding user to component')
                status = c.default_status
                c.verified_status.add(
                                        user,
                                        through_defaults={'status': status})
                c.save()

        elif sender == ProfileComponent:
            # print('component created')
            c = instance
            users = User.objects.all()
            for user in users:
                status = c.default_status
                c.verified_status.add(user,
                                      through_defaults={'status': status})
            c.save()


@receiver(post_save, sender=ComponentValidated)
def set_validation_flags(sender, instance, created, **kwargs):
    print(instance)
    if not created:
        if instance.status == 'VA':
            user = instance.user.Uprofile
            component = instance.component.alias
            if 'direccion' in component:
                user.validacion_direccion = True
                sendOCR(user.user)
            elif 'telefono' in component:
                user.validacion_telefono = True
            elif 'Info' in component:
                user.validacion_perfil = True
            user.save()


class InvalidatedToken(models.Model):

    key = models.CharField(max_length=255)

    def __str__(self):
        return self.key
