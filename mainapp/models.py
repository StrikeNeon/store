
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator #uncomment maxvalue if you need a subs limit
from django.db import models



class UserProfileInfo(models.Model):#Thank GOD I stopped with the task, or I might have created a full site with reviews, metrics etc.
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='media/profile_pics',blank=True)
    def __str__(self):
      return self.user.username
    
    
class Brand(models.Model):
    ID = models.AutoField(primary_key=True)
    Brandname = models.CharField(max_length=20)
    Picture = models.ImageField(null=True, blank=True, upload_to="media/brands/")
    Countries_Choices = [
    ('RU', 'Russia'),
    ('CN', 'China'),
    ('JP', 'Japan'),
    ('US', 'United States'),
    ('EG', 'Egypt'),
    ]
    Country = models.CharField(
        max_length=2,
        choices=Countries_Choices)
    
    def __str__(self):
        return self.Brandname
    
class Merch(models.Model):
    ID = models.AutoField(primary_key=True)
    Name = models.CharField(verbose_name='Name', max_length=200, blank = False,null = True)
    Usage = models.CharField(max_length=50, blank = False)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    Price = models.PositiveIntegerField(verbose_name='Price', default = 0)
    
    Description = models.TextField(blank=True)
    Picture = models.ImageField(null=True, blank=True, upload_to="media/products/")
    PublishDate = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.Name


class Order(models.Model): #order is the client's contacts, OrderItem is what the client ordered
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Merch, on_delete=models.CASCADE, related_name='order_items')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity
    
class Review(models.Model):
    ID = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User,on_delete=models.CASCADE, verbose_name='reviewer id')
    product = models.ForeignKey(Merch, on_delete=models.CASCADE, verbose_name='reviewed product')
    review_text = models.TextField(blank=False, verbose_name='review text')
    Rating_Choices = [
    (1, 'one'),(2, 'two'),(3, 'three'),(4, 'four'),(5, 'five')
    ]
    rating = models.PositiveIntegerField(choices=Rating_Choices)

    def __str__(self):
        return 'Review id: {}'.format(self.ID)



class Banner(models.Model): #check the template tag for banner - there's somewhat of a surprise mechanic there
    id = models.AutoField(primary_key=True)
    link = models.URLField(max_length=200,blank=False)
    banner_pic = models.ImageField(upload_to='media/banners',blank=False)
    subscribed = models.PositiveIntegerField(default=1,
                                             validators =[MinValueValidator(1), MaxValueValidator(12)] #add maxvalue here
                                             )