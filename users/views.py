from django.shortcuts import render,redirect
from .forms import RegisterForm,LoginForm
from .models import CustomUser
from shop.models import Item
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.models import User
from django.contrib import messages

def register(request):
    footercoffes = Item.objects.order_by('-numberofsales')[:4]
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request,"Kayıt Olundu")
            return redirect('index')
        else:
            messages.warning(request,form.errors)
    else:
        form = RegisterForm()
    context = {
        "form": form,
        "footercoffes":footercoffes
    }
    return render(request,"register.html",context)


def loginuser(request):
    footercoffes = Item.objects.order_by('-numberofsales')[:4]
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(email=email, password=password)
            if user is None:
                messages.warning(request,"Kullanıcı Bulunamadı")
            else:
                login(request, user)
                messages.success(request,"Başarıyla Giriş Yapıldı")
                return redirect('index')
        else:
            messages.warning(request,form.errors)
    else:
        form = LoginForm()
    context = {
        "form":form,
        "footercoffes":footercoffes
    }
    return render(request,"login.html",context)


def updateuser(request):
    footercoffes = Item.objects.order_by('-numberofsales')[:4]
    if request.method == "POST":
        form = RegisterForm(request.POST, instance=request.user)
        if form.is_valid():
            newuser = form.save()
            login(request, newuser)
            messages.success(request,"Kullanıcı Başarıyla Güncellendi Ve Giriş Yapıldı")
            return redirect('index')
        else:
            messages.warning(request,form.errors)
    else:
        form = RegisterForm()
    context = {
        "form":form,
        "footercoffes":footercoffes
    }
    return render(request,"updateuser.html",context)


def logoutuser(request):
    logout(request)
    messages.warning(request,"Başarıyla Çıkış Yapıldı")
    return redirect('index')

