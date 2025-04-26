"""
URL configuration for coffeshop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from users import views as users_views
from blogs import views as blogs_views
from shop import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('blog/<slug:slug>',blogs_views.blog,name="blog"),
    path('blogs/',blogs_views.blogs,name="blogs"),
    path('register/',users_views.register,name="register"),
    path('login/',users_views.loginuser,name="login"),
    path('delete/<int:id>',views.deletecoffeincart,name="deletecoffeincart"),
    path('updateuser/',users_views.updateuser,name="updateuser"),
    path('logoutuser/',users_views.logoutuser,name="logoutuser"),
    path('admin/', admin.site.urls),
    path('',views.index,name="index"),
    path('order/',views.order,name="order"),
    path('coffes/',views.coffes,name="coffes"),
    path('<slug:slug>/',views.coffesdetail,name="coffesdetail"),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

def create_superuser():
    from django.contrib.auth import get_user_model
    User = get_user_model()
    if not User.objects.filter(username="admin").exists():
        User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="AdminPassword123"
        )

try:
    create_superuser()
except Exception as e:
    print(f"Superuser creation error: {e}")
