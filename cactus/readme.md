#Ejecución de CreateTransaccion Mutation en GraphQL

## Url de GraphQL API
[Localhost](http://127.0.0.1:8000/graphql)

## Mutación 

Todo el esquema/lenguaje de GraphQL está basado en { }
Para crear una nueva transacción es necesario comenzar el query con el comando **mutation** seguido de la apertura de **{}** y el MutationType **createTransaccion**

Entre parentesis seguido **createTransaccion** se deben ingresar los argumentos sin ningún orden en particular a pasar a la función:

⋅⋅* monto
⋅⋅* comision
⋅⋅* comisionIVA
⋅⋅* pagadoMonto
⋅⋅* pagadoComision
⋅⋅* pagadoComisionIVA
⋅⋅* porcentajeComision
⋅⋅* porcentajeComisionIVA
⋅⋅* fechaLiquidacion
⋅⋅* producto_id
⋅⋅* statusTrans_id
⋅⋅* tipoAnual_id
⋅⋅* statusCobranza
⋅⋅* statusVencimiento

El usuario es sacado del contexto. **Requiere haber hecho login en el administrador**
[Login](http://127.0.0.1:8000/admin/)

## Respuesta del servidor
Una vez que se cierra los parentesis, se pueden volver a abrir { } y dentro se puede solicitar al servidor los datos que queremos de vuelta como el *id*, *fechaTrans*, etc.
Para ver las opciones, una vez dentro se puede dar el keyboard shortcut `CTRL + SPACE` para ver más opciones.

###Ejemplo
mutation{
  createTransaccion(monto:"15.0022", comision:"12", comisionIVA:"12", pagadoMonto:"23", pagadoComision: "1999", pagadoComisionIVA: "25", porcentajeComision:"12", porcentajeComisionIVA:"12", fechaLiquidacion: "2019-07-31T00:01:04+00:00", productoId:1, statusTransId:1, tipoAnualId:1, statusCobranza:"V", statusVencimiento:"v"){
    id
    fechaTrans
    monto
    user {
      id
      isSuperuser
      username
      email
    }
    comision
    pagadoMonto
    porcentajeComisionIVA
  }
}

####Respuesta
{
  "data": {
    "createTransaccion": {
      "id": 65,
      "fechaTrans": "2019-08-01T03:10:15.773855+00:00",
      "monto": "15.0022",
      "user": {
        "id": "1",
        "isSuperuser": true,
        "username": "javierpiedra",
        "email": "jpiedra@ppdc.mx"
      },
      "comision": "12",
      "pagadoMonto": "23",
      "porcentajeComisionIVA": "12"
    }
  }
}