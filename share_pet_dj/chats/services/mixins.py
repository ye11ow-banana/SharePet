from django.urls import reverse
from django.views.generic import FormView

from chats.forms import MessageForm
from chats.models import Chat
from core.exceptions import EmptyMessageError


class ChatDetailFormMixin(FormView):
    @staticmethod
    def _raise_if_message_empty(form: MessageForm) -> None:
        if not form.text and not form.file:
            raise EmptyMessageError

    def form_valid(self, form):
        form = form.save(commit=False)

        try:
            self._raise_if_message_empty(form)
        except EmptyMessageError:
            return super().form_valid(form)

        form.sender = self.request.user
        form.chat = Chat.objects.get(slug=self.kwargs['slug'])
        form.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'chat_detail', kwargs={'slug': self.kwargs['slug']})
