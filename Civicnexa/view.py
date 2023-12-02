from django.shortcuts import get_object_or_404, render, redirect
from django.http.request import HttpRequest
from django.http.response import HttpResponse


def landing(request):
    return render(request, 'landing.html')