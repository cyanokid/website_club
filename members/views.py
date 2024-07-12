from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
#library for register
from django.contrib.auth.forms import UserCreationForm

from .forms import RegisterUserForm


# Create your views here.
def login_user(request):

    #if they fill the form
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Redirect to a success page.
            messages.success(request, ("You are log in successfully."))
            return redirect('home')

        else:
            # Return an 'invalid login' error message.
            messages.success(request, ("There is an Error. Please Try to Login Again."))
            return redirect('login')

    #return an 'invalid login' error
    else:
        return render(request, 'authenticate/login.html', {})

def logout_user(request):
    logout(request)
    # Redirect to a success page.
    messages.success(request, ("You were Logged Out."))
    return redirect('home')

def register_user(request):
    #if they fill up the form
    if request.method == "POST":
        #the form is filled and submit
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            #to sign in after sign up the form
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("Registration Successful! "))
            return redirect('home')
            
    #if they want to fill up the form/ not yet fill up the form
    else:
        #pass the blank form
        form = RegisterUserForm()

    return render(request, 'authenticate/register_user.html', {
        "form" : form,
    })
