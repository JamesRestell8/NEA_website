from django import forms
import json

# a class that represents the form on the MyFPL page.
class userTeamEntry(forms.Form):
    playerTeamJSON = forms.CharField(max_length=10000, label="Team Information")

    def cleanJSONField(self):
        jdata = self.cleaned_data['playerTeamJSON']
        # check that the data entered is in JSON form, and return error if not.
        try:
            json_data = json.loads(jdata)
        except:
            jdata = "Error"
        return jdata