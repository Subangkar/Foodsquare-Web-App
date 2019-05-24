from django.shortcuts import render

# Create your views here.
import json

from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

# from .serializers import *


def index(request):
	return render(request, "browse/index.html", {})


def viewOrder(request):
	return render(request, "browse/order.html")


def viewRestaurants(request):
	return render(request, "browse/restaurants.html", {})

