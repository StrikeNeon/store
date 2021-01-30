# -*- coding: utf-8 -*-
from django import template
from mainapp.models import Banner
from mainapp.views import constructPath
from os import  path
from itertools import accumulate
from random import choices

def change():
    '''
    This seems stupid, BUT if you want to incentivize advertisers to pay more, here's a fair system:
        the more you pay, the better the chances of their ad showing up, you need a weighted choice for that,
        ecxept it uses cumulatives, not relatives
        no one will probably see this though, it's just a banner tag :(
    '''
    bannerid = list(Banner.objects.values_list('id', flat=True))
    subs = list(Banner.objects.values_list('subscribed', flat=True))
    weights = accumulate(subs)
    return choices(bannerid, weights,k=1)[0]



register=template.Library()

@register.inclusion_tag(path.join(constructPath(), 'banner.html'))
def big_banner():
    try:
        banners = Banner.objects.get(id = change())
        return {'banners': banners}
    except IndexError:
        return None
