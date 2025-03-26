# context_processors.py
from .models import Cart, Favourite

def cart_data(request):
    """Optimized cart data processor with single query for authenticated users"""
    context = {
        'cart_count': 0,
        'cart_total': 0,
        'wishlist_count': 0,
    }

    if request.user.is_authenticated:
        # Single query to get cart items and calculate totals
        cart_items = Cart.objects.filter(user=request.user).select_related('product')
        cart_count = cart_items.count()
        total = sum(item.item_total for item in cart_items)
        
        # Single query for wishlist count
        wishlist_count = Favourite.objects.filter(user=request.user).count()
        
        context.update({
            'cart_count': cart_count,
            'cart_total': total,
            'wishlist_count': wishlist_count,
        })
    else:
        session_id = request.session.session_key
        if session_id:
            cart_items = Cart.objects.filter(session_id=session_id).select_related('product')
            cart_count = cart_items.count()
            total = sum(item.item_total for item in cart_items)
            context.update({
                'cart_count': cart_count,
                'cart_total': total,
            })

    return context