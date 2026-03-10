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

class Question(models.Model):
    CATEGORY_CHOICES = [
        ('QUIZ', 'Quiz'),
        ('VOCAB', 'Vocabulary Match'),
        ('BLANKS', 'Fill in the Blanks'),
        ('MEMORY', 'Memory Match'),
    ]
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    content = models.JSONField()
    is_static = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.category} - {'Static' if self.is_static else 'Dynamic'} - {self.id}"

class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'question')
        verbose_name_plural = "User Progress"

class SearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='search_history')
    prompt = models.TextField()
    ai_response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.user.username} - {self.prompt[:50]} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"
