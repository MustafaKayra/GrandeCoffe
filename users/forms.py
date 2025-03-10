from django import forms
from .models import CustomUser
from django.core.exceptions import ValidationError


class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Şifre'}),
        label="Şifre"
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Şifreyi Onayla'}),
        label="Şifre Onay"
    )

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'address', 'city', 'country', 'zipcode', 'gsmnumber', 'cardnumber', 'expire', 'cvc')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise ValidationError("Şifreler uyuşmuyor!")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        self.fields['address'].required = False
        self.fields['city'].required = False
        self.fields['country'].required = False
        self.fields['zipcode'].required = False
        self.fields['gsmnumber'].required = False
        self.fields['cardnumber'].required = False
        self.fields['expire'].required = False
        self.fields['cvc'].required = False

        if commit:
            user.save()
        return user



class LoginForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        widget=forms.TextInput(attrs={'placeholder': 'Email Girin'})
    )
    password = forms.CharField(
        label="Şifre",
        widget=forms.PasswordInput(attrs={'placeholder': 'Şifrenizi Girin'})
    )