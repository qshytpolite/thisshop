import json
import requests
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt

from .form import CheckoutForm
from .models import Cart, Catagory, Favourite, Order, OrderItem, Payment, Product
from .utils import generate_reference


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


# remove_cart view function
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
    # Check if the provided category name exists in the database
    if (Catagory.objects.filter(name=cname)):
        # If the category name exists, check if the product name exists in the database
        if (Product.objects.filter(name=pname)):
            # If the product name exists, retrieve the first occurrence of the product
            products = Product.objects.filter(name=pname).first()
            # Render the product details page with the retrieved product data
            return render(request, "store/product_details.html", {"products": products})
        else:
            # If the product name does not exist, display an error message and redirect to the collections page
            messages.error(request, "No Such Product Found")
            return redirect('collections')
    else:
        # If the category name does not exist, display an error message and redirect to the collections page
        messages.error(request, "No Such Category Found")
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

            # Create Payment
            payment = Payment.objects.create(
                user=request.user,
                order=order,
                amount=total,
                reference=generate_reference(),
                status='pending'
            )

            # Redirect to the payment view
            return redirect('payment', payment_id=payment.pk)
    else:
        form = CheckoutForm()

    context = {
        'cart_items': cart_items,
        'total': total,
        'form': form
    }
    return render(request, 'store/checkout.html', context)


@login_required
def payment(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id, user=request.user)
    total = payment.amount
    paystack_secret_key = settings.PAYSTACK_SECRET_KEY
    paystack_public_key = settings.PAYSTACK_PUBLIC_KEY

    headers = {
        "Authorization": f"Bearer {paystack_secret_key}",
        "Content-Type": "application/json",
    }

    data = {
        "email": request.user.email,
        "amount": int(total * 100),  # Paystack amount is in kobo
        "reference": payment.reference,  # Use the payment reference
    }

    response = requests.post(
        "https://api.paystack.co/transaction/initialize", headers=headers, json=data)
    response_data = response.json()

    if response_data['status']:
        authorization_url = response_data['data']['authorization_url']
        return redirect(authorization_url)
    else:
        payment.status = 'failed'
        payment.save()
        return render(request, 'store/payment_failed.html', {"message": response_data['message']})


@csrf_exempt
def paystack_webhook(request):
    paystack_secret_key = settings.PAYSTACK_SECRET_KEY
    payload = json.loads(request.body)
    event = payload['event']

    if event == 'charge.success':
        reference = payload['data']['reference']
        payment = get_object_or_404(Payment, reference=reference)

        headers = {
            "Authorization": f"Bearer {paystack_secret_key}",
            "Content-Type": "application/json",
        }
        url = f"https://api.paystack.co/transaction/verify/{reference}"
        response = requests.get(url, headers=headers)
        response_data = response.json()

        if response_data['status'] and response_data['data']['status'] == 'success':
            payment.status = 'completed'
            payment.save()

            # Update the order status
            order = payment.order
            order.is_paid = True
            order.save()
            return HttpResponse(status=200)

    return HttpResponse(status=400)
