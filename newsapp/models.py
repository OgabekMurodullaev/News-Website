from django.db import models
from django.utils import timezone
from django.urls import reverse


# Create your models here.

class PublishManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=News.Status.Published)


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    objects = models.Manager()


class News(models.Model):
    class Status(models.TextChoices):
        Draft = 'DF', 'Draft'
        Published = 'PB', 'Publish'

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    body = models.TextField()
    image = models.ImageField(upload_to='news/images/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    publish_time = models.DateTimeField(default=timezone.now)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.Draft
                              )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('new_detail', args=[self.slug])

    objects = models.Manager()
    published = PublishManager()

    class Meta:
        ordering = ["-publish_time"]




class Contact(models.Model):
    username = models.CharField(max_length=150)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.email
