from django.db import models

from users.models import User


class ProductCategory(models.Model):
    name = models.CharField(max_length=128, null=False, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name



class Product(models.Model):
    name = models.CharField(max_length=256, null=False)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=256, decimal_places=2)
    image = models.ImageField(upload_to='products_images')
    quantity = models.PositiveIntegerField()
    category = models.ForeignKey(to=ProductCategory, on_delete=models.CASCADE)

    def __str__(self):
        return f"Name : {self.name} | Category : {self.category}"


class BasketQueryset(models.QuerySet):

    def total_sum(self):
        return sum(basket.sum() for basket in self)

    def total_quantity(self):
        return sum(basket.quantity for basket in self)


class Basket(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    creating_date = models.DateTimeField(auto_now_add=True)

    objects = BasketQueryset.as_manager()

    def __str__(self):
        return f"Basket of {self.user.username} | {self.product.name}"

    def sum(self):
        return self.quantity * self.product.price

