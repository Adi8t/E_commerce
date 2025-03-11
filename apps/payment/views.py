# Create your views here.
from django.shortcuts import render, redirect
import stripe
from django.conf import settings

from django.shortcuts import render

from apps.cart.views import _cart_id
from apps.cart.models import Cart, CartItem

def checkout(request):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        total = sum(item.product.price * item.quantity for item in cart_items)
        tax = (2 * total) / 100  
        grand_total = total + tax

        # Session me grand total store kar rahe hain
        request.session["cart_total"] = int(grand_total)
        request.session["cart_total_display"] = round(grand_total, 2)  # Show in dollars

    except Cart.DoesNotExist:
        cart_items = []
        total = 0
        tax = 0
        grand_total = 0
        request.session["cart_total"] = 0
        request.session["cart_total_display"] = 0

    return render(request, "payment_integration/checkout.html", {
        "cart_items": cart_items,
        "total": total,
        "tax": tax,
        "grand_total": grand_total
    })



def payment(request):
    return render(request, 'payment_integration/payment.html', {
        "stripe_public_key": settings.STRIPE_PUBLIC_KEY
    })

import stripe
from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse

def process_payment(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY

    total_amount = request.session.get('cart_total', 0)

    if total_amount == 0:
        return redirect("checkout")  # Agar amount 0 hai toh wapas checkout page bhej do

    try:
        # Stripe Checkout Session Create kar rahe hain
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {
                            "name": "Your Cart Items",
                        },
                        "unit_amount": int(total_amount * 100),  # Cents mein value bhejna hoga
                    },
                    "quantity": 1,
                },
            ],
            mode="payment",
            success_url=request.build_absolute_uri(reverse("success")),
            cancel_url=request.build_absolute_uri(reverse("failure")),
        )
        
        return redirect(checkout_session.url)  # Hosted Stripe Page pe redirect karna

    except stripe.error.StripeError as e:
        return redirect("failure")  # Koi issue aaye toh failure page dikhao




def success(request):
    return render(request, 'payment_integration/success.html')

def failure(request):
    return render(request, 'payment_integration/failure.html')
