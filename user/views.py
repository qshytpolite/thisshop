from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.sessions.models import Session
from django.contrib import messages
from user.form import CustomUserForm
from store.models import Cart, Product

def logout_page(request):
    if request.user.is_authenticated:
        # Get the current session key
        current_session_key = request.session.session_key

        # Logout the user
        logout(request)

        # Delete only the current session key
        Session.objects.filter(session_key=current_session_key).delete()

        messages.success(request, "Logged out Successfully")
    return redirect("/")

# Dedicated Admin Logout View
# def admin_logout(request):
#     if request.user.is_authenticated:
#         logout(request)
#         messages.success(request, "Logged out Successfully")
#     return redirect("/")

# Handle Login and the next Parameter
def login_page(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Logged in Successfully")

                # Merge cart data from session to the user's cart
                session_cart = request.session.get('cart', {})
                if session_cart:
                    for product_id, product_qty in session_cart.items():
                        product = Product.objects.get(id=product_id)
                        cart_item, created = Cart.objects.get_or_create(
                            user=user,
                            product=product,
                            defaults={'product_qty': product_qty}
                        )
                        if not created:
                            cart_item.product_qty += product_qty
                            cart_item.save()
                    # Clear the cart data from the session
                    del request.session['cart']

                # Redirect to the 'next' URL if it exists, otherwise redirect to the home page
                next_url = request.POST.get('next', '/')
                return redirect(next_url)
            else:
                messages.error(request, "Invalid User Name or Password")
                return redirect("login")
        else:
            # Pass the 'next' parameter from the GET request to the template
            next_url = request.GET.get('next', '/')
            return render(request, "auths/login.html", {'next': next_url})

def register(request):
    form = CustomUserForm()
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration Success You can Login Now..!")
            return redirect('/')
    return render(request, "auths/register.html", {'form': form})
