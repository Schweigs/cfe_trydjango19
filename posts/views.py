from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .forms import PostForm
from .models import Post


def post_create(request):
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, 'Successfully Created')
        print 'success'
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
    queryset_list = Post.objects.all()#.order_by("-timestamp")
    # Pagination code start:
    paginator = Paginator(queryset_list, 5) # Show 25 contacts per page
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)
    # Pagination code end
    context = {
            'title': 'List',
            'object_list': queryset,
            'page_request_var': page_request_var
         }
    return render(request, "post_list.html", context)





def listing(request):
    contact_list = Contacts.objects.all()


    return render(request, 'list.html', {'contacts': contacts})





def post_update(request, id=None):
    instance = get_object_or_404(Post, id=id)
    form = PostForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, '<a href="#">Item</a> Saved', extra_tags='html_safe')
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        'title': instance.title,
        'instance': instance,
        'form': form,
    }
    return render(request, "post_form.html", context)



def post_delete(request, id=None):
    instance = get_object_or_404(Post, id=id)
    instance.delete()
    messages.success(request, 'Successfully deleted')
    return redirect('posts:list')