from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.core.exceptions import ValidationError



class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        if not email:
            raise ValueError("Email alanı gereklidir")
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password):
        user = self.create_user(email, first_name, last_name, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user




class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30,null=False,blank=False)
    last_name = models.CharField(max_length=30,null=False,blank=False)
    address = models.CharField(max_length=500,null=True,blank=True)
    city = models.CharField(max_length=100,null=True,blank=True)
    country = models.CharField(max_length=50,null=True,blank=True)
    zipcode = models.CharField(null=True,blank=True,max_length=5)
    gsmnumber = models.CharField(null=True,blank=True,max_length=11)
    cardnumber = models.CharField(null=True,blank=True,max_length=16)
    expire = models.CharField(max_length=5,null=True,blank=True)
    cvc = models.CharField(null=True,blank=True, max_length=3)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date = models.DateField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["first_name","last_name","password"]

    objects = CustomUserManager()

    def clean(self):
        """Alanların geçerliliğini kontrol eden metod"""
        # Kart numarası kontrolü
        if self.cardnumber and not self.cardnumber.isdigit():
            raise ValidationError({"cardnumber": "Kart numarası sadece rakamlardan oluşmalıdır."})

        if self.cardnumber and len(self.cardnumber) != 16:
            raise ValidationError({"cardnumber": "Kart numarası tam olarak 16 haneli olmalıdır."})

        # CVV kontrolü
        if self.cvc and not self.cvc.isdigit():
            raise ValidationError({"cvc": "CVV sadece rakamlardan oluşmalıdır."})

        if self.cvc and not (3 <= len(self.cvc) <= 4):
            raise ValidationError({"cvc": "CVV 3 veya 4 haneli olmalıdır."})

        # GSM numarası kontrolü
        if self.gsmnumber and not self.gsmnumber.isdigit():
            raise ValidationError({"gsmnumber": "Telefon numarası sadece rakamlardan oluşmalıdır."})

        # Posta kodu kontrolü
        if self.zipcode and not self.zipcode.isdigit():
            raise ValidationError({"zipcode": "Posta kodu sadece rakamlardan oluşmalıdır."})

        # Son kullanma tarihi kontrolü (MM/YY formatında olmalı)
        if self.expire:
            parts = self.expire.split("/")
            if len(parts) != 2 or not all(part.isdigit() for part in parts) or len(parts[0]) != 2 or len(parts[1]) != 2:
                raise ValidationError({"expire": "Son kullanma tarihi MM/YY formatında olmalıdır."})

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
