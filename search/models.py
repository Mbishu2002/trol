from django.db import models
from Profile.models import Business

class Search(models.Model):
    query = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True, null=True)
    category = models.CharField(max_length=30, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('Profile.User', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Search for '{self.query}' by {self.user} at {self.timestamp}"
