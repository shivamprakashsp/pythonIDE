from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Snippet(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # lang = models.CharField(max_length=20, choices=Lang_CHOICES, default='py')
    filename = models.CharField(max_length=100)
    text = models.TextField()
    input = models.TextField(blank=True)
    output = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at', )