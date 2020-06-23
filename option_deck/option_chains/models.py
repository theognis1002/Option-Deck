from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Chain(models.Model):
    slug = models.SlugField (
        verbose_name = "Slug",
        allow_unicode = True,
        unique=True,
        blank = True,
        null = False
    )
    ticker = models.CharField(max_length=4)
    price = models.FloatField()
    company_name = models.CharField(max_length=50)
    description = models.TextField()
    pe = models.FloatField()
    date_updated = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.ticker

    def get_absolute_url(self):
        return reverse('chain-detail', kwargs={'pk': self.pk})
