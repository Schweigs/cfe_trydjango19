from django.http import HttpResponse
from django.shortcuts import render

from .models import Post

def post_create(request):
    return HttpResponse("<h1>Create</h1>")


def post_detail(request):
    context = {
        'title': 'Detail'
    }
    return render(request, "index.html", context)


def post_list(request):
    # if request.user.is_authenticated():
    #     context = {
    #         'title': 'My user list'
    #     }
    # else:
    #     context = {
    #         'title': 'List'
    #     }
    queryset = Post.objects.all()
    context = {
            'title': 'List',
            'object_list': queryset
         }
    return render(request, "index.html", context)


def post_update(request):
    return HttpResponse("<h1>Update</h1>")


def post_delete(request):
    return HttpResponse("<h1>Delete</h1>")