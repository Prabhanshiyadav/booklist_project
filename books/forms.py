from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'description', 'published_date']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'border p-2 w-full rounded'}),
            'author': forms.TextInput(attrs={'class': 'border p-2 w-full rounded'}),
            'description': forms.Textarea(attrs={'class': 'border p-2 w-full rounded'}),
            'published_date': forms.DateInput(attrs={'class': 'border p-2 w-full rounded', 'type': 'date'}),
        }
