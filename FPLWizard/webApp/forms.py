from django import forms

class fplIDForm(forms.Form):
    fplID = forms.CharField(label='FPL ID', max_length=10)
    email = forms.CharField(label='Email', max_length=50)
    # password widget means that password will be protected on screen
    password = forms.CharField(label='Password', widget=forms.PasswordInput())