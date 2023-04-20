from . import views
from django.urls import path

urlpatterns = [
    # must add as_view due to class-based view structure.
    path('', views.PostList.as_view(), name='home'),
    # The 'slug' keyword name matches the 'slug' parameter in
    # the get method of the PostDetail class in the blog/views.py file.
    # That's how we link them together.
    # The first slug is a path converter and the second, a keyword name.
    # The path converter converts its text into a slug field.
    # Then, it tells Django to match any slug string.
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
]
