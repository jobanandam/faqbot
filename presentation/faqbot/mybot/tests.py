# Create your tests here.
import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import ChatModel


def create_question(question_text, reply):
    time = timezone.now() + datetime.timedelta(days=days)
    return ChatModel.objects.create(bot_reply=reply, human_ques=question_text)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        response = self.client.get(reverse('mybot:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No chat history")
        self.assertQuerysetEqual(response.context['chat_history'], [])