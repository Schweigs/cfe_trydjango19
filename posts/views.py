from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from .forms import PostForm
from .models import Post


def post_create(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return HttpResponseRedirect(instance.get_absolute_url())
    # if request.method == 'POST':
    #     print request.POST.get('title')
    #     print request.POST.get('content')
    context = {
        'form': form,
    }
    return render(request, "post_form.html", context)


def post_detail(request, id=None):
    # this method could through an error if the id doesn't exist:
    # instance = Post.objects.get(id=1)
    # this method will return a 404 page instead:
    instance = get_object_or_404(Post, id=id)
    context = {
        'title': instance.title,
        'instance': instance,
    }
    return render(request, "post_detail.html", context)


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


def post_update(request, id=None):
    instance = get_object_or_404(Post, id=id)
    form = PostForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        'title': instance.title,
        'instance': instance,
        'form': form,
    }
    return render(request, "post_form.html", context)



def post_delete(request):
    return HttpResponse("<h1>Delete</h1>")