from django.db import models
from django.contrib.auth import get_user_model
from products.models import Product, Promotion

User = get_user_model()

class Cart(models.Model):
    # Для простоти - прив'язка кошика до користувача
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    # Стан кошика (наприклад, активний, оформлений тощо)
    status = models.CharField(max_length=50, default='active')
    # За бажанням можна додати дату створення, модифікації й т.д.

    def apply_promotions(self):
        # У цьому методі можна застосувати акції з Promotion
        # Наприклад, перевірити, чи є активні акції для товарів у кошику, й розрахувати знижки
        pass

    def get_total_cost(self):
        # Метод поверне підсумкову вартість з урахуванням кількості товарів, акцій тощо
        total = 0
        items = self.cartitem_set.all()
        for item in items:
            total += item.get_subtotal()
        return total

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def get_subtotal(self):
        # Повертає суму за товар (кількість * ціна), без урахування акцій
        # (Якщо потрібні акції, можна обраховувати їх у Cart або додати окремий метод)
        return self.product.price * self.quantity
