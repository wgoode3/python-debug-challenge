from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse

from ..userDash_app.models import User
from .models import Message, Comment


# Create your views here.
def index(request, id):
    board_id = id
    logged_id = request.session['user_id']
    user = { 'user': User.objects.get(pk=board_id) }
    userMessages = Message.messageManager.getReversedMessages(user)
    userComments = Comment.commentManager.filter(board_id=board_id)

    data = { 'user': user,
             'userMessages': userMessages,
             'userComments': userComments,
           }
    # print data['user']['user'].first_name
    return render(request, "board/index.html", data)

def createMessage(request, id):
    board_id = id
    logged_id = request.session['user_id']
    data = { 'message_leaver': User.objects.get(pk=logged_id),
             'message_reciever': User.objects.get(pk=board_id),
             'message': request.POST['message']
           }
    theMessage = Message.messageManager.validator(data)
    print theMessage[0]
    if theMessage[0]:
        print theMessage[1]
        return redirect("../../board/show"+board_id)
    else:
        print theMessage[1]
        messages.add_message(request, messages.ERROR, theMessage[1])
        return redirect("../../board/show"+board_id)

def createComment(request, id):
    message_id = id
    logged_id = request.session['user_id']
    board_id = request.POST['board_id']
    # comment = request.POST['comment']
    data = {
        'comment_leaver': User.objects.get(pk=logged_id),
        'attached_to_message': Message.objects.get(pk=message_id),
        'board_id': request.POST['board_id'],
        'comment': request.POST['comment']
    }
    theComment = Comment.commentManager.validator(data)
    print theComment[0]
    if theComment[0]:
        print theComment[1]
        return redirect("../../board/show"+board_id)
    else:
        print theComment[1]
        messages.add_message(request, messages.ERROR, theMessage[1])
        return redirect("../../board/show"+board_id)
