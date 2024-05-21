from django.http import HttpRequest, JsonResponse
from django.http import JsonResponse
from django.shortcuts import redirect, render
from user.form import CustomUserForm
from user.models import User
from store.models import Catagory, Product, Cart, Favourite
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import json


def home(request):
    products = Product.objects.all()
    return render(request, "store/index.html", {"products": products})


def favviewpage(request):
    if request.user.is_authenticated:
        fav = Favourite.objects.filter(user=request.user)
        return render(request, "store/fav.html", {"fav": fav})
    else:
        return redirect("/")


def remove_fav(request, fid):
    item = Favourite.objects.get(id=fid)
    item.delete()
    return redirect("/favviewpage")


def cart_page(request):
    cart_items = []

    # Get cart items for logged-in user
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        # Get cart items from session (if available)
        cart_data = request.session.get('cart', {})
        for product_id, quantity in cart_data.items():
            product = Product.objects.get(
                pk=product_id)  # Assuming product exists
            cart_items.append({'product': product, 'quantity': quantity})

    context = {'cart_items': cart_items}
    return render(request, 'store/cart.html', context)


@login_required
def remove_cart(request, product_id):
    if request.user.is_authenticated:
        Cart.objects.filter(user=request.user, product__id=product_id).delete()
    else:
        cart_data = request.session.get('cart', {})
        if str(product_id) in cart_data:
            del cart_data[str(product_id)]
            request.session['cart'] = cart_data

    return redirect('cart')


def fav_page(request: HttpRequest):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if request.user.is_authenticated:
            data = json.loads(request.body)
            product_id = data['pid']
            product_status = Product.objects.get(id=product_id)
            if product_status:
                if Favourite.objects.filter(user=request.user, product_id=product_id).exists():
                    return JsonResponse({'status': 'Product Already in Favourite'}, status=200)
                else:
                    Favourite.objects.create(
                        user=request.user, product_id=product_id)
                    return JsonResponse({'status': 'Product Added to Favourite'}, status=200)
            else:
                return JsonResponse({'status': 'Product Not Found'}, status=404)
        else:
            return JsonResponse({'status': 'Login to Add Favourite'}, status=200)
    else:
        return JsonResponse({'status': 'Invalid Access'}, status=200)


def add_to_cart(request, product_id):
    if request.method != 'POST':
        return JsonResponse({'status': 'Invalid request method'}, status=400)

    try:
        product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        return JsonResponse({'status': 'Product not found'}, status=404)

    # Retrieve quantity from request body
    quantity = int(request.POST.get('product_qty', 0))  # Handle missing value

    # Check for existing cart item or create a new one based on user status
    if request.user.is_authenticated:
        cart_item, created = Cart.objects.get_or_create(
            user=request.user, product=product
        )
        if created:
            cart_item.product_qty = quantity
        else:
            cart_item.product_qty += quantity
        cart_item.save()
    else:
        # Handle anonymous cart (using session)
        cart_data = request.session.get('cart', {})
        cart_data[str(product_id)] = quantity
        request.session['cart'] = cart_data

    return JsonResponse({'status': 'Item added to cart'})


def collections(request):
    catagory = Catagory.objects.filter(status=1)
    return render(request, "store/collection.html", {"catagory": catagory})


def collectionsview(request, name):
    if (Catagory.objects.filter(name=name, status=1)):
        products = Product.objects.filter(category__name=name)
        return render(request, "store/products.html", {"products": products, "category_name": name})
    else:
        messages.warning(request, "No Such Catagory Found")
        return redirect('collections')


def product_details(request, cname, pname):
    if (Catagory.objects.filter(name=cname)):
        if (Product.objects.filter(name=pname)):
            products = Product.objects.filter(name=pname).first()
            return render(request, "store/product_details.html", {"products": products})
        else:
            messages.error(request, "No Such Produtct Found")
            return redirect('collections')
    else:
        messages.error(request, "No Such Catagory Found")
        return redirect('collections')
