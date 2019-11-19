from django import forms

class SolutionForm(forms.Form):
    code = forms.CharField(widget=forms.Textarea)

class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea)
    score = forms.IntegerField()