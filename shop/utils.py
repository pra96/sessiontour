import json
import datetime
from . models import *
# Helper functions for views. These functions do the bulk of the work and
# processing for the views when it comes to data.


# Function to create cart and context data for shop pages
def make_context(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cart_items = order.get_cart_items
    else:
        # Check to see if a cart exists for user
        try:
            user_cart = json.loads(request.COOKIES['cart'])
        except 'No Cart Exists':
            user_cart = {}

        # Create a shopping cart
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        items = []
        cart_items = order['get_cart_items']
        for i in user_cart:
            # Try ensures all items/products still exist in database
            try:
                cart_items += user_cart[i]['quantity']
                product = Product.objects.get(id=i)
                total = product.price * user_cart[i]['quantity']
                order['get_cart_total'] += total
                order['get_cart_items'] += user_cart[i]['quantity']
                item = {
                    'product': {
                        'id': product.id,
                        'name': product.name,
                        'price': product.price,
                        'image_url': product.image_url
                    },
                    'quantity': user_cart[i]['quantity'],
                    'get_total': total
                }
                items.append(item)
                if not product.digital:
                    order['shipping'] = True
            # Product was deleted from database, do not display.
            # TODO: fix so that cart total display properly
            except 'Product no longer exists.':
                pass
    return {'items': items, 'order': order, 'cart_items': cart_items}


# Helper function for cart API
def process_cart(request):
    data = json.loads(request.body)
    product_id = data['product_id']
    action = data['action']
    customer = request.user.customer
    product = Product.objects.get(id=product_id)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    order_item, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        order_item.quantity += 1
    elif action == 'remove':
        order_item.quantity -= 1

    order_item.save()
    if order_item.quantity <= 0:
        order_item.delete()


# Helper function for Processing API
def process_user_data(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    print(data)
    total = float(data['form']['total'])

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        # Fill in guest user data
        name = data['form']['name']
        email = data['form']['email']
        data = make_context(request)

        # create customer
        customer, create = Customer.objects.get_or_create(email=email)
        customer.name = name
        customer.save()

        # create order
        order = Order.objects.create(customer=customer, complete=False)

        # loop through items to add to items to order
        for item in data['items']:
            if item['quantity'] < 0:
                item['quantity'] = 0
            product = Product.objects.get(id=item['product']['id'])
            OrderItem.objects.create(product=product,
                                     order=order,
                                     quantity=item['quantity'])

    order.transaction_id = transaction_id
    # Prevents users from modifying data on the frontend.
    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if not order.shipping:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode']
        )
