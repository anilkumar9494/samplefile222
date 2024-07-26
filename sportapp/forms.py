from django.forms.widgets import TextInput
from django import forms


class CodeVerificationForm(forms.Form):

    code = forms.CharField(label=(""), max_length=6, widget=forms.TextInput(attrs={'class':'required'}))