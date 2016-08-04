
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone

class Post(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)
    #image=models.FileField(null=True, blank=True)


    """def get_absolute_url(self):
        return reverse('view:post_detail',kwargs={'pk':self.pk})"""



    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
