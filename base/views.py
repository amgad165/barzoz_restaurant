from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseServerError, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
from .models import Menu_Item, OrderItem, Order, Category , Coupon , User_details
from django.contrib.sessions.models import Session
from django.utils import timezone
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
import stripe
from django.views import View
from django.views.generic import TemplateView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from django.http import HttpResponseForbidden
from django.core.mail import send_mail
from . utilities import mail
from django.templatetags.static import static
from django.views.static import serve
from django.http import HttpResponse, FileResponse


stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.
def home(request):
    categories = Category.objects.filter(view_homepage=True)
    menu_items_by_category = {}

    for category in categories:
        menu_items_by_category[category.name] = Menu_Item.objects.filter(category=category)
    context = {'menu_items_by_category': menu_items_by_category}
    return render(request,"index.html", context)

def main_menu(request):
    categories = Category.objects.all()
    menu_items_by_category = {}

    for category in categories:
        menu_items_by_category[category.name] = Menu_Item.objects.filter(category=category)

    context = {'menu_items_by_category': menu_items_by_category}
    
    return render(request, "main_menu.html", context)


def menu(request):
    categories = Category.objects.all()
    menu_items_by_category = {}

    for category in categories:
        menu_items_by_category[category.name] = Menu_Item.objects.filter(category=category)

    context = {'menu_items_by_category': menu_items_by_category}
    
    return render(request, "menu.html", context)

def add_to_cart(request):
    
    if request.method == 'POST':
        
        menu_item_id = request.POST.get('id')
        

        menu_item = get_object_or_404(Menu_Item, pk=menu_item_id)
        
        # Use session key to identify the cart for the user
        session_key = request.session.session_key
        if not session_key:
            request.session.cycle_key()
            session_key = request.session.session_key

        order_item, created = OrderItem.objects.get_or_create(
            session_key=session_key,
            menu_item=menu_item,
            ordered=False
        )



        order_item.save()

        # Check if an order exists for the user's session
        order_qs = Order.objects.filter(session_key=session_key, ordered=False)

        if order_qs.exists():
            order = order_qs.first()
            if not order.items.filter(menu_item__id=order_item.menu_item.id, ordered=False).exists():
                order.items.add(order_item)
        else:
            # Create a new order for the user's session
            ordered_date = timezone.now()
            order = Order.objects.create(session_key=session_key, ordered_date=ordered_date)
            order.items.add(order_item)

        cart_items = order.items.all()
        
        total_quantity = sum(item.quantity for item in cart_items)

        return JsonResponse({'success': 'Item added to cart', 'cart_items_count': total_quantity})

    return JsonResponse({'error': 'Invalid request'})


def cart(request):
    session_key = request.session.session_key  # Get the currently logged-in session user
    try:
        order = Order.objects.get(session_key=session_key, ordered=False)
        order_items = order.items.all()
        cart_count = len(order.items.all())
        
        # get total orders 
        total_price = order.get_total()


        if order.coupon:
            discount= order.coupon.percent_off
        else:
            discount = None

        if order.delivery_fee:
            delivery_fee= order.delivery_fee.fee
        else:
            delivery_fee = None


        return render(request, "cart.html", {'order_items': order_items,'total_price':total_price,"cart_count":cart_count,"discount":discount,"delivery_fee":delivery_fee})

    except Order.DoesNotExist:
        # Handle the case where the order doesn't exist
        order_items = None    
        return render(request, "cart.html", {'order_items': order_items})


def update_cart(request):
    if request.method == "POST":
        # Process the data sent by the "Update Cart" button
        product_ids = request.POST.getlist('product_id')
        quantities = request.POST.getlist('quantity')  # These are the updated quantities
        
        session_key = request.session.session_key
        # Loop through the product IDs and quantities to update the cart
        for product_id, quantity in zip(product_ids, quantities):
            menu_item = get_object_or_404(Menu_Item, id=product_id)
            quantity = int(quantity)  # Convert the quantity to an integer

            cart = OrderItem.objects.get(session_key=session_key,menu_item__id=product_id,ordered=False)
            cart.quantity = quantity
            
            cart.save()
        
        # Return a JSON response to indicate success (you can customize this)
        
        return redirect("cart")

    # Handle GET requests (if needed)
    return JsonResponse({"message": "Invalid request"}, status=400)

def checkout(request):
    session_key = request.session.session_key  # Get the currently logged-in session user
    try:
        order = Order.objects.get(session_key=session_key, ordered=False)
        order_items = order.items.all()
        cart_count = len(order.items.all())
        
        # get total orders 
        total_price = order.get_total()
        subtotal_price = order.get_sub_total()

        if order.coupon:
            discount= order.coupon.percent_off
        else:
            discount = None

        if order.delivery_fee:
            delivery_fee= order.delivery_fee.fee
        else:
            delivery_fee = None


        return render(request, "checkout.html", {'order_items': order_items,'total_price':total_price,'subtotal_price':subtotal_price,"cart_count":cart_count , "discount":discount,"order":order,"delivery_fee":delivery_fee})

    except Order.DoesNotExist:
        # Handle the case where the order doesn't exist
        order_items = None    
        return render(request, "checkout.html", {'order_items': order_items})


class CreateStripeCheckoutSessionView(View):


    def post(self, request, *args, **kwargs):

        # get user details
        payment_type = request.POST.get('payment_type')

        vorname = request.POST.get('vorname')
        nachname = request.POST.get('nachname')        
        bezirk = request.POST.get('bezirk')
        street_address = request.POST.get('street_address')     
        hausnummer = request.POST.get('hausnummer')
        plz_zip = request.POST.get('plz_zip')     
        telefon = request.POST.get('telefon')     
        email = request.POST.get('email')
        um_hinweise = request.POST.get('um_hinweise')

        user_details_obj = User_details.objects.create(vorname=vorname,nachname=nachname,bezirk=bezirk,street_address=street_address,hausnummer=hausnummer,plz_zip=plz_zip, telefon= telefon ,email = email, um_hinweise=um_hinweise)
        user_details_obj.save()

        order = Order.objects.get(id=self.kwargs["pk"])
        order.user_details = user_details_obj
        order.save()

        if payment_type == 'on_delivery':

            return redirect(confirm_order)

        else:

            items = order.items.all()
            items_details_list = []
            for item in items:
                items_details = {
                    "price_data": {
                        "currency": "eur",
                        "unit_amount": int(item.menu_item.price) * 100,
                        "product_data": {
                            "name": item.menu_item.name,
                            "description": item.menu_item.description,  
                        },
                    },
                    "quantity": item.quantity,
                }

                items_details_list.append(items_details)
            try:    
                if order.coupon:
                    checkout_session = stripe.checkout.Session.create(
                        payment_method_types=["card"],
                        line_items=items_details_list,
                        discounts=[{"coupon": order.coupon.stripe_coupon_id}],
                        metadata={"product_id": order.id},
                        mode="payment",
                        success_url=settings.PAYMENT_SUCCESS_URL,
                        cancel_url=settings.PAYMENT_CANCEL_URL,
                    )
                else:
                    checkout_session = stripe.checkout.Session.create(
                        payment_method_types=["card"],
                        line_items=items_details_list,
                        metadata={"product_id": order.id},
                        mode="payment",
                        success_url=settings.PAYMENT_SUCCESS_URL,
                        cancel_url=settings.PAYMENT_CANCEL_URL,
                    )
                # Extract the session_id from the created Checkout Session
                session_id = checkout_session.id
                order.stripe_session_id = session_id
                order.save()       
                return redirect(checkout_session.url)        

            except stripe.error.CardError as e:
                    body = e.json_body
                    err = body.get('error', {})
                    return Response({"message": f"{err.get('message')}"}, status=HTTP_400_BAD_REQUEST)

            except stripe.error.RateLimitError as e:
                # Too many requests made to the API too quickly
                messages.warning(self.request, "Rate limit error")
                return Response({"message": "Rate limit error"}, status=HTTP_400_BAD_REQUEST)

            except stripe.error.InvalidRequestError as e:
                print(e)
                # Invalid parameters were supplied to Stripe's API
                return Response({"message": "Invalid parameters"}, status=HTTP_400_BAD_REQUEST)

            except stripe.error.AuthenticationError as e:
                # Authentication with Stripe's API failed
                # (maybe you changed API keys recently)
                return Response({"message": "Not authenticated"}, status=HTTP_400_BAD_REQUEST)

            except stripe.error.APIConnectionError as e:
                # Network communication with Stripe failed
                return Response({"message": "Network error"}, status=HTTP_400_BAD_REQUEST)

            except stripe.error.StripeError as e:
                # Display a very generic error to the user, and maybe send
                # yourself an email
                return Response({"message": "Something went wrong. You were not charged. Please try again."}, status=HTTP_400_BAD_REQUEST)

            except Exception as e:
                # send an email to ourselves
                return Response({"message": "A serious error occurred. We have been notifed."}, status=HTTP_400_BAD_REQUEST)




def success(request):

    try:
        #get user session key
        user_session_key = request.session.session_key  # Get the currently logged-in session user
        order = Order.objects.get(session_key=user_session_key, ordered=False)
        if order:
            stripe_session_id = order.stripe_session_id
            
            session = stripe.checkout.Session.retrieve(stripe_session_id)
            
            if session.payment_status == 'paid':
                                
                order_items = order.items.all()
                order_items.update(ordered=True)
                items_lists = []
                index = 1
                for item in order_items:
                    item.save()
                    items_lists.append(str(index)+'- ' +str(item))
                    index +=1


                order.ordered = True
                order.save()

                items_lists = '<br> '.join(items_lists)

                # send email to the client mail
                email_from = settings.EMAIL_HOST_USER
                mail(order = order, sender = email_from, items_lists=items_lists,payment_type='cart')


                return render(request, "success.html")
    
    except stripe.error.StripeError:
        # Log the error or handle it as needed
        return HttpResponseForbidden("Access Denied: Invalid Payment Status")

    # Handle other cases if needed
    return HttpResponseForbidden("Access Denied: Invalid Payment Status")

class SuccessView(TemplateView):
    template_name = "success.html"

class CancelView(TemplateView):
    template_name = "cancel.html"





def remove_item(request):
    if request.method == "POST":
        product_id = request.POST.get('product_id')
        session_key = request.session.session_key 
        
        # Delete the OrderItem
        order_item = OrderItem.objects.filter(
            menu_item__id=product_id,
            session_key=session_key,
            ordered=False
        ).first()
        
        if order_item:
            order_item.delete()
        
        order = Order.objects.get(session_key=session_key, ordered=False) 
        if order:
            
            
            
            cart_items = order.items.all()
            
            total_quantity = sum(item.quantity for item in cart_items)

            # Calculate the updated total price
            updated_total_price = float(order.get_total())


        
            # Return the updated total price as JSON response
            return JsonResponse({'total_price': updated_total_price,"cart_items_count":total_quantity})
        
    return JsonResponse({'message': 'Invalid request'}, status=400)


def get_coupon(request, code):
    try:
        coupon = Coupon.objects.get(code=code)
        return coupon
    except :
        
        messages.info(request, "Error adding a coupong, Please try again later")
        return redirect("checkout")

def add_coupon(request):
    if request.method == "POST":
        try:
            code = request.POST.get('coupon')
            session_key = request.session.session_key
            order = Order.objects.get(
                session_key=session_key, ordered=False)
            
            order.coupon = get_coupon(request, code)
            order.save()
            messages.success(request, "Successfully added coupon")
            return redirect("cart")
        except :
            messages.info(request, "You do not have an active order")

    return redirect("cart")




def confirm_order(request):
    session_key = request.session.session_key
    
    try:
        order = Order.objects.get(session_key=session_key, ordered=False)
        order_items = order.items.all()
        
        order_items.update(ordered=True)
        items_lists = []
        index = 1
        for item in order_items:
            item.save()
            items_lists.append(str(index)+'- ' +str(item))
            index +=1

        items_lists = '<br>'.join(items_lists)

        # send email to the client mail
        email_from = settings.EMAIL_HOST_USER
        mail(order = order, sender = email_from, items_lists=items_lists,payment_type='cash')



        order.ordered = True

        order.save()

        return render(request,"success.html")  

    except Exception as e:
        
        
        return HttpResponseServerError("A serious error occurred. We have been notified.", content_type="text/plain")





def cookies_details(request):

    return render(request,"cookies_details.html")

def Datenschutzerklarung(request):

    return render(request,"Datenschutzerklarung.html")

def impressum(request):

    return render(request,"impressum.html")


def download_pdf(request):
    s3_base_url = settings.AWS_S3_CUSTOM_DOMAIN
    pdf_path = "static_files/assets/pdf/Speisekarte.pdf"
    pdf_url = f"https://{s3_base_url}/{pdf_path}"

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Speisekarte.pdf"'

    # Use FileResponse directly with the S3 URL
    return FileResponse(requests.get(pdf_url).content, content_type='application/pdf')