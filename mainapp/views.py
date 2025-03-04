from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView
from django.db.models import Avg
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.db import transaction
from django.core.cache.backends.base import DEFAULT_TIMEOUT

from django.core.cache import cache
from django.views.decorators.cache import cache_page

from .tokens import account_activation_token
from .models import brand, merch, order_item, review
from .forms import (login_form, user_profile_info_form,
                    user_form, cart_add_product_form,
                    order_create_form, review_form,
                    search_form)
from . import basket_logic

from os import getcwd, path


def construct_path():
    # just for convinience, don't want to spell the whole path
    projPath = getcwd()
    appPath = path.join(projPath, 'mainapp')
    template_path = path.join(appPath, 'templates')
    return template_path


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


# -----------------------------CART SECTION--------------------------------
@require_POST
def cart_add(request, product_id):
    basket = basket_logic.basket(request)
    form = cart_add_product_form(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        # the cd will return all of the form objects as strings !REMEMBER THAT!
        basket.add(product_id=product_id,  # calling the add method
                   quantity=cd.get('quantity'))
    return HttpResponseRedirect(reverse('mainapp:cart_detail'))


@csrf_exempt
@require_POST
def cart_remove(request):
    if request.is_ajax():
        product_id = request.POST['product_id']
        basket = basket_logic.basket(request)
        basket.remove(product_id)
        content = {
            'basket': basket,
        }
        return render(request, 'inc_basket_list.html', content)


def cart_detail(request):  # it just calls the basket and renders
    basket = cache.get(request.session)
    if not basket:
        basket = basket_logic.basket(request)
        cache.set(request.session, basket, CACHE_TTL)
    basket = basket_logic.basket(request)
    return render(request, 'basket.html', {'basket': basket})


@transaction.atomic
def order_create(request):
    basket = basket_logic.basket(request)
    if request.method == 'POST':
        form = order_create_form(request.POST)
        if form.is_valid():
            order = form.save()
            for item in basket:
                product = get_object_or_404(merch, id=item.get('product_id'))
                order_item.objects.create(order=order,
                                          product=product,
                                          price=item.get('price'),
                                          quantity=item.get('quantity'))

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
            user = authenticate(username=cd.get('username'),
                                password=cd.get('password'))
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


@transaction.atomic
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
                profile.profile_pic = request.FILES.get('profile_pic')
            current_site = get_current_site(request)
            mail_subject = 'Activate your shop account.'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
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


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user,
              backend='django.contrib.auth.backends.ModelBackend')

        return HttpResponse('Thank you for your email confirmation.\
                             Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


@transaction.atomic
def edit(request):
    title = 'profile edit'

    if request.method == 'POST':
        profile_form = user_profile_info_form(request.POST,
                                              instance=request.user.
                                              user_profile_info)
        if profile_form.is_valid():
            profile_form.save()
            return HttpResponseRedirect(reverse('mainapp:edit_profile'))
    else:
        profile_form = user_profile_info_form(
            instance=request.user.user_profile_info
        )

    content = {
        'title': title,
        'profile_form': profile_form
    }

    return render(request, 'edit.html', content)

# -------------------PAGES SECTION--------------------------------------------


class index(ListView):
    model = merch
    paginate_by = 5
    template_name = 'index.html'
    context_object_name = 'product'
    form = search_form()

    def get_queryset(self):
        queryset = cache.get('products')
        if not queryset:
            queryset = merch.objects.all().\
                       select_related('brand').\
                       order_by('-publish_date')
            cache.set("products", queryset, CACHE_TTL)
        return queryset

    def get_context_data(self):
        context = super().get_context_data()
        context['products'] = self.get_queryset()

        return context


class search(ListView):
    model = merch
    ordering = ['-publish_date']
    paginate_by = 5
    template_name = 'search.html'
    context_object_name = 'result'

    def get_queryset(self):
        result = super(search, self).get_queryset()
        query = self.request.GET.get('search')
        if query:
            postresult = merch.objects.filter(name__contains=query)
            result = postresult
        else:
            result = None
        return result


class brand_list(ListView):
    model = brand
    paginate_by = 5
    template_name = 'brands.html'
    context_object_name = 'brand_list'

    def get_queryset(self):
        queryset = cache.get('brands')
        if not queryset:
            queryset = brand.objects.all().order_by('-brand_name')
            cache.set("brands", queryset, CACHE_TTL)
        return queryset

    def get_context_data(self):
        context = super().get_context_data()
        context['brand_list'] = self.get_queryset()
        return context


@transaction.atomic
def review_add(request, product_id):
    form = review_form(request.POST)
    if form.is_valid():
        review_post = review()
        review_post.review_text = form.cleaned_data['text']
        review_post.rating = int(form.cleaned_data['rating'])
        review_post.product = merch.objects.get(id=product_id)
        review_post.user_id = request.user
        review_post.save()
    return HttpResponseRedirect(reverse('mainapp:product_detail',
                                        args=[product_id]))


@cache_page(CACHE_TTL)
def product_detail(request, product_id):
    product = get_object_or_404(merch, pk=product_id,)
    cart_product_form = cart_add_product_form()
    reviews = review.objects.filter(product=product_id)
    review_list = reviews[:5]
    form = review_form()
    context = {'product': product, 'cart_product_form': cart_product_form,
               'review_form': form, 'review_list': review_list}
    if review_list:
        review_avg = round(reviews.aggregate(Avg('rating'))['rating__avg'], 2)
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


@cache_page(CACHE_TTL)
def brand_detail(request, brand_id):
    brand_object = get_object_or_404(brand, pk=brand_id)
    return render(request, 'brand_detail.html', {'brand': brand_object})
