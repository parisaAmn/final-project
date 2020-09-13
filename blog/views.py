from django.shortcuts import render

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
    return render(request, 'blog/test.html', {})