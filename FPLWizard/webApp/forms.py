from django import forms
import json

class userTeamEntry(forms.Form):
    playerTeamJSON = forms.CharField(max_length=10000, label="Team Information")

    def cleanJSONField(self):
        jdata = self.cleaned_data['playerTeamJSON']
        try:
            json_data = json.loads(jdata)
        except:
            jdata = "Error"
        return jdata