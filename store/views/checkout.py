from django.shortcuts import render, redirect
from Eshop.settings import RAZORPAY_API_KEY, PAZORPAY_API_SECRET_KEY
from django.contrib.auth.hashers import check_password
from store.models.customer import Customer
from django.views import View

from store.models.product import Product
from store.models.orders import Order
import razorpay


client = razorpay.Client(auth=(RAZORPAY_API_KEY, PAZORPAY_API_SECRET_KEY))

class CheckOut(View):
    def post(self, request):
        customer = request.session.get('customer')
        cart = request.session.get('cart')
        products = Product.get_products_by_id(list(cart.keys()))
        print(customer, cart, products)

        for product in products:
            print(cart.get(str(product.id)))
            order = Order(customer=Customer(id=customer),
                          product=product,
                          price=product.price,
                          quantity=cart.get(str(product.id)))
            order.save()
        total = 0
        for product in products:
            quantity = cart.get(str(product.id))
            price = product.price
            total += quantity * price
        print(total)
        amount = total
        total = total*100
        payment_order = client.order.create(dict(amount=total, currency="INR",payment_capture=1))
        payment_order_id = payment_order['id']
        data = {
            'amount': amount, 
            'api_key': RAZORPAY_API_KEY, 
            'order_id': payment_order_id
        }
        request.session['cart'] = {}
        return render(request, 'pay.html', data)
