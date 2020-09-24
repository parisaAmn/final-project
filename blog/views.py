from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .forms import SignUpForm
from .models import Profile
from django.contrib.auth.hashers import make_password

# Create your views here.
def index(request):
    return render(request, 'blog/index.html', {})

def sign_up(request):
    return render(request, 'blog/sign_up.html', {})


def sign_in(request):
    return render(request, 'blog/sign_in.html', {})

def about(request):
    return render(request, 'blog/about.html', {})

def contact(request):
    return render(request, 'blog/contact.html', {})

def test(request):
    return render(request, 'blog/default.html', {})

def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            unique = True # if browser fingerprint is unique
            fingerprint = form.cleaned_data.get('browserfingerprint')
            #try to find user with this fingerprint in database
            number = Profile.objects.filter(browserfingerprint=fingerprint).count()
            #if fingerprint doesn't exist in database
            if number == 1 :
                print("111111")
                unique = False
                Profile.objects.filter(browserfingerprint=fingerprint).update(bf_uniquenes=False)
            elif number > 1 :
                print('222222') 
                unique = False
            user = Profile.objects.create(username=form.cleaned_data.get('username'),
                                        password=make_password(form.cleaned_data.get('password1')),
                                        email=form.cleaned_data.get('email'),
                                        browserfingerprint=fingerprint,
                                        bf_uniquenes=unique)
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            # login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'blog/signup2.html', {'form': form})
