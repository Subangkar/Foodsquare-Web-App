from django.forms import ModelForm

from browse.models import Package


class PackageForm(ModelForm):
	class Meta:
		model = Package
		fields = ('pkg_name', 'for_n_persons', 'image', 'details', 'price', 'category')
