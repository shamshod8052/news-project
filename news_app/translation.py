from modeltranslation.translator import register, TranslationOptions
from .models import New, Category


@register(New)
class NewTranslationOptions(TranslationOptions):
    fields = ('title', 'body')

@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)
