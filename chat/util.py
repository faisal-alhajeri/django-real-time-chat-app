from authi.models import User
from .models import Chat
from django.db.models import Q


def is_friend_to(user1, user2):
    return user1 != user2 and Chat.objects.filter(Q(user1=user1, user2=user2) | Q(user1=user2, user2=user1)).exists() 

def test_is_firend():
    # temp test
    user1 = User.objects.filter(username='faisal').first()
    user2 = User.objects.filter(username='a').first()
    user3 = User.objects.filter(username='aa').first()
    user4 = User.objects.filter(username='faisal12').first()
    print(user1)
    print(user2)
    print(user3)
    print(user4)


    print("True:", is_friend_to(user1,user2))
    print("True:", is_friend_to(user2,user3))
    print("False:", is_friend_to(user1,user3))
    print("False:", is_friend_to(user1,user4))
    print("False:", is_friend_to(user2,user4))
    print("False:", is_friend_to(user4,user3))
