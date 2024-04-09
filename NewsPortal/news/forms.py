from django import forms
from .models import Post

class SearchForm(forms.Form):
    # Определение полей формы для поиска
    title = forms.CharField(label='Название', max_length=100)
    author = forms.CharField(label='Автор', max_length=100)
    date = forms.DateField(label='Дата')

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['author', 'choice_types', 'categories', 'news_title', 'news_text', 'subscribers']

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['categories'].widget.attrs['class'] = 'form-control'  
        self.fields['subscribers'].widget.attrs['class'] = 'form-control'  