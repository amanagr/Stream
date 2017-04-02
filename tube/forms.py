from django import forms

class UploadFileForm(forms.Form):
    title = forms.CharField(label = "Name of Video", required=True, max_length=50)			# name of uploaded file
    file = forms.FileField(label = "Choose video", help_text='Only Video files Supported')	# file uploaded
