from django import forms
from django.contrib.auth import login
from django.shortcuts import render
from django.views import View
from .models import Product,Cart, Customer, OrderPlaced, Offer
from .forms import LoginForm, ProfileForm, RegistrationForm
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse, request
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


def home(request):
    offers = Offer.objects.all()
    total_items = 0
    if request.user.is_authenticated:
        total_items = len(Cart.objects.filter(user=request.user))
    fish = Product.objects.filter(category="F")
    cat = Product.objects.filter(category="C")
    dog = Product.objects.filter(category="D")
    pet = Product.objects.filter(category="P")
    assc = Product.objects.filter(category="A")
    products = Product.objects.prefetch_related("product_image").filter(is_active=True)
    return render(request, "home.html", {"offers": offers, "products":products, "fish":fish, "cat":cat, "dog":dog, "pet":pet, "assc":assc, "total_items":total_items})


class ProductDetailView(View):
    def get(self, request, pk):
        total_items = 0
        product = Product.objects.get(pk=pk)
        product_in_cart = False
        if request.user.is_authenticated:
            total_items = len(Cart.objects.filter(user=request.user))
            product_in_cart = Cart.objects.filter(
                Q(product=product.id) & Q(user=request.user)).exists()
        return render(request, "product_detail.html", {"product":product, "total_items":total_items, "product_in_cart":product_in_cart})
        
    
@login_required(login_url='/login/')
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect('/cart')



@login_required(login_url='/login/')
def display_cart(request):
    total_items = 0
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        total_items = len(Cart.objects.filter(user=request.user))
        amount = 0.0
        shipping_charge = 0.0
        total_amount = 0.0
        cart_products = [p for p in Cart.objects.all() if p.user == user]

        if cart_products:
            for p in cart_products:
                temp_amount = (p.quantity * p.product.price)
                amount += temp_amount
                if amount >= 250:
                    shipping_charge = 0
                else:
                    shipping_charge = 25.0
                total_amount = amount + shipping_charge
            return render(request, 'add_to_cart.html', {'carts':cart, 'total_amount':total_amount, 'amount':amount, 'total_items':total_items})
        else:
            return render(request, 'empty_cart.html')
        


@login_required(login_url='/login/')
def add_cart(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()
        amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user ==
                        request.user]
        for p in cart_product:
            temp_amount = (p.quantity * p.product.price)
            amount += temp_amount
            if amount >= 250:
                shipping_charge = 0
            else:
                shipping_charge = 25.0
            total_amount = amount + shipping_charge

        data = {
            'quantity': c.quantity,
            'amount': amount,
            'total_amount': amount + shipping_charge
        }
        return JsonResponse(data)


@login_required(login_url='/login/')
def subtract_cart(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -= 1
        c.save()
        amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user ==
                        request.user]
        for p in cart_product:
            temp_amount = (p.quantity * p.product.price)
            amount += temp_amount
            if amount >= 250:
                shipping_charge = 0
            else:
                shipping_charge = 25.0
            total_amount = amount + shipping_charge
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'total_amount': amount + shipping_charge
        }
        return JsonResponse(data)


@login_required(login_url='/login/')
def delete_cart(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user ==
                        request.user]
        for p in cart_product:
            temp_amount = (p.quantity * p.product.price)
            amount += temp_amount
            if amount >= 250:
                shipping_charge = 0
            else:
                shipping_charge = 25.0
            total_amount = amount + shipping_charge

        data = {
            'amount': amount,
            'total_amount': amount + shipping_charge
        }
        return JsonResponse(data)
    

@method_decorator(login_required(login_url='/login/'), name='dispatch')
class UserProfile(View):
    def get(self, request):
        total_items = 0
        if request.user.is_authenticated:
            total_items = len(Cart.objects.filter(user=request.user))
        form = ProfileForm()
        return render(request, 'profile.html', {'form':form, 'total_items':total_items})
    
    def post(self, request):
        form = ProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            phone_number = form.cleaned_data['phone_number']
            house_number = form.cleaned_data['house_number']
            locality = form.cleaned_data['locality']
            landmark = form.cleaned_data['landmark']
            city = form.cleaned_data['city']
            reg = Customer(user=user, name=name, phone_number=phone_number, house_number=house_number, locality=locality, landmark=landmark, city=city)
            messages.success(
                request, "Your Address has been added to your Profile"
            )
            reg.save()
        return redirect('/', {'form':form})
    


def address(request):
    total_items = 0
    if request.user.is_authenticated:
        total_items = len(Cart.objects.filter(user=request.user))
    address = Customer.objects.filter(user=request.user)
    return render(request, 'address.html', {'add': address, 'active': 'btn-primary', 'total_items': total_items})


@login_required(login_url='/login/')
def orders(request):
    total_items = 0
    if request.user.is_authenticated:
        total_items = len(Cart.objects.filter(user=request.user))
    orders_placed = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'orders.html', {'orders': orders_placed, 'total_items': total_items})



def login(request):
    render(request, 'login.html')
    return redirect("address")



class RegistrationView(View):
    def get(self, request):
        form = RegistrationForm()
        return render(request, 'signup.html', {'form': form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            messages.success(
                request, 'Successfuly Registered. Please login to continue.')
            form.save()
            
        return render(request, 'signup.html', {'form': form})



@login_required(login_url='/login/')
def checkout(request):
    total_items = 0
    if request.user.is_authenticated:
        total_items = len(Cart.objects.filter(user=request.user))
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount = 0.0
    total_amount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user ==
                    request.user]
    
    
    if cart_product:
        for p in cart_product:
            temp_amount = (p.quantity * p.product.price)
            amount += temp_amount
            if amount >= 250:
                shipping_charge = 0
            else:
                shipping_charge = 25.0
            total_amount = amount + shipping_charge

    return render(request, 'checkout.html', {'add': add, 'total_amount': total_amount, 'cart_items': cart_items, 'total_items': total_items})


@login_required(login_url='/login/')
def order_placed(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    
    for c in cart:
        OrderPlaced(user=user, customer=customer,
                    product=c.product, quantity=c.quantity).save()
        c.delete()
    return redirect("orders")

