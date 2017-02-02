from __future__ import unicode_literals
from django.db import models
from ..userDash_app.models import User
# Create your models here.

class MessageManager(models.Manager):
    def validator(self, data):
        if(len(data['message']) < 1):
            err = "Your message cannot be blank"
            return (False, err)
        else:
            safeMessage = Message.objects.create(
                message = data['message'],
                message_leaver = data['message_leaver'],
                message_reciever = data['message_reciever']
            )
            return (True, "Message successfully posted")
        print data

    def getReversedMessages(self, user):
        return Message.objects.filter(message_reciever = user['user']).order_by('-created_at')

class Message(models.Model):
    message = models.TextField(max_length=200)
    message_leaver = models.ForeignKey(User, related_name='message_leaver')
    message_reciever = models.ForeignKey(User, related_name='message_reciever')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    messageManager = MessageManager()
    objects = models.Manager()

class CommentManager(models.Manager):
    def validator(self, data):
        if(len(data['comment']) < 1):
            err = "Your comment cannot be blank"
            return (False, err)
        else:
            safeComment = Comment.objects.create(
                comment = data['comment'],
                attached_to_message = data['attached_to_message'],
                board_id = data['board_id'],
                comment_leaver = data['comment_leaver']
            )
            return (True, "Comment successfully posted")
        print data

class Comment(models.Model):
    comment = models.TextField(max_length=200)
    attached_to_message = models.ForeignKey(Message)
    board_id = models.IntegerField()
    comment_leaver = models.ForeignKey(User, related_name='comment_leaver')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    commentManager = CommentManager()
    objects = models.Manager()
