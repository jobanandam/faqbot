from django.db import models


class ChatModel(models.Model):
    bot_reply = models.CharField(max_length=200)
    human_ques = models.CharField(max_length=200, blank=True)