"""
URL configuration for barzoz_restaurant project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from base import views
from django.conf import settings
from django.conf.urls.static import static

from base.views import CreateStripeCheckoutSessionView ,CancelView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home,name='home'),
    path('main_menu', views.main_menu,name='main_menu'),
    
    # without add to cart
    path('menu', views.menu,name='menu'),

    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('update_cart/', views.update_cart, name='update_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('remove_item/', views.remove_item, name='remove_item'),
    path('add_coupon/', views.add_coupon, name='add_coupon'),
    path("create-checkout-session/<int:pk>/",CreateStripeCheckoutSessionView.as_view(),name="create-checkout-session",
    ),
    path('speisekarte/', views.download_pdf, name='download_pdf'),

    path('confirm_order/', views.confirm_order, name='confirm_order'),

    path('cookies_details/', views.cookies_details, name='cookies_details'),
    path('Datenschutzerklarung/', views.Datenschutzerklarung, name='Datenschutzerklarung'),
    path('impressum/', views.impressum, name='impressum'),
    path("success/", views.success, name="success"),
    path("cancel/", CancelView.as_view(), name="cancel"),
]



