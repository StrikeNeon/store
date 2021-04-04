# -*- coding: utf-8 -*-
from django import template
from mainapp.models import banner
from mainapp.views import construct_path
from os import path
from itertools import accumulate
from random import choices


def change():
    '''
    This seems stupid, BUT if you want to incentivize advertisers to pay more, here's a fair system:
        the more you pay, the better the chances of their ad showing up, you need a weighted choice for that,
        ecxept it uses cumulatives, not relatives
        no one will probably see this though, it's just a banner tag :(
    '''
    banners = banner.objects.all()
    bannerid = [choice.id for choice in banners]
    subs = [choice.subscribed for choice in banners]
    weights = accumulate(subs)
    winrar = choices(bannerid, weights, k=1)[0]
    result = banner.objects.get(id=winrar)
    return result


register = template.Library()


@register.inclusion_tag(path.join(construct_path(), 'banner.html'))
def big_banner():
    try:
        banners = change()
        return {'banners': banners}
    except IndexError:
        return None
