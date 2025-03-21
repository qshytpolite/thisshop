# context_processors.py
from .models import Cart, Favourite

def cart_data(request):
    """Add cart count, total, and wishlist count to the template context for all pages."""
    cart_count = 0
    total = 0
    wishlist_count = 0

    if request.user.is_authenticated:
        # For authenticated users
        cart_items = Cart.objects.filter(user=request.user)
        cart_count = cart_items.count()
        total = sum(item.item_total for item in cart_items)
        wishlist_count = Favourite.objects.filter(user=request.user).count()
    else:
        # For anonymous users
        session_id = request.session.session_key
        if session_id:
            cart_items = Cart.objects.filter(session_id=session_id)
            cart_count = cart_items.count()
            total = sum(item.item_total for item in cart_items)

    return {
        'cart_count': cart_count,
        'cart_total': total,
        'wishlist_count': wishlist_count,
    }