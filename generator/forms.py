from django import forms

class ProjectForm(forms.Form):
    project_name = forms.CharField(max_length=100, label='Nom du projet')
    application = forms.CharField(max_length=100, label='Nom du application')
    app = forms.CharField(max_length=100, label='Nom du application2')
