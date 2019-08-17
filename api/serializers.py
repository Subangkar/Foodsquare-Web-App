from rest_framework import routers, serializers, viewsets

# from accounts.models import *
from browse.models import *


# from manager.models import *


# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = User
		# fields = ['username', 'is_delivery_man', 'is_customer', 'is_branch_manager', 'is_manager', 'is_superuser']
		fields = '__all__'


class PackageSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Package
		fields = ['id', 'pkg_name', 'price', 'category']
		# fields = '__all__'
