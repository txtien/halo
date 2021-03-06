from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.db import IntegrityError
from taggit.managers import TaggableManager
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
    tags = TaggableManager()

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # Send argument to question_detail route
        return reverse('qa:question_detail', args=[self.slug])

    def upvote(self, user):
        try:
            self.question_vote.create(user=user, question=self, vote_type='up')
            self.votes += 1
            self.save(update_fields=['votes'])
        except IntegrityError:
            return "Already upvotes"
        return 'ok'

    def downvote(self, user):
        try:
            self.question_vote.create(
                user=user, question=self, vote_type='down')
            self.votes -= 1
            self.save(update_fields=['votes'])
        except IntegrityError:
            return "Already downvotes"
        return 'ok'


class Answer(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="answers")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="answer")
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    votes = models.IntegerField(default=0)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.question}'

    def upvote(self, user):
        try:
            self.answer_vote.create(user=user, answer=self, vote_type='up')
            self.votes += 1
            self.save(update_fields=['votes'])
        except IntegrityError:
            return "Already upvotes"
        return 'ok'
    
    def downvote(self, user):
        try:
            self.answer_vote.create(user=user, answer=self, vote_type='down')
            self.votes -= 1
            self.save(update_fields=['votes'])
        except IntegrityError:
            return "Already downvotes"
        return 'ok'
    
class UserVoteQuestion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_vote_question')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question_vote')
    vote_type = models.CharField(max_length=10)

    class Meta:
        unique_together = ('user', 'question', 'vote_type')


class UserVoteAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_vote_answer')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='answer_vote')
    vote_type = models.CharField(max_length=10)

    class Meta:
        unique_together = ('user', 'answer', 'vote_type')
