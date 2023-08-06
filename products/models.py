import stripe
from django.conf import settings
from django.db import models

from users.models import User

stripe.api_key = settings.STRIPE_SECRET_KEY


class ProductCategory(models.Model):
    name = models.CharField(max_length=128, null=False, unique=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        app_label = 'products'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=256, null=False)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=256, decimal_places=2)
    image = models.ImageField(upload_to='products_images')
    quantity = models.PositiveIntegerField()
    stripe_product_price_id = models.CharField(max_length=128, null=True, blank=True)
    category = models.ForeignKey(to=ProductCategory, on_delete=models.CASCADE)

    class Meta:
        app_label = 'products'

    def __str__(self):
        return f"Name : {self.name} | Category : {self.category}"

    def save(
            self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if not self.stripe_product_price_id:
            stripe_product_price = self.stripe_product_creator()
            self.stripe_product_price_id = stripe_product_price['id']
        super(Product, self).save(force_insert=False, force_update=False, using=None, update_fields=None)

    def delete(self, using=None, keep_parents=False):
        if self.stripe_product_price_id:
            self.stripe_product_price_id = None
        super(Product, self).delete(using=None, keep_parents=False)

    def stripe_product_creator(self):
        stripe_product = stripe.Product.create(name=self.name)
        stripe_product_price = stripe.Price.create(
             product=stripe_product['id'],
             unit_amount=round(self.price) * 100,
             currency='usd')
        return stripe_product_price


class BasketQueryset(models.QuerySet):
    class Meta:
        app_label = 'products'

    def total_sum(self):
        return sum(basket.sum() for basket in self)

    def total_quantity(self):
        return sum(basket.quantity for basket in self)


class Basket(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    creating_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'products'

    objects = BasketQueryset.as_manager()

    def __str__(self):
        return f"Basket of {self.user.username} | {self.product.name}"

    def sum(self):
        return self.quantity * self.product.price

    def de_json(self):
        basket_item = {
            'product_name': self.product.name,
            'quantity': self.quantity,
            'price': float(self.product.price),
            'sum': float(self.sum()),
        }
        return basket_item
