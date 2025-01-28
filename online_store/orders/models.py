from django.db import models
from django.contrib.auth import get_user_model
from cart.models import Cart

User = get_user_model()

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, default='new')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    # Дані про доставку
    delivery_method = models.CharField(max_length=100, blank=True, null=True)
    # Дані про оплату
    payment_method = models.CharField(max_length=100, blank=True, null=True)
    # Можна додати поля для адреси доставки, контакту, дати тощо

    def __str__(self):
        return f"Order #{self.id} - {self.status}"

class PaymentTransaction(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, default='initiated')
    # Можна додати додаткові поля для дати, інформації від платіжної системи тощо

    def __str__(self):
        return f"PaymentTransaction #{self.id} - {self.status}"

# Наприклад, для відстеження (трекінгу) відправлених замовлень
class DeliveryTracking(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    tracking_number = models.CharField(max_length=100, unique=True)
    current_status = models.CharField(max_length=100, default='InTransit')
    # Можна додати поле для дати оновлення, останніх координат тощо

    def __str__(self):
        return f"DeliveryTracking for Order #{self.order.id}"
