from django import forms

class AddServerForm(forms.Form):
    name = forms.CharField(max_length=255,label="Server Name")
