from django import forms

class userTeamEntry(forms.Form):
    player1 = forms.CharField(max_length=100, label="Player 1")
    player2 = forms.CharField(max_length=100, label="Player 2")
    player3 = forms.CharField(max_length=100, label="Player 3")
    player4 = forms.CharField(max_length=100, label="Player 4")
    player5 = forms.CharField(max_length=100, label="Player 5")
    player6 = forms.CharField(max_length=100, label="Player 6")
    player7 = forms.CharField(max_length=100, label="Player 7")
    player8 = forms.CharField(max_length=100, label="Player 8")
    player9 = forms.CharField(max_length=100, label="Player 9")
    player10 = forms.CharField(max_length=100, label="Player 10")
    player11 = forms.CharField(max_length=100, label="Player 11")
    sub1 = forms.CharField(max_length=100, label="Sub 1")
    sub2 = forms.CharField(max_length=100, label="Sub 2")
    sub3 = forms.CharField(max_length=100, label="Sub 3")
    sub4 = forms.CharField(max_length=100, label="Sub 4")