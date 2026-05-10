from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import User

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Foydalanuvchi nomi',
        widget=forms.TextInput(attrs={'placeholder': 'username', 'autofocus': True})
    )
    password = forms.CharField(
        label='Parol',
        widget=forms.PasswordInput(attrs={'placeholder': '••••••••'})
    )

class UserCreateForm(forms.ModelForm):
    password1 = forms.CharField(label='Parol', widget=forms.PasswordInput(attrs={'placeholder': '••••••••'}))
    password2 = forms.CharField(label='Parolni tasdiqlang', widget=forms.PasswordInput(attrs={'placeholder': '••••••••'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'role', 'phone']
        labels = {
            'username': 'Login (foydalanuvchi nomi)',
            'first_name': 'Ism',
            'last_name': 'Familiya',
            'email': 'Email',
            'role': 'Rol',
            'phone': 'Telefon',
        }

    def clean_password2(self):
        p1 = self.cleaned_data.get('password1')
        p2 = self.cleaned_data.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Parollar mos kelmadi!")
        return p2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

class UserEditForm(forms.ModelForm):
    """Admin tomonidan to'liq tahrirlash — login va parol ham"""
    new_password = forms.CharField(
        label='Yangi parol (o\'zgartirmasangiz bo\'sh qoldiring)',
        required=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Bo\'sh = o\'zgarmaydi'})
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'role', 'phone', 'bio', 'is_active']
        labels = {
            'username': 'Login',
            'first_name': 'Ism',
            'last_name': 'Familiya',
            'email': 'Email',
            'role': 'Rol',
            'phone': 'Telefon',
            'bio': 'Qo\'shimcha ma\'lumot',
            'is_active': 'Faol holat',
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        new_pass = self.cleaned_data.get('new_password')
        if new_pass:
            user.set_password(new_pass)
        if commit:
            user.save()
        return user

class ProfileEditForm(forms.ModelForm):
    """Foydalanuvchi o'zi o'z profilini tahrirlaydi"""
    new_password = forms.CharField(
        label='Yangi parol',
        required=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Bo\'sh = o\'zgarmaydi'})
    )
    confirm_password = forms.CharField(
        label='Parolni tasdiqlang',
        required=False,
        widget=forms.PasswordInput(attrs={'placeholder': '••••••••'})
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'bio', 'avatar']
        labels = {
            'first_name': 'Ism',
            'last_name': 'Familiya',
            'email': 'Email',
            'phone': 'Telefon',
            'bio': 'O\'zim haqimda',
            'avatar': 'Rasm',
        }

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get('new_password')
        p2 = cleaned.get('confirm_password')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Parollar mos kelmadi!")
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        new_pass = self.cleaned_data.get('new_password')
        if new_pass:
            user.set_password(new_pass)
        if commit:
            user.save()
        return user
