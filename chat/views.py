from django.shortcuts import redirect, render
from django.urls import reverse
from authi.models import User

from chat.models import Chat, Message
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, ListView, RedirectView

from chat.util import is_friend_to

# Create your views here.
@login_required()
def lobby(request):
    chates = Chat.objects.all().order_by('created_at')
    context = {'chates': chates}
    return render(request, 'chat/lobby.html', context=context)


class LobbyView(ListView):
    model=User
    template_name: str = 'chat/lobby.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        non_friends = []
        friends = []
        for user in queryset:
            if is_friend_to(user, self.request.user):
                friends.append(user)
            else:
                if user != self.request.user:
                    non_friends.append(user)


        ctx['friends'] = friends
        ctx['non_friends'] = non_friends
        return ctx

class ChatView(DetailView):
    model= User
    template_name: str = 'chat/chat.html'
    slug_field: str = 'id'
    slug_url_kwarg: str = 'user_id'

    def get_context_data(self, **kwargs) :
        ctx =  super().get_context_data(**kwargs)
        user = self.request.user
        another_user = self.get_object()
        chat: Chat = Chat.get_chat(user, another_user)
        ctx['chat_messages'] = chat.message_set.all()
        ctx['chat_ws_url'] = f'ws/chat/{chat.id}'
        ctx['chat'] = chat
        ctx['chatter'] = chat.get_other(self.request.user)
        return ctx


class AddView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse('lobby')

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        if not user_id:
            return super().get(request, *args, **kwargs)
            
        another_user = User.objects.get(pk=user_id)
        if not another_user:
            return super().get(request, *args, **kwargs)

        if is_friend_to(request.user, another_user):
            return super().get(request, *args, **kwargs)

        Chat(user1=request.user, user2=another_user).save()

        return super().get(request, *args, **kwargs)