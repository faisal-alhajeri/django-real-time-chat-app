from django.db import models
from authi.models import User
from django.db.models import Q

# Create your models here.



class Chat(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user1 = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='user1')
    user2 = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='user2')

    def __str__(self) -> str:
        return f'{self.user1} - {self.user2}'

    @classmethod
    def get_chat(cls, user1, user2):
        return cls.objects.filter(Q(user1=user1, user2=user2) | Q(user1=user2, user2=user1)).first()

    def user_is_part_of(self, user):
        return user == self.user1 or user ==self.user2


class Message(models.Model):
    text = models.CharField(max_length=255)
    sender = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.text
