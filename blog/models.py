from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

STATUS = ((0, "Draft"), (1, "Published"))

# EVERY TIME YOU EITHER/OR EDIT OR ADD TO MODELS YOU NEED TO:
# 0. (OPTIONAL) python3 manage.py makemigrations --dry-run
# 1. python3 manage.py makemigrations
# 2. python3 manage.py migrate


class Post(models.Model):

    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blog_posts")
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()
    featured_image = CloudinaryField('image', default='placeholder')
    excerpt = models.TextField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    likes = models.ManyToManyField(User, related_name='blog_likes', blank=True)

    class Meta:
        ordering = ['-created_on']  # minus means use descending order.

    def __str__(self):
        return self.title  # returns a string representation of an object.

    def number_of_likes(self):
        return self.likes.count()  # return the total number of likes on a post.


class Comment(models.Model):

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']  # this is ascending order.

    def __str__(self):
        return f"Comment {self.body} by {self.name}"
