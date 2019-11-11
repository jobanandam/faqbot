from django.db import models


class ChatModel(models.Model):
    type = models.CharField(max_length=200)
    text = models.CharField(max_length=200)
