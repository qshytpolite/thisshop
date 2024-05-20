from django.http import HttpRequest, JsonResponse
from django.http import JsonResponse
from django.shortcuts import redirect, render
from user.form import CustomUserForm
from user.models import User
from store.models import Catagory, Product, Cart, Favourite
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
import json


def home(request):
    products = Product.objects.filter(trending=1)
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
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)
        return render(request, "store/cart.html", {"cart": cart})
    else:
        return redirect("/")


def remove_cart(request, cid):
    cartitem = Cart.objects.get(id=cid)
    cartitem.delete()
    return redirect("/cart")


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


def add_to_cart(request: HttpRequest):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if request.user.is_authenticated:
            data = json.loads(request.body)
            product_qty = data['product_qty']
            product_id = data['pid']
            product_status = Product.objects.filter(id=product_id).first()
            if product_status:
                if Cart.objects.filter(user=request.user, product_id=product_id).exists():
                    return JsonResponse({'status': 'Product Already in Cart'}, status=200)
                else:
                    if product_status.quantity >= product_qty:
                        Cart.objects.create(
                            user=request.user, product_id=product_id, product_qty=product_qty)
                        return JsonResponse({'status': 'Product Added to Cart'}, status=200)
                    else:
                        return JsonResponse({'status': 'Product Stock Not Available'}, status=200)
            else:
                return JsonResponse({'status': 'Product Not Found'}, status=404)
        else:
            return JsonResponse({'status': 'Login to Add Cart'}, status=200)
    else:
        return JsonResponse({'status': 'Invalid Access'}, status=200)


def collections(request):
    catagory = Catagory.objects.filter(status=0)
    return render(request, "store/collection.html", {"catagory": catagory})


def collectionsview(request, name):
    if (Catagory.objects.filter(name=name, status=0)):
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
