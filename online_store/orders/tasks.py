from celery import shared_task
from .models import Order

@shared_task
def send_order_to_external_system(order_id):
    # Отримуємо замовлення
    order = Order.objects.get(id=order_id)
    # Тут можна зібрати дані про замовлення, перетворити в JSON/XML та відправити в ERP/зовнішню систему
    # Якщо виникає помилка - спробувати повторити (Celery retry)
    # Після успішної відправки можна змінити статус замовлення або зберегти відповідь
    pass

@shared_task
def sync_from_external_system():
    # Ця таска може викликатися за розкладом (Celery Beat) або вручну
    # 1. Отримуємо із зовнішньої системи список/статуси замовлень
    # 2. Оновлюємо наші замовлення у БД
    # 3. Якщо знайдені нові замовлення, створюємо їх
    pass

class DeliveryService:
    """Сервіс для взаємодії з API служби доставки"""

    @staticmethod
    def create_shipment(order):
        # Логіка створення відправлення у сторонній службі
        # Наприклад, формуємо JSON, відправляємо його через requests
        pass

    @staticmethod
    def track_shipment(tracking_number):
        # Повертає поточний статус відправлення
        pass
