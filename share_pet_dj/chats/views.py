from django.views.generic import ListView, DetailView

from .forms import MessageForm
from .models import Chat
from .services.mixins import ChatDetailFormMixin


class ChatListView(ListView):
    model = Chat
    template_name = 'chats/chats.html'


class ChatDetailView(ChatDetailFormMixin, DetailView):
    form_class = MessageForm
    model = Chat
    template_name = 'chats/chat.html'


chat_list = ChatListView.as_view()
chat_detail = ChatDetailView.as_view()
