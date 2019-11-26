from django.http import HttpResponse
from .models import ChatModel
from django.views import generic


class VersionOne(generic.ListView):
    template_name = 'versionOne/index.html'
    context_object_name = 'chat_history'

    def get_queryset(self):
        return ChatModel.objects.all()


class VersionTwo(generic.ListView):
    template_name = 'versionTwo/index.html'
    context_object_name = 'chat_history'

    def get_queryset(self):
        return ChatModel.objects.all()


def get_human_ques(request):
    input_text = request.POST['question']
    ChatModel.objects.create(type="HUMAN", text=input_text)
    ChatModel.objects.create(type="BOT", text="Here's my reply")
    return HttpResponse("{}", content_type='application/json')