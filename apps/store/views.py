from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render

from apps.cart.models import CartItem
from apps.cart.views import _cart_id
from apps.category.models import Category

from .models import Product , Variation


# Create your views here.
def store(request, category_slug=None):
    page = request.GET.get("page")
    size_filter = request.GET.getlist("size")  
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category, is_available=True)
    else:
        products = Product.objects.filter(is_available=True)

    if size_filter:
        products = products.filter(variation__variation_value__in=size_filter)  

    if min_price and max_price:
        try:
            min_price = float(min_price)
            max_price = float(max_price)
            products = products.filter(price__gte=min_price, price__lte=max_price)
        except ValueError:
            pass  

    products = products.order_by("id")  
    paginator = Paginator(products, 6)
    paged_product = paginator.get_page(page)

    sizes = Variation.objects.filter(variation_category="size").values("variation_value").distinct()

    return render(
        request,
        "store/store.html",
        context={"products": paged_product, "product_counts": products.count(), "sizes": sizes},
    )


def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(
            category__slug=category_slug, slug=product_slug
        )
        in_cart = CartItem.objects.filter(
            cart__cart_id=_cart_id(request), product=single_product
        ).exists()
    except Exception as e:
        raise e
    return render(
        request,
        "store/product_detail.html",
        context={"single_product": single_product, "in_cart": in_cart},
    )


def search(request):
    if "keyword" in request.GET:
        key_word = request.GET["keyword"]
        products = Product.objects.filter(
            description__icontains=key_word, product_name__icontains=key_word
        ).order_by("id")
    else:
        products = Product.objects.all().order_by("id")
    context = {"products": products, "product_counts": products.count()}
    return render(
        request,
        "store/store.html",
        context=context,
    )
