from django.contrib.auth import login, authenticate , logout
from django.shortcuts import render, redirect
from .forms import SignUpForm , SignInForm
from .models import CanvasProfile
from django.contrib.auth.hashers import make_password
from django.contrib import messages 
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings 


# Create your views here.

def index(request):
    print('index func:')
    return render(request , 'canvas/index.html' , {'check_fingerprint':True})

def ajaxx(request):
    print('ajax func:')
    if request.is_ajax() and request.method == 'GET':
        print('1')
        fingerprint = request.GET.get("result_data" , None)
        if fingerprint is not None:
            print('2')
            number = CanvasProfile.objects.filter(canvasfingerprint = fingerprint ).count()
            if number == 1:
                print('3')
                user = CanvasProfile.objects.get(canvasfingerprint = fingerprint)
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request , user)
                print('5')
                return render(request , 'canvas/index.html' , {'check_fingerprint':False})
            else:
                print('6')
                return render(request , 'canvas/index.html' , {'check_fingerprint':False})
        else:
            print('7')
            return render(request , 'canvas/index.html' , {'check_fingerprint':False})
    else:
        print('8')
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
            unique = True # if canvas fingerprint is unique
            fingerprint = form.cleaned_data.get('canvasfingerprint')
            #try to find user with this fingerprint in database
            number = CanvasProfile.objects.filter(canvasfingerprint=fingerprint).count()
            if number == 1 :
                print("111111")
                unique = False
                CanvasProfile.objects.filter(canvasfingerprint=fingerprint).update(uniqueness=False)
            elif number > 1 :
                print('222222') 
                unique = False
            user = CanvasProfile.objects.create(username=form.cleaned_data.get('username'),
                                        password=make_password(form.cleaned_data.get('password1')),
                                        email=form.cleaned_data.get('email'),
                                        canvasfingerprint=fingerprint,
                                        uniqueness=unique)
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('c_index')
    else:
        form = SignUpForm()
    return render(request, 'canvas/signup2.html', {'form': form})

def sign_in(request):
    if request.method == 'POST':
        form = SignInForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            fingerprint = form.cleaned_data.get('canvasfingerprint') # fingerprint that has been calculated in the front
            user = authenticate(username=username, password=password)
            if user is not None:
                this_user = CanvasProfile.objects.get(username = username )
                print("sign in function :")
                if this_user.canvasfingerprint != fingerprint : 
                    # SEND WARNING EMAIL
                    now = timezone.now()
                    subject = "XX Unexpected sign-in attempt XX"
                    line0 = "somenoe using an unrecognised device attempted to sign in to your account.\n"
                    line1 = " this sign in attempt was made at:\n"
                    line2 = "TIME: {}\n".format(now)
                    line3 = "if this was you, you don't need to do anything else.\n"
                    line4 = "If you did not recently sign in, you should immediately change your password.\n"
                    line5 = "Passwords should be unique and not used for any other sites or services.\n"
                    message = line0+line1 + line2 + line3 + line4 + line5
                    email_from = settings.EMAIL_HOST_USER 
                    email_to = ['parisa.amani17@gmail.com', ]
                    # email_to = [this_user.email, ]
                    send_mail(subject, message, email_from, email_to, fail_silently=False, )
                    # END SEND WARNING EMAIL
                    #calcuate number of users with the new fingerprint
                    number = CanvasProfile.objects.filter(canvasfingerprint=fingerprint).count()
                    if number == 1 :
                        print("111111")
                        # in this case we should change uniqueness of previuse user and this user to False
                        # and update fingerprint of this user to the new fingerprint
                        CanvasProfile.objects.filter(canvasfingerprint=fingerprint).update(uniqueness=False)
                        CanvasProfile.objects.filter(username=user.username).update(canvasfingerprint = fingerprint,
                                                                                uniqueness=False)
                    else:
                        print('222222')
                        # if number >1 :
                        # if there is more than one user with new fingerprint, there is no need to update
                        # uniqueness of previuse users.
                        # just update fingerprint of this user and put its uniqueness=False
                        # if number = 0 :
                        # there is no users with new fingerprint
                        # so just update dingerprint of this user and put its uniqueness= False 
                        CanvasProfile.objects.filter(username=user.username).update(canvasfingerprint = fingerprint,
                                                                           uniqueness=False)
                
                login(request, user)
                print("user loged in")
                # messages.info(request, f"You are now logged in as {username}")
                return redirect('c_index')
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

