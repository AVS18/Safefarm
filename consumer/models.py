from django.db import models
from base.models import User
from producer.models import Product
# Create your models here.
class Order(models.Model):
    producer=models.ForeignKey(User,related_name='producer',on_delete=models.DO_NOTHING)
    consumer=models.ForeignKey(User,related_name='consumer',on_delete=models.DO_NOTHING)
    quantity=models.IntegerField()
    value=models.IntegerField()
    status=models.CharField(max_length=20,choices=(('Pending','Pending'),('Approved','Approved'),('Rejected','Rejected'),('Dispatched','Dispatched'),('Delivered','Delivered')))
    product=models.ForeignKey(Product,on_delete=models.CASCADE,blank=True,null=True)
    tracking_id=models.CharField(max_length=100,null=True,blank=True)
    courier_name=models.CharField(max_length=200,null=True,blank=True)
    exp_delivery=models.DateField(blank=True,null=True)