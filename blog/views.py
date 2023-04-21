from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic, View
from django.http import HttpResponseRedirect
from .models import Post
from .forms import CommentForm

# EVERY TIME A VIEW IS CREATED TO THE FOLLOWING;
# 1. CREATE THE VIEW CODE
# 2. CREATE A TEMPLATE TO RENDER THE VIEW
# 3. CONNECT UP URLs IN THE urls.py FILE


class PostList(generic.ListView):
    model = Post
    queryset = Post.objects.filter(status=1).order_by("-created_on")
    template_name = "index.html"
    paginate_by = 6


class PostDetail(View):

    def get(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by("-created_on")
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        return render(
            request,
            "post_detail.html",
            {
                "post": post,
                "comments": comments,
                "commented": False,
                "liked": liked,
                "comment_form": CommentForm()
            },
        )

    def post(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by("-created_on")
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        comment_form = CommentForm(data=request.POST)  # gets all posted data from form

        if comment_form.is_valid():  # if all fields are filled, its valid and a comment is created
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False)  # don't commit before a post is assigned
            comment.post = post  # once comment is assigned to a post, push it to db
            comment.save()
        else:
            comment_form = CommentForm()

        return render(
            request,
            "post_detail.html",
            {
                "post": post,
                "comments": comments,
                "commented": True,
                "liked": liked,
                "comment_form": CommentForm()
            },
        )


class PostLike(View):

    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug)  # get the Post object

        if post.likes.filter(id=request.user.id).exists():  # check if liked already
            post.likes.remove(request.user)  # if so, remove the like
        else:
            post.likes.add(request.user)  # if not, add a like

        # when liking/unliking the page will reload
        # args allows for targeting the correct post to load
        return HttpResponseRedirect(reverse('post_detail', args=[slug]))  # reload the template to render changes
