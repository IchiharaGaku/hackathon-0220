from django import forms
from .models import Article

class ArticleUploadForm(forms.Form):

    movie = forms.FileField()
   
