from django import forms

from ..constants import (
    REVIEW_TITLE_VALIDATE,
    REVIEW_CONTENT_VALIDATE,
    REVIEW_CONTENT_ROWS
)
from ..models.review import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['title', 'content', 'is_active']
        labels = {
            'title': 'Заголовок',
            'content': 'Текст отзыва',
            'is_active': 'Активный'
        }
        help_texts = {
            'title': 'Введите краткий заголовок отзыва',
            'content': 'Напишите ваш отзыв подробно',
            'is_active': 'Отображать этот отзыв на сайте'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['content'].widget = forms.Textarea(attrs={
            'rows': REVIEW_CONTENT_ROWS,
            'placeholder': 'Напишите ваш отзыв здесь...'
        })
        self.fields['title'].widget.attrs.update({
            'placeholder': 'Краткий заголовок'
        })

    def clean_title(self):
        """Валидация заголовка"""
        title = self.cleaned_data['title']
        if len(title) < REVIEW_TITLE_VALIDATE:
            raise forms.ValidationError("Заголовок слишком короткий (минимум 5 символов)")
        return title

    def clean_content(self):
        """Валидация текста отзыва"""
        content = self.cleaned_data['content']
        if len(content) < REVIEW_CONTENT_VALIDATE:
            raise forms.ValidationError("Отзыв слишком короткий (минимум 20 символов)")
        return content
