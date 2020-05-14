from django.contrib import admin
from .models import Question, Answer

# Register your models here.
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'user', 'created')
    list_filter = ('created', 'user')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('user',)
    date_hierarchy = 'created'
    ordering = ('created',)

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'created')
    list_filter = ('created', 'updated')
    search_fields = ('body',)
