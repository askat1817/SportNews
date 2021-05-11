from django.db import models
from django.contrib.auth import get_user_model
from pytils.translit import slugify
from django.utils import timezone

User = get_user_model()


class Types(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, primary_key=True)
    image = models.ImageField(upload_to='categories/', null=True, blank=True)

    def __str__(self):
        return self.title

    def save(self):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save()


class Post(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, primary_key=True)
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='posts')
    category = models.ForeignKey(Types, on_delete=models.CASCADE,
                                 related_name='posts')
    image = models.ImageField(upload_to='posts/')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self):
        if not self.slug:
            current = timezone.now().strftime('%s')
            self.slug = slugify(self.title) + current
        super().save()
