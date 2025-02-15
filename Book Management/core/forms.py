from django import forms
from .models import Books


class BookForm(forms.ModelForm):
    class Meta:
        model = Books
        fields = '__all__'
        # widgets = {
        #     'title': forms.TextInput(attrs={'class': 'form-control'}),
        #
        # }
