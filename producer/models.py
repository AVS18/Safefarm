from django.db import models
from base.models import User
import datetime
# Create your models here.
class Product(models.Model):
    name=models.CharField(max_length=200)
    image=models.ImageField(upload_to='product_images')
    ptype=models.CharField(max_length=20,choices=(('Pulses','Pulses'),('Grains','Grains'),('Vegetables','Vegetables')))
    quantity=models.IntegerField()
    ready_to_dispatch=models.BooleanField()
    usual_deliver_time=models.IntegerField(default=5)
    added_by=models.ForeignKey(User,on_delete=models.CASCADE)
    added_on=models.DateTimeField(auto_now_add=True)
    cost = models.IntegerField(default=100)