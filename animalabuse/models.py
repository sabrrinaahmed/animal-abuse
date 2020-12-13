from django.db import models
from localflavor.us.models import USStateField

# Create your models here.
class animalabuse(models.Model):

	name = models.CharField(max_length = 120)
	DOB = models.DateField(null = True, blank = True)
	Age = models.DecimalField(null = True, blank = True, decimal_places = 0, max_digits = 3)
	Address = models.TextField(blank = True, null = True)
	county = models.CharField(blank = True, null = True, max_length = 120)
	#state = models.CharField(blank = True, null = True, max_length = 30)
	state = USStateField(blank = True, null = True)
	Offense = models.TextField(blank = True, null = True)
	convictiondate = models.DateField(null = True, blank = True) 
	expirationdate = models.DateField(null = True)
	image = models.URLField(null = True, blank = True)
	dataSource = models.CharField(blank = True, null = True, max_length = 120)
	sourceDescription = models.CharField(blank = True, null = True, max_length = 120)
	sourceLink = models.URLField(null = True, blank = True)


	def __str__(self):
		return self.name

