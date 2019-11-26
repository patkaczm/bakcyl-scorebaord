from django import forms
from .models import Group

class SolutionForm(forms.Form):
    code = forms.CharField(widget=forms.Textarea)

class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea)
    score = forms.IntegerField()

class TaskForm(forms.Form):
    link = forms.URLField()
    name = forms.CharField()
    max_score = forms.IntegerField()
    group_level = forms.ChoiceField(choices=Group.GROUP_LEVEL, label="Group Level", initial='', widget=forms.Select(), required=True)