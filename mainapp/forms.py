# -*- coding: utf-8 -*-

from django import forms
from .models import user_profile_info, order, review
from django.contrib.auth.models import User


class user_form(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username', 'password', 'email')


class user_profile_info_form(forms.ModelForm):

    class Meta():
        model = user_profile_info
        fields = ('profile_pic','age','gender')


class login_form(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class cart_add_product_form(forms.Form):
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES,
                                      coerce=int)
    update = forms.BooleanField(required=False,
                                initial=False, widget=forms.HiddenInput)


class review_form(forms.Form):
    rating = forms.TypedChoiceField(choices=review.rating_choices, coerce=int)
    text = forms.CharField(required=False, initial='')

    class Meta():
        model = review
        fields = ('text', 'rating')


class order_create_form(forms.ModelForm):

    class Meta:
        model = order
        fields = ['first_name', 'last_name', 'email',
                  'address', 'postal_code', 'city']


class search_form(forms.Form):
    query = forms.CharField()

    class Meta():
        fields = ('query')
