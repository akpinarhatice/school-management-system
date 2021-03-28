# models.py
from django.db import models


# Create your models here.

class School(models.Model):
    name = models.CharField(max_length=50)
    city = models.CharField(max_length=50)

class Member(models.Model):
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    password = models.CharField(max_length=12)
    type = models.CharField(max_length=30)


    def __str__(self):
        return self.firstname + " " + self.lastname
class Class(models.Model):
    name = models.CharField(max_length=30)
    okul_id = models.IntegerField()

class Teacher(models.Model):
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    password = models.CharField(max_length=12)
    class_id=models.IntegerField()


class Student(models.Model):
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    password = models.CharField(max_length=12)
    class_id=models.IntegerField()

class Manager(models.Model):
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    password = models.CharField(max_length=12)
    okul_id=models.IntegerField()