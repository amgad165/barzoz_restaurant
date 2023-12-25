from base.models import Order, OrderItem  # Import your Order and OrderItem models

def cart_count(request):
    if request.session.session_key:
        # Get the cart for the logged-in user
        session_key = request.session.session_key
        cart = Order.objects.filter(session_key=session_key, ordered=False).first()

        if cart:
            # Calculate the total number of items and their quantities in the cart
            cart_items = cart.items.all()
            total_quantity = sum(item.quantity for item in cart_items)
        else:
            total_quantity = 0
    else:
        total_quantity = 0

    return {'total_quantity': total_quantity}