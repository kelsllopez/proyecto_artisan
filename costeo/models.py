from django.db import models


# clase para ingresar permisos al sistema

class CosteoPermisos(models.Model):

    class Meta:

        managed = False

        default_permissions = ()

        permissions = (
            ('listar', 'Permite listar los costeos'),
        )
