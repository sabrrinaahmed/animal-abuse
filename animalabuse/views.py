from django.contrib.auth.decorators import permission_required
#from django.contrib.auth.models import User

from django.shortcuts import get_object_or_404

from .models import animalabuse


import csv, io
from django.shortcuts import render, redirect
from django.contrib import messages

from django.contrib.auth import authenticate, login, logout

from datetime import datetime
from .filters import UserFilter
from .forms import SubmitForm

from django.http import HttpResponseRedirect

# User registration and login authentication
from django.contrib.auth.decorators import login_required


# Create your views here.
def product_detail_view(request):
	
	return render()

# Create your views here.
# one parameter named request
@permission_required('admin.can_add_log_entry')
def profile_upload(request):
    # declaring template
    template = "profile_upload.html"
    data = animalabuse.objects.all()
    # prompt is a context variable that can have different values      depending on their context
    prompt = {
        'order': 'Order of the CSV should be index, name, data of birth, age, address, county, state, offense, conviction date, expiration date, image',
        'profiles': data    
              } 
    # GET request returns the value of the data with the specified key.
    if request.method == "GET":
        return render(request, template, prompt)
    csv_file = request.FILES['file']
    # let's check if it is a csv file
    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'THIS IS NOT A CSV FILE')
    data_set = csv_file.read().decode('UTF-8')
    # setup a stream which is when we loop through each line 
    #we are able to handle a data in a stream
    io_string = io.StringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string, delimiter=',', quotechar='"'):
            _, created = animalabuse.objects.update_or_create(
                name = column[0].upper(),
                DOB = datetime.strptime(column[1], "%m/%d/%y") if column[1] != '' else None,
                Age = int(column[2]) if column[2] != '' else None,
                Address = column[3].split('"')[1 ] if column[3] != '' else 'UNAVAILABLE',
                county = column[4],
                state = column[5],
                Offense = column[6].upper() if column[6] != '' else 'UNAVAILABLE',
                convictiondate = datetime.strptime(column[7], "%m/%d/%y") if column[7] != '' else None,
                expirationdate = datetime.strptime(column[8], "%m/%d/%y") if column[8] != '' else None,
                image = column[9]
            )
    messages.success(request,u"Thank you for your submission !")
    context = {}
    return render(request, template, context)


# Check whether query is valid
def is_valid_queryparam(param):
    return param != '' and param is not None


def search(request):
    user_list = animalabuse.objects.all()
    user_filter = UserFilter(request.GET, queryset = user_list)

    
    # Make tuples for State and State abbreviation
    CONTIGUOUS_STATES = (('AL', 'Alabama'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('CA', 'California'), 
        ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'), ('DC', 'District of Columbia'), 
        ('FL', 'Florida'), ('GA', 'Georgia'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), 
        ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), 
        ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'), 
        ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), 
        ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), 
        ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'), 
        ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), 
        ('VT', 'Vermont'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming'))

    CONTIGUOUS_STATES_DIC = dict(CONTIGUOUS_STATES)

    state_list = []
    field_object = animalabuse._meta.get_field('state')
    for obj in user_list:
        field_value = field_object.value_from_object(obj)
        if field_value not in state_list:
            state_list.append(field_value)

    # State dict
    states = dict((st, state) for st, state in CONTIGUOUS_STATES_DIC.items() if st in state_list)        
    
    
    # Categorize offenses
    OFFENSE_TYPE = ['AGGRAVATED CRUELTY TO ANIMALS',
                                'ANIMAL FIGHTING',            
                                'CONFINEMENT/ABANDONMENT OF ANIMAL',
                                'CRIMINAL OFFENSES AGAINST ANIMALS' ,
                                'CRUELTY TO POLICE/FIRE/SAR ANIMAL',
                                'FELONY CRUELTY TO ANIMALS',
                                'SEXUAL ACTIVITIES INVOLVING ANIMALS',
                                'OTHER']
    '''OFFENSE_TYPE = (('AGGRAVATED CRUELTY', 'AGGRAVATED CRUELTY TO ANIMALS'),
                                ('ANIMAL FIGHTING', 'ANIMAL FIGHTING'),            
                                ('CONFINEMENT/ABANDONMENT', 'CONFINEMENT/ABANDONMENT OF ANIMAL'),
                                ('CRIMINAL OFFENSES', 'CRIMINAL OFFENSES AGAINST ANIMALS') ,
                                ('POLICE', 'CRUELTY TO POLICE/FIRE/SAR ANIMAL'),
                                ('FELONY CRUELTY', 'FELONY CRUELTY TO ANIMALS'),
                                ('SEXUAL', 'SEXUAL ACTIVITIES INVOLVING ANIMALS'),
                                ('OTHER', 'OTHER'))'''
    #OFFENSE_TYPE_DIC = dict(OFFENSE_TYPE)
    offense_type = [off.title() for off in OFFENSE_TYPE]
    
    # Get offenses from model           
    offense_list = []
    field_object = animalabuse._meta.get_field('Offense')
    for obj in user_list:
        field_value = field_object.value_from_object(obj)
        if field_value not in offense_list:
            offense_list.append(field_value)
    offense_list.sort()
            
    offenses={}

    for off in offense_list: 
        for off_type in OFFENSE_TYPE:
            if off_type in off:
                offenses[off] = off_type
                break
            elif 'sex' in off.lower():
                offenses[off] = 'SEXUAL ACTIVITIES INVOLVING ANIMALS'
                break
            elif 'police' in off.lower():
                offenses[off] = 'CRUELTY TO POLICE/FIRE/SAR ANIMAL'
                break
            else:
                offenses[off] = 'OTHER'


    convictiondate_query = request.GET.get('convictiondate')
    state_query = request.GET.get('state')
    offense_query = request.GET.get('Offense')


    if is_valid_queryparam(convictiondate_query):
        user_list = user_list.filter(convictiondate = convictiondate_query)

    if is_valid_queryparam(state_query) :
        user_list = user_list.filter(state = state_query)

    if is_valid_queryparam(offense_query) :
                    user_list = user_list.filter(Offense__icontains = offense_query)


    context = {
        #'queryset': user_list,
        'filter': user_filter,
        'states': states,
        #'offenses': offenses,
        #'offense_type': offense_type,
    }

    return render(request, 'search_list.html', context)


#@require_http_methods(["GET"])
def user_profile_view(request, user_id):
    """User profile page."""
    user = get_object_or_404(animalabuse, id=user_id)

    from django.contrib.staticfiles import finders
    if finders.find('images/'+ f'{user.name}' +'.png') is None:
        image_name = 'default'
    else:
        image_name = user.name

    context = {'user': user,
               'title': f'{user.name}\'s Profile',
               'path': request.path,
               'image_name':image_name}

    return render(request, 'profile.html', context)


@login_required
def submitnew(request):
    CONTIGUOUS_STATES = (('AL', 'Alabama'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('CA', 'California'), 
        ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'), ('DC', 'District of Columbia'), 
        ('FL', 'Florida'), ('GA', 'Georgia'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), 
        ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), 
        ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'), 
        ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), 
        ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), 
        ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'), 
        ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), 
        ('VT', 'Vermont'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming'))

    states = dict(CONTIGUOUS_STATES)

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SubmitForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            name = form.cleaned_data['name']
            Age = form.cleaned_data['Age']
            county = form.cleaned_data['county']
            state = form.cleaned_data['state']
            Offense = form.cleaned_data['Offense']
            convictiondate = form.cleaned_data['convictiondate']
            p = animalabuse(name=name.upper(), Age=Age, county=county.upper(), state=state, Offense=Offense.upper(),convictiondate = convictiondate)
            p.save()
            messages.success(request,u"Thank you for your submission !")
            # redirect to a new URL:
            #return HttpResponseRedirect('/success/')

      # if a GET (or any other method) we'll create a blank form    
    else: 
        form = SubmitForm()

    return render(request, 'submitform.html', {'states': states, 'form': form})


def success(request):
    return render(request, "success.html")


def test_view(request):
    return render(request, "test.html")