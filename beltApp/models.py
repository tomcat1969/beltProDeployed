from django.db import models
import re
from datetime import datetime

class UsersManager(models.Manager):
    def basic_validator(self, post_data):
        errors = {}
        if len(post_data['first_name']) < 2 and post_data['first_name'].isalpha():
            errors['first_name'] = "first name must be at least 2 characters and letters only"
        if len(post_data['last_name']) < 2 and post_data['last_name'].isalpha():
            errors['last_name'] = "Last name must be at least 2 characters and letters only"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(post_data['email']):  # test whether a field matches the pattern
            errors['email'] = "Invalid email address!"
        if Users.objects.filter(email=post_data['email']):
            errors['email'] = "the email has been registed!"
        if len(post_data['password']) < 8 and post_data['password'] != post_data['confirmPW']:
            errors['password'] = "at least 8 characters and must match the password comfirmation!"
        return errors


class Users(models.Model):
    first_name = models.CharField(max_length=255)
    last_name=  models.CharField(max_length=255)
    email =  models.CharField(max_length=255)
    password =  models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UsersManager()

class TripsManager(models.Manager):
    def basic_validator(self, post_data):
        errors = {}
        if len(post_data['destination']) < 3:
            errors['first_name'] = "destination must be provided and at least 3 characters!"
        if post_data['start_date'] == '' :
            errors['start_date'] = "start_date must be provided!"
        if post_data['end_date'] == '' :
            errors['end_date'] = "end_date must be provided!"
        if len(post_data['plan']) < 3:
            errors['plan'] = "plan must be provided and at least 3 characters!"
        return errors


class Trips(models.Model):
    destination = models.CharField(max_length=255)
    startDate = models.DateField()
    endDate = models.DateField()
    plan = models.TextField()
    user = models.ForeignKey(Users,related_name="trips",on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TripsManager()