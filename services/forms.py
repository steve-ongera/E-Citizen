from django import forms
from .models import *
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class PersonSearchForm(forms.Form):
    id_number = forms.CharField(max_length=8, required=True)


class VehicleSearchForm(forms.Form):
    number_plate = forms.CharField(max_length=100, required=False, label='Number Plate')


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['owner_name', 'owner_id_number', 'number_plate', 'model', 'year', 'insured', 'image1', 'image2', 'image3', 'image4', 'image5', 'image6']


class PublicRecordForm(forms.ModelForm):
    class Meta:
        model = PublicRecord
        fields = ['record_type', 'description', 'id_image']

class MarriageLicenseForm(forms.ModelForm):
    class Meta:
        model = MarriageLicense
        fields = ['applicant1', 'applicant2', 'license_number', 'cert_pdf']

class PropertyDeedForm(forms.ModelForm):
    class Meta:
        model = PropertyDeed
        fields = ['owner', 'property_address', 'deed_number', 'deed_pdf']




class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = '__all__'




class TaxPaymentForm(forms.ModelForm):
    class Meta:
        model = TaxPayment
        fields = ['amount', 'month']
        widgets = {
            'month': forms.DateInput(attrs={'type': 'month'}),
        }
        labels = {
            'amount': 'Amount to Pay',
            'month': 'Tax Month',
        }

class VerifyCodeForm(forms.Form):
    secret_code = forms.CharField(max_length=10, required=True, widget=forms.TextInput(attrs={'placeholder': 'Enter secret code'}))


class SearchSecretCodeForm(forms.Form):
    secret_code = forms.CharField(max_length=10, required=True, widget=forms.TextInput(attrs={'placeholder': 'Enter secret code'}))


class CustomUserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), label='Password')
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label='Confirm Password')

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise ValidationError("Passwords do not match.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class CustomAuthenticationForm(forms.Form):
    username = forms.CharField(max_length=150, label='Username')
    password = forms.CharField(widget=forms.PasswordInput(), label='Password')



class RegisterForm(forms.Form):
    username = forms.CharField(max_length=100)
    id_number = forms.CharField(max_length=20)
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        id_number = cleaned_data.get('id_number')

        if username and id_number:
            try:
                staff = Person.objects.get(username=username, id_number=id_number)
            except Person.DoesNotExist:
                raise ValidationError('The provided username (Surname) and Reg No do not match.')

        return cleaned_data
    

class UserSearchForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)


class PaymentForm(forms.Form):
    amount = forms.DecimalField(label='Amount', max_digits=10, decimal_places=2, min_value=0)
    description = forms.CharField(label='Description', max_length=255, required=False)