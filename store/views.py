from django.shortcuts import render
from .models import Cartitems, Customer, Product, Cart, ShippingAddress
from django.http import JsonResponse
import json
import datetime

# Create your views here.
def store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        cart, created = Cart.objects.get_or_create(customer = customer, completed = False)
        cartitems = cart.cartitems_set.all()
    else:
        cartitems = []
        cart = {"get_cart_total": 0, "get_itemtotal": 0}

    products = Product.objects.all()
    return render(request, 'store.html', {'products': products, 'cart':cart})


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        cart, created = Cart.objects.get_or_create(customer = customer, completed = False)
        cartitems = cart.cartitems_set.all()
    else:
        cartitems = []
        cart = {"get_cart_total": 0, "get_itemtotal": 0}


    return render(request, 'cart.html', {'cartitems' : cartitems, 'cart':cart})


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        cart, created = Cart.objects.get_or_create(customer = customer, completed = False)
        cartitems = cart.cartitems_set.all()
    else:
        cartitems = []
        cart = {"get_cart_total": 0, "get_itemtotal": 0}
    return render(request, 'checkout.html', {'cartitems': cartitems, 'cart': cart})

def updateCart(request):
    data = json.loads(request.body)
    productId = data["productId"]
    action = data["action"]
    product = Product.objects.get(id=productId)
    customer = request.user.customer
    cart, created = Cart.objects.get_or_create(customer = customer, completed = False)
    cartitem, created = Cartitems.objects.get_or_create(cart = cart, product = product)

    if action == "add":
        cartitem.quantity += 1
        cartitem.save()
    

    return JsonResponse("Cart Updated", safe = False)


def updateQuantity(request):
    data = json.loads(request.body)
    quantityFieldValue = data['qfv']
    quantityFieldProduct = data['qfp']
    product = Cartitems.objects.filter(product__name = quantityFieldProduct).last()
    product.quantity = quantityFieldValue
    product.save()
    return JsonResponse("Quantity updated", safe = False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        cart, created = Cart.objects.get_or_create(customer = customer, completed = False)
        cart.transaction_id = transaction_id
        total = float(data['form']['total'])
        
        if total == cart.get_cart_total:
            cart.completed = True
        cart.save()

        ShippingAddress.objects.create(
            customer = customer,
            cart=cart,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode = data['shipping']['zipcode']
        )
        
        
    else:
        print('User is not signed in')
    
    return JsonResponse("Payment complete", safe = False)