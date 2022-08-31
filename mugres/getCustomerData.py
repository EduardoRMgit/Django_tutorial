from django.db import models

# Transfer?
class getCustomerData(models.Model):

    externalCustomerId = models.CharField(max_length=20, primary_key=True)
    returnCode = models.CharField(max_length=80)
    returnDescription = models.CharField(max_length=80)
    firstName = models.CharField(max_length=30)
    firstLastName = models.CharField(max_length=30)
    secondLastName = models.CharField(max_length=30)
    dateOfBirth = models.DateField(null=True)
    curp = models.CharField(max_length=16)
    msisdn = models.CharField(max_length=30)
    addressStreet = models.CharField(max_length=30)
    addressBuildingExternal = models.CharField(max_length=30)
    addressBuildingInternal = models.CharField(max_length=30)
    postalCode = models.CharField(max_length=10)
    addressNeighbourhood = models.CharField(max_length=30)
    addressLocation = models.CharField(max_length=30)
    addressState = models.CharField(max_length=30)
    cardNumber = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    cuentaHabiente = models.CharField(max_length=90)
