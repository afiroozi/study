from django.forms import ModelForm
from django import forms 
from .models import Room, User, Profile
from django.contrib.auth.forms import UserCreationForm


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','email']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['full_name','gender','country','city','address', 'bio', 'avatar']



