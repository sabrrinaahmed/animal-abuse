from django.shortcuts import render

# Create your views here.
def newsPage(request):

	import requests
	import json


	APIKEY = "2d822fbda85d4083a3cab2f218ca20b6"
	animal_abuser = requests.get("https://newsapi.org/v2/everything?q=animal+abuser&apiKey=2d822fbda85d4083a3cab2f218ca20b6")
	animal_cruelty = requests.get("https://newsapi.org/v2/everything?q=animal+cruelty&apiKey=2d822fbda85d4083a3cab2f218ca20b6")
	animal_abuse = requests.get("https://newsapi.org/v2/everything?q=animal+abuse&apiKey=2d822fbda85d4083a3cab2f218ca20b6")

	api_abuser = json.loads(animal_abuser.content)
	api_cruelty = json.loads(animal_cruelty.content)
	api_abuse = json.loads(animal_abuse.content)

	return render(request, 'news_template.html', {'api_abuser': api_abuser, 'api_cruelty': api_cruelty, 'api_abuse': api_abuse})

