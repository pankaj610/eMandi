from decimal import Decimal
from django.conf import settings
from efarm.models import Crop


class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, crop, quantity=1, update_quantity=False):
        product_id = str(crop.id)
        if product_id not in self.cart:
            self.cart[product_id] =  {'quantity': 0, 'price': str(crop.price)}
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, crop):
        product_id = str(crop.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Crop.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True

    def get_total_item(self):
        # return sum(item['quantity'] for item in self.cart.values())
        i=0
        for item in self.cart.values():
            i=i+1
        return i
    
    def add_description(self, desc):
        self.description = desc
    def add_order(self, id):
        self.orderid = id
        self.save()