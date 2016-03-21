from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.http import Http404
from django import forms

# Create your views here.
def index(request):
	return render(request, 'homepage.html')


def login(request):
	return HttpResponse("Sup my dude. The login screen should be here.")