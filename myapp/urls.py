"""myapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views 
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include, reverse
from pages.views import home_view 
from users.views import registerPage, profilePage, VerificationView, ManageSubmission #, activate

from animalabuse.views import profile_upload, search, user_profile_view, submitnew, success,test_view
from django.conf.urls import url

from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name = 'home'),
    

    path('upload-csv/', profile_upload, name="profile_upload"),
    url(r'^search/$', search, name='search'),
    # abuser profile
    path('search/<int:user_id>/', user_profile_view), 
    url(r'^submitnew/$', submitnew, name='submitnew'),
    url(r'^success/$', success),

    # allauth path

    path('accounts/', include('allauth.urls')),
    
    path('register/', registerPage, name="register"),
    path('login/', auth_views.LoginView.as_view(template_name = 'login.html', redirect_authenticated_user=True), name="login"),
    path('logout/', auth_views.LogoutView.as_view(template_name = 'logout.html'), name="logout"), 
    
    path('password_reset/', 
         auth_views.PasswordResetView.as_view(template_name = 'password_reset.html'), 
         name="password_reset"), 
    path('password_reset/done/', 
         auth_views.PasswordResetDoneView.as_view(template_name = 'password_reset_done.html'), 
         name="password_reset_done"), 
    path('password_reset_confirm/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name = 'password_reset_confirm.html'), 
         name="password_reset_confirm"), 
    path('password_reset_complete/', 
         auth_views.PasswordResetCompleteView.as_view(template_name = 'password_reset_complete.html'), 
         name="password_reset_complete"), 


    # User profile
    path('profile/', profilePage, name="profile"),


    path('test/', test_view, name = "test view"),
    #url(r'^', include('django.contrib.auth.urls')),
    #url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    #    activate, name='activate'),

    path('activate/<uidb64>/<token>', VerificationView.as_view(), name="activate"),
    path('submission/', ManageSubmission.as_view(), name='manage_submission')

]




if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


