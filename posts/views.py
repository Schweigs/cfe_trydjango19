from urllib import quote_plus
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .forms import PostForm
from .models import Post


def post_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
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
    if instance.draft or instance.publish > timezone.now().date():
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404
    share_string = quote_plus(instance.content)
    context = {
        'title': instance.title,
        'instance': instance,
        'share_string': share_string,
    }
    return render(request, "post_detail.html", context)


def post_list(request):
    today = timezone.now().date()
    # if request.user.is_authenticated():
    #     context = {
    #         'title': 'My user list'
    #     }
    # else:
    #     context = {
    #         'title': 'List'
    #     }
    queryset_list = Post.objects.active()#.filter(draft=False).filter(publish__lte=timezone.now())#.all()#.order_by("-timestamp")
    if request.user.is_staff or request.user.is_superuser:
        queryset_list = Post.objects.all()
    # implementing search function:
    query = request.GET.get('q')
    if query:
        queryset_list = queryset_list.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query)
        ).distinct()
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
            'page_request_var': page_request_var,
            'today': today
         }
    return render(request, "post_list.html", context)





def listing(request):
    contact_list = Contacts.objects.all()


    return render(request, 'list.html', {'contacts': contacts})





def post_update(request, id=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    # if not request.user.is_authenticated:
    #     raise Http404
    instance = get_object_or_404(Post, id=id)
    form = PostForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
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
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post, id=id)
    instance.delete()
    messages.success(request, 'Successfully deleted')
    return redirect('posts:list')