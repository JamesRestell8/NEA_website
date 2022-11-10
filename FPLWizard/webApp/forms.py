from django import forms

class fplIDForm(forms.Form):
    fplID = forms.CharField(label='FPL ID', max_length=10)
