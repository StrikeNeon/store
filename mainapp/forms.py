# -*- coding: utf-8 -*-

from django import forms
from .models import UserProfileInfo, Order, Review
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = User
        fields = ('username','password','email')

class UserProfileInfoForm(forms.ModelForm):
     class Meta():
        model = UserProfileInfo
        fields = ('profile_pic',)
         
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
        

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]

class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int)
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
    
class Review_form(forms.Form):
    rating = forms.TypedChoiceField(choices=Review.Rating_Choices, coerce=int)
    text = forms.CharField(required=False, initial='')
    class Meta():
        model = Review
        fields = ('text','rating')

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'postal_code', 'city']
        
class SearchForm(forms.Form):
    query = forms.CharField()
    class Meta():
        fields = ('query')