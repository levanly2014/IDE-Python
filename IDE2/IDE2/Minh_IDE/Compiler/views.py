from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .run_py import run_py
from .time_limit import calculate_execution_time

@login_required(login_url='login')
def index(request):
    context = {}
    if request.method == 'POST':
        code = request.POST.get('code', '')
        context['code'] = code
        if code.strip():
            timeout = calculate_execution_time(code)
            result = run_py(code, time_limit=timeout)
            context['result'] = result

    return render(request, 'Compiler/index.html', context)

def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')
        
    error = None
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(request, username=u, password=p)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            error = "Tên đăng nhập hoặc mật khẩu không chính xác!"

    return render(request, 'Compiler/login.html', {'error': error})

def register_view(request):
    if request.user.is_authenticated:
        return redirect('index')

    error = None
    if request.method == 'POST':
        u = request.POST.get('username')
        e = request.POST.get('email')
        p = request.POST.get('password')
        cp = request.POST.get('confirm_password')

        if p != cp:
            error = "Mật khẩu xác nhận không trùng khớp!"
        elif User.objects.filter(username=u).exists():
            error = "Tên đăng nhập này đã tồn tại!"
        elif User.objects.filter(email=e).exists():
            error = "Email này đã được đăng ký!"
        else:
            # Tạo tài khoản bao gồm cả email
            user = User.objects.create_user(username=u, email=e, password=p)
            login(request, user) 
            return redirect('index')

    return render(request, 'Compiler/register.html', {'error': error})

def logout_view(request):
    logout(request)
    return redirect('login')