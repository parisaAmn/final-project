from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profiles


# class SignUpForm(UserCreationForm):
#     browserfingerprint = forms.CharField(max_length=64)

#     class Meta:
#         model = Profile
#         fields = ('username', 'email', 'password1', 'password2', 'browserfingerprint')

#     def __init__(self, *args, **kwargs):
#         super(SignUpForm, self).__init__(*args, **kwargs)
#         self.fields['username'].widget.attrs['placeholder'] = 'Username'
#         self.fields['email'].widget.attrs['placeholder'] = 'Email'
#         self.fields['password1'].widget.attrs['placeholder'] = 'Password'
#         self.fields['password2'].widget.attrs['placeholder'] = 'Repeat your password'

class SignUpForm(UserCreationForm):
    browserfingerprint = forms.CharField(max_length=64)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'browserfingerprint' )
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Repeat your password'



