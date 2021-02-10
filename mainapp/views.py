from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView
from django.db.models import Avg
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate, login, logout

from .models import brand, merch, order_item, review
from os import getcwd, path
from .forms import (login_form, user_profile_info_form,
                    user_form, cart_add_product_form,
                    order_create_form, review_form,
                    search_form)
from . import basket_logic


# gonna go on a limb here - this whole block of nonsence would be obvious
# nah, commenting it anyways

def construct_path():
    # just for convinience, don't want to spell the whole path
    projPath = getcwd()
    appPath = path.join(projPath, 'mainapp')
    template_path = path.join(appPath, 'templates')
    return template_path


# -----------------------------CART SECTION--------------------------------
@require_POST  # this allows for multiple products to be added (via forms)
def cart_add(request, product_id):
    basket = basket_logic.basket(request)
    product = get_object_or_404(merch, id=product_id)
    form = cart_add_product_form(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        # the cd will return all of the form objects as strings !REMEMBER THAT!
        basket.add(product=product,  # calling the add method
                   quantity=cd['quantity'],
                   update_quantity=cd['update'])
    return HttpResponseRedirect(reverse('mainapp:cart_detail'))


def cart_remove(request, product_id):
    basket = basket_logic.basket(request)
    product = get_object_or_404(merch, id=product_id)
    basket.remove(product)
    return HttpResponseRedirect(reverse('mainapp:cart_detail'))


def cart_detail(request):  # it just calls the basket and renders
    basket = basket_logic.basket(request)
    return render(request, 'basket.html', {'basket': basket})


def order_create(request):
    basket = basket_logic.basket(request)
    if request.method == 'POST':
        form = order_create_form(request.POST)
        if form.is_valid():
            order = form.save()
            for item in basket:
                order_item.objects.create(order=order,
                                          product=item['product'],
                                          price=item['price'],
                                          quantity=item['quantity'])

            basket.clear()
            return render(request, 'ordered.html',
                          {'order': order})
    else:
        form = order_create_form()
    return render(request, 'order.html',
                  {'cart': basket, 'form': form})


# ----------------------------USER SECTION-------------------------------------
def user_login(request):
    if request.method == 'POST':
        form = login_form(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('mainapp:frontpage'))
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = login_form()
    return render(request, 'login.html', {'form': form})


def register(request):
    registered = False
    if request.method == 'POST':
        form = user_form(data=request.POST)
        profile_form = user_profile_info_form(data=request.POST)
        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']
            profile.save()
            registered = True
        else:
            print(form.errors, profile_form.errors)
    else:
        form = user_form()
        profile_form = user_profile_info_form()
    return render(request, 'register.html',
                  {'user_form': form,
                   'profile_form': profile_form,
                   'registered': registered})


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('mainapp:frontpage'))

# this is a dumb way to do it
# make a REST API for shop metrics


# -------------------INDEX PAGE SECTION-------------------------------------
class index(ListView):
    model = merch
    ordering = ['-publish_date']
    paginate_by = 5
    template_name = 'index.html'
    context_object_name = 'product'
    form = search_form()

    def get_context_data(self):
        context = super().get_context_data()
        context['products'] = merch.objects.all()
        return context


class search(ListView):
    model = merch
    template_name = 'search.html'
    context_object_name = 'result'

    def get_queryset(self):
        result = super(search, self).get_queryset()
        query = self.request.GET.get('search')
        if query:
            postresult = merch.objects.filter(Name__contains=query)
            result = postresult
        else:
            result = None
        return result


class brand_list(ListView):
    model = brand
    ordering = ['-brand_name']
    paginate_by = 5
    template_name = 'brands.html'
    context_object_name = 'brand_list'

    def get_context_data(self):
        context = super().get_context_data()
        context['brand_list'] = brand.objects.all()
        return context


def review_add(request, product_id):
    form = review_form(request.POST)
    if form.is_valid():
        review_post = review()
        review_post.review_text = form.cleaned_data['text']
        review_post.rating = int(form.cleaned_data['rating'])
        review_post.product = merch.objects.get(id=product_id)
        review_post.user_id = request.user
        review_post.save()
    return HttpResponseRedirect(reverse('mainapp:product detail',
                                        args=[product_id]))


def product_detail(request, product_id):
    product = get_object_or_404(merch, pk=product_id,)
    cart_product_form = cart_add_product_form()
    review_list = review.objects.filter(product=product_id)[:5]
    form = review_form()
    context = {'product': product, 'cart_product_form': cart_product_form,
               'review_form': form, 'review_list': review_list}
    if review_list:
        review_avg = round(review.objects.filter(product=product_id).aggregate(Avg('rating'))['rating__avg'], 2)
        context['rating'] = review_avg
    else:
        pass
    return render(request, 'detail.html', context)


def about_page(request):
    # this is an empty template and only has 2 variables
    # (so, like, 'partnered with x brands', 'selling y products',
    #  but dynamic and all that jazz)
    merch_count = merch.objects.all().count()
    brand_count = brand.objects.all().count()
    context = {'merch_count': merch_count, 'brand_count': brand_count}
    return render(request, path.join(construct_path(), 'about.html'), context)


def brand_detail(request, brand_id):
    brand_object = get_object_or_404(brand, pk=brand_id)
    return render(request, 'brand_detail.html', {'brand': brand_object})
