from django.contrib.auth import login, authenticate , logout
from django.shortcuts import render, redirect
from .forms import SignUpForm , SignInForm
from .models import CanvasProfile
from django.contrib.auth.hashers import make_password
from django.contrib import messages 

# Create your views here.

def index(request):
    print('index func:')
    return render(request , 'canvas/index.html' , {'check_fingerprint':True})

def ajaxx(request):
    # print('ajax func:')
    # if request.is_ajax() and request.method == 'GET':
    #     print('1')
    #     fingerprint = request.GET.get("result_data" , None)
    #     if fingerprint is not None:
    #         print('2')
    #         number = Profile.objects.filter(browserfingerprint = fingerprint ).count()
    #         if number == 1:
    #             print('3')
    #             user = Profile.objects.get(browserfingerprint = fingerprint)
    #             user.backend = 'django.contrib.auth.backends.ModelBackend'
    #             login(request , user)
    #             print('5')
    #             return render(request , 'canvas/index.html' , {'check_fingerprint':False})
    #         else:
    #             print('6')
    #             return render(request , 'canvas/index.html' , {'check_fingerprint':False})
    #     else:
    #         print('7')
    #         return render(request , 'canvas/index.html' , {'check_fingerprint':False})
    # else:
    #     print('8')
        return render(request , 'canvas/index.html' , {'check_fingerprint':False})
        

def about(request):
    return render(request, 'canvas/about.html', {})

def contact(request):
    return render(request, 'canvas/contact.html', {})

def test(request):
    return render(request, 'canvas/default.html', {})

def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            print('sign up func:')
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
    return render(request, 'canvas/signup2.html', {'form': form})

def sign_in(request):
    if request.method == 'POST':
        form = SignInForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            fingerprint = form.cleaned_data.get('browserfingerprint') # fingerprint that has been calculated in the front
            user = authenticate(username=username, password=password)
            if user is not None:
                this_user = Profile.objects.get(username = username )
                print("sign in function :")
                if this_user.browserfingerprint != fingerprint : 
                    #calcuate number of users with the new fingerprint
                    number = Profile.objects.filter(browserfingerprint=fingerprint).count()
                    if number == 1 :
                        print("111111")
                        # in this case we should change uniqueness of previuse user and this user to False
                        # and update fingerprint of this user to the new fingerprint
                        Profile.objects.filter(browserfingerprint=fingerprint).update(bf_uniquenes=False)
                        Profile.objects.filter(username=user.username).update(browserfingerprint = fingerprint,
                                                                                bf_uniquenes=False)
                    else:
                        print('222222')
                        # if number >1 :
                        # if there is more than one user with new fingerprint, there is no need to update
                        # uniqueness of previuse users.
                        # just update fingerprint of this user and put its uniqueness=False
                        # if number = 0 :
                        # there is no users with new fingerprint
                        # so just update dingerprint of this user and put its uniqueness= False 
                        Profile.objects.filter(username=user.username).update(browserfingerprint = fingerprint,
                                                                           bf_uniquenes=False)
                
                login(request, user)
                print("user loged in")
                # messages.info(request, f"You are now logged in as {username}")
                return redirect('index')
                # return render(request , "canvas/index.html", {'check_fingerprint':False})
            else:
                messages.error(request, "Invalid username or password.")
                return render(request, 'canvas/sign_in.html', {'form': form})
        else:
            messages.error(request, "Invalid username or password.")
            return render(request, 'canvas/sign_in.html', {'form': form})
    else:
        form = SignInForm()
    return render(request, 'canvas/sign_in.html', {'form': form})

def signout(request):
    print('sign out func:')
    logout(request)
    # messages.info(request, "Logged out successfully!")
    return render(request , "canvas/logout.html")

