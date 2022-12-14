from django.urls import path, include
from . import views


app_name = "reviews"

urlpatterns = [
  path("index/", views.index, name="index"),
  path("create/", views.create, name="create"),
  path("<int:pk>/", views.detail, name='detail'),
  path("<int:pk>/update/", views.update, name="update"),
  path("<int:pk>/delete/", views.delete, name="delete"),
  path("<int:pk>/comment_create/", views.comment_create, name="comment_create"),
  path("<int:review_pk>/comment_delete/<int:comment_pk>/delete/", views.comment_delete, name="comment_delete"),
  path("<int:review_pk>/like/<int:comment_pk>/", views.comment_like, name="comment_like"),
  path("<int:pk>/like/", views.like, name='like'),
  path("<int:pk>/bookmark/", views.bookmark, name='bookmark'),
  path("<int:pk>/best/", views.best, name="best"),
  path("review_search/", views.review_search, name="review_search"),
]
