
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class user_profile_info(models.Model):
    MALE = 'M'
    FEMALE = 'F'

    GENDER_CHOICES = (
        (MALE, 'M'),
        (FEMALE, 'F'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True)
    age = models.PositiveIntegerField(verbose_name='age', null=True,
                                      blank=True,
                                      validators=[MaxValueValidator(100)])
    gender = models.CharField(verbose_name='gender', max_length=1,
                              choices=GENDER_CHOICES, null=True, blank=True)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            user_profile_info.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.user_profile_info.save()

    def __str__(self):
        return self.user.Username


class brand(models.Model):
    brand_name = models.CharField(max_length=20)
    picture = models.ImageField(null=True, blank=True,
                                upload_to="brands/")
    countries_choices = [
                        ('RU', 'Russia'),
                        ('CN', 'China'),
                        ('JP', 'Japan'),
                        ('US', 'United States'),
                        ('EG', 'Egypt'),
                        ]
    country = models.CharField(
        max_length=2,
        choices=countries_choices)

    def __str__(self):
        return self.brand_name


class merch(models.Model):
    name = models.CharField(verbose_name='name', max_length=200,
                            blank=False, null=True)
    usage = models.CharField(max_length=50, blank=False)
    brand = models.ForeignKey(brand, on_delete=models.CASCADE)
    price = models.PositiveIntegerField(verbose_name='price', default=0)
    description = models.TextField(blank=True)
    picture = models.ImageField(null=True, blank=True,
                                upload_to="products/")
    publish_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class order(models.Model):
    # order is the client's contacts, OrderItem is what the client ordered
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
        verbose_name = 'order'
        verbose_name_plural = 'orders'

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class order_item(models.Model):
    order = models.ForeignKey(order, on_delete=models.CASCADE,
                              related_name='items')
    product = models.ForeignKey(merch, on_delete=models.CASCADE,
                                related_name='order_items')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity


class review(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE,
                                verbose_name='reviewer id')
    product = models.ForeignKey(merch, on_delete=models.CASCADE,
                                verbose_name='reviewed product')
    review_text = models.TextField(blank=False, verbose_name='review text')
    rating_choices = [
                    (1, 'one'), (2, 'two'),
                    (3, 'three'), (4, 'four'),
                    (5, 'five')
                    ]
    rating = models.PositiveIntegerField(choices=rating_choices)

    def __str__(self):
        return 'Review id: {}'.format(self.id)


class banner(models.Model):
    # check the template tag for banner
    # there's somewhat of a surprise mechanic there
    link = models.URLField(max_length=200, blank=False)
    banner_pic = models.ImageField(upload_to='banners/', blank=False)
    subscribed = models.PositiveIntegerField(default=1,
                                             validators=[MinValueValidator(1),
                                                         MaxValueValidator(12)]
                                             )
