from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # Тут можуть бути додаткові поля: опис, зображення тощо

    def __str__(self):
        return self.name


class Promotion(models.Model):
    discount_percentage = models.PositiveIntegerField()
    products = models.ManyToManyField(Product, blank=True)

    # У більш розгорнутому варіанті можна зберігати дату початку/завершення акції, мінімальну кількість товарів тощо

    def __str__(self):
        return f"Promotion {self.discount_percentage}%"
