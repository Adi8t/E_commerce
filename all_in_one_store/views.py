from django.shortcuts import render
from django.core.paginator import Paginator  
from apps.store.models import Product

def home_view(request):
    products_list = Product.objects.filter(is_available=True)  
    paginator = Paginator(products_list, 8)  
    page_number = request.GET.get("page")  
    products = paginator.get_page(page_number)  # that page data 

    return render(request, "home.html", context={"products": products})
