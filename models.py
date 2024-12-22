from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts'
    ) 
    content = models.TextField(blank=True, null=True) 
    image = models.ImageField(
        upload_to='posts/',
        blank=True,
        null=True
    )  
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"{self.user.username}'s post at {self.created_at}"

    
    @property
    def likes_count(self):
        return self.likes.count()

    @property
    def comments_count(self):
        return self.comments.count()


class Like(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )  
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='likes'
    ) 
    created_at = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return f"{self.user.username} liked post {self.post.id}"


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    ) 
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )  
    content = models.TextField()  
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post}"


from django.db import models
from django.contrib.auth.models import User  

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"From {self.sender.username} to {self.receiver.username}: {self.content[:30]}"

class Friend(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend_user')
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend_friend')

    def __str__(self):
        return f"{self.user.username} - {self.friend.username}"

from django.db import models
from django.contrib.auth.models import User

class FriendRequest(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend_request_sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend_request_receiver')
    created_at = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return f"{self.sender.username} -> {self.receiver.username}"
    
class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('friend_request', 'Friend Request'),
        ('friend_accept', 'Friend Accept'),
    ]

    type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_notifications')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_notifications')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} -> {self.receiver} ({self.type})"   


# models.py
# from django.db import models
# from django.contrib.auth.models import User

# class Group(models.Model):
#     name = models.CharField(max_length=255)
#     description = models.TextField()
#     members = models.ManyToManyField(User, related_name='group_members')

#     def __str__(self):
#         return self.name
