from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name='c_index'),
    path('signup/', views.signup, name='c_signup'),
    path('sign_in/', views.sign_in, name='c_sign_in'),
    path("signout", views.signout, name="c_signout"),
    path('about/', views.about, name='c_about'),
    path('contact/', views.contact, name='c_contact'),
    path('test/', views.test, name='c_test'),
    path('ajax/', views.ajaxx, name='c_ajax'),

] 