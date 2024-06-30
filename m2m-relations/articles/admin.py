from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, Scope, Tag


class ScopeInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        if any(self.errors):
            return
        if not any(form.cleaned_data.get('is_main') for form in self.forms):
            raise ValidationError("Пожалуйста, выберите основной элемент.")
        main_count = sum(form.cleaned_data.get('is_main', False) for form in self.forms)
        if main_count != 1:
            raise ValidationError('Выберите только один основной элемент')


class ScopeInline(admin.TabularInline):
    model = Scope
    formset = ScopeInlineFormSet


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'text', 'published_at', 'image']
    inlines = [ScopeInline]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']
