from django.db import models


class ChatModel(models.Model):
    type = models.CharField(max_length=200)
    text = models.CharField(max_length=200)

class CategoryModel(models.Model):
    category = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.category

class QuestionAnswerModel(models.Model):
    question = models.TextField()
    answer = models.TextField()
    category = models.ForeignKey(CategoryModel, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Q&A'
        verbose_name_plural = 'Q&A'

    def __str__(self):
        return self.question[:3000] + '...'
