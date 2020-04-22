from django.contrib import admin

# Register your models here.
from .models import CategoryModel, QuestionAnswerModel, FeedBackModel

class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ['category']
    list_per_page = 20
admin.site.register(CategoryModel, CategoryModelAdmin)

class QuestionAnserModelAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer', 'category')
    list_filter = ['category']
    search_fields = ('question', 'answer')
    list_per_page = 20
admin.site.register(QuestionAnswerModel, QuestionAnserModelAdmin)

class FeedBackModelAdmin(admin.ModelAdmin):
    list_filter = ('processed', 'accepted')
    list_per_page = 20
    list_display = ('actual_question_s', 'asked_question', 'answer_s', 'processed', 'accepted', 'score', 'comments')
    search_fields = ('asked_question', 'answer', 'comments', 'score')

    # This will help you to disbale add functionality
    def has_add_permission(self, request):
        return True

admin.site.register(FeedBackModel, FeedBackModelAdmin)
