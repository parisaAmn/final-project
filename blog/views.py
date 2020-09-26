from django.contrib.auth import login, authenticate , logout
from django.shortcuts import render, redirect
from .forms import SignUpForm , SignInForm
from .models import Profile
from django.contrib.auth.hashers import make_password

# Create your views here.
def index(request):
    return render(request, 'blog/index.html', {})

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
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'blog/signup2.html', {'form': form})

def sign_in(request):
    if request.method == 'POST':
        form = SignInForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            fingerprint = form.cleaned_data.get('browserfingerprint')
            user = authenticate(username=username, password=password)
            if user is not None:
                this_user = Profile.objects.get(username = username )
                print(this_user.username)
                print(this_user.browserfingerprint)
                print(this_user.bf_uniquenes)
                if this_user.browserfingerprint != fingerprint : 
                    number = Profile.objects.filter(browserfingerprint=fingerprint).count()
                    if number == 1 :
                        print("111111")
                        Profile.objects.filter(browserfingerprint=fingerprint).update(bf_uniquenes=False)
                        Profile.objects.filter(username=user.username).update(browserfingerprint = fingerprint,
                                                                                bf_uniquenes=False)
                    elif number > 1 :
                        print('222222')
                        Profile.objects.filter(username=user.username).update(browserfingerprint = fingerprint,
                                                                                bf_uniquenes=False)
                    else:
                        Profile.objects.filter(username=user.username).update(browserfingerprint = fingerprint,
                                                                                bf_uniquenes=True)
                login(request, user)
                # messages.info(request, f"You are now logged in as {username}")
                return redirect('index')
            else:
                # messages.error(request, "Invalid username or password.")
                return render(request, 'blog/sign_in.html', {'form': form})
        else:
            # messages.error(request, "Invalid username or password.")
            return render(request, 'blog/sign_in.html', {'form': form})
    else:
        form = SignInForm()
    return render(request, 'blog/sign_in.html', {'form': form})


def sign_in2(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is None:
            context = {}
            context['error'] = 1
            return redirect('main_page', context)
            #age redirect javab nadad
            #return render(request , main.html , context) 
    else:
        login(request,user)
        return redirect('main_page')
    return render(request, 'blog/sign_in.html', {})

def signout(request):
    logout(request)
    # messages.info(request, "Logged out successfully!")
    return redirect("index")