from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        exclude = ["user"]

class HomeWorkForm(forms.ModelForm):
    class Meta:
        model = HomeWork
        exclude = ["user"]
        widgets = {
            "due": forms.DateInput(attrs={"type": "date"})
        }

class DashboardForm(forms.Form):
    text = forms.CharField(max_length=100, label="Enter your search ")

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        exclude = ["user"]

class ConversionForm(forms.Form):
    CHOICES = [("length", "Length"), ("mass", "Mass")]
    measurement = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)

class ConversionLengthForm(forms.Form):
    CHOICES = [("yard", "Yard"), ("foot", "Foot")]
    input =     forms.CharField(required=False, label=False, widget=forms.TextInput(attrs={
        "type": "number", "placeholder" : "Enter a length",
    }))
    measure1 = forms.CharField(label="", widget= forms.Select(choices=CHOICES))
    measure2 = forms.CharField(label="", widget= forms.Select(choices=CHOICES))

class ConversionMassForm(forms.Form):
    CHOICES = [("pound", "Pound"), ("kilogram", "Kilogram")]
    input =     forms.CharField(required=False, label=False, widget=forms.TextInput(attrs={
        "type": "number", "placeholder" : "Enter a weight",
    }))
    measure1 = forms.CharField(label="", widget= forms.Select(choices=CHOICES))
    measure2 = forms.CharField(label="", widget= forms.Select(choices=CHOICES))

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]