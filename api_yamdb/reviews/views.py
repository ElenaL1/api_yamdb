from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from .forms import CommentForm
from .models import Title


@login_required
def add_comment(request, title_id):
    post = get_object_or_404(Title, pk=title_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
        return redirect('posts:post_detail', title_id=title_id)
