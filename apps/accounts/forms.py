from django import forms
from django.contrib.auth import authenticate

from apps.accounts.models import User


class PhoneLoginForm(forms.Form):
    phone_number = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            "class": "dw-input",
            "dir": "ltr",
            "inputmode": "tel",
            "autocomplete": "tel",
            "placeholder": "06XXXXXXXX",
        }),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "dw-input",
            "dir": "ltr",
            "autocomplete": "current-password",
        }),
    )

    def clean(self):
        cleaned = super().clean()
        phone = cleaned.get("phone_number", "").strip()
        password = cleaned.get("password", "")
        if phone and password:
            self.user = authenticate(username=phone, password=password)
            if self.user is None:
                raise forms.ValidationError("رقم الهاتف أو كلمة السر غلط")
            if not self.user.is_active:
                raise forms.ValidationError("هاد الحساب معطل")
        return cleaned


class PhoneRegisterForm(forms.Form):
    phone_number = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            "class": "dw-input",
            "dir": "ltr",
            "inputmode": "tel",
            "autocomplete": "tel",
            "placeholder": "06XXXXXXXX",
        }),
    )
    full_name = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            "class": "dw-input",
            "placeholder": "الاسم الكامل (اختياري)",
        }),
    )
    password = forms.CharField(
        min_length=6,
        widget=forms.PasswordInput(attrs={
            "class": "dw-input",
            "dir": "ltr",
            "autocomplete": "new-password",
        }),
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "dw-input",
            "dir": "ltr",
            "autocomplete": "new-password",
        }),
    )

    def clean_phone_number(self):
        phone = self.cleaned_data["phone_number"].strip()
        if User.objects.filter(phone_number=phone).exists():
            raise forms.ValidationError("هاد الرقم مسجل من قبل. جرب دخل.")
        return phone

    def clean(self):
        cleaned = super().clean()
        pw = cleaned.get("password", "")
        pw2 = cleaned.get("password_confirm", "")
        if pw and pw2 and pw != pw2:
            raise forms.ValidationError("كلمة السر ماشي بحال بحال")
        return cleaned
