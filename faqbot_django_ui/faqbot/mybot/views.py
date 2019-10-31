from django.views import generic
from .models import ChatModel
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic


class IndexView(generic.ListView):
    template_name = 'mybot/index.html'
    context_object_name = 'chat_history'

    def get_queryset(self):
        return ChatModel.objects.all()


def get_human_ques(request):
    input_text = request.POST['humanentry']
    print(input_text)
    activeChat = ChatModel.objects.filter(
        bot_reply__contains="restart"
    ).update(human_ques = input_text);
    ChatModel.objects.create(bot_reply="Happy helping you, see you soon :)",human_ques="")
    return HttpResponseRedirect(reverse('mybot:index'))
