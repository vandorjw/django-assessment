# -*- coding: utf-8 -*-
from django.http import HttpResponse
from assessment import VERSION

def details(request):
    return HttpResponse(VERSION)