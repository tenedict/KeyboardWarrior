from django.db import models
from articles.models import Keyboard
from KW.settings import AUTH_USER_MODEL

# Create your models here.

grade_ = [(1, "★"), (2, "★★"), (3, "★★★"), (4, "★★★★"), (5, "★★★★★")]


class Review(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=80)
    content = models.TextField(max_length=500)
    grade = models.IntegerField(choices=grade_)
    like_users = models.ManyToManyField(AUTH_USER_MODEL, related_name="like_review")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    hits = models.PositiveIntegerField(default=0, verbose_name="조회수")
    bookmark_users = models.ManyToManyField(
        AUTH_USER_MODEL, related_name="bookmark_reivew"
    )
    keyboard = models.ForeignKey(Keyboard, on_delete=models.CASCADE)


class Photo(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="images/", blank=True)


class Comment(models.Model):
    content = models.CharField(max_length=80)
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    like_users = models.ManyToManyField(AUTH_USER_MODEL, related_name="like_comment")
