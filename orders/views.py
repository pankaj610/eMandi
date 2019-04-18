from django.shortcuts import render, HttpResponseRedirect
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from django.urls import reverse
import stripe

temporder=""
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            # cart.add_description( order.first_name + "  " + order.last_name )
            # print("--------------",cart.description )
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            # cart.add_order(order.id)
            # print("-------------------", cart.orderid)
            # cart.clear()
            # request.session['order'] = order.pk
            temporder=order
            return HttpResponseRedirect( '/orders/payment/')
    else:
        form = OrderCreateForm()
    return render(request, 'orders/order/create.html', {'form': form, 'cart':cart})


from django.conf import settings
from django.views.generic.base import TemplateView

def HomePageView(request):
    # template_name = 
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    context = { 'key' : settings.STRIPE_PUBLISHABLE_KEY , 'cart' : Cart(request)}
    return render(request, 'orders/order/payment.html', context)


def charge(request):
    if request.method == 'POST':
        stripe.api_key = settings.STRIPE_SECRET_KEY
        cart = Cart(request)
        charge = stripe.Charge.create(
            amount=int( cart.get_total_price() ),
            currency='usd',
            description="Pankaj Verma",
            source=request.POST['stripeToken']
        )

        cart.clear()
        return render(request, 'orders/order/created.html', )
    

    