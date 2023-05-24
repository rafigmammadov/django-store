from django.db import models


class ProductCategory(models.Model):
    name = models.CharField(max_length=128, null=False, unique=True)
    description = models.TextField(null=True, blank=True)



class Product(models.Model):
    name = models.CharField(max_length=256, null=False)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=256, decimal_places=2)
    image = models.ImageField(upload_to='products_images')
    quantity = models.PositiveIntegerField()
    category = models.ForeignKey(to=ProductCategory, on_delete=models.CASCADE)
