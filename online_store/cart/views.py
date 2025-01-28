from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Cart, CartItem
from products.models import Product, Promotion

@require_POST
def create_cart(request):
    # Створюємо новий кошик для поточного користувача (або анонімного, за потреби)
    cart = Cart.objects.create(user=request.user if request.user.is_authenticated else None)
    return JsonResponse({'cart_id': cart.id, 'status': cart.status})

@require_POST
def add_item_to_cart(request):
    # Припустимо, що в body є product_id, quantity
    product_id = request.POST.get('product_id')
    quantity = int(request.POST.get('quantity', 1))
    # Знайти або створити активний кошик для користувача
    # Для простоти візьмемо перший активний кошик
    cart = Cart.objects.filter(user=request.user, status='active').first()
    product = Product.objects.get(id=product_id)

    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    item.quantity += quantity
    item.save()

    return JsonResponse({'message': 'Товар додано до кошика', 'item_id': item.id})

@require_POST
def apply_promotion_to_cart(request):
    # Припустимо, що передаємо promotion_id
    promotion_id = request.POST.get('promotion_id')
    cart = Cart.objects.filter(user=request.user, status='active').first()
    promotion = Promotion.objects.get(id=promotion_id)
    # Викликаємо метод кошика для застосування акцій
    cart.apply_promotions()  # умовний виклик, логіка усередині методу
    return JsonResponse({'message': 'Акція застосована (умовно)'})

def get_cart_total(request):
    cart = Cart.objects.filter(user=request.user, status='active').first()
    if not cart:
        return JsonResponse({'total': 0})
    total = cart.get_total_cost()
    return JsonResponse({'total': float(total)})
