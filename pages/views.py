from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def home_view(request, *args, **kwargs):
	print(args, kwargs)
	print(request.user)
	my_context = {
		'my_text':'This is about us',
		'my_number':123
	}
	#return HttpResponse('<h1>Hellp World</h1>')
	return render(request, "home.html", my_context)