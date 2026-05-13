from django.db import models
from django.utils.text import slugify

from apps.core.models import BaseModel


class Service(BaseModel):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    summary = models.TextField()
    icon = models.CharField(max_length=100, blank=True, default="")
    url = models.URLField(max_length=300, blank=True, default="")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Service"
        verbose_name_plural = "Services"
        ordering = ["order"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class TeamMember(BaseModel):
    name = models.CharField(max_length=200)
    role = models.CharField(max_length=200)
    bio = models.TextField(blank=True, default="")
    photo = models.ImageField(upload_to="team/", blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Team Member"
        verbose_name_plural = "Team Members"
        ordering = ["order"]

    def __str__(self):
        return self.name


class News(BaseModel):
    title = models.CharField(max_length=300)
    slug = models.SlugField(unique=True, blank=True)
    excerpt = models.TextField(blank=True, default="")
    body = models.TextField()
    cover = models.ImageField(upload_to="news/", blank=True)
    published = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "News"
        verbose_name_plural = "News"
        ordering = ["-published_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
