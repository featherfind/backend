from django.http import HttpResponse
from django.shortcuts import render
def my_view(request):
    return render(request,'authlanding.html')