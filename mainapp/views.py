from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView
from django.db.models import Avg
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate, login, logout

from .models import Brand, Merch, OrderItem, Review
from os import getcwd, path
from .forms import LoginForm, UserProfileInfoForm, UserForm, CartAddProductForm, OrderCreateForm, Review_form, SearchForm
from . import cart


#gonna go on a limb here - this whole block of nonsence would be obvious
#nah, commenting it anyways

def constructPath(): #just for convinience, don't want to spell the whole path
    projPath = getcwd()
    appPath = path.join(projPath, 'mainapp')
    templatePath = path.join(appPath, 'templates')
    return templatePath

#-----------------------------CART SECTION--------------------------------
@require_POST #this allows for multiple products to be added (via forms)
def cart_add(request, product_id):
    basket = cart.Cart(request) #this will call cart (don't ask why it's basket, I'm not renaming it)
    product = get_object_or_404(Merch, ID=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data #the cd will return all of the form objects as strings !REMEMBER THAT!
        basket.add(product=product,#calling the add method
                    quantity=cd['quantity'],
                    update_quantity=cd['update'])
    return HttpResponseRedirect(reverse('mainapp:cart_detail'))

def cart_remove(request, product_id):
    basket = cart.Cart(request)
    product = get_object_or_404(Merch, ID=product_id)
    basket.remove(product)#calling remove method
    return HttpResponseRedirect(reverse('mainapp:cart_detail'))

def cart_detail(request):#it just calls the basket and renders
    basket = cart.Cart(request)
    return render(request, 'basket.html', {'basket': basket})

def order_create(request):# calling the order form to place an order, duh
    basket = cart.Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in basket:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['Price'],
                                         quantity=item['quantity'])
            
            basket.clear()
            return render(request, 'ordered.html',
                          {'order': order})
    else:
        form = OrderCreateForm()
    return render(request, 'order.html',
                  {'cart': basket, 'form': form})

#----------------------------USER SECTION-------------------------------------
def user_login(request):#logs the user in
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('mainapp:frontpage'))
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')#Ideally, I'd redirect in all cases and flash a message, I know you can do it in flask, but no idea if Django does
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']
            profile.save()
            registered = True
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
    return render(request,'register.html',
                          {'user_form':user_form,
                           'profile_form':profile_form,
                           'registered':registered})


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('mainapp:frontpage'))

#this is a dumb way to do it
#make a REST API for shop metrics
    

#-------------------INDEX PAGE SECTION-------------------------------------    
class Index(ListView):
    model = Merch
    ordering = ['-PublishDate']
    paginate_by = 5
    template_name = 'index.html'
    context_object_name = 'product'
    form = SearchForm()
    
    def get_context_data(self):
        context = super().get_context_data()
        context['products'] =  Merch.objects.all()
        return context
        
    
class Search(ListView):
    model = Merch
    template_name = 'search.html'
    context_object_name = 'result'
    
    def get_queryset(self):
       result = super(Search, self).get_queryset()
       query = self.request.GET.get('search')
       if query:
          postresult = Merch.objects.filter(Name__contains=query)
          result = postresult
       else:
           result = None
       return result  

class brand_list(ListView):
    model = Brand
    ordering = ['-Brandname']
    paginate_by = 5
    template_name = 'brands.html'
    context_object_name = 'brand_list'
    
    def get_context_data(self):
        context = super().get_context_data()
        context['brand_list'] = Brand.objects.all()
        return context


def review_add(request, product_id):
    form = Review_form(request.POST)
    if form.is_valid():
        review = Review()
        review.review_text = form.cleaned_data['text']
        review.rating = int(form.cleaned_data['rating'])
        review.product = Merch.objects.get(ID=product_id)
        review.user_id = request.user
        review.save()
    return HttpResponseRedirect(reverse('mainapp:product detail',args=[product_id]))

def product_detail(request, product_id):
    product = get_object_or_404(Merch, pk=product_id,)
    cart_product_form = CartAddProductForm()
    review_list = Review.objects.filter(product=product_id)[:5]
    review_form = Review_form()
    context = {'product': product,'cart_product_form': cart_product_form,'review_form':review_form, 'review_list':review_list}
    if review_list:
        review_avg = round(Review.objects.filter(product=product_id).aggregate(Avg('rating'))['rating__avg'], 2)
        context['rating'] = review_avg
    else:pass
    return render(request, 'detail.html', context)

def about_page(request):#this is an empty template and only has 2 variables (so, like, 'partnered with x brands', 'selling y products', but dynamic and all that jazz)
    Merchcount= Merch.objects.all().count()
    Brandcount= Brand.objects.all().count()
    context= {'Merchcount': Merchcount, 'Brandcount':Brandcount}
    return render(request, path.join(constructPath(),'about.html'), context)

def brand_detail(request, brand_id):
    brand = get_object_or_404(Brand, pk=brand_id)
    return render(request, 'brand_detail.html', {'brand': brand})
