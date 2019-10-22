from django import forms
from org.models import Org


class OrgForm(forms.ModelForm):
    class Meta:
        model = Org
        exclude = ['users']
        widgets = {
            'coords': forms.TextInput
        }