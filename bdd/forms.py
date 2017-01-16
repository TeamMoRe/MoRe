from django import forms

class RatingForm(forms.Form):
    rating = forms.IntegerField(label='Note', min_value=0, max_value=5)

