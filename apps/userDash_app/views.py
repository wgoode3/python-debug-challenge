from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from .models import User

# Create your views here.

def index(request):
    # user = User.objects.get(pk = request.session['user_id'])
    # user.auth_level = 0
    # user.save()
    print "about to render"
    try:
        print request.session['user_id']
    except:
        pass
    return render(request, 'uDash/index.html')

def login(request, methods=['POST']):
    if request.method == 'POST':
            data = {
                "email": request.POST['email'],
                "password": request.POST['password']
            }
            theMessage = User.userManager.login(data)
            message = dict()
            if theMessage[0]:
                request.session['user_id'] = theMessage[1]
                message['success'] = "Sucessfully Logged In!"
                id = str(request.session['user_id'])
                # return redirect('/board/show/'+id)
                return redirect('/panel')
                # return render(request, 'board/index.html', message)
            else:
                messages.add_message(request, messages.ERROR, "Invalid Login")
                return render(request, 'uDash/signin.html', message)
    else:
        return render(request, 'uDash/signin.html')

def register(request):
    print "about to render register"
    return render(request, 'uDash/register.html')

def registerUser(request, methods=['POST']):
    print "register a user into db"

    data = {
        "first_name": request.POST['first_name'],
        "last_name": request.POST['last_name'],
        "email": request.POST['email'],
        "password": request.POST['password'],
        "cPassword": request.POST['cPassword']
    }

    theMessage = User.userManager.validator(data)

    if theMessage[0]:
        request.session['user_id'] = theMessage[1]
        return redirect('/panel')
        # return render(request, 'board/index.html', message)
    else:
        data = theMessage[1]
        for message in data:
            print message
            messages.add_message(request, messages.ERROR, data[message])
        return redirect('/register')

def buildNewUser(request):
    return render(request, 'uDash/createUser.html')

def createNewUser(request, methods=['POST']):
    print "register a user into db"

    data = {
        "first_name": request.POST['first_name'],
        "last_name": request.POST['last_name'],
        "email": request.POST['email'],
        "password": request.POST['password'],
        "cPassword": request.POST['cPassword']
    }

    theMessage = User.userManager.validator(data)

    if theMessage[0]:
        return redirect('/panel')
        # return render(request, 'board/index.html', message)
    else:
        data = theMessage[1]
        for message in data:
            print message
            messages.add_message(request, messages.ERROR, data[message])
        return redirect('/createNewUser')

def wall(request):
    pass

def panel(request):
    user = User.objects.get(pk = request.session['user_id'])
    all_users = User.objects.all()
    data = {'all_users': all_users}

    if int(user.auth_level) == 0:
        return render(request, 'uDash/adminPanel.html', data)
    else:
        return render(request, 'uDash/panel.html', data)

def remove(request, id):
    user = User.objects.filter(id=id)
    user.delete()
    return redirect('/adminPanel')

def edit(request, id = None):

    def getUser():
        user = User.objects.get(pk = request.session['user_id'])
        return user

    if request.method == 'POST' and id == None:
        user = getUser()
        print user.first_name
        if request.POST['first_name']:
            print "first_name was present"
            user.first_name = request.POST['first_name']
            user.save()
        if request.POST['last_name']:
            print "last_name was present"
            user.last_name = request.POST['last_name']
            user.save()
        if request.POST['email']:
            print "email was present", request.POST['email']
            user.email = request.POST['email']
            user.save()

        data = { 'user': user }
        return render(request, 'uDash/editUser.html', data)
    else:
        if id is not None:
            print id
            print request.session['user_id']
            user = User.objects.get(id=id)
            data = { 'user': user }
            return render(request, 'uDash/editUser.html', data)
        else:
            # this is for non-admin users
            print "no id"
            user = User.objects.get(id = request.session['user_id'])
            data = { 'user': user }
            return render(request, 'uDash/editUser.html', data)

def change_pass(request, id):
    data = {'id': id,
            'password': request.POST['password'],
            'cPassword': request.POST['cPassword']
           }
    theMessage = User.userManager.change_pass(data)
    if theMessage[0]:
        messages.add_message(request, messages.SUCCESS, "Your password was sucessfully changed")
        return redirect('/edit')
        # return render(request, 'uDash/editUser.html')
    else:
        messages.add_message(request, messages.ERROR, "Your password could not be changed")
        return redirect('/edit')

def change_desc(request, id):
    if request.POST['description']:
        user = User.objects.get(pk=id)
        user.description = request.POST['description']
        user.save()
        print "Description was sucessfully changed."

    return redirect('/edit')

def logout(request):
    request.session.flush()
    return redirect('/')
