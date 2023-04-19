from django.shortcuts import render
from django.views import generic
from .models import Post

# EACH TIME A NEW VIEW IS CREATED DO THE FOLLOWING:
# 1. CREATE THE VIEW CODE.
# 2. CREATE A TEMPLATE TO RENDER THE VIEW.
# 3. CONNECT UP URLs IN THE urls.py FILE.


class PostList(generic.ListView):

    model = Post
    # this allows only published posts to be visible to users.
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    # the html file that this view will render.
    template_name = 'index.html'
    # separation of pages, if more than 6, nav will be added to page.
    paginate_by = 6