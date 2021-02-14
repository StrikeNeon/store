# -*- coding: utf-8 -*-
from decimal import Decimal
from django.conf import settings
from .models import merch


class basket(object):

    def __init__(self, request):
        """
        Initialise shopping cart obj.
        """
        self.session = request.session
        # don't forget to comment out the rest of debug stuff (some was in banner.py I think)
        cart = self.session.get(settings.CART_SESSION_ID)  # refers to the session stored in the settings.py
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}  # or an empty dict if it doesn't exist
        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        """
        Add to cart and update quantity
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            # ! don't remove conversion to str, it breaks the cart entierly, it has to do with form vlaues being strings !
            self.cart[product_id] = {'quantity': 0,
                                     'price': str(product.price)}  # inner dict for saving quantity and price
        if update_quantity:
            # if quantity is one use default 'case'
            self.cart[product_id]['quantity'] = quantity
        else:
            # or add the quantity value if the clienc chooses more than one
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        # Updating cart session
        self.session[settings.CART_SESSION_ID] = self.cart
        # mark as modified to make sure it's saved (raise an exception if it wasn't?)
        self.session.modified = True

    def remove(self, product):
        """
        Removing item from cart
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]  # deletes the k:v pair
            self.save()

    def __iter__(self):
        """
        Iterate over the items in cart
        """
        product_ids = self.cart.keys()
        # get product objects and add them
        products = merch.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():  # converts to decimal and get total
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        this returns the total amount of items in cart
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """
        this calculates the sum of all items
        """
        return sum(Decimal(item['price']) * item['quantity'] for item in
                   self.cart.values())

    def get_total_quantity(self):
        """
        this calculates the sum of all items
        """
        return sum(item['quantity'] for item in self.cart.values())

    def clear(self):
        # delete the cart from session
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
