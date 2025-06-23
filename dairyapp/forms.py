from django import forms
from django.contrib.auth.models import User

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
