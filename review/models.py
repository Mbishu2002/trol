from django.db import models
from Profile.models import User
import uuid

class Review(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    review_text = models.TextField()
    rating = models.IntegerField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='review_images/', null=True, blank=True)

    def __str__(self):
        return f"Review by {self.author} - Rating: {self.rating}"
