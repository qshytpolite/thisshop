from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.sessions.models import Session
from django.contrib import messages
# from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from user.form import CustomUserForm, ChangePasswordForm, EditProfileForm
from store.models import Cart, Product, Order

# Only the user can log themselves out by checking the session key.
# Prevent normal users from logging out superusers/admins and vice versa
def logout_page(request):
    if request.user.is_authenticated:
        # Prevent normal users from logging out superusers/admins
        if request.user.is_superuser and request.user.session_key != request.session.session_key:
            messages.error(request, "You cannot log out another user.")
            return redirect("/")

        # Check if the session key matches the one stored in the user model
        if request.user.session_key == request.session.session_key:
            # Clear the session key in the user model
            request.user.session_key = None
            request.user.save()
            logout(request)
            messages.success(request, "Logged out Successfully")
        else:
            messages.error(request, "You cannot log out another user.")
    return redirect("/")

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
                # Store the session key in the user model
                user.session_key = request.session.session_key
                user.save()
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

# Handle Registration
def register(request):
    form = CustomUserForm()
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration Success You can Login Now..!")
            return redirect('/')
    return render(request, "auths/register.html", {'form': form})

# Handle Password Change
def change_password(request):
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to change your password.")
        return redirect("login")

    if request.method == 'POST':
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Keep the user logged in
            messages.success(request, "Your password has been changed successfully.")
            return redirect('profile')  # Redirect to the user's profile or any other page
        else:
            messages.error(request, "Please correct the error below.")
    else:
        form = ChangePasswordForm(request.user)

    return render(request, 'auths/change_password.html', {'form': form})

# Handle Profile Update and my_account
@login_required
def my_account(request):
    user = request.user
    orders = Order.objects.filter(user=user).order_by('-created_at')
    return render(request, 'auths/my_account.html', {'user': user, 'orders': orders})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully.")
            return redirect('my_account')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = EditProfileForm(instance=request.user)
    return render(request, 'auths/edit_profile.html', {'form': form})
# @login_required
# def profile(request):
#     if request.method == 'POST':
#         form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Your profile has been updated!')
#             return redirect('profile')
#     else:
#         form = ProfileUpdateForm(instance=request.user)
#     return render(request, 'auths/profile.html', {'form': form})