from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

def login_view(request):

    # ✅ If already logged in → go dashboard
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('dashboard')

        return render(request, 'login.html', {
            'error': 'Invalid username or password'
        })

    return render(request, 'login.html')


from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('login')