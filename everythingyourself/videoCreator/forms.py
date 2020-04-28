from django import forms

class UploadFaceForm(forms.Form):
    face = forms.ImageField(label="Ihr Gesicht")