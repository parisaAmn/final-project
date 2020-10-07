from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name='cindex'),
    path('signup/', views.signup, name='csignup'),
    path('sign_in/', views.sign_in, name='csign_in'),
    path("signout", views.signout, name="csignout"),
    path('about/', views.about, name='cabout'),
    path('contact/', views.contact, name='ccontact'),
    path('test/', views.test, name='ctest'),
    path('ajax/', views.ajaxx, name='cajax'),

] 