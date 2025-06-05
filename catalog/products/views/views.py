from datetime import datetime

from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.utils.timezone import make_aware
from django.conf import settings
from rest_framework import viewsets, filters

from catalog.products.forms import OrderCreateForm
from catalog.utils.email.email import send_order_confirmation_email

from products.models import Payment, Product, Category, Cart, CartItem, OrderItem, Order


def calculate_discount(value, arg):
    discount_value = value * arg / 100
    return value - discount_value


def index(request):
    products = Product.objects.all()

    category_name = request.GET.get("category")
    filter_name = request.GET.get("filter")
    product_name = request.GET.get("search")
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")

    categories = Category.objects.all()

    if product_name:
        products = products.filter(name__icontains=product_name)

    if min_price:
        products = products.filter(price__gte=min_price)

    if max_price:
        products = products.filter(price__lte=max_price)

    if category_name:
        category = Category.objects.get(name=category_name)
        products = products.filter(category=category)

    if start_date:
        start_date = make_aware(datetime.strptime(start_date, "%Y-%m-%dT%H:%M")).date()

    if end_date:
        end_date = make_aware(datetime.strptime(end_date, "%Y-%m-%dT%H:%M")).date()

    if start_date and end_date:
        products = products.filter(created_at__date__range=(start_date, end_date))
    elif start_date:
        products = products.filter(created_at__date=start_date)
    elif end_date:
        products = products.filter(created_at__date=end_date)

    match filter_name:
        case "price_increase":
            products = products.order_by("price")
        case "price_decrease":
            products = products.order_by("-price")
        case "rating_increase":
            products = products.order_by("rating")
        case "rating_decrease":
            products = products.order_by("-rating")

    products_count = products.count()

    context = {
        "products": products,
        "categories": categories,
        "products_count": products_count,
    }
    return render(request, "index.html", context=context)


def product_details(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, "product_details.html", {"product": product})


def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if not request.user.is_authenticated:
        cart = request.session.get(settings.CART_SESSION_ID, {})
        if cart.get(product_id):
            cart[product_id] += 1
        else:
            cart[product_id] = 1
        request.session[settings.CART_SESSION_ID] = cart
        return redirect("products:cart_detail")
    else:
        cart = request.user.cart
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.amount += 1
            cart_item.save()
    return redirect("shop:cart_detail")


def cart_delete(request, product_id: int):
    product = get_object_or_404(Product, id=product_id)
    product_key = str(product_id)

    if not request.user.is_authenticated:
        cart = request.session.get(settings.CART_SESSION_ID, {})
        cart[product_key] -= 1
        request.session[settings.CART_SESSION_ID] = cart
    else:
        cart = request.user.cart
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.amount -= 1
            cart_item.save()

    return redirect("products:cart_detail")


def cart_detail_view(request):
    if not request.user.is_authenticated:
        cart = request.session.get(settings.CART_SESSION_ID, {})
        product_ids = cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        card_items = []
        total_price = 0
        for product in products:
            count = cart[str(product.id)]
            price = count * product.price
            total_price += price
            card_items.append({"product": product, "count": count, "price": price})
    else:
        try:
            cart = request.user.cart
        except Cart.DoesNotExist:
            cart = None

        if not cart or not cart.items.exists():
            card_items = []
            total_price = 0
        else:
            cart_items = cart.items.select_related("product")
            total_price = cart.total_price

    return render(
        request,
        "cart_detail.html",
        {"card_items": cart_items, "total_price": total_price},
    )


def checkout(request):
    if (request.user.is_authenticated and not getattr(request.user, "cart", None)) or (
        not request.user.is_authenticated and not request.session.get(settings.CART_SESSION_ID)
    ):
        messages.error(request, "Cart is empty")
        return redirect("products:cart:detail")

    if request.method == "GET":
        form = OrderCreateForm()
        if request.user.is_authenticated:
            form.initial["contact_email"] = request.user.email

    elif request.method == "POST":
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            order.save()

            if request.user.is_authenticated:
                cart = getattr(request.user, "cart")
                cart_items = cart.items.select_related("product")
                order_items = [
                    OrderItem(
                        order=order,
                        product=item.product,
                        amount=item.amount,
                        price=item.product.discount_price or item.product.price,
                    )
                    for item in cart_items
                ]
            else:
                session_cart = request.session.get(settings.CART_SESSION_ID, {})
                order_items = []
                for product_id, amount in session_cart.items():
                    product = Product.objects.get(id=product_id)
                    price = product.discount_price or product.price
                    order_items.append(
                        OrderItem(
                            order=order,
                            product=product,
                            amount=amount,
                            price=price,
                        )
                    )

            OrderItem.objects.bulk_create(order_items)

            total_price = order.total_price 

            method = form.cleaned_data.get("payment_method")
            if method != "cash":
                Payment.objects.create(order=order, provider=method, amount=total_price)
            else:
                order.status = 2 

            order.save()

            if request.user.is_authenticated:
                cart.items.all().delete()
            else:
                request.session[settings.CART_SESSION_ID] = {}

            send_order_confirmation_email(order=order)
            messages.success(request, "Order successfully placed.")
            return redirect("products:index")

    return render(request, "checkout.html", context={"form": form})

