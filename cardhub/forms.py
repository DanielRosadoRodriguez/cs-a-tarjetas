from django import forms

class CreateNewPerson(forms.Form):
    name = forms.CharField(label="username", max_length=200)
    email = forms.EmailField(label="email", max_length=200)
    password = forms.CharField(label="password", max_length=200)
