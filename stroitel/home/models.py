from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Bid(models.Model):
    smeta_path = models.CharField(max_length=255, null=True)
    number_phones = models.CharField(max_length=12)
    communication_method = models.CharField(max_length=50)
    people = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    data_of_bid = models.DateField(auto_now=True)

    def __str__(self):
        return self.smeta_path


