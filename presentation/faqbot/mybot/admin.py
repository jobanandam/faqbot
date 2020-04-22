from django.contrib import admin

# Register your models here.
from .models import CategoryModel, QuestionAnswerModel

admin.site.register(CategoryModel)
admin.site.register(QuestionAnswerModel)
