from __future__ import unicode_literals
from django.db import models
import bcrypt
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
number_check = re.compile(r'^[a-zA-Z]+$')

class UserManager(models.Manager):
    def validator(self, data):
        message = dict()
        if len(data['first_name']) < 2:
            message['first_name_length'] = "Your First Name must be at least 2 characters long."
        if not number_check.match(data['first_name']):
            message['first_name_type'] = "Your First Name must only contain letters."
        if len(data['last_name']) < 2:
            message['last_name_length'] = "Your Last Name must be at least 2 characters long."
        if not number_check.match(data['last_name']):
            message['last_name_type'] = "Your Last Name must only contain letters."
        if not EMAIL_REGEX.match(data['email']):
            message['invalid_email'] = "Use a valid email address"
        # UNIQUE EMAIL VALIDATION HERE!
        users = User.objects.filter(email__iexact=data['email'])
        if users:
            message['unique'] = "Your email is already in use."
        if not data['password'] == data['cPassword']:
            message['pw_match'] = "Your passwords don't match."
        if len(message) > 0:
            return (False, message)
        else:
            password = data['password'].encode()
            hashed = bcrypt.hashpw(password, bcrypt.gensalt())
            data['password'] = hashed
            safeUser = User.objects.create(
                first_name = data['first_name'],
                last_name = data['last_name'],
                email = data['email'],
                password = data['password']
            )
            if safeUser.id == 1:
                safeUser.auth_level = 0
                safeUser.save()

            # message['success'] = "Successfully Registered!"

            return (True, safeUser.id)


    def login(self, data):
        message = dict()
        try:
            user = User.objects.get(email = data['email'])
        except:
            message['failedLogin'] = "Invalid Login"
            return (False, "Not Okay!")

        password = data['password'].encode()
        uPassword = user.password.encode()
        if user and bcrypt.hashpw(password, uPassword) == uPassword:
            print "Okay!"
            return (True, user.id)
        else:
            print "Not Okay!"
            return (False, "Not Okay!")

    def change_pass(self, data):
        if data['password'] == data['cPassword'] and len(data['password']) > 2:
            password = data['password'].encode()
            hashed = bcrypt.hashpw(password, bcrypt.gensalt())
            user = User.objects.get(pk = data['id'])
            user.password = hashed
            user.save()
            return (True, "password changed")
        else:
            return (False, "password not changed")

class User(models.Model):
    authorization = (
        (0, 'Admin'),
        (1, 'User')
    )
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    password = models.CharField(max_length=60)
    description = models.TextField(max_length=200)
    auth_level = models.CharField(max_length=5, choices=authorization, default = 1)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    userManager = UserManager()
    objects = models.Manager()
