from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .form import CustomUserForm, ChangePasswordForm, EditProfileForm
from store.models import Cart, Product, Order

# Logout
def logout_page(request):
    if request.user.is_authenticated:
        # For superusers: allow logging out other users through admin interface only
        if request.user.is_superuser and request.user.session_key != request.session.session_key:
            messages.error(request, "Please use the admin interface to log out other users.")
            return redirect("/admin/")
        
        # For all users (including superusers logging themselves out)
        request.user.session_key = None
        request.user.save()
        logout(request)
        messages.success(request, "Logged out successfully")
    return redirect("/")

# Login
def login_page(request):
    if request.user.is_authenticated:
        return redirect("/")
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")

            # Restore cart from session if exists
            if 'anonymous_cart' in request.session:
                cart_data = request.session['anonymous_cart']
                for item_data in cart_data.get('items', []):
                    try:
                        product = Product.objects.get(id=item_data['product_id'])
                        cart_item, created = Cart.objects.get_or_create(
                            user=user,
                            product=product,
                            defaults={'product_qty': item_data['quantity']}
                        )
                        if not created:
                            cart_item.product_qty += item_data['quantity']
                            cart_item.save()
                    except Product.DoesNotExist:
                        continue
                del request.session['anonymous_cart']

            next_url = request.POST.get('next', '/')
            return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password")
            return redirect("login")
    
    next_url = request.GET.get('next', '/')
    return render(request, "auths/login.html", {
        'next': next_url,
        'page_title': 'Login'
    })

# Register
def register(request):
    if request.user.is_authenticated:
        return redirect("/")
        
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Account created successfully! You can now log in.")
            return redirect('login')
    else:
        form = CustomUserForm()
    
    return render(request, "auths/register.html", {
        'form': form,
        'page_title': 'Register'
    })

# Change password
@login_required
def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Your password has been changed successfully!")
            return redirect('my_account')
    else:
        form = ChangePasswordForm(request.user)
    
    return render(request, 'auths/change_password.html', {
        'form': form,
        'page_title': 'Change Password'
    })

# My account
@login_required
def my_account(request):
    user = request.user
    orders = Order.objects.filter(user=user).select_related('user').prefetch_related('items').order_by('-created_at')[:10]
    
    # Get wishlist items with product information to avoid N+1 queries
    wishlist_items = user.favourite_set.select_related('product').all()
    
    return render(request, 'auths/my_account.html', {
        'user': user,
        'orders': orders,
        'wishlist_items': wishlist_items,
        'page_title': 'My Account'
    })

# Edit profile
@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Your profile has been updated successfully!")
            
            # If profile picture was changed, update the session
            if 'profile_picture' in form.changed_data:
                request.session['profile_picture'] = user.profile_picture.url if user.profile_picture else None
            
            return redirect('my_account')
    else:
        form = EditProfileForm(instance=request.user)
    
    return render(request, 'auths/edit_profile.html', {
        'form': form,
        'page_title': 'Edit Profile'
    })