from django import forms

class UploadForm(forms.Form):
    name = forms.CharField()
    category = forms.CharField()