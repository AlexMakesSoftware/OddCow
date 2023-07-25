from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterUserForm, UpdateUserForm, ChangePasswordForm
from django.contrib.auth.models import User


def unauthorised_page(request):
    return render(request, 'authenticate/unauthorised.html')


def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return redirect('home')
        else:
            # Return an 'invalid login' error message.
            messages.error(request, 'There was a problem loging you in. Please check your details and try again.')
            return redirect('login')
    else:
        return render(request, 'authenticate/login.html', {})
    

def logout_user(request):
    logout(request)
    messages.success(request, 'You were logged out.')
    return redirect('login')


def register_user(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username,password=password)
            login(request, user)
            messages.success(request, ("Registration sucessful."))
            return redirect('home')
    else:
        form = RegisterUserForm()
    return render(request, 'authenticate/register_user.html',{'form':form})


def update_user(request):
    # N.B. Our middleware already takes care of users who aren't logged in.

    current_user = User.objects.get(id=request.user.id)

    update_form = UpdateUserForm(request.POST or None, instance=current_user)
   
    if update_form.is_valid():
        update_form.save()        
        messages.success(request, "Your profile has been updated.")
        return redirect('home')
    else:        
        for field_errors in update_form.errors.values():
            for error in field_errors:
                messages.error(request, error)

    return render(request, 'authenticate/update_user.html', {
        'update_form': update_form
    })


def change_pass(request):
    current_user = User.objects.get(id=request.user.id)
    password_form = ChangePasswordForm(request.user, request.POST or None)

    if password_form.is_valid():
        password_form.save()
        messages.success(request, "Your profile has been updated.")
        return redirect('home')
    else:
        for field_errors in password_form.errors.values():
            for error in field_errors:
                messages.error(request, error)    

    return render(request, 'authenticate/change_pass.html', {
        'password_form': password_form,
    })