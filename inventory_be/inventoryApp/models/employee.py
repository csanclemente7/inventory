from django.db import models


class Employee(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField('name',max_length=500)

    def __str__(self):
        return str(self.id) + ' ' + str(self.name)
