# Generated by Django 3.0.6 on 2020-05-15 03:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('qa', '0013_uservotes'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserVoteAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vote_type', models.CharField(max_length=10)),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answer_vote', to='qa.Answer')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_vote_answer', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'answer', 'vote_type')},
            },
        ),
        migrations.CreateModel(
            name='UserVoteQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vote_type', models.CharField(max_length=10)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question_vote', to='qa.Question')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_vote_question', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'question', 'vote_type')},
            },
        ),
        migrations.DeleteModel(
            name='UserVotes',
        ),
    ]