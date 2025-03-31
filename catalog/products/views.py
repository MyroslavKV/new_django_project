from django.shortcuts import render, get_object_or_404

from products.models import Product, Category


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

