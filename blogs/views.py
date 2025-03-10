from django.shortcuts import render,get_object_or_404
from .models import Blog
from shop.models import Item

def blog(request,slug):
    footercoffes = Item.objects.order_by('-numberofsales')[:4]
    blog = get_object_or_404(Blog,slug=slug)
    context = {
        "blog":blog,
        "footercoffes":footercoffes
    }
    return render(request,"blog.html",context)


def blogs(request):
    blog = Blog.objects.all()
    footercoffes = Item.objects.order_by('-numberofsales')[:4]
    context = {
        "blog":blog,
        "footercoffes":footercoffes
    }
    return render(request,"blogs.html",context)