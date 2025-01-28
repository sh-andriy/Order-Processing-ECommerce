from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.views.decorators.http import require_POST
from .models import Order, PaymentTransaction, DeliveryTracking
from cart.models import Cart
from .tasks import send_order_to_external_system, sync_from_external_system

@require_POST
def checkout_order(request):
    delivery_method = request.POST.get('delivery_method')
    payment_method = request.POST.get('payment_method')
    cart = Cart.objects.filter(user=request.user, status='active').first()

    if not cart:
        return JsonResponse({'error': 'Немає активного кошика'}, status=400)

    # Створюємо замовлення, переносимо суму з кошика
    order = Order.objects.create(
        user=request.user,
        status='new',
        total_amount=cart.get_total_cost(),
        delivery_method=delivery_method,
        payment_method=payment_method
    )
    # Змінюємо статус кошика (припустимо, "converted")
    cart.status = 'converted'
    cart.save()

    # Запускаємо фонову задачу для синхронізації з ERP чи іншою системою
    send_order_to_external_system.delay(order.id)

    return JsonResponse({'order_id': order.id, 'status': order.status})

@require_POST
def process_payment(request):
    # Імітуємо процес оплати для order_id, сума може братися із Order
    order_id = request.POST.get('order_id')
    order = Order.objects.get(id=order_id)
    # Створюємо платіж (транзакцію)
    payment = PaymentTransaction.objects.create(
        order=order,
        transaction_id='TX123456789',  # Правдиво сюди підставляється ідентифікатор від платіжної системи
        amount=order.total_amount,
        status='success'
    )
    # Змінюємо статус замовлення
    order.status = 'paid'
    order.save()

    return JsonResponse({'payment_id': payment.id, 'order_status': order.status})

@require_POST
def confirm_delivery(request):
    order_id = request.POST.get('order_id')
    order = Order.objects.get(id=order_id)
    tracking_number = request.POST.get('tracking_number', 'TRK123')
    # Створюємо запис трекінгу
    DeliveryTracking.objects.create(
        order=order,
        tracking_number=tracking_number,
        current_status='InTransit'
    )
    # Змінюємо статус замовлення
    order.status = 'shipped'
    order.save()

    return JsonResponse({'order_id': order.id, 'order_status': order.status})

def sync_orders_from_external(request):
    # Викликаємо фонову таску, яка опитує зовнішню систему і оновлює замовлення
    sync_from_external_system.delay()
    return JsonResponse({'message': 'Синхронізація замовлень запущена'})


@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({"message": "Login successful."})
        else:
            return JsonResponse({"error": "Invalid credentials."}, status=400)
    return JsonResponse({"detail": "Method not allowed."}, status=405)


@ensure_csrf_cookie
def get_csrf_token(request):
    token = get_token(request)
    return JsonResponse({"csrfToken": token})
