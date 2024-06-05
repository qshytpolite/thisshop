from django.http import HttpRequest, JsonResponse
from django.http import JsonResponse
from django.shortcuts import redirect, render
from user.form import CustomUserForm
from user.models import User
from store.form import CheckoutForm
from store.models import Catagory, Product, Cart, Favourite, Order, OrderItem, Payment
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import requests
from django.conf import settings
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

    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_data = request.session.get('cart', {})
        for product_id, product_qty in cart_data.items():
            product = Product.objects.get(pk=product_id)
            cart_items.append(Cart(product=product, product_qty=product_qty))

    total = sum(item.item_total for item in cart_items)
    context = {'cart_items': cart_items, 'total': total}
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

# add_to_cart view function


def add_to_cart(request, product_id):
    print(f"Adding product {product_id} to cart")

    if request.method != 'POST':
        print("Error: Invalid request method")
        return JsonResponse({'status': 'Invalid request method'}, status=400)

    try:
        product = Product.objects.get(pk=product_id)
        print(f"Retrieved product {product.name} with id {product_id}")
    except Product.DoesNotExist:
        print(f"Error: Product with id {product_id} not found")
        return JsonResponse({'status': 'Product not found'}, status=404)

    # Retrieve quantity from request body
    quantity = int(request.POST.get('product_qty', 1))  # Handle missing value
    print(f"Product quantity: {quantity}")

    # Check for existing cart item or create a new one based on user status
    if request.user.is_authenticated:
        print("Authenticated user, checking for existing cart item")
        cart_item, created = Cart.objects.get_or_create(
            user=request.user, product=product
        )
        if created:
            print(f"Created new cart item for {product.name}")
            cart_item.product_qty = quantity
        else:
            print(
                f"Found existing cart item for {product.name}, updating quantity")
            cart_item.product_qty += quantity
        cart_item.save()
    else:
        print("Anonymous user, using session for cart")
        # Handle anonymous cart (using session)
        cart_data = request.session.get('cart', {})
        print("Current cart data: ", cart_data)
        cart_data[str(product_id)] = quantity
        print("Updated cart data: ", cart_data)
        request.session['cart'] = cart_data

    print("Returning success response")
    return JsonResponse({'status': 'Item added to cart'})


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

# Checkout view function


@login_required
def checkout_page(request):
    cart_items = Cart.objects.filter(user=request.user)
    total = sum(item.item_total for item in cart_items)

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Create Order
            order = Order.objects.create(
                user=request.user,
                total_amount=total,
                is_paid=False
            )
            # Create Order Items
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.product_qty,
                    price=item.item_total
                )
            # Clear the cart
            cart_items.delete()

            # Redirect to a success page
            return redirect('checkout_success')
    else:
        form = CheckoutForm()

    context = {
        'cart_items': cart_items,
        'total': total,
        'form': form
    }
    return render(request, 'store/checkout.html', context)


@login_required
def checkout_success(request):
    return render(request, 'store/checkout_success.html')

# Payment view function (Paystack)


def initiate_payment(request):
    if request.method == "POST":
        user = request.user
        amount = int(request.POST['amount']) * 100  # Convert amount to kobo

        headers = {
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json",
        }
        data = {
            "email": user.email,
            "amount": amount,
            "callback_url": "http://your-domain.com/verify_payment/",
        }

        response = requests.post(
            "https://api.paystack.co/transaction/initialize", headers=headers, json=data)
        response_data = response.json()

        if response_data['status']:
            payment = Payment.objects.create(
                user=user, amount=amount / 100, reference=response_data['data']['reference'])
            return redirect(response_data['data']['authorization_url'])
        else:
            # Handle error
            pass

    return render(request, 'store/initiate_payment.html')


def verify_payment(request):
    reference = request.GET.get('reference')
    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
    }

    response = requests.get(
        f"https://api.paystack.co/transaction/verify/{reference}", headers=headers)
    response_data = response.json()

    if response_data['status'] and response_data['data']['status'] == 'success':
        payment = Payment.objects.get(reference=reference)
        payment.verified = True
        payment.save()
        # Payment was successful
    else:
        # Payment failed
        pass

    return render(request, 'store/verify_payment.html', {'response': response_data})
