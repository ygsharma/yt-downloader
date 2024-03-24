from django import forms

class DownloadForm(forms.Form):
    url = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Try our built-in search - just start typing something'}), label = False)