from django.db import models
from vote.models import VoteModel
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.


class Question(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='created')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="question")
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    votes = models.IntegerField(default=0)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('qa:question_detail', args=[self.slug])


class Answer(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="answers")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="answer")
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    votes = models.IntegerField(default=0)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.question}'
