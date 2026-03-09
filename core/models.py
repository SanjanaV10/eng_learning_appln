from django.db import models
from django.contrib.auth.models import User

class UserInteraction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    user_text = models.TextField()
    ai_response = models.TextField()
    corrections = models.TextField(default="None")
    is_mistake = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"
