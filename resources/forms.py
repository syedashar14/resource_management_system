from django import forms
from .models import Project, Resource

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description']

class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ['name']
