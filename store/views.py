import json
import requests
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.urls import reverse

from .form import CheckoutForm, ReviewForm, ContactForm
from .models import Cart, Category, Favourite, Order, OrderItem, Payment, Product, HeroSlide, Review
from .utils import generate_reference
from django.db.models import Q, Sum
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Home view


def home(request):
    slides = HeroSlide.objects.all()
    category = Category.objects.filter(status=1)
    featured_products = Product.objects.filter(featured=True).order_by('-discounted_price')
    products = Product.objects.filter(featured=True).order_by('-created_at')
    latest_products = Product.objects.all().order_by('-created_at')
    context = {
        'category': category,
        'featured_products': featured_products,
        'products': products,
        'slides': slides,
        'latest_products': latest_products
    }
    return render(request, "store/index.html", context)

# Contact view
def contact_page(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Send email
            send_mail(
                subject=f"Contact Form: {form.cleaned_data['subject']}",
                message=f"From: {form.cleaned_data['name']} <{form.cleaned_data['email']}>\n\n{form.cleaned_data['message']}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.CONTACT_EMAIL],
                fail_silently=False,
            )
            messages.success(request, "Your message has been sent successfully!")
            return redirect('contact')
    else:
        form = ContactForm()
    
    return render(request, 'store/contact.html', {
        'form': form,
        'page_title': 'Contact Us'
    })

# Shop view with filters


def shop(request):
    # Get all categories to display in the filter options
    categories = Category.objects.all()

    # Start with a base queryset ordered by a consistent field
    products = Product.objects.all().order_by('-created_at')  # Default ordering by newest first

    # Filtering by category (if category is selected)
    category_filter = request.GET.get('category')
    if category_filter:
        products = products.filter(category__slug=category_filter)

    # Filtering by price range (if price is selected)
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price and max_price:
        products = products.filter(
            selling_price__gte=min_price, selling_price__lte=max_price)

    # Filtering by latest (if 'latest' is selected)
    latest = request.GET.get('latest')
    if latest == '1':
        products = products.order_by('-created_at')  # Explicit ordering for latest

    # Handling search query
    search_query = request.GET.get('search')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | Q(
                description__icontains=search_query)
        )

    # Pagination - 12 items per page
    paginator = Paginator(products, 12)
    page = request.GET.get('page')
    
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    return render(request, 'store/shop.html', {
        'products': products,
        'categories': categories,
        'search_query': search_query,
    })

# Cart page


def cart_page(request):
    if request.user.is_authenticated:
        # Check for session cart items that need to be transferred
        session_id = request.session.session_key
        if session_id:
            anonymous_items = Cart.objects.filter(session_id=session_id)
            if anonymous_items.exists():
                request.session['anonymous_cart'] = True
                
        cart_items = Cart.objects.filter(user=request.user)
    else:
        session_id = request.session.session_key
        if not session_id:
            request.session.create()
            session_id = request.session.session_key
        cart_items = Cart.objects.filter(session_id=session_id)

    total = sum(item.item_total for item in cart_items)
    context = {'cart_items': cart_items, 'total': total}
    return render(request, 'store/cart.html', context)

# add_to_cart view function


@csrf_exempt
@require_POST
def add_to_cart(request, product_id):
    try:
        product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        return JsonResponse({'status': 'Product not found'}, status=404)

    try:
        data = json.loads(request.body)
        quantity = int(data.get('product_qty', 1))
    except (ValueError, KeyError):
        return JsonResponse({'status': 'Invalid quantity'}, status=400)

    if request.user.is_authenticated:
        cart_item, created = Cart.objects.get_or_create(
            user=request.user, product=product
        )
        if created:
            cart_item.product_qty = quantity
        else:
            cart_item.product_qty += quantity
        cart_item.save()

        # Fetch the updated cart count and total
        cart_items = Cart.objects.filter(user=request.user)
        cart_count = cart_items.count()
        total = sum(item.item_total for item in cart_items)
    else:
        session_id = request.session.session_key
        if not session_id:
            request.session.create()
            session_id = request.session.session_key

        cart_item, created = Cart.objects.get_or_create(
            session_id=session_id, product=product
        )
        if created:
            cart_item.product_qty = quantity
        else:
            cart_item.product_qty += quantity
        cart_item.save()

        # Fetch the updated cart count and total
        cart_items = Cart.objects.filter(session_id=session_id)
        cart_count = cart_items.count()
        total = sum(item.item_total for item in cart_items)

    messages.success(request, "Item added to cart")
    return JsonResponse({
        'status': 'Item added to cart',
        'cart_count': cart_count,
        'total': total
    })

# Update cart


@csrf_exempt
@require_POST
def update_cart(request, cart_item_id):
    try:
        cart_item = Cart.objects.get(id=cart_item_id)
    except Cart.DoesNotExist:
        return JsonResponse({'status': 'Cart item not found'}, status=404)

    try:
        data = json.loads(request.body)
        new_quantity = int(data.get('quantity', 1))
    except (ValueError, KeyError):
        return JsonResponse({'status': 'Invalid quantity'}, status=400)

    # Update the cart item quantity
    cart_item.product_qty = new_quantity
    cart_item.save()

    # Recalculate the cart total
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        session_id = request.session.session_key
        cart_items = Cart.objects.filter(session_id=session_id)

    total = sum(item.item_total for item in cart_items)

    messages.success(request, "Cart updated")
    return JsonResponse({
        'status': 'Cart updated',
        'cart_count': cart_items.count(),
        'total': total,
        'item_total': cart_item.item_total,  # Total for the updated item
    })

# remove_cart view function


@csrf_exempt
@require_POST
def remove_cart(request, cart_item_id):
    try:
        cart_item = Cart.objects.get(id=cart_item_id)
    except Cart.DoesNotExist:
        return JsonResponse({'status': 'Cart item not found'}, status=404)

    # Delete the cart item
    cart_item.delete()

    # Recalculate the cart total
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        session_id = request.session.session_key
        cart_items = Cart.objects.filter(session_id=session_id)

    total = sum(item.item_total for item in cart_items)

    return JsonResponse({
        'status': 'Item removed from cart',
        'cart_count': cart_items.count(),
        'total': total,
    })

# Favourite view


def favviewpage(request):
    if request.user.is_authenticated:
        fav = Favourite.objects.filter(user=request.user)
        return render(request, "store/fav.html", {"fav": fav})
    else:
        return redirect("/")

# Remove favourite
@csrf_exempt
def remove_fav(request, fid):
    if request.method == "POST":
        try:
            item = Favourite.objects.get(id=fid)
            item.delete()
            return JsonResponse({"status": "success", "message": "Product removed from wishlist."})
        except Favourite.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Product not found in wishlist."}, status=404)
    else:
        return JsonResponse({"status": "error", "message": "Invalid request method."}, status=400)

# Add favourite
@csrf_exempt
def fav_page(request: HttpRequest):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if request.user.is_authenticated:
            try:
                data = json.loads(request.body)
                product_id = data.get('pid')  # Extract product_id from the request body
                product_status = Product.objects.get(id=product_id)
                if product_status:
                    if Favourite.objects.filter(user=request.user, product_id=product_id).exists():
                        return JsonResponse({'status': 'Product Already in Favourite'}, status=200)
                    else:
                        Favourite.objects.create(user=request.user, product_id=product_id)
                        return JsonResponse({'status': 'Product Added to Favourite'}, status=200)
                else:
                    return JsonResponse({'status': 'Product Not Found'}, status=404)
            except Product.DoesNotExist:
                return JsonResponse({'status': 'Product Not Found'}, status=404)
            except json.JSONDecodeError:
                return JsonResponse({'status': 'Invalid JSON data'}, status=400)
        else:
            return JsonResponse({'status': 'Login to Add Favourite'}, status=200)
    else:
        return JsonResponse({'status': 'Invalid Access'}, status=200)


def collections(request):
    category = Category.objects.filter(status=1)
    return render(request, "store/collection.html", {"category": category})


def collectionsview(request, name):
    if (Category.objects.filter(name=name, status=1)):
        products = Product.objects.filter(category__name=name)
        return render(request, "store/shop.html", {"products": products, "category_name": name})
    else:
        messages.warning(request, "No Such Category Found")
        return redirect('collections')


def product_details(request, slug):
    product = get_object_or_404(Product, slug=slug)
    reviews = product.reviews.all()
    review_count = product.review_count
    average_rating = product.average_rating

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            # Redirect to the same page to avoid form resubmission
            return redirect('product_details', slug=slug)
    else:
        form = ReviewForm()

    context = {
        'product': product,
        'reviews': reviews,
        'review_count': review_count,
        'average_rating': average_rating,
        'form': form,
    }

    return render(request, 'store/product_details.html', context)


@login_required
def submit_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            return redirect('product_details', slug=product.slug)

    return redirect('product_details', slug=product.slug)

# Save cart data to the session
@csrf_exempt
@require_POST
def save_cart_session(request):
    if not request.user.is_authenticated:
        session_id = request.session.session_key
        if not session_id:
            request.session.create()
            session_id = request.session.session_key
        
        # Save cart items to session
        cart_items = Cart.objects.filter(session_id=session_id)
        cart_data = {
            'items': [
                {
                    'product_id': item.product.id,
                    'quantity': item.product_qty
                } for item in cart_items
            ]
        }
        request.session['anonymous_cart'] = cart_data
        return JsonResponse({'status': 'Cart saved'})
    
    return JsonResponse({'status': 'User already authenticated'})

# Order_details view
@login_required
def order_details(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'store/order_details.html', {
        'order': order,
        'page_title': f'Order #{order.id}'
    })

# Checkout page
@login_required
def checkout_page(request):
    # Check if we need to transfer anonymous cart items
    if request.session.get('anonymous_cart'):
        session_id = request.session.session_key
        if session_id:
            # Get anonymous cart items
            anonymous_cart_items = Cart.objects.filter(session_id=session_id)
            
            for item in anonymous_cart_items:
                # Check if user already has this product in cart
                existing_item = Cart.objects.filter(
                    user=request.user, 
                    product=item.product
                ).first()
                
                if existing_item:
                    # Update quantity if item exists
                    existing_item.product_qty += item.product_qty
                    existing_item.save()
                    item.delete()
                else:
                    # Transfer item to user
                    item.user = request.user
                    item.session_id = None
                    item.save()
            
            del request.session['anonymous_cart']

    # Retrieve all Cart items belonging to the logged-in user
    cart_items = Cart.objects.filter(user=request.user)
    # Calculate the total price of all items in the cart
    total = sum(item.item_total for item in cart_items)

    # Check if the request is a POST request (i.e., form submission)
    if request.method == 'POST':
        # Create a form instance using the POST data
        form = CheckoutForm(request.POST)
        # Check if the form is valid (i.e., all required fields are filled)
        if form.is_valid():
            # Create a new Order object
            order = Order.objects.create(
                user=request.user,  # Associate the order with the logged-in user
                total_amount=total,  # Set the total amount of the order
                is_paid=False  # Mark the order as unpaid initially
            )
            # Create OrderItems for each item in the cart
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,  # Associate the OrderItem with the order
                    product=item.product,  # Associate the OrderItem with the product
                    quantity=item.product_qty,  # Set the quantity of the product
                    price=item.item_total  # Set the price of the product
                )
            # Delete all Cart items belonging to the logged-in user
            cart_items.delete()

            # Create a new Payment object
            payment = Payment.objects.create(
                user=request.user,  # Associate the payment with the logged-in user
                order=order,  # Associate the payment with the order
                amount=total,  # Set the amount of the payment
                reference=generate_reference(),  # Generate a unique reference for the payment
                status='pending'  # Mark the payment as pending initially
            )

            # Redirect to the payment view, passing the payment ID as a parameter
            return redirect('payment', payment_id=payment.pk)
    else:
        # If the request is not a POST request, create a new form instance
        form = CheckoutForm()

    # Prepare the context to be passed to the template
    context = {
        'cart_items': cart_items,  # Pass the cart items to the template
        'total': total,  # Pass the total price to the template
        'form': form  # Pass the form instance to the template
    }
    # Render the checkout page template with the prepared context
    return render(request, 'store/checkout.html', context)


@login_required
def delete_cart_items(request):
    # Retrieve all Cart items belonging to the logged-in user
    cart_items = Cart.objects.filter(user=request.user)
    # Delete all Cart items
    cart_items.delete()
    # Redirect back to the checkout page or any other desired page
    return redirect('checkout_page')


@login_required
def payment(request, payment_id):
    """
    This function is responsible for handling the payment process.

    It retrieves the payment object associated with the given payment ID and the
    currently logged-in user. It then retrieves the total amount of the payment
    and the Paystack secret key from the settings.

    It creates a dictionary with the email of the logged-in user, the total amount
    of the payment multiplied by 100 (since Paystack uses kobo as the unit of
    currency), and the reference of the payment.

    It sends a POST request to the Paystack API to initialize a transaction.
    It includes the Paystack secret key in the Authorization header and sets the
    Content-Type header to application/json. It also includes the data dictionary
    in the request body.

    If the response from the Paystack API is successful, it retrieves the
    authorization URL from the response data and redirects the user to that URL.
    Otherwise, it updates the status of the payment to 'failed' and saves the
    payment object. It then renders the 'store/payment_failed.html' template with
    the failure message from the Paystack API response.
    """
    # Retrieve the payment object associated with the given payment ID and the currently logged-in user
    payment = get_object_or_404(Payment, id=payment_id, user=request.user)
    # Retrieve the total amount of the payment
    total = payment.amount
    # Retrieve the Paystack secret key from the settings
    paystack_secret_key = settings.PAYSTACK_SECRET_KEY
    # Retrieve the Paystack public key from the settings (not used in this function)
    paystack_public_key = settings.PAYSTACK_PUBLIC_KEY

    # Create the headers dictionary with the Paystack secret key and the Content-Type header
    headers = {
        "Authorization": f"Bearer {paystack_secret_key}",
        "Content-Type": "application/json",
    }

    # Create the data dictionary with the email of the logged-in user, the total amount of the payment, and the reference of the payment
    data = {
        "email": request.user.email,
        "amount": int(total * 100),  # Paystack amount is in kobo
        "reference": payment.reference,  # Use the payment reference
    }

    # Send a POST request to the Paystack API to initialize a transaction
    response = requests.post(
        "https://api.paystack.co/transaction/initialize", headers=headers, json=data)
    # Parse the response data as JSON
    response_data = response.json()

    # Check if the response from the Paystack API is successful
    if response_data['status']:
        # Retrieve the authorization URL from the response data
        authorization_url = response_data['data']['authorization_url']
        # Redirect the user to the authorization URL
        return redirect(authorization_url)
    else:
        # Update the status of the payment to 'failed' and save the payment object
        payment.status = 'failed'
        payment.save()
        # Render the 'store/payment_failed.html' template with the failure message from the Paystack API response
        return render(request, 'store/payment_failed.html', {"message": response_data['message']})


@csrf_exempt
def paystack_webhook(request):
    # Retrieve the Paystack secret key from the settings
    paystack_secret_key = settings.PAYSTACK_SECRET_KEY
    # Parse the request body as JSON
    payload = json.loads(request.body)
    # Retrieve the event from the request payload
    event = payload['event']

    # Check if the event is 'charge.success'
    if event == 'charge.success':
        # Retrieve the reference from the request payload
        reference = payload['data']['reference']
        # Retrieve the Payment object associated with the given reference
        payment = get_object_or_404(Payment, reference=reference)

        # Create the headers dictionary with the Paystack secret key and the Content-Type header
        headers = {
            "Authorization": f"Bearer {paystack_secret_key}",
            "Content-Type": "application/json",
        }
        # Construct the URL to verify the transaction
        url = f"https://api.paystack.co/transaction/verify/{reference}"
        # Send a GET request to the Paystack API to verify the transaction
        response = requests.get(url, headers=headers)
        # Parse the response data as JSON
        response_data = response.json()

        # Check if the response from the Paystack API is successful and the transaction status is 'success'
        if response_data['status'] and response_data['data']['status'] == 'success':
            # Update the status of the payment to 'completed' and save the payment object
            payment.status = 'completed'
            payment.save()

            # Update the order status to 'paid'
            order = payment.order
            order.is_paid = True
            order.save()

            # Return a HTTP 200 OK response
            return HttpResponse(status=200)

    # Return a HTTP 400 Bad Request response if the event is not 'charge.success' or the transaction verification fails
    return HttpResponse(status=400)
