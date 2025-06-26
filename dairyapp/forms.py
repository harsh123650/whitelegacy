from django import forms
from django.contrib.auth.models import User
from .models import ContactMessage, SubscriptionRequest

class UserCreateForm(forms.ModelForm):
    role = forms.ChoiceField(choices=[
        ('staff', 'Staff'),
        ('worker', 'Worker'),
        ('customer', 'Customer')
    ])
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password', 'role']

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']

class SubscribeForm(forms.ModelForm):
    class Meta:
        model = SubscriptionRequest
        fields = ['name', 'mobile', 'address', 'litre_needed']
