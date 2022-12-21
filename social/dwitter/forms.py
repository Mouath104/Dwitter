from django import forms
from .models import Dweet


class DweetForm(forms.ModelForm):

    body = forms.CharField(
    required=True,
    widget=forms.widgets.Textarea(
    attrs={
    "placeholder": "Dweet something...",
    "class": "textarea is-success is-medium",
    }
    ),
    label="",
    )

    class Meta:
        model = Dweet
        exclude = ("user", )

# class CommentForm(forms.ModelForm):
#     body=forms.CharField(
#     required=True,
#     widget=forms.widgets.Textarea(
#     attrs={
#     "placeholder": "Comment something...",
#     "class": "textarea is-success is-medium",
#     }
#     ),
#     label="",
#     )

#     class Meta:
#         model = Dweet
#         exclude = ("user",)