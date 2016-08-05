
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone
from django.conf import settings

class Post(models.Model):
    author = models.ForeignKey('auth.User')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, default=1) # to associate a post with a user which may or may not be admin

    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)
    #category = models.ForeignKey('blog.Category', related_name='posts')

    #image=models.FileField(null=True, blank=True)


    def get_absolute_url(self):
        return reverse('view:post_detail',kwargs={'pk':self.pk})



    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title





class Category(models.Model):
    category_type = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.category_type
