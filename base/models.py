from django.db import models
from PIL import Image
import stripe
from django.conf import settings
import secrets

class DeliveryFee(models.Model):
    fee = models.FloatField(default=0.0)

    def save(self, *args, **kwargs):
        # Ensure only one row exists in the DeliveryFee model
        if not self.pk and DeliveryFee.objects.exists():
            # If a row exists, update it
            existing_fee = DeliveryFee.objects.first()
            existing_fee.fee = self.fee
            existing_fee.save()
            return existing_fee
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"Delivery Fee: {self.fee}"


class Category(models.Model):
    name = models.CharField(max_length=255)
    view_homepage = models.BooleanField(default=False)
    display_order = models.PositiveIntegerField(default=0)  # New field for manual ordering


    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['display_order', 'name']  # Order categories by display_order, then by name



class Menu_Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255,blank=True, null=True)
    price = models.FloatField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.FileField(upload_to='menu_images/')

    display_order = models.PositiveIntegerField(default=0)  # New field for manual ordering

    def __str__(self):
        return '('+self.category.name+') '+ self.name

    class Meta:
        ordering = ['display_order', 'name']  # Order categories by display_order, then by name


            
class OrderItem(models.Model):
    session_key = models.CharField(max_length=32)
    menu_item = models.ForeignKey(Menu_Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.quantity} x {self.menu_item.name}"

    def get_total_item_price(self):
        return self.quantity * self.menu_item.price

class Order(models.Model):
    session_key = models.CharField(max_length=32)
    items = models.ManyToManyField(OrderItem)
    ordered = models.BooleanField(default=False)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    ordered_date = models.DateTimeField(null=True)
    payment_type = models.CharField(max_length=10, choices=[("cash", "Cash"), ("cart", "Cart")],default = "cash")
    stripe_session_id = models.CharField(max_length=255, blank=True, null=True)
    coupon = models.ForeignKey(
    'Coupon', on_delete=models.SET_NULL, blank=True, null=True)

    user_details = models.ForeignKey(
    'User_details', on_delete=models.SET_NULL,blank=True, null=True )

    delivery_fee = models.ForeignKey(DeliveryFee, on_delete=models.SET_NULL, null=True)

    casher = models.BooleanField(default=False)  # New field

    def __str__(self):
        return f"Order {self.pk}"

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_total_item_price()
        if self.coupon:
            total = total - (self.coupon.percent_off / 100) * total
        if self.delivery_fee:
            total += self.delivery_fee.fee
        return total
    

    def get_sub_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_total_item_price()

        return total
    
    def get_total_quantity(self):
        quantity = 0
        for order_item in self.items.all():
            quantity += order_item.quantity

        return quantity
    
    def save(self, *args, **kwargs):
    # If there is no associated delivery fee, set it to the first one in the database
        if not self.delivery_fee_id:
            self.delivery_fee = DeliveryFee.objects.first()

        super().save(*args, **kwargs)
    
    


class Coupon(models.Model):
    code = models.CharField(max_length=15, unique=True)
    percent_off = models.PositiveIntegerField(null=True)
    duration = models.CharField(max_length=10, choices=[("once", "Once"), ("repeating", "Repeating")],null=True)
    stripe_coupon_id = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.code

    def save(self, *args, **kwargs):
        # Call the original save method
        super().save(*args, **kwargs)

        # Create or update the corresponding Stripe coupon
        stripe.api_key = settings.STRIPE_SECRET_KEY

        try:
            # Check if the coupon already exists on Stripe
            stripe_coupon = stripe.Coupon.retrieve(self.code)
            stripe_coupon.percent_off = self.percent_off
            stripe_coupon.duration = self.duration
            stripe_coupon.save()
        except stripe.error.StripeError:
            # If the coupon doesn't exist, create it
            stripe_coupon = stripe.Coupon.create(
                percent_off=self.percent_off,
                duration=self.duration,
                id=self.code  # Use the coupon code as the Stripe coupon ID
            )

        # Store the Stripe coupon ID in the model
        self.stripe_coupon_id = stripe_coupon.id
        super().save(*args, **kwargs)




class User_details(models.Model):
    vorname = models.CharField(max_length=255)
    nachname = models.CharField(max_length=255)
    bezirk = models.CharField(max_length=255)
    street_address = models.CharField(max_length=255)
    hausnummer = models.CharField(max_length=255)
    plz_zip = models.CharField(max_length=255)
    telefon = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    um_hinweise = models.CharField(max_length=500,null=True, blank= True)
    def __str__(self):
        return self.vorname + " " + self.nachname



class APIKey(models.Model):
    key = models.CharField(max_length=100, unique=True)

    def save(self, *args, **kwargs):
        if not self.key:
            # Generate a unique API key
            self.key = secrets.token_hex(32)  # Generates a random 64-character hex string
        super().save(*args, **kwargs)
