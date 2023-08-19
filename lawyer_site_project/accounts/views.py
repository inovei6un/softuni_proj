from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from accounts.forms import UserRegistrationForm, UserLoginForm, UserProfileForm


@login_required
def redact_profile(request):
    user = request.user
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            new_password = request.POST.get('password')
            if new_password:
                user.password = make_password(new_password)
            form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserProfileForm(instance=user)

    return render(request, 'redact_profile.html', {'form': form})


def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()

            user.set_password(request.POST['password'])
            user.save()

            login(request, user)

            return redirect('index')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})


def login_user(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                request.session['user_id'] = user.id
                return redirect('index')
            else:
                form.add_error(None, 'Невалидни данни! Моля опитайте отново!')
    else:
        form = UserLoginForm()

    return render(request, 'login.html', {'form': form})


@login_required
def logout_user(request):
    logout(request)
    return redirect('index')


@login_required
def deactivate_account(request):
    user = request.user

    user.is_active = False
    user.save()

    return render(request, 'account_deactivated.html')
