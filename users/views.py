from django.shortcuts import render, redirect
from .forms import UserSignUpForm, UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def signup(request):
    
    if request.method == 'POST':
        form  = UserSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Account Created for {username}")
            return redirect('users-login')

    else:
        form  = UserSignUpForm()
    
    return render(request, 'users/signup.html', context={"title": "Registrar", "form": form, "active": 'signup'})

@login_required # MAKE SURE THAT THE PROFILE PAGE IS ACCESSABLE ONLY IF USER IS LOGED IN
def profile(request):
    
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST, 
            request.FILES, 
            instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid:
            u_form.save()
            p_form.save()
            messages.success(request, f"Account has been updated!")
            return redirect('users-profile')
            
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'u_form': u_form,
        'p_form': p_form,
        "active": 'profile',
        "title": 'Perfil'
    }
    
    return render(request, 'users/profile.html', context)
