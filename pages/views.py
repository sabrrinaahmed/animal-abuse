from django.shortcuts import render
from animalabuse.models import animalabuse

# Create your views here.
def home_view(request, *args, **kwargs):
	abuse_count = animalabuse.objects.count()
	if abuse_count > 1000:
    		abuse_count = '1000+'
	
	my_context = {
		'my_text':'This is about us',
		'my_number':123,
		'abuses': abuse_count
	}
	return render(request, "home.html", my_context)