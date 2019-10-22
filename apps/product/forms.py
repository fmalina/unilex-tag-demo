from django import forms
from product.models import Product, Concept


TO_CONCEPT = forms.ModelChoiceField(
    queryset=Concept.objects.all(),
    widget=forms.TextInput(attrs={'class': 'autocomplete',
                                  'placeholder': 'Type and choose'})
)


class TagForm(forms.Form):
    predicate = TO_CONCEPT


class ProductForm(forms.ModelForm):
    desc = forms.CharField(widget=forms.Textarea(attrs={'cols':80, 'rows': 4}), label="Description")

    class Meta:
        model = Product
        exclude = ['org', 'sector']
