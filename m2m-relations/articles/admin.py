from django.contrib import admin

from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Tag, Scope, Article


class ScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        if len(self.forms) == 0:
            raise ValidationError('Не определены рубрики')

        count_main = 0
        for form in self.forms:
            if form.cleaned_data.get('is_main'):
                count_main += 1
            if count_main > 1:
                raise ValidationError('Главная рубрика отмечена более одного раза!')
        return super().clean()


class ScopeInline(admin.TabularInline):
    model = Scope
    formset = ScopeInlineFormset


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'published_at', 'image']
    inlines = [ScopeInline]


@admin.register(Scope)
class ScopeAdmin(admin.ModelAdmin):
    model = Scope
    list_display = ['id', 'tag', 'article', 'is_main']
    extra = 0
