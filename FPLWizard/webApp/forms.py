from django import forms

class fplIDForm(forms.Form):
    My_Fpl_ID = forms.CharField(label='FPL ID', max_length=10)
