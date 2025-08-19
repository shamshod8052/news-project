from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
            return self.name or '?'

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class New(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft',
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255)
    body = models.TextField()
    image = models.ImageField(upload_to='news/images/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    publish_time = models.DateTimeField(null=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)

    def __str__(self):
        return self.title or '?'

    class Meta:
        verbose_name = 'New'
        verbose_name_plural = 'News'
        ordering = ['-publish_time']

    def get_absolute_url(self):
        return reverse('news_detail', args=[self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while New.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

class Contact(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.email


class Comment(models.Model):
    new = models.ForeignKey(New, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created_time']

    def __str__(self):
        return f"Comment - {self.body} by {self.user}"
