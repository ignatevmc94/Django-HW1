from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, Tag, Scope

class ScopeFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        main_count = 0
        for form in self.forms:
            try:
                is_main = form.cleaned_data['is_main']
                if is_main:
                    main_count += 1

                    if main_count > 1:
                        raise ValidationError(
                            "Можно выбрать только 1 основной тег!"
                        )
            except KeyError:
                pass


class ScopeInline(admin.StackedInline):
    model = Scope
    extra = 1
    formset = ScopeFormSet


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'text',)
    inlines = [ScopeInline]

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('topic',)
