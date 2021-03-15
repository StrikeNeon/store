"""STORE URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')S
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from . import views

app_name = 'mainapp'
urlpatterns = [
    path('', views.index.as_view(), name='frontpage'),

    path('search/', views.search.as_view(), name='search'),
    
    path('<int:product_id>/', views.product_detail, name='product_detail'),
    path('brands/', views.brand_list.as_view(), name='brands'),
    path('about/', views.about_page, name='about'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('cart_detail/', views.cart_detail, name='cart_detail'),
    path('add/<int:pk>/<int:quantity>/', views.basket_edit, name='cart_edit'),
    path('review_add/<int:product_id>/', views.review_add, name='review_add'),
    path('cart_add/<int:product_id>', views.cart_add, name='cart_add'),
    path('cart_remove/<int:product_id>', views.cart_remove, name='cart_remove'),
    path('cart_detail/create/', views.order_create, name='order_create'),
    path('register/', views.register, name='register'),
    path('activate/<str:uidb64>/<str:token>/', views.activate, name='activate'),
]
