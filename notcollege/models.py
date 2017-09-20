from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
import uuid

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.TextField()
    birthday = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    friends = models.ManyToManyField("self")
    liked_books = models.ManyToManyField('Book', related_name="likes")
    page = models.OneToOneField('Page', related_name="user")

class Book(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    isbn = models.PositiveIntegerField()
    authors = models.ManyToManyField(Profile, related_name="books")
    page = models.OneToOneField('Page', related_name="book")

class Review(models.Model):
    rating = models.PositiveSmallIntegerField()
    text = models.TextField()
    user = models.ForeignKey(Profile, related_name="reviews")
    book = models.ForeignKey(Book, related_name="reviews")
    course = models.ForeignKey('Course', related_name="reviews")

class Course(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    teacher = models.ForeignKey(User, related_name="taught_courses")
    required_books = models.ManyToManyField(Book, related_name="courses")
    students = models.ManyToManyField(Profile, related_name='joined_courses')
    page = models.OneToOneField('Page', related_name="course")

class Chatroom(models.Model):
    topic = models.CharField(max_length=255)
    members = models.ManyToManyField(Profile, related_name='chatrooms')
    page = models.OneToOneField('Page', related_name="chatroom")

class Post(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(Profile, related_name="posts", null=True)
    parent_post = models.ForeignKey('Post', related_name="children")
    review = models.ForeignKey(Review, related_name="posts")
    page = models.ForeignKey('Page', related_name="posts")

class Page(models.Model):
    TYPE_CHOICES = (
        ('USER', 'USER'),
        ('BOOK', 'BOOK'),
        ('COURSE', 'COURSE'),
        ('CHATROOM', 'CHATROOM')
    )
    type = models.CharField(max_length=8, choices=TYPE_CHOICES)
