from distutils.command.upload import upload
from email.policy import default
from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

from PIL import Image
from django.contrib.auth.models import User
from django.contrib.auth.base_user import BaseUserManager

from django.db.models import Sum



# Create your models here.
class Prices(models.Model):
    laundry_type = models.CharField(max_length=250)
    price = models.FloatField(max_length=15, default=0)
    status = models.CharField(max_length=2, choices=(('1','Active'), ('2','Inactive')), default = 1)
    delete_flag = models.IntegerField(default = 0)
    date_added = models.DateTimeField(default = timezone.now)
    date_updated = models.DateTimeField(auto_now = True)

    class Meta:
        verbose_name_plural = "List of Laundy Prices"

    def __str__(self):
        return str(f"{self.laundry_type}")

class Products(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField(blank= True, null= True)
    price = models.FloatField(max_length=15, default=0)
    status = models.CharField(max_length=2, choices=(('1','Active'), ('2','Inactive')), default = 1)
    delete_flag = models.IntegerField(default = 0)
    date_added = models.DateTimeField(default = timezone.now)
    date_updated = models.DateTimeField(auto_now = True)

    class Meta:
        verbose_name_plural = "List of Products"

    def __str__(self):
        return str(f"{self.name}")

    def available(self):
        try:
            stockin = StockIn.objects.filter(product__id = self.id).aggregate(Sum('quantity'))
            stockin = stockin['quantity__sum']
        except:
            stockin = 0
        try:
            stockout = LaundryProducts.objects.filter(product__id = self.id).aggregate(Sum('quantity'))
            stockout = stockout['quantity__sum']
        except:
            stockout = 0
        stockin = stockin if not stockin is None else 0
        stockout = stockout if not stockout is None else 0
        
        return float(stockin - stockout)
    


class StockIn(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.FloatField(default = 0)
    date_added = models.DateTimeField(default = timezone.now)
    date_updated = models.DateTimeField(auto_now = True)

    class Meta:
        verbose_name_plural = "List of Stock-In"

    def __str__(self):
        return str(f"{self.product}")

class Laundry(models.Model):
    code = models.CharField(max_length=100)
    client = models.CharField(max_length=250)
    contact = models.CharField(max_length=250, blank=True, null = True)
    total_amount = models.FloatField(max_length=15)
    tendered = models.FloatField(max_length=15)
    status = models.CharField(max_length=2, choices=(('0','Pending'), ('1', 'In-progress'), ('2', 'Done'), ('3', 'Picked Up')), default = 0)
    payment = models.CharField(max_length=2, choices=(('0','Unpaid'), ('1', 'Paid')), default = 0)
    date_added = models.DateTimeField(default = timezone.now)
    date_updated = models.DateTimeField(auto_now = True)

    class Meta:
        verbose_name_plural = "List of Laundries"

    def __str__(self):
        return str(f"{self.code} - {self.client}")

    def change(self):
        change = float(self.tendered) - float(self.total_amount)
        return change

    def totalItems(self):
        try:
            Items =  LaundryItems.objects.filter(laundry = self).aggregate(Sum('total_amount'))
            Items = Items['total_amount__sum']
        except:
            Items = 0
        return float(Items)
        
    def totalProducts(self):
        try:
            Products =  LaundryProducts.objects.filter(laundry = self).aggregate(Sum('total_amount'))
            Products = Products['total_amount__sum']
        except:
            Products = 0
        return float(Products)

class LaundryItems(models.Model):
    laundry = models.ForeignKey(Laundry, on_delete=models.CASCADE,related_name="laundry_fk")
    laundry_type = models.ForeignKey(Prices, on_delete=models.CASCADE,related_name="prices_fk")
    price = models.FloatField(max_length=15, default=0)
    weight = models.FloatField(max_length=15, default=0)
    total_amount = models.FloatField(max_length=15)
  

    class Meta:
        verbose_name_plural = "List of Laundry Items"

    def __str__(self):
        return str(f"{self.laundry.code} - {self.laundry_type.laundry_type}")


class LaundryProducts(models.Model):
    laundry = models.ForeignKey(Laundry, on_delete=models.CASCADE,related_name="laundry_fk2")
    product = models.ForeignKey(Products, on_delete=models.CASCADE,related_name="product_fk")
    price = models.FloatField(max_length=15, default=0)
    quantity = models.FloatField(max_length=15, default=0)
    total_amount = models.FloatField(max_length=15)
  

    class Meta:
        verbose_name_plural = "List of Laundry Products"

    def __str__(self):
        return str(f"{self.laundry.code} - {self.product.name}")
