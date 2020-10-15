#from django.contrib.auth.models import User

from .models import animalabuse
import django_filters
from multiselectfield import MultiSelectField
from django.forms.widgets import TextInput

OFFENSE_TYPE = (('AGGRAVATED CRUELTY', 'AGGRAVATED CRUELTY TO ANIMALS'),
                ('ANIMAL FIGHTING', 'ANIMAL FIGHTING'),            
                ('CONFINEMENT/ABANDONMENT', 'CONFINEMENT/ABANDONMENT OF ANIMAL'),
                ('CRIMINAL OFFENSES', 'CRIMINAL OFFENSES AGAINST ANIMALS') ,
                ('POLICE', 'CRUELTY TO POLICE/FIRE/SAR ANIMAL'),
                ('FELONY CRUELTY', 'FELONY CRUELTY TO ANIMALS'),
                ('SEXUAL', 'SEXUAL ACTIVITIES INVOLVING ANIMALS'),
                ('OTHER', 'OTHER'))

class UserFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name="name", lookup_expr='icontains', label = 'Abuser Name', 
    								widget = TextInput(attrs={'placeholder': 'Name'}))
    county = django_filters.CharFilter(field_name="county", lookup_expr='icontains', label = 'County', 
    								widget = TextInput(attrs={'placeholder': 'County'}))
    #state = django_filters.CharFilter(field_name="state", lookup_expr='icontains', label = 'State', 
    #								widget = TextInput(attrs={'placeholder': 'Choose State'}))
    Offense = django_filters.CharFilter(field_name="Offense", lookup_expr='icontains', label = 'Offense',
    								widget = TextInput(attrs={'placeholder': 'Offense Type'}))
    #offense_choice = django_filters.ChoiceFilter(field_name="offense_choice", label = 'Offense', choices = OFFENSE_TYPE) 
    convictionyear = django_filters.NumberFilter(field_name="convictiondate", lookup_expr='year', label = 'Conviction Year')
    #convictiondate = django_filters.NumberFilter(field_name="convictiondate", lookup_expr='date', label = 'Conviction Date')

    class Meta:
        model = animalabuse
        fields = ['name', 'county', 'Offense', 'state', 'convictiondate']


