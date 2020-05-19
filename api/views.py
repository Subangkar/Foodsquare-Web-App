from django.shortcuts import render

# Create your views here.

# from django.contrib.auth.models import User
from api.serializers import *
from rest_framework import routers, serializers, viewsets


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
	queryset = User.objects.all()
	serializer_class = UserSerializer


# ViewSets define the view behavior.
class PackageViewSet(viewsets.ModelViewSet):
	queryset = Package.objects.all()
	serializer_class = PackageSerializer


# # ViewSets define the view behavior.
# class PackageViewSet(viewsets.ModelViewSet):
# 	from django.core import serializers
# 	queryset = Package.objects.all()
# 	# serializer_class = PackageSerializer
# 	data = serializers.serialize('json', list(queryset))
