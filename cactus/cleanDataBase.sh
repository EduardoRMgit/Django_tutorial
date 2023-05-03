#!/bin/bash
# #El archivo está ordenado especificamente para instalar primero las dependencias
# #Algunos campos están repetidos como user.json si se quiere hacer la instalación de sólo una de las aplicaciones
#

source autodeploy_env.sh

PROD=${PRODUCTION:-false}

if [[ $DELETE_DB == true ]] || [[ $PROD == false ]] ; then
  rm db.sqlite3
  rm -rf */__pycache__
  if [[ $PROD == true ]] ; then
    python drop_db.py;
  fi;
fi;

./manage.py check

if [[ $STATIC == true ]] ; then
  python manage.py collectstatic --noinput
fi;

if [[ $MIGRATIONS == true ]] || [[ $PROD == false ]] ; then
  ./manage.py makemigrations
  ./manage.py migrate

fi;

# Solo usar para migrar la base entera
# ./manage.py dumpdata > db.json
# ./manage.py loaddata db.json

if [[ $LOADDATA == true ]] || [[ $PROD == false ]] ; then
  #PLD
  ./manage.py loaddata urls.json
  ./manage.py loaddata adminUtils.json


  # #DEMOGRAFICOS
  ./manage.py shell < tests/perms.py
  ./manage.py loaddata nivelCuenta.json
  # ./manage.py loaddata user.json
  ./manage.py loaddata statusRegistro.json
  ./manage.py loaddata statusCuenta.json
  ./manage.py loaddata indiceDisponible.json
  ./manage.py loaddata docAdjuntoTipo.json
  # ./manage.py loaddata docAdjunto.json
  # ./manage.py loaddata userProfile.json
  # ./manage.py loaddata userNotas.json
  ./manage.py loaddata institucion.json
  ./manage.py loaddata tipoTelefono.json
  ./manage.py loaddata proveedorTelefonico.json
  # ./manage.py loaddata telefono.json
  ./manage.py loaddata statusTarjeta.json
  # ./manage.py loaddata tarjeta.json
  ./manage.py loaddata tipoDireccion.json
  ./manage.py loaddata entidad_federativa.json
  # ./manage.py loaddata direccion.json
  ./manage.py loaddata preguntas_secretas.json
  ./manage.py loaddata component.json
  # ./manage.py loaddata ssid.json
  # ./manage.py loaddata contactos.json
  ./manage.py loaddata adminUtils.json
  ./manage.py loaddata countries.json
  ./manage.py loaddata parentesco.json
  ./manage.py loaddata tipocomprobante.json
  ./manage.py loaddata transferenciasmensuales.json
  ./manage.py loaddata operacionesmensuales.json
  ./manage.py loaddata origendeposito.json
  ./manage.py loaddata usocuenta.json
  ./manage.py loaddata iguanofixture.json

  # BANCA
  # Catalogos
  ./manage.py loaddata carProducto.json
  ./manage.py loaddata paisesDisponibles.json
  ./manage.py loaddata statusTrans.json
  ./manage.py loaddata tipoAnual.json
  ./manage.py loaddata tipoTransaccion.json
  ./manage.py loaddata comision.json
  ./manage.py loaddata cami.json
  ./manage.py loaddata errorestransaccion.json
  ./manage.py loaddata codigoconfianza.json
  ./manage.py loaddata comisionstp.json

  # Transaccion
  # ./manage.py loaddata transaccion.json
  # ./manage.py loaddata transpago.json
  # ./manage.py loaddata transpagoExterno.json

  # Legal
  ./manage.py loaddata pdflegal.json

  # SPEI
  ./manage.py loaddata institutionbanjico.json
  # ./manage.py loaddata stptrans.json
  ./manage.py loaddata adminUtils.json

  # Contabilidad
  ./manage.py loaddata tipo_contable_cuenta.json
  ./manage.py loaddata contable_cuenta.json
  ./manage.py loaddata cuenta_tipo.json
  ./manage.py loaddata cuenta_saldo.json

  # SCOTIABANK
  ./manage.py loaddata catalogoCodigosTEF.json
  ./manage.py loaddata datosFijos.json

fi;

# CUSTOM SCRIPT
if [[ $CUSTOM_SHELL == true ]]; then
  source autodeploy_custom.sh;
fi;
