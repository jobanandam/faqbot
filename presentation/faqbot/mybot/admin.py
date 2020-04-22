from django.contrib import admin

# Register your models here.
from .models import CategoryModel, QuestionAnswerModel

class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ['category']

admin.site.register(CategoryModel, CategoryModelAdmin)

class QuestionAnserModelAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer', 'category')
    list_filter = ['category']
    search_fields = ('question', 'answer')

admin.site.register(QuestionAnswerModel, QuestionAnserModelAdmin)
