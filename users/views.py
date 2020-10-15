from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.urls import reverse


# User registration and login authentication
from django.contrib.auth.forms import UserCreationForm
# Mandatory user login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User


from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site

from django.template.loader import render_to_string



from .forms import CreateUserForm, UserUpdateForm, ProfileUpdateForm
from .tokens import account_activation_token
from .utils import account_activation_token


from django.core.mail import EmailMessage

from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

# Send emails using sendGrid
import sendgrid
import os
from sendgrid.helpers.mail import *


# Create your views here.
def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            form = CreateUserForm(request.POST) 
            if form.is_valid():
                
                #form.save()
                user = form.save(commit=False)

                user.is_active = False
                user.save()
                
                current_site = get_current_site(request)
                email_subject = 'Activate your account'
                email_body = {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                }
                domain = get_current_site(request).domain
                
                link = reverse('activate', kwargs={
                               'uidb64': email_body['uid'], 'token': email_body['token']})
                activate_url = 'http://' + domain + link
                message = 'Hi ' + user.username + ',\n\nPlease use the following link to activate your account:\n' + activate_url + '\n\nThanks,'                                                                  
                to_email = form.cleaned_data.get('email')
                email = EmailMessage(
                    email_subject,
                    message,
                    'nonreply@gmail.com',
                    to = [to_email],
                )

                email.send()


                username = form.cleaned_data.get('username')
                messages.success(request, f'Hi, {user}! A verification email has been sent to {to_email}! Please follow the email instruction to activate your account.')
                #print(username)

                return redirect('login')

        else:
            form = CreateUserForm()


        context = {'form': form}
        return render(request, 'register.html', context)
'''
# Send grid testing
def registerPage(request):

    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))


    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            form = CreateUserForm(request.POST) 
            from_email = Email("app187760892@heroku.com")
            if form.is_valid():
                
                #form.save()
                user = form.save(commit=False)

                user.is_active = False
                user.save()
                
                current_site = get_current_site(request)
                email_subject = 'Activate your account'
                email_body = {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                }
                domain = get_current_site(request).domain
                
                link = reverse('activate', kwargs={
                               'uidb64': email_body['uid'], 'token': email_body['token']})
                activate_url = 'http://' + domain + link
                message = 'Hi ' + user.username + ',\n\nPlease use the following link to activate your account:\n' + activate_url + '\n\nThanks,'                                                                  
                to_email = form.cleaned_data.get('email')
                email = EmailMessage(
                    email_subject,
                    message,
                    'nonreply@gmail.com',
                    to = [to_email],
                )
                mail = Mail(from_email, email_subject, to_email, message)
                response = sg.client.mail.send.post(request_body=mail.get())

                email.send()


                username = form.cleaned_data.get('username')
                messages.success(request, f'Hi, {user}! A verification email has been sent to {to_email}! Please follow the email instruction to activate your account.')
                #print(username)

                return redirect('login')

        else:
            form = CreateUserForm()


        context = {'form': form}
        return render(request, 'register.html', context)
'''


class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            if not account_activation_token.check_token(user, token):
                return redirect('login'+'?message='+'User already activated!')

            if user.is_active:
                return redirect('login')
            user.is_active = True
            user.save()
            login(request, user)
            messages.success(request, 'Account activated successfully!')
            return redirect('login')

        except Exception as ex:
            pass

        return redirect('login')
        

'''class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')'''


@login_required
def profilePage(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }

    return render(request, 'user_profile.html', context)





    