from django.urls import path
from . import views
urlpatterns = [
    path('canvas/', views.index, name='index'),
    path('canvas/signup/', views.signup, name='signup'),
    path('canvas/sign_in/', views.sign_in, name='sign_in'),
    path("canvas/signout", views.signout, name="signout"),
    path('canvas/about/', views.about, name='about'),
    path('canvas/contact/', views.contact, name='contact'),
    path('canvas/test/', views.test, name='test'),
    path('canvas/ajax/', views.ajaxx, name='ajax'),

]