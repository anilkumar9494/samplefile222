
from django import forms
from sportapp.models import Register, Country
from dashboard.models import Addaccounttype


class DateInput(forms.DateInput):
    input_type = 'date'


class RegisterUpdateForm(forms.ModelForm):
    country = forms.ModelChoiceField(queryset=Country.objects.all().order_by('countryName'),
                                     widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Register
        fields = (
            'fname', 'lname', 'uname', 'email', 'country', 'address', 'mob', 'dob', 
            # 'acc_type', 
            'acc_limit', 'demo_acc_limit'
        )

        widgets = {
            'fname': forms.TextInput(attrs={'class': 'form-control'}),
            'lname': forms.TextInput(attrs={'class': 'form-control'}),
            'uname': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'dob': DateInput(attrs={'class':'form-control'}),
        }
