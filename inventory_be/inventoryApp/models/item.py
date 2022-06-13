from django.db import models


class Item(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField('name',max_length=100)
    evidence = models.ImageField(upload_to='evidence', null=True, blank=True)

    def __str__(self):
        return str(self.id) + ' ' + str(self.name) + ' ' + str(self.evidence)
