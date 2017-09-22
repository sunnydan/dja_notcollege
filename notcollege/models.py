from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.TextField()
    birthday = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    friends = models.ManyToManyField("self")
    liked_books = models.ManyToManyField('Book', related_name="likes")

class Book(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    isbn = models.PositiveIntegerField()
    authors = models.ManyToManyField(Profile, related_name="books")

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
    teachers = models.ManyToManyField(User, related_name="taught_courses")
    required_books = models.ManyToManyField(Book, related_name="courses")
    students = models.ManyToManyField(Profile, related_name='joined_courses')

class Chatroom(models.Model):
    topic = models.CharField(max_length=255)
    members = models.ManyToManyField(Profile, related_name='chatrooms')

class Post(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(Profile, related_name="authored_posts", null=True)
    parent_post = models.ForeignKey('Post', related_name="child_posts", null=True)
    to_profile = models.ForeignKey(Profile, related_name="profile_posts", null=True)
    review = models.ForeignKey(Review, related_name="review_posts", null=True)
    chatroom = models.ForeignKey(Chatroom, related_name="chatroom_posts", null=True)
    course = models.ForeignKey(Course, related_name="course_posts", null=True)
    book = models.ForeignKey(Book, related_name="book_posts", null=True)
