from store.models import Cart, Product

# Create context processor so cart can work on all pages of the site.


# def cart(request):
#     # Return the default data from our Cart.
#     return {'cart': Cart(request)}
# # yourapp/context_processors.py

# first implement.
def cart_context(request):
    cart_total = 0
    cart_count = 0
    cart_items = []

    if request.user.is_authenticated:
        cart_queryset = Cart.objects.filter(user=request.user)
        for item in cart_queryset:
            cart_items.append({
                'product': item.product,
                'product_qty': item.product_qty,
                'item_total': item.item_total
            })
    else:
        session_cart = request.session.get('cart', {})
        for product_id, quantity in session_cart.items():
            try:
                product = Product.objects.get(id=product_id)
                item_total = product.selling_price * quantity  # Adjust if using discounted price
                cart_items.append({
                    'product': product,
                    'product_qty': quantity,
                    'item_total': item_total
                })
            except Product.DoesNotExist:
                continue

    cart_total = sum(item['item_total'] for item in cart_items)
    cart_count = sum(item['product_qty'] for item in cart_items)

    return {
        'cart_total': cart_total,
        'cart_count': cart_count,
        'cart_items': cart_items,  # Optional, if you need detailed cart items in the context
    }


# <!-- Example usage in a template -->

# <p>Total items in cart: {{ cart_count }}</p>
# <p>Total cost: {{ cart_total }}</p>
