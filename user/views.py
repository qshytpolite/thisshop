from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from user.form import CustomUserForm
from store.models import Cart, Product

def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Logged out Successfully")
    return redirect("/")

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
                    
                return redirect("/")
            else:
                messages.error(request, "Invalid User Name or Password")
                return redirect("login")
        return render(request, "auths/login.html")

def register(request):
    form = CustomUserForm()
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration Success You can Login Now..!")
            return redirect('/')
    return render(request, "auths/register.html", {'form': form})
