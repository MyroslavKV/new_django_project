from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings

from products.models import Product, Category, Cart, CartItem


def index(request):
    products = Product.objects.all()
    categories = Category.objects.all

    category_name = request.GET.get("category")
    filter_name = request.GET.get("filter")
    product_name = request.GET.get("search")
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")


    if product_name:
        products = products.filter(name__icontains=product_name)

    if category_name:
        products = products.filter(category_name=category_name)

    if min_price:
        products = products.filter(price__gte=min_price)

    if max_price:
        products = products.filter(price__lte=max_price)
    
    if filter_name == "price_increase":
        products = products.order_by("price")
    elif filter_name == "price_decrease":
        products = products.order_by("-price")
    elif filter_name == "rating_increase":
        products = products.order_by("rating")
    elif filter_name == "rating_decrease":
        products = products.order_by("-rating")
    elif filter_name == "date_newest":
        products = products.order_by("-created_at")
    elif filter_name == "date_oldest":
        products = products.order_by("created_at")

    return render(request=request, template_name="index.html", context={"products": products, "categories": categories},)


def about_us(request):
    return render(request=request, template_name="about.html")



def product_details(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request=request, template_name="product_details.html", context={"product": product})


def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if not request.user.is_authenticated:
        cart = request.session.get(settings.CART_SESSION_ID, dict())
        if cart.get(product_id):
            cart[product_id] += 1
        else:
            cart[product_id] = 1     
        request.session[settings.CART_SESSION_ID] = cart
    else:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.amount += 1
            cart_item.save()
    return redirect("cart_detail")


def cart_detail_view(request):
    if not request.user.is_authenticated:
        cart = request.session.get(settings.CART_SESSION_ID, dict())
        product_ids = cart.keys()
        products = Product.objects.filter(id__in = product_ids)
        cart_items = []
        total_price = 0
        for product in products:
            count = cart[str(product.id)]
            price = count * product.price
            total_price += price
            cart_items.append({"product" : product, "count" : count, "price" : price})
    else:
        try:
            cart = request.user.cart
        except Cart.DoesNotExist:
            cart = None
        if not cart or not cart.items.count():
            cart_items = []
            total_price = 0
        else:
            cart_items = cart.items.select_related("product").all()
            total_price = sum(item.product.price * item.amount for item in cart_items)
    return render(request=request, template_name="cart_detail.html", context={"cart_items" : cart_items, "total_price" : total_price})

def remove_from_cart(request):
    if request.method == "POST":
        product_id = request.POST.get('product_id')
        
        if not request.user.is_authenticated:
            cart = request.session.get(settings.CART_SESSION_ID, dict())
            if product_id in cart:
                del cart[product_id]
            request.session[settings.CART_SESSION_ID] = cart
        else:
            cart = request.user.cart
            cart_item = CartItem.objects.filter(cart=cart, product_id=product_id).first()
            if cart_item:
                cart_item.delete()
        
        return redirect('cart_detail')

def update_cart_item_quantity(request):
    if request.method == "POST":
        product_id = request.POST.get('product_id')
        amount = int(request.POST.get('amount'))
        
        if not request.user.is_authenticated:
            cart = request.session.get(settings.CART_SESSION_ID, dict())
            if product_id in cart:
                cart[product_id] = amount 
            request.session[settings.CART_SESSION_ID] = cart
        else:
            cart = request.user.cart
            cart_item = CartItem.objects.filter(cart=cart, product_id=product_id).first()
            if cart_item:
                cart_item.amount = amount
                cart_item.save()

        return redirect('cart_detail')
