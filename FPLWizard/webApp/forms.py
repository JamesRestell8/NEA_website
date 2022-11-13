from django import forms

class fplIDForm(forms.Form):
    fplID = forms.CharField(label='FPL ID', max_length=10)
    email = forms.CharField(label='Email', max_length=50)
    # NEED TO MAKE THIS MORE SECURE
    password = forms.CharField(label='Password')