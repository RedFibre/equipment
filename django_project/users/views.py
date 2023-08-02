from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.contrib.auth import login, authenticate


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            password = form.cleaned_data.get('password1')
            username = form.cleaned_data.get('username')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
            return redirect('u_profile')
    else:
        form = UserRegisterForm

    return render(request, 'users/register.html', {'form': form})
