from django.db import models
from django.utils import timezone
from .item import Item


class Report(models.Model):
    id = models.BigAutoField(primary_key=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    dateTime = models.DateTimeField(default= timezone.localdate())
    status = models.charField(max_length=10)
    observation = models.TextField(max_length=100)
    employee = models.charField(max_length=50)

    def __str__(self):
        return str(self.id) + ' ' + str(self.item) + ' ' + str(self.dateTime) + ' ' + str(self.status) + ' ' + str(self.observation) + ' ' + str(self.employee)
