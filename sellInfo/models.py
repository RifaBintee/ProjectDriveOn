from django.contrib.auth.models import User
from django.db import models

from carInfo.models import Selling_Car


# Create your models here.

class Sell_Car_Record(models.Model):
    sell_car_id = models.ForeignKey(Selling_Car, on_delete=models.DO_NOTHING)
    user_profile = models.ForeignKey(User, on_delete=models.CASCADE)