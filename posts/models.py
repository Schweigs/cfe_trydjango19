from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save

from django.utils.text import slugify

# Create your models here.
# MVC - Model View Controller


class PostManager(models.Manager):
    def active(self, *args, **kwargs):
        # this overwrites the original Post.object.all() PostManager and adds some filters
        # Post.object.all() == super(PostManager, self).all()
        # change from .all() to .active() afterwards
        return super(PostManager, self).filter(draft=False).filter(publish__lte=timezone.now())
        # this needs to be instantiated in the model by calling: objects = PostManager()

# this saves files into a given folder. in this case it is the instance id but it could for
# example be the username
def upload_location(instance, filename):
    return "%s/%s" %(instance.id, filename)


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    title = models.CharField(max_length=120)
    image = models.ImageField(upload_to=upload_location,
                              null=True,
                              blank=True,
                              width_field="width_field",
                              height_field="height_field")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    draft = models.BooleanField(default=False)
    publish = models.DateField(auto_now=False, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    # this instantiates the ModelManager
    objects = PostManager()

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('posts:detail', kwargs={'id': self.id})
        # return "/posts/%s/" %(self.id)

    class Meta:
        ordering = ["-timestamp", "-updated"]


def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug=slug).order_by('-id')
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_safe_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


pre_save.connect(pre_safe_post_receiver, sender=Post)
