from django.db import models

# Create your models here.

class Product_detail(models.Model):
    product_name = models.CharField(max_length=400)