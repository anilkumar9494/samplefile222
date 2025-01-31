
from django.utils.translation import gettext_lazy as _
from django.forms.widgets import TextInput
from django import forms


class ResetPasswordForm(forms.Form):
    email = forms.CharField(label=_("Email"), max_length=256,widget=forms.TextInput(attrs={'placeholder': 'Enter Email','name':'email','class':'required'}))


class ResetPasswordConfirmForm(forms.Form):

    new_password1 = forms.CharField(label=_("New password"), max_length=25,widget=forms.PasswordInput(attrs={'placeholder': 'New password','class':'required','pattern':'[A-Za-z0-9]+'}))
    new_password2 = forms.CharField(label=_("Enter Password Again"), max_length=25,widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password Again','class':'required','pattern':'[A-Za-z0-9]+'}))
