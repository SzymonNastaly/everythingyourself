from django import forms

class UploadFaceForm(forms.Form):
    face = forms.ImageField(label="Ihr Gesicht")


class CropFaceForm(forms.Form):
    imagefield = forms.CharField(label="Cropped Face")