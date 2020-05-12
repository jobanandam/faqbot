from django.db import models
from django.template.defaultfilters import truncatechars  # or truncatewords



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

class FeedBackModel(models.Model):
    user_id = models.CharField(max_length=200)
    actual_question = models.ForeignKey(QuestionAnswerModel, on_delete=models.CASCADE)
    asked_question = models.TextField()
    answer = models.TextField()
    score = models.IntegerField()
    processed = models.BooleanField(default=False)
    accepted = models.BooleanField(default=False)
    comments = models.TextField(null=True)

    @property
    def actual_question_s(self):
        return truncatechars(self.answer, 20)

    @property
    def answer_s(self):
        return truncatechars(self.answer, 20)

    class Meta:
        verbose_name = 'Feedback System'
        verbose_name_plural = 'Feedback System'

    def __str__(self):
        return self.asked_question[:300] + '...'

class GenericQuestionModel(models.Model):
    question = models.TextField()

    def __str__(self):
        return self.question[:300] + '...'