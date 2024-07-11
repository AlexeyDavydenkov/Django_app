from django import forms

from blogapp.models import Article, Author, Category, Tag


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = "title", "content", "author", "category", "tags"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['author'].queryset = Author.objects.all()
        self.fields['author'].widget = forms.Select(
            choices=[(author.id, author.name) for author in Author.objects.all()])

        self.fields['category'].queryset = Category.objects.all()
        self.fields['category'].widget = forms.Select(
            choices=[(category.id, category.name) for category in Category.objects.all()])

        self.fields['tags'].queryset = Tag.objects.all()
        self.fields['tags'].widget = forms.SelectMultiple(choices=[(tag.id, tag.name) for tag in Tag.objects.all()])

