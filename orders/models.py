from django.db import models

from products.models import Basket
from users.models import User


class Order(models.Model):

    CREATED = 0
    PAID = 1
    ON_WAY = 2
    DELIVERED = 3

    STATUSES = (
        (CREATED, 'Created'),
        (PAID, 'Paid'),
        (ON_WAY, 'On Way'),
        (DELIVERED, 'Delivered'),
    )


    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.EmailField(max_length=256)
    address = models.CharField(max_length=256)
    basket_history = models.JSONField(default=dict)
    created = models.DateTimeField(auto_now_add=True)
    status = models.SmallIntegerField(default=CREATED, choices=STATUSES)
    initiator = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Order №{self.id}; {self.first_name} {self.last_name}, {self.status}, {self.created}'

    def update_after_payment(self):
        baskets = Basket.objects.filter(user=self.initiator)
        print(f"Found {baskets.count()} basket items for user {self.initiator}")
        self.status = self.PAID
        self.basket_history = {
            'purchased_items': [basket.de_json() for basket in baskets],
            'total_sum': float(baskets.total_sum()),
        }
        baskets.delete()
        self.save()
        print(f"Order {self.id} updated and basket deleted")


    def get_total_sum(self):
        return self.basket_history.get('total_sum', 0)

    def get_purchased_items(self):
        return self.basket_history.get('purchased_items', [])
