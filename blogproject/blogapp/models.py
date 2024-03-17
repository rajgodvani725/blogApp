from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
import json
User._meta.get_field('email')._unique = True

class Blog(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_draft = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'author': self.author.username,
            'created_at': self.created_at.strftime("%B %d, %Y"),
            'is_draft': json.dumps(self.is_draft),
        }
    def __str__(self):
        return self.title