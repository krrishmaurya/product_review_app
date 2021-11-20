from django import forms

class LoginForm(forms.Form):
    user_name = forms.CharField(max_length = 20)
    password = forms.CharField(widget = forms.PasswordInput())


class SignupForm(forms.Form):
    user_name = forms.CharField(max_length = 20)
    email = forms.EmailField()
    password = forms.CharField(widget = forms.PasswordInput())
    confirmed_password = forms.CharField(widget = forms.PasswordInput())