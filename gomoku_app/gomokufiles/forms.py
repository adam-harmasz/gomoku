from django import forms


class GomokuFileForm(forms.Form):
    files = forms.FileField()

