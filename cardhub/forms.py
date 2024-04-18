from django import forms

class UserForm(forms.Form):
    name = forms.CharField(label="name", max_length=200)
    email = forms.EmailField(label="email", max_length=200)
    password = forms.CharField(label="password", max_length=200)


class LogInForm(forms.Form):
    email = forms.EmailField(label="email", max_length=200)
    password = forms.CharField(label="password", max_length=200)
    