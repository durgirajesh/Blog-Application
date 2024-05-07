from django import forms
from .models import post_model

class post_form(forms.ModelForm):
    class Meta:
        model = post_model
        fields = ['title', 'content']

